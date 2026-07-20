# Nexus 个人私有 Maven 仓库

部署在 `nexus.azhi-home.top`，通过 Docker Compose 启动。

## 🚀 一次性部署步骤

### 1. 在服务器（192.168.31.36）上

```bash
# 1.1 安装依赖（如果是 macOS）
brew install docker docker-compose nginx certbot

# 1.2 进入 nexus 目录
cd nexus/

# 1.3 复制配置
cp .env.example .env
# 编辑 .env，设置强密码！

# 1.4 申请 SSL 证书
chmod +x setup-https.sh
sudo ./setup-https.sh
# 提示时输入你的邮箱（用于 SSL 证书续期提醒）

# 1.5 启动 Nexus
docker compose up -d

# 1.6 看启动日志
docker logs -f nexus
# 等看到 "Started Sonatype Nexus OSS" 后 Ctrl+C
```

### 2. 浏览器访问

打开 https://nexus.azhi-home.top

**首次登录**：
- 用户名：`admin`
- 密码：`.env` 里的 `NEXUS_ADMIN_PASSWORD`

### 3. 创建私有仓库

登录后：
1. 齿轮图标 → `Repositories` → `Create repository`
2. 选择 **`maven2 (hosted)`**
3. 填写：
   - Name: `my-private-maven`
   - Version policy: `Release`
   - Layout policy: `Strict`
   - Deployment policy: `Allow redeploy`（允许更新）
4. 点 `Create repository`

### 4. 启用匿名访问（让 Maven 能拉包）

1. 齿轮 → `Security` → `Anonymous Access`
2. 打开 "Allow anonymous users to access the server"
3. 保存

---

## 📤 上传私有包

### 在 IDEA/Maven 中配认证

`~/.m2/settings.xml`:
```xml
<servers>
    <server>
        <id>my-private-nexus</id>
        <username>admin</username>
        <password>你的密码</password>
    </server>
</servers>
```

### 部署包到私有仓库

修改项目的 `pom.xml`:
```xml
<distributionManagement>
    <repository>
        <id>my-private-nexus</id>
        <url>https://nexus.azhi-home.top/repository/my-private-maven/</url>
    </repository>
</distributionManagement>
```

然后：
```bash
mvn deploy
```

---

## 📥 在其他项目中使用私有包

修改 `pom.xml`:
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

## ⚠️ 安全提醒

1. **必须改 admin 密码**（首次登录后会强制要求）
2. **域名 HTTPS 必须配**（否则密码明文传输）
3. **强烈建议开启 IP 白名单**（编辑 `nginx.conf`，取消 `allow/deny` 注释）
4. **Nexus 数据备份**：
   ```bash
   docker run --rm -v nexus-data:/data -v $(pwd):/backup \
     alpine tar czf /backup/nexus-backup-$(date +%Y%m%d).tar.gz /data
   ```

---

## 🔧 日常运维

```bash
# 查看状态
docker ps | grep nexus

# 看日志
docker logs -f nexus

# 重启
docker compose restart

# 升级到新版本
docker compose pull
docker compose up -d

# 完全删除（⚠️ 数据会丢）
docker compose down
docker volume rm nexus-data
```