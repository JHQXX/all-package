# 🏠 Nexus 个人私有 Maven 仓库

部署在 `nexus.azhi-home.top`，通过 **Cloudflare Tunnel** 安全暴露到公网。

## 🛡️ 为什么用 Cloudflare Tunnel？

| 方案 | 公网暴露 | 安全性 | 部署难度 | 费用 |
|------|---------|--------|---------|------|
| 直接开放 8081 | ⚠️ 危险 | ❌ 低 | 简单 | 免费 |
| Nginx + HTTPS | 需开放 443 | ⚠️ 中 | 复杂 | 免费 |
| **Cloudflare Tunnel** | **❌ 零暴露** | **✅ 高** | **中等** | **免费** |

**核心优势**：
- ✅ 服务器**不需要公网 IP**（可以藏在内网）
- ✅ **零端口开放**到公网（Cloudflare 反向连接）
- ✅ 自动 HTTPS（Cloudflare 管证书）
- ✅ 自动 WAF（Web 应用防火墙）
- ✅ 自动 DDoS 防护

---

## 🚀 一次性部署步骤

### 步骤 1：创建 Cloudflare Tunnel

**1.1 登录 Cloudflare**
```
https://one.dash.cloudflare.com/
```
（如果没有账号，免费注册一个，把域名 `azhi-home.top` 添加到 Cloudflare）

**1.2 进入 Tunnels 页面**
- 左侧菜单：`Zero Trust` → `Networks` → `Tunnels`
- 第一次使用会让你设置一个 team name（团队名）

**1.3 创建 Tunnel**
- 点 `Create a tunnel`
- 选 `Cloudflared` 类型
- 命名：`nexus-tunnel`（任意名字）
- 点 `Save tunnel`

**1.4 复制 Token**
- 接下来页面会显示 `TUNNEL TOKEN`，长这样：
  ```
  eyJhIjoiYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXowMTIzNDU2Nzg5MCIsInMiOj...
  ```
- **复制它**，粘到后面用

**1.5 配置 Public Hostname**
- 在 tunnel 详情页，"Public Hostnames" 标签
- 点 `Add a public hostname`
- 填写：
  | 字段 | 值 |
  |------|-----|
  | Subdomain | `nexus` |
  | Domain | `azhi-home.top` |
  | Service | `http://nexus:8081` |
    - ⚠️ 注意：`nexus` 是 docker compose 里的服务名
    - `8081` 是 Nexus 容器内的端口
- 点 `Save hostname`

**1.6 给 azhi-home.top 添加 CNAME（可选）**

Cloudflare 通常会自动接管 DNS，但如果是手动管理：
- 在 Cloudflare DNS 里加：
  ```
  CNAME  nexus  <你的 tunnel UUID>.<region>.cfargotunnel.com
  ```
  （具体值在 tunnel 详情页能看到）

---

### 步骤 2：在服务器部署

**2.1 安装 Docker（如果没有）**
```bash
brew install docker docker-compose
```

**2.2 拉取代码**
```bash
cd ~/projects  # 或任意目录
git clone git@github.com:JHQXX/all-package.git
cd all-package/nexus
```

**2.3 复制并编辑 .env**
```bash
cp .env.example .env

# 编辑 .env，把刚才复制的 Tunnel Token 粘进去
nano .env
# 或
vim .env
```

**2.4 启动**
```bash
docker compose up -d

# 看启动状态
docker compose ps

# 看日志
docker logs -f nexus
docker logs -f cloudflared
```

---

### 步骤 3：访问并配置 Nexus

**3.1 访问 Nexus**

打开浏览器：
```
https://nexus.azhi-home.top
```

**3.2 首次登录**
- 用户名：`admin`
- 密码：容器里 `/nexus-data/admin.password`
  ```bash
  # 第一次启动后，等 1-2 分钟，查看密码：
  docker exec nexus cat /nexus-data/admin.password
  ```

**3.3 强制改密码**
- 登录后会要求你修改密码
- **改成强密码**：16+ 位、大小写、数字、符号

**3.4 启用匿名访问**
1. 齿轮 → `Security` → `Anonymous Access`
2. 打开 "Allow anonymous users to access the server"
3. 保存

**3.5 创建私有仓库**
1. 齿轮 → `Repositories` → `Create repository`
2. 选 `maven2 (hosted)`
3. 填写：
   - Name: `my-private-maven`
   - Version policy: `Release`
   - Deployment policy: `Allow redeploy`
4. 点 `Create`

---

## 📤 上传私有包

### 配置认证（~/.m2/settings.xml）

```xml
<servers>
    <server>
        <id>my-private-nexus</id>
        <username>admin</username>
        <password>你的密码</password>
    </server>
</servers>
```

### 项目 pom.xml 加 distributionManagement

```xml
<distributionManagement>
    <repository>
        <id>my-private-nexus</id>
        <url>https://nexus.azhi-home.top/repository/my-private-maven/</url>
    </repository>
</distributionManagement>
```

### 部署
```bash
mvn clean deploy
```

---

## 📥 在其他项目中使用

```xml
<repositories>
    <repository>
        <id>my-private-nexus</id>
        <url>https://nexus.azhi-home.top/repository/my-private-maven/</url>
    </repository>
</repositories>

<dependencies>
    <dependency>
        <groupId>com.lizhi</groupId>
        <artifactId>my-private-lib</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

---

## 🔧 日常运维

```bash
# 查看状态
docker compose ps

# 查看日志
docker compose logs -f

# 重启
docker compose restart

# 升级版本
docker compose pull
docker compose up -d

# 完全删除（⚠️ 数据会丢）
docker compose down
docker volume rm nexus-data

# 备份数据
docker run --rm \
  -v nexus-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/nexus-$(date +%Y%m%d).tar.gz /data
```

---

## 🔐 进一步加强安全（推荐）

### 1️⃣ 在 Cloudflare 添加访问策略

Cloudflare Zero Trust → `Access` → `Applications`：
- 添加一个 Application，类型选 `Self-hosted`
- 域名：`nexus.azhi-home.top`
- 策略：只允许你的邮箱登录（比如 `one-time PIN`）
- 这样即使 Nexus 密码泄露，没有你的邮箱也进不去

### 2️⃣ Nexus 启用 Anonymous User 限制

Nexus → `Security` → `Roles`：
- `nx-anonymous` 角色只赋予 `read` 权限
- `nx-admin` 角色只给你的账号

### 3️⃣ 定期备份

加个 cron job：
```bash
# 每周日凌晨 3 点备份
0 3 * * 0 cd /path/to/all-package/nexus && /usr/local/bin/docker run --rm -v nexus-data:/data -v $(pwd):/backup alpine tar czf /backup/nexus-weekly-$(date +\%Y\%m\%d).tar.gz /data
```

---

## ❓ 故障排查

### 1️⃣ 访问域名是 502 Bad Gateway
- 检查 cloudflared 容器日志：`docker logs cloudflared`
- 检查 `Public Hostname` 配置的 Service 是否正确：`http://nexus:8081`

### 2️⃣ Tunnel 一直 Connecting
- 检查 `.env` 里的 `CLOUDFLARE_TUNNEL_TOKEN` 是否正确
- 检查服务器是否能访问外网（cloudflared 需要 outbound HTTPS）

### 3️⃣ Nexus 启动慢
- 第一次启动要 1-2 分钟（初始化 + 健康检查）
- 等到 `docker compose ps` 显示 `healthy` 状态

### 4️⃣ 忘了 admin 密码
```bash
# 重置（⚠️ 需要重启 nexus）
docker exec -it nexus bash
vi /nexus-data/admin.password
# 改成新密码（明文）
# 重启容器让它 hash
docker restart nexus
```