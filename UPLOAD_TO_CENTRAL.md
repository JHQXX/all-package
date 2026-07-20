# 上传到 Maven 中央仓库 - 立即开始

## 🎯 你现在需要做的 3 步

### 第 1 步：上传 zip 包

1. 打开 https://central.sonatype.com/publishing
2. 登录（用你之前注册用的 GitHub 账号）
3. 点击 **Upload Component** 或 **Publish** 按钮
4. 选择文件：`/tmp/central-publish/central-bundle.zip`
5. 点击上传

### 第 2 步：填写必要信息（如果有提示）

上传时如果要求填写：
- **Group ID**: `io.github.jhqxx`
- **Artifact ID**: `springai-agent-archetype`
- **Version**: `1.0.0`
- **Name**: `SpringAI Agent Archetype`
- **Description**: `Maven Archetype for generating Spring Boot 3 + Spring AI agent projects`
- **Project URL**: `https://github.com/JHQXX/all-package`

### 第 3 步：提交发布

1. 上传成功后，点击 **Publish** 或 **Drop** 按钮
2. 等待 **5 分钟 ~ 几小时** 的审核
3. 审核通过后，你的脚手架就会出现在：
   - https://repo.maven.apache.org/maven2/io/github/jhqxx/springai-agent-archetype/

---

## ✅ 发布成功的标志

发布成功后，全世界的开发者都可以用如下命令生成项目：

```bash
mvn archetype:generate \
  -DarchetypeGroupId=io.github.jhqxx \
  -DarchetypeArtifactId=springai-agent-archetype \
  -DarchetypeVersion=1.0.0 \
  -DgroupId=com.mycompany \
  -DartifactId=my-agent \
  -Dpackage=com.mycompany.agent \
  -DinteractiveMode=false
```

无需任何额外配置，直接成功！

---

## 🌐 发布后还需要做的事

### 更新 archetype-catalog.xml

发布成功后，把 `docs/archetype-catalog.xml` 中的 URL 改成 Maven 中央仓库的标准地址：

```xml
<archetype>
    <groupId>io.github.jhqxx</groupId>
    <artifactId>springai-agent-archetype</artifactId>
    <version>1.0.0</version>
    <repository>
        <id>central</id>  <!-- 改为 central -->
        <url>https://repo.maven.apache.org/maven2</url>  <!-- Maven 中央仓库 -->
    </repository>
    <description>...</description>
</archetype>
```

让 IDEA 可以通过 Catalog 找到你的脚手架。

---

## 📦 这次准备好的文件位置

```
/tmp/central-publish/
├── central-bundle.zip      ← ⭐ 这是你要上传的 31KB 文件
└── public-key.asc          ← 备用：GPG 公钥（一般不用单独传）
```

---

## 🔄 如果上传失败

可能的原因：
1. **签名验证失败** - 重新上传 `/tmp/central-publish/public-key.asc`
2. **元信息不全** - 检查 pom.xml 是否有 url、licenses、developers、scm
3. **版本已存在** - 你之前发布过 1.0.0 版本，需要改成 1.0.1 重新发布
4. **网络问题** - 重试几次

---

## ⏱️ 上传后的时间线

| 时间 | 状态 |
|------|------|
| 0 分钟 | 你上传了 zip |
| 5-30 分钟 | Sonatype 验证文件完整性、签名 |
| 1-4 小时 | 审核发布（一般会自动通过） |
| 1-2 天 | 完全同步到所有 Maven 镜像（aliyun、华为云等） |

---

## 📞 遇到问题怎么排查？

- 查看构建日志：https://central.sonatype.com/publishing （登录后查看 Deployments）
- 邮件通知：Sonatype 会在发布过程中发邮件给你
- 上传日志：页面会有详细的错误信息

---

## 🎉 发布成功后怎么知道？

1. 在 https://central.sonatype.com/browse （或登录后的 Browse 页面）能找到你的 artifact
2. 在 https://search.maven.org 搜索 `io.github.jhqxx` 能找到
3. 在 IDEA 中添加 Catalog URL `https://repo.maven.apache.org/maven2/archetype-catalog.xml` 能看到你的脚手架
