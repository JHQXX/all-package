# 发布到 Maven Central 完整指南

本文档详细说明如何把 Maven Archetype 脚手架发布到 Maven 中央仓库。

---

## 🎯 整体流程

```
┌─────────────────────────────────────────────────────┐
│  1. 注册 Sonatype 账号（一次性）                     │
│     └─ https://central.sonatype.com                 │
│     └─ GitHub 登录                                  │
│     └─ 添加 Namespace: io.github.jhqxx             │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  2. 安装 GPG 工具（一次性）                          │
│     brew install gnupg                              │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  3. 生成 GPG 密钥对（每个脚手架一次）                │
│     gpg --homedir /tmp/gpg-home --generate-key      │
│     # 切勿放进 ~/.gnupg，IDE sandbox 拒访问          │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  4. 上传公钥到密钥服务器（每个密钥对一次）           │
│     curl -X POST                                    │
│       -d @public-key.asc                            │
│       https://keyserver.ubuntu.com/pks/add          │
│     # 同样上传 pgp.mit.edu 和 keys.openpgp.org      │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  5. 配置 ~/.m2/settings.xml（一次性）                │
│     - <servers> 填写 Sonatype Token                 │
│     - <mirrors> 添加 <mirrorOf>*,!central</mirrorOf>│
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  6. 修改 archetype/pom.xml（关键）                  │
│     - <url>, <licenses>, <developers>, <scm>        │
│     - 4 个插件：source, javadoc, gpg, checksum      │
│     - 配置 gpgArguments 指定 --homedir /tmp/gpg-home│
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  7. 运行一键打包脚本                                  │
│     cd maven/spring-ai-agent/archetype              │
│     bash build-and-pack.sh                          │
│     # 生成 central-bundle.zip                        │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  8. 上传到 Sonatype Central Portal（每次发布）      │
│     https://central.sonatype.com/publishing         │
│     选择 Publish（不是 Deploy！）                    │
│     选择 central-bundle.zip 上传                    │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  9. 等待审核（一般 1-4 小时）                       │
│     https://repo.maven.apache.org/maven2/io/...    │
│     可以查看是否已经同步                            │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  10. 更新 GitHub Pages Catalog（可选）              │
│      修改 docs/jhqxx-catalog.xml                    │
│      增加新的 <archetype> 节点                      │
└─────────────────────────────────────────────────────┘
```

---

## 📋 详细步骤

### 步骤 1：注册 Sonatype

**第一次发布需要做，之后不用。**

1. 打开 https://central.sonatype.com
2. 点 **Sign In** → **Sign in with GitHub**
3. 授权后进入主面板
4. 点击 **Namespaces** → **Add Namespace**
5. 选择类型 **GitHub**
6. 输入 `io.github.jhqxx`（会自动验证你的 GitHub 账号）
7. 状态变为 **Verified** ✓

### 步骤 2：安装 GPG

```bash
brew install gnupg
```

### 步骤 3：生成密钥对

**每个脚手架系列用一对密钥，多个脚手架复用同一对即可。**

创建参数文件（避免交互式询问）：
```bash
cat > /tmp/gpg-key-params.txt <<'EOF'
%no-protection
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: JHQXX
Name-Email: 2733827845l@gmail.com
Expire-Date: 0
%commit
EOF
```

生成密钥到 `/tmp/gpg-home`（⚠️ 不要用 `~/.gnupg`，因为 IDE sandbox 限制）：
```bash
gpg --homedir /tmp/gpg-home --batch --generate-key /tmp/gpg-key-params.txt
```

查看：
```bash
gpg --homedir /tmp/gpg-home --list-secret-keys
```

### 步骤 4：上传公钥到密钥服务器

```bash
# 导出公钥
gpg --homedir /tmp/gpg-home --armor --export 2733827845l@gmail.com > public-key.asc

# 上传到 3 个服务器
SERVERS=("keyserver.ubuntu.com" "pgp.mit.edu" "keys.openpgp.org")
for server in "${SERVERS[@]}"; do
    curl -s -X POST --data-urlencode "keytext@public-key.asc" "https://$server/pks/add"
    echo "  ↑ $server"
done

# keys.openpgp.org 上传后会发邮件，需要点确认链接！
```

### 步骤 5：配置 settings.xml

编辑 `~/.m2/settings.xml`：

```xml
<servers>
    <server>
        <id>central</id>
        <username>在 https://central.sonatype.com/account 生成的 Token 用户名</username>
        <password>Token 密码</password>
    </server>
</servers>

<mirrors>
    <mirror>
        <id>aliyunmaven</id>
        <url>https://maven.aliyun.com/repository/public</url>
        <mirrorOf>*,!central</mirrorOf>   <!-- 关键：!central 让发布能走到 central -->
    </mirror>
</mirrors>
```

### 步骤 6：配置 archetype/pom.xml

参考 [maven/spring-ai-agent/archetype/pom.xml](maven/spring-ai-agent/archetype/pom.xml)。**关键部分**：

#### a. 项目元信息（必填）
```xml
<url>https://github.com/JHQXX/all-package</url>

<licenses>
    <license>
        <name>MIT License</name>
        <url>https://opensource.org/licenses/MIT</url>
    </license>
</licenses>

<developers>
    <developer>
        <name>JHQXX</name>
        <email>2733827845l@gmail.com</email>
    </developer>
</developers>

<scm>
    <connection>scm:git:git://github.com/JHQXX/all-package.git</connection>
    <developerConnection>scm:git:ssh://github.com:JHQXX/all-package.git</developerConnection>
    <url>https://github.com/JHQXX/all-package/tree/main</url>
</scm>
```

#### b. 4 个必填插件
```xml
<build>
    <extensions>
        <extension>
            <groupId>org.apache.maven.archetype</groupId>
            <artifactId>archetype-packaging</artifactId>
            <version>3.2.1</version>
        </extension>
    </extensions>

    <plugins>
        <!-- 源码包 -->
        <plugin>
            <artifactId>maven-source-plugin</artifactId>
            <version>3.2.1</version>
            <executions><execution><id>attach-sources</id>
                <goals><goal>jar-no-fork</goal></goals></execution></executions>
        </plugin>

        <!-- Javadoc 包 -->
        <plugin>
            <artifactId>maven-javadoc-plugin</artifactId>
            <version>3.6.3</version>
            <configuration><doclint>none</doclint></configuration>
            <executions><execution><id>attach-javadocs</id>
                <goals><goal>jar</goal></goals></execution></executions>
        </plugin>

        <!-- GPG 签名 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-gpg-plugin</artifactId>
            <version>3.2.5</version>
            <executions><execution><id>sign-artifacts</id>
                <phase>verify</phase>
                <goals><goal>sign</goal></goals></execution></executions>
            <configuration>
                <gpgArguments>
                    <arg>--homedir</arg>
                    <arg>/tmp/gpg-home</arg>
                    <arg>--no-tty</arg>
                </gpgArguments>
            </configuration>
        </plugin>

        <!-- 校验和 -->
        <plugin>
            <groupId>net.nicoulaj.maven.plugins</groupId>
            <artifactId>checksum-maven-plugin</artifactId>
            <version>1.11</version>
            <executions><execution><id>create-checksums</id>
                <goals><goal>artifacts</goal></goals></execution></executions>
        </plugin>
    </plugins>
</build>
```

### 步骤 7：一键打包

```bash
cd maven/spring-ai-agent/archetype
bash build-and-pack.sh
```

输出：
- ✅ `central-bundle.zip` (~31KB)
- ✅ `public-key.asc` (备用)
- ⏰ 提示 24 小时后自动清理

### 步骤 8：上传到 Sonatype

⚠️ **不要用 mvn deploy！** Sonatype 从 2024 年 2 月起不再支持 deploy，必须**手动网页上传**。

1. 打开 https://central.sonatype.com/publishing
2. 登录（GitHub 账号）
3. 选择 **Publish**（不是 Deploy！）
4. 上传 `central-bundle.zip`
5. 等待审核

### 步骤 9：等待审核并验证

- 5-30 分钟：文件验证
- 1-4 小时：完全同步到 Maven Central
- 验证：访问 https://repo.maven.apache.org/maven2/io/github/jhqxx/springai-agent-archetype/ 看到 1.0.0 目录就 OK

### 步骤 10：更新 GitHub Pages Catalog

修改 [docs/jhqxx-catalog.xml](docs/jhqxx-catalog.xml)，增加版本或新脚手架：

```xml
<archetype>
    <groupId>io.github.jhqxx</groupId>
    <artifactId>springai-agent-archetype</artifactId>
    <version>1.0.0</version>   <!-- 新版本 -->
    <repository>
        <id>central</id>
        <url>https://repo.maven.apache.org/maven2</url>
    </repository>
    <description>...</description>
</archetype>
```

提交到 main，1-2 分钟后 GitHub Pages 自动部署。

---

## ⚠️ 升级版本流程

如果需要发布 1.0.1：

```bash
# 1. 修改 archetype/pom.xml 的 <version>
sed -i '' 's/<version>1.0.0<\/version>/<version>1.0.1<\/version>/' \
  maven/spring-ai-agent/archetype/pom.xml

# 2. 修改 build-and-pack.sh 的 VERSION 变量
sed -i '' 's/VERSION="1.0.0"/VERSION="1.0.1"/' \
  maven/spring-ai-agent/archetype/build-and-pack.sh

# 3. 打包并上传
cd maven/spring-ai-agent/archetype
bash build-and-pack.sh

# 4. 更新 GitHub Pages catalog.xml
```

⚠️ **每次升级都要修改 README 中的链接和 catalog.xml**。

---

## 🚫 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `Operation not permitted` on `~/.gnupg` | IDE sandbox 阻止 | 用 `--homedir /tmp/gpg-home` |
| `Invalid md5 checksum` | macOS BSD 格式带文件名 | 用 `md5 -q` 而不是 `md5` |
| `Could not find a public key` | 公钥没上传到密钥服务器 | 手动 curl 上传 |
| `aliyun 镜像拦截 central` | mirror 没排除 central | `<mirrorOf>*,!central</mirrorOf>` |
| `<version>X.0.0</version> already exists` | 重复发布同版本 | 升级到 X.0.1 |
