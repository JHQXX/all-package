# 添加新的脚手架指南

本指南说明如何往 `all-package` 仓库添加新的脚手架，并发布到 Maven 中央仓库。

---

## 📐 整体架构

```
┌─────────────────────────────────────────────────────┐
│                all-package 仓库                     │
├─────────────────────────────────────────────────────┤
│                                                       │
│  新脚手架流程：                                       │
│                                                       │
│  ┌──────────────────┐                                │
│  │ 1. 创建项目源   │  ← 新脚手架的源码               │
│  │    文件          │     （模板项目）                │
│  └──────────────────┘                                │
│           ↓                                          │
│  ┌──────────────────┐                                │
│  │ 2. 配置 archetype│  ← 把源文件改造为               │
│  │    元数据        │     Archetype 模板             │
│  └──────────────────┘                                │
│           ↓                                          │
│  ┌──────────────────┐                                │
│  │ 3. 配置构建     │  ← 添加 GPG、签名、              │
│  │    插件          │     校验插件                    │
│  └──────────────────┘                                │
│           ↓                                          │
│  ┌──────────────────┐                                │
│  │ 4. 本地构建     │  ← mvn clean verify             │
│  └──────────────────┘                                │
│           ↓                                          │
│  ┌──────────────────┐                                │
│  │ 5. 打包 zip     │  ← 按 Sonatype 目录结构          │
│  └──────────────────┘                                │
│           ↓                                          │
│  ┌──────────────────┐                                │
│  │ 6. 上传         │  ← https://central.sonatype.com │
│  └──────────────────┘                                │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 详细步骤（以一个新脚手架为例）

假设你要添加一个名为 `my-react-scaffold` 的脚手架（任意语言/框架）。

### 第一步：创建脚手架源文件

在仓库根目录创建 `my-react-scaffold/` 目录，按 Maven Archetype 的要求组织文件。

**目录结构示例**（Java 风格）：

```
my-react-scaffold/
├── pom.xml                              # Archetype 项目 POM
└── src/
    └── main/
        └── resources/
            ├── META-INF/
            │   └── maven/
            │       └── archetype-metadata.xml   # ⭐ 关键文件
            └── archetype-resources/             # 模板资源
                ├── pom.xml                       # 生成的项目的 POM 模板
                └── src/
                    └── main/
                        └── java/
                            └── App.java        # 代码模板
```

### 第二步：编写 archetype-metadata.xml

这个文件告诉 Maven Archetype 哪些文件需要处理，怎么处理（变量替换等）。

**示例：** [maven-archetype/src/main/resources/META-INF/maven/archetype-metadata.xml](file:///Users/lizhi/projects/all-package/maven-archetype/src/main/resources/META-INF/maven/archetype-metadata.xml)

参考现在的配置，定义了：
- `requiredProperties`：必填参数（groupId、artifactId、version、package）
- `fileSets`：要包含的文件
  - `filtered="true"`：启用变量替换（如 `${package}`）
  - `packaged="true"`：按 package 路径自动创建目录

### 第三步：编写 archetype 的 pom.xml

参考 [maven-archetype/pom.xml](file:///Users/lizhi/projects/all-package/maven-archetype/pom.xml)。关键点：

#### 3.1 基本信息
```xml
<groupId>io.github.jhqxx</groupId>          <!-- 你的 groupId -->
<artifactId>my-react-scaffold</artifactId> <!-- 脚手架 ID -->
<version>1.0.0</version>
<packaging>maven-archetype</packaging>
```

#### 3.2 必填的项目元信息（Maven 中央仓库强制要求）

**⚠️ 缺一项都会被 Sonatype 拒绝：**

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

#### 3.3 必填的构建插件

```xml
<build>
    <extensions>
        <!-- archetype 打包扩展 -->
        <extension>
            <groupId>org.apache.maven.archetype</groupId>
            <artifactId>archetype-packaging</artifactId>
            <version>3.2.1</version>
        </extension>
    </extensions>

    <plugins>
        <!-- ① 源码包 -->
        <plugin>
            <artifactId>maven-source-plugin</artifactId>
            <version>3.2.1</version>
            <executions>
                <execution>
                    <id>attach-sources</id>
                    <goals>
                        <goal>jar-no-fork</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>

        <!-- ② 文档包 -->
        <plugin>
            <artifactId>maven-javadoc-plugin</artifactId>
            <version>3.6.3</version>
            <configuration>
                <doclint>none</doclint>  <!-- 关键：避免 javadoc 警告失败 -->
            </configuration>
            <executions>
                <execution>
                    <id>attach-javadocs</id>
                    <goals>
                        <goal>jar</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>

        <!-- ③ GPG 签名 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-gpg-plugin</artifactId>
            <version>3.2.5</version>
            <executions>
                <execution>
                    <id>sign-artifacts</id>
                    <phase>verify</phase>
                    <goals>
                        <goal>sign</goal>
                    </goals>
                </execution>
            </executions>
            <configuration>
                <gpgArguments>
                    <arg>--homedir</arg>
                    <arg>/tmp/gpg-home</arg>
                    <arg>--no-tty</arg>
                </gpgArguments>
            </configuration>
        </plugin>

        <!-- ④ 校验和（生成 .md5 .sha1） -->
        <plugin>
            <groupId>net.nicoulaj.maven.plugins</groupId>
            <artifactId>checksum-maven-plugin</artifactId>
            <version>1.11</version>
            <executions>
                <execution>
                    <id>create-checksums</id>
                    <goals>
                        <goal>artifacts</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### 第四步：本地构建验证

```bash
cd my-react-scaffold  # 进入新脚手架目录
mvn clean verify -DskipTests
```

构建成功后 `target/` 会有这些文件：
```
my-react-scaffold-1.0.0.jar
my-react-scaffold-1.0.0.jar.asc
my-react-scaffold-1.0.0.jar.md5
my-react-scaffold-1.0.0.jar.sha1
my-react-scaffold-1.0.0.pom
my-react-scaffold-1.0.0.pom.asc
my-react-scaffold-1.0.0.pom.md5
my-react-scaffold-1.0.0.pom.sha1
my-react-scaffold-1.0.0-sources.jar
my-react-scaffold-1.0.0-sources.jar.asc
... (sources 的 .md5 .sha1)
```

⚠️ 注意：`checksum-maven-plugin` **不会**自动为 pom 生成 md5/sha1，需要手动补：
```bash
cd target
md5 my-react-scaffold-1.0.0.pom > my-react-scaffold-1.0.0.pom.md5
shasum -a 1 my-react-scaffold-1.0.0.pom > my-react-scaffold-1.0.0.pom.sha1
md5 my-react-scaffold-1.0.0.pom.asc > my-react-scaffold-1.0.0.pom.asc.md5
shasum -a 1 my-react-scaffold-1.0.0.pom.asc > my-react-scaffold-1.0.0.pom.asc.sha1
```

### 第五步：打包成 zip

参考现有的 [pack-for-central.sh](file:///Users/lizhi/projects/all-package/maven-archetype/pack-for-central.sh)，**重要改两点**：

```bash
GROUP_PATH="io/github/jhqxx"
ARTIFACT_ID="my-react-scaffold"   # ← 改这里
VERSION="1.0.0"
TARGET_DIR="/Users/lizhi/projects/all-package/my-react-scaffold/target"  # ← 改这里
```

然后执行：
```bash
bash pack-for-central.sh
```

生成 `/tmp/central-publish/central-bundle.zip`（包含完整的 Sonatype 目录结构）。

### 第六步：上传到 Maven 中央仓库

1. 打开 https://central.sonatype.com/publishing
2. 登录（用 GitHub 账号）
3. 点击 **Upload Component** 或 **Publish**
4. 选择 `central-bundle.zip` 上传
5. 等待几小时审核

---

## 🔑 Namespace 注册（每个新 groupId 都要做）

如果你用新的 groupId（比如 `com.mycompany`），需要先注册 Namespace：

### GitHub 类型的 Namespace（推荐）

比如 `io.github.你的用户名`：

1. 登录 https://central.sonatype.com
2. Namespaces → Add Namespace
3. 选择 GitHub 类型
4. 输入 `io.github.<用户名>`
5. 自动验证通过

### 自定义域名类型

比如 `com.mycompany`：

1. 添加 TXT 记录到 `mycompany.com`：
   ```
   TXT _sonatype-challenge-mycompany.com=<token>
   ```
2. 在 Sonatype 添加 Namespace 即可

---

## 📋 发布检查清单

每次发布前核对：

- [ ] pom.xml 必填字段齐全：
  - [ ] `url`
  - [ ] `licenses` (name, url)
  - [ ] `developers` (name, email)
  - [ ] `scm` (connection, developerConnection, url)
- [ ] 4 个插件齐全：
  - [ ] maven-source-plugin
  - [ ] maven-javadoc-plugin（带 `<doclint>none</doclint>`）
  - [ ] maven-gpg-plugin（带 gpgArguments 配置）
  - [ ] checksum-maven-plugin
- [ ] 本地构建成功，target/ 下文件齐全
- [ ] 手动补全 pom 的 md5/sha1
- [ ] zip 包组织正确（按 groupId 路径分目录）
- [ ] 签名验证通过（`gpg --verify xxx.asc`）

---

## 🚀 一键发布流程（推荐）

把这套流程封装成一个脚本，未来新脚手架就只需要改配置：

```bash
#!/bin/bash
# 用法: ./release-new-scaffold.sh <脚手架目录名>
# 例如: ./release-new-scaffold.sh my-react-scaffold

SCAFFOLD_NAME=$1
VERSION="1.0.0"
ARTIFACT_ID="${SCAFFOLD_NAME}"

cd "${SCAFFOLD_NAME}"

echo "==== 1. 构建项目 ===="
mvn clean verify -DskipTests

echo "==== 2. 生成 pom 校验和 ===="
cd target
for ext in "" ".asc"; do
    md5 "${ARTIFACT_ID}-${VERSION}.pom${ext}" > "${ARTIFACT_ID}-${VERSION}.pom${ext}.md5"
    shasum -a 1 "${ARTIFACT_ID}-${VERSION}.pom${ext}" > "${ARTIFACT_ID}-${VERSION}.pom${ext}.sha1"
done

echo "==== 3. 打包 ===="
bash ../pack-for-central.sh  # 已存在的脚本

echo "==== 4. 验证签名 ===="
unzip -o /tmp/central-publish/central-bundle.zip -d /tmp/verify
for asc in $(find /tmp/verify -name "*.asc"); do
    gpg --homedir /tmp/gpg-home --verify "$asc" 2>&1 | grep -E "(Good|BAD)"
done

echo "==== 5. 完成 ===="
echo "请上传 /tmp/central-publish/central-bundle.zip 到"
echo "https://central.sonatype.com/publishing"
```

---

## ❓ 常见问题

### Q: Maven 3 vs Maven 4 的插件兼容性？
A: 你看到构建日志里有 "Ignoring incompatible plugin version 4.0.0-beta-1" 是 Maven 自动忽略了不兼容的 beta 插件，会找到兼容的稳定版。可以忽略。

### Q: 没有 javadoc 怎么办？
A: 如果脚手架本身没有 Java 类（比如 archetype 类型），会自动跳过 javadoc，**这是正常的**。

### Q: GPG 签不了名？
A: 检查 `/tmp/gpg-home` 目录存在，且有密钥文件。

### Q: 阿里云镜像拦截 central 仓库？
A: 确保 `~/.m2/settings.xml` 中 mirror 是 `<mirrorOf>*,!central</mirrorOf>`。

### Q: 想修改 groupId？
A: 修改 pom.xml 中的 `<groupId>`，但要先去 Sonatype 注册对应的 Namespace。

---

## 📚 相关文档

- [MAVEN_CENTRAL_PUBLISH.md](file:///Users/lizhi/projects/all-package/MAVEN_CENTRAL_PUBLISH.md) - 详细的发布步骤
- [README.md](file:///Users/lizhi/projects/all-package/README.md) - 项目总览
- 参考文章：https://bugstack.cn/md/road-map/ddd-archetype-maven.html
- 官方文档：https://central.sonatype.org/
