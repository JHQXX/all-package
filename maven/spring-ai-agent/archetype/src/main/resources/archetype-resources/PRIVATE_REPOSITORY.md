# 🏠 私有 Maven 仓库配置示例

如果你的团队部署了自己的 Nexus（或其他 Maven 仓库），可以在 `pom.xml` 中添加：

## 1. 拉取依赖（repositories）

```xml
<repositories>
    <repository>
        <id>my-private-nexus</id>
        <name>个人私有仓库</name>
        <url>https://nexus.azhi-home.top/repository/my-private-maven/</url>
        <releases>
            <enabled>true</enabled>
        </releases>
        <snapshots>
            <enabled>false</enabled>
        </snapshots>
    </repository>
</repositories>
```

## 2. 上传包（distributionManagement）

```xml
<distributionManagement>
    <repository>
        <id>my-private-nexus</id>
        <name>个人私有仓库</name>
        <url>https://nexus.azhi-home.top/repository/my-private-maven/</url>
    </repository>
</distributionManagement>
```

## 3. 认证（~/.m2/settings.xml）

```xml
<servers>
    <server>
        <id>my-private-nexus</id>
        <username>admin</username>
        <password>your-password</password>
    </server>
</servers>
```

## 4. 上传到私有仓库

```bash
mvn clean deploy
```

## 5. 在其他项目里使用私有包

```xml
<dependencies>
    <dependency>
        <groupId>com.your-company</groupId>
        <artifactId>your-private-lib</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

---

## 部署自己的 Nexus？

参考父仓库的 [nexus/](https://github.com/JHQXX/all-package/tree/main/nexus) 目录，里面有完整的：

- `docker-compose.yml` - Docker Compose 配置
- `nginx.conf` - 反向代理 + HTTPS
- `setup-https.sh` - 一键申请 Let's Encrypt 证书
- `README.md` - 详细部署文档