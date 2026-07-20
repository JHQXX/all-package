# All Package - 脚手架集合

> 一个仓库统一管理所有语言的脚手架，按目录分类。

[![Maven Central](https://img.shields.io/badge/Maven%20Central-1.0.0-blue)](https://repo.maven.apache.org/maven2/io/github/jhqxx/springai-agent-archetype/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-LIVE-green)](https://jhqxx.github.io/all-package/)

---

## 📦 已发布的脚手架

| 脚手架 | 语言/框架 | 状态 | 说明 |
|--------|-----------|------|------|
| [springai-agent-archetype](maven/spring-ai-agent/archetype/) | Java + Spring AI | ✅ Maven Central 1.0.0 | Spring Boot 3 + Spring AI 智能体脚手架 |
| [demo-agent](maven/demo/demo-agent/) | Java + Spring AI | ✅ 示例 | 从脚手架生成的项目示例 |

---

## 📁 项目结构

```
all-package/
├── maven/                           # Maven/Java 相关脚手架
│   ├── spring-ai-agent/            # Spring AI 智能体脚手架
│   │   └── archetype/               # Maven Archetype 源码
│   │       ├── pom.xml
│   │       ├── build-and-pack.sh   # 🔨 一键打包 + 上传准备
│   │       ├── clean-publish.sh    # 🧹 手动清理脚本
│   │       └── src/main/resources/archetype-resources/  # 模板文件
│   └── demo/demo-agent/             # 可运行的示例项目
├── python/                          # Python 脚手架（未来扩展）
├── docs/                            # GitHub Pages（部署后是网站）
│   ├── index.html                   # 🌐 项目首页
│   ├── jhqxx-catalog.xml            # 🎯 IDEA 用的私有 Catalog
│   └── archetype-catalog.xml        # Maven Central 兼容的 Catalog
└── README.md
```

---

## 🚀 在 IDEA 中使用（推荐 ⭐）

### 一次性配置

**步骤 1**：添加 Catalog（推荐 jsDelivr ⭐）

打开 IDEA 添加 Catalog 的时候，**两个都试一下**，谁快用谁：

| 优先级 | Location | 优点 |
|--------|----------|------|
| ⭐ 首选 | `https://cdn.jsdelivr.net/gh/JHQXX/all-package/docs/jhqxx-catalog.xml` | 全球 CDN、推送即生效、国内可用 |
| 备用 | `https://jhqxx.github.io/all-package/jhqxx-catalog.xml` | GitHub 原生、但国内偶有超时 |

```
File → New → Project → Maven Archetype → Manage catalogs...
→ 点 "+" → Add Catalog
→ Location: 上面的 URL（推荐 jsDelivr）
→ Name: JHQXX 脚手架
→ OK
```

**步骤 2**：使用脚手架
```
File → New → Project → Maven Archetype
→ 选中 jhqxx-catalog
→ 只看得到 JHQXX 自己的脚手架，干净！
→ 选 springai-agent-archetype:1.0.0
```

### 通过命令行使用

```bash
mvn archetype:generate \
  -DarchetypeGroupId=io.github.jhqxx \
  -DarchetypeArtifactId=springai-agent-archetype \
  -DarchetypeVersion=1.0.0 \
  -DgroupId=com.example \
  -DartifactId=my-agent \
  -Dpackage=com.example.agent \
  -DinteractiveMode=false
```

---

## 🔧 维护指南

### 🏗️ 修改已发布的脚手架

修改 `maven/spring-ai-agent/archetype/src/main/resources/archetype-resources/` 下的文件，然后：

```bash
cd maven/spring-ai-agent/archetype
bash build-and-pack.sh     # 构建并生成 central-bundle.zip
# 上传到 https://central.sonatype.com/publishing
```

详细发布流程：见 [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md)

### ➕ 添加新的脚手架

1. 创建新目录：`maven/your-scaffold/` 或 `python/your-scaffold/`
2. 按照已有的 `spring-ai-agent/archetype/` 结构组织
3. 修改 `build-and-pack.sh` 适配你的脚手架
4. 更新 README 的「已发布的脚手架」表格

### 🧹 清理发布产物

archetype 目录下的产物（zip、target/）应该会自动清理。如果要**立即**清理：

```bash
cd maven/spring-ai-agent/archetype
bash clean-publish.sh
```

---

## 🔗 相关链接

- 🌐 项目首页：https://jhqxx.github.io/all-package/
- 🎯 私有 Catalog：https://jhqxx.github.io/all-package/jhqxx-catalog.xml
- 📦 Maven Central：https://repo.maven.apache.org/maven2/io/github/jhqxx/springai-agent-archetype/
- 🐙 GitHub：https://github.com/JHQXX/all-package

---

## 📚 文档

- [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) - 如何发布到 Maven Central
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 常见问题与解决

---

## 🎉 当前进度

```
✅ 已发布: springai-agent-archetype 1.0.0
✅ GitHub Pages 在线
✅ 在 IDEA 中可通过私有 Catalog 直接看到
⏳ 待做: 添加更多脚手架（Python、RAG、Web Agent 等）
```
