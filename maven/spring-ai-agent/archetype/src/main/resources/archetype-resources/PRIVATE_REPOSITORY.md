# 🏠 私有 Maven 仓库（jhqxx）使用指南

本项目已**默认启用** JHQXX 私有 Nexus 仓库。

| 配置项 | 值 |
|--------|-----|
| 仓库 ID | `jhqxx` |
| URL | `https://nexus.azhi-home.top/repository/my-private-maven/` |
| 模式 | Disable anonymous access（需认证） |
| 用途 | 拉取/发布私有包 |

⚠️ **Nexus 部署在你家里**（`192.168.31.36`），通过你的内网穿透暴露到公网。
**所有操作（拉包、上传）都需要账号密码认证。**

---

## 📋 一次性配置：Maven 认证

编辑 `~/.m2/settings.xml`，添加：

```xml
<servers>
    <server>
        <id>jhqxx</id>
        <username>admin</username>
        <password>你的Nexus密码</password>
    </server>
</servers>
```

⚠️ `<id>jhqxx</id>` 必须跟 pom.xml 里的 `<repository><id>` 一致！

---

## 📦 仓库怎么用

### 拉包（自动启用）

pom.xml 里已经默认启用 jhqxx 仓库，像普通依赖一样：

```xml
<dependencies>
    <dependency>
        <groupId>com.lizhi</groupId>
        <artifactId>my-private-lib</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

Maven 会自动用 `admin/你的密码` 去 jhqxx 仓库拉包。

### 发布包（自动启用）

直接执行：

```bash
mvn clean deploy
```

自动推送到 `https://nexus.azhi-home.top/repository/my-private-maven/`。

---

## 🔧 IDEA 中配置

1. **File** → **Settings** → **Build, Execution, Deployment** → **Maven**
2. 确认 **User settings file** 指向你的 `~/.m2/settings.xml`
3. 保存

---

## 🧪 测试认证是否生效

### 测试 1：拉一个不存在的包（验证认证）

```bash
mvn dependency:get \
  -Dartifact=com.lizhi:my-private-lib:1.0.0 \
  -DremoteRepositories=jhqxx::default::https://nexus.azhi-home.top/repository/my-private-maven/
```

| 结果 | 含义 |
|------|------|
| `BUILD SUCCESS` | ✅ 认证通过，包拉到了 |
| `401 Unauthorized` | ❌ 密码错，检查 settings.xml |
| `404 Not Found` | ✅ 认证通过，但包不存在（正常） |

### 测试 2：发布一个 demo 包

1. 临时改 pom.xml 的 `<version>` 为 `1.0.0-test`
2. `mvn clean deploy`
3. 看是否上传成功
4. 在 Nexus 网页（https://nexus.azhi-home.top）Browse 仓库，能看到刚上传的包

---

## ❓ 故障排查

### Q: 报 401 Unauthorized

```
[ERROR] Failed to read artifact descriptor... 401 Unauthorized
```

**解决**：
1. 检查 `~/.m2/settings.xml` 里 `<server><id>` 跟 pom.xml 里 `<repository><id>` 都是 `jhqxx`
2. 检查密码是否正确
3. 试试 `curl -u admin:密码 https://nexus.azhi-home.top/`

### Q: 报 Could not resolve dependencies / Connection refused

**可能原因**：
1. Nexus 没启动（`docker ps | grep nexus`）
2. 内网穿透挂了
3. 域名解析失败

**解决**：
1. 服务器上检查：`docker ps | grep nexus`
2. 直接 IP 访问测试：`curl -u admin:密码 http://192.168.31.36:8081`
3. 公网域名测试：`curl -u admin:密码 https://nexus.azhi-home.top`

### Q: 想完全不用 jhqxx 仓库

不需要 Nexus 时，删除或注释 pom.xml 里的这两段：

```xml
<!-- 注释掉 -->
<repositories>
    <repository>...</repository>
</repositories>

<distributionManagement>
    <repository>...</repository>
</distributionManagement>
```

---

## 🆚 跟 Maven Central 的关系

| 仓库 | 用途 | 用法 |
|------|------|------|
| Maven Central | 公共包（Spring、Apache 等） | 默认支持 |
| **jhqxx** (Nexus) | 你的私有包 | 本项目已默认启用 |

两者**互不影响**：
- 公共包从 Maven Central 拉（自动）
- 私有包从 jhqxx 拉（需要时）

---

## 📚 部署你自己的 Nexus？

参考父仓库的 [nexus/](https://github.com/JHQXX/all-package/tree/main/nexus) 目录，
里面有完整的 `docker-compose.yml`，一键启动。