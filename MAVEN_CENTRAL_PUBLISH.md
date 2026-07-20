# 发布到 Maven 中央仓库指南

本指南详细说明如何将 `springai-agent-archetype` 发布到 Maven 中央仓库（Sonatype Central Portal）。

---

## 🔍 概述

发布到 Maven 中央仓库需要以下步骤：

1. 注册 Sonatype 账号并验证 Namespace
2. 安装 GPG 并生成密钥对（已完成 ✅）
3. 配置 pom.xml（已完成 ✅）
4. 配置 Maven settings.xml（已完成 ✅）
5. 构建并签名
6. 上传到中央仓库

---

## 📋 第一步：注册 Sonatype 账号

### 1.1 注册账号

访问 https://central.sonatype.com ，使用 GitHub 账号登录。

### 1.2 验证 Namespace

登录后，进入 **Namespaces** 页面，添加你的 Namespace。

由于我们的 groupId 是 `io.github.jhqxx`：

1. 选择 **Add Namespace**
2. 选择 **GitHub** 命名空间类型
3. 系统会自动验证你的 GitHub 账号
4. 验证通过后，`io.github.jhqxx` 就可以使用了

> 💡 如果你使用的是自定义域名（如 `com.example`），需要通过 DNS TXT 记录验证。

---

## 🔑 第二步：GPG 密钥（已完成）

### 2.1 已生成的密钥信息

- 姓名：JHQXX
- 邮箱：2733827845l@gmail.com
- 密钥 ID：`7A0F7F223F826CAD`
- 密钥指纹：`2E259008DBF7281C45A00D027A0F7F223F826CAD`

### 2.2 上传公钥到密钥服务器

Maven 中央仓库需要验证你的公钥。需要将公钥上传到公共密钥服务器：

```bash
# 方法一：上传到 Ubuntu 密钥服务器
gpg --keyserver hkp://keyserver.ubuntu.com --send-keys 7A0F7F223F826CAD

# 方法二：上传到 MIT 密钥服务器
gpg --keyserver hkp://pgp.mit.edu --send-keys 7A0F7F223F826CAD

# 方法三：上传到 OpenPGP 密钥服务器
gpg --keyserver hkp://keys.openpgp.org --send-keys 7A0F7F223F826CAD
```

验证公钥是否上传成功：

```bash
gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 7A0F7F223F826CAD
```

### 2.3 导出公钥（备用）

```bash
# 导出公钥
gpg --armor --export 2733827845l@gmail.com > public-key.asc

# 导出私钥（备份用，妥善保管！）
gpg --armor --export-secret-keys 2733827845l@gmail.com > private-key.asc
```

---

## ⚙️ 第三步：配置 Maven settings.xml

编辑 `~/.m2/settings.xml`，添加服务器认证：

1. 登录 https://central.sonatype.com
2. 进入 **Account** 页面
3. 点击 **Generate Token** 生成访问令牌
4. 复制用户名和密码

然后将 settings.xml 中的以下注释取消并填写：

```xml
<servers>
    <server>
        <id>central</id>
        <username>你的 token 用户名</username>
        <password>你的 token 密码</password>
    </server>
</servers>
```

同时取消 GPG 密码配置：

```xml
<profiles>
    <profile>
        <id>release</id>
        <properties>
            <gpg.executable>gpg</gpg.executable>
            <gpg.passphrase>你的 GPG 密钥密码</gpg.passphrase>
        </properties>
    </profile>
</profiles>

<activeProfiles>
    <activeProfile>release</activeProfile>
</activeProfiles>
```

> ⚠️ 注意：当前生成的密钥没有设置密码（为了方便测试）。生产环境建议设置密码。

---

## 🏗️ 第四步：构建项目

进入 `maven-archetype` 目录，执行构建：

```bash
cd maven-archetype

# 构建并签名
mvn clean verify

# 或者使用 release profile
mvn clean verify -P release
```

构建成功后，在 `target/` 目录下会生成以下文件：

```
springai-agent-archetype-1.0.0.jar
springai-agent-archetype-1.0.0.pom
springai-agent-archetype-1.0.0-sources.jar
springai-agent-archetype-1.0.0-javadoc.jar
springai-agent-archetype-1.0.0.jar.asc
springai-agent-archetype-1.0.0.pom.asc
springai-agent-archetype-1.0.0-sources.jar.asc
springai-agent-archetype-1.0.0-javadoc.jar.asc
springai-agent-archetype-1.0.0.jar.md5
springai-agent-archetype-1.0.0.pom.md5
... (以及 sha1 文件)
```

---

## 📦 第五步：打包上传

### 5.1 手动上传（推荐新手）

1. 访问 https://central.sonatype.com/publishing
2. 点击 **Upload Component**
3. 按目录结构组织文件：

```
io/
└── github/
    └── jhqxx/
        └── springai-agent-archetype/
            └── 1.0.0/
                ├── springai-agent-archetype-1.0.0.jar
                ├── springai-agent-archetype-1.0.0.jar.asc
                ├── springai-agent-archetype-1.0.0.jar.md5
                ├── springai-agent-archetype-1.0.0.jar.sha1
                ├── springai-agent-archetype-1.0.0.pom
                ├── springai-agent-archetype-1.0.0.pom.asc
                ├── springai-agent-archetype-1.0.0.pom.md5
                ├── springai-agent-archetype-1.0.0.pom.sha1
                ├── springai-agent-archetype-1.0.0-sources.jar
                ├── springai-agent-archetype-1.0.0-sources.jar.asc
                ├── springai-agent-archetype-1.0.0-sources.jar.md5
                ├── springai-agent-archetype-1.0.0-sources.jar.sha1
                ├── springai-agent-archetype-1.0.0-javadoc.jar
                ├── springai-agent-archetype-1.0.0-javadoc.jar.asc
                ├── springai-agent-archetype-1.0.0-javadoc.jar.md5
                └── springai-agent-archetype-1.0.0-javadoc.jar.sha1
```

4. 将整个 `io/` 目录打包成 zip
5. 上传 zip 文件
6. 等待验证通过

### 5.2 使用 Maven 插件自动上传

配置 pom.xml 的 distributionManagement（待补充）。

---

## 📋 第六步：更新 archetype-catalog.xml

发布成功后，更新 `docs/archetype-catalog.xml`，让用户可以通过 IDEA 直接使用。

---

## 🐛 常见问题

### Q: 上传失败，提示缺少签名文件？
A: 确保 `maven-gpg-plugin` 正确配置，并且 GPG 密钥可用。

### Q: 上传失败，提示校验和错误？
A: `checksum-maven-plugin` 不会自动为 pom 文件生成校验和，需要手动生成：
```bash
md5 target/springai-agent-archetype-1.0.0.pom > target/springai-agent-archetype-1.0.0.pom.md5
shasum target/springai-agent-archetype-1.0.0.pom > target/springai-agent-archetype-1.0.0.pom.sha1
```

### Q: Javadoc 生成失败？
A: 确保 Java 版本正确，并且代码中有合法的 Javadoc 注释。
   当前 pom.xml 已配置 `doclint>none`，可以忽略大部分 Javadoc 警告。

### Q: GPG 签名失败？
A: 检查 GPG 密钥是否存在，以及密码是否正确。
   查看密钥列表：`gpg --list-secret-keys`

---

## 📚 参考资料

- 官方文档：https://central.sonatype.org/
- 上传指南：https://central.sonatype.org/publish/publish-portal-upload/
- Namespace 验证：https://central.sonatype.org/register/central-portal/
