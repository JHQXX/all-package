# All Package - 脚手架集合

> 一站式项目脚手架仓库，包含多种技术栈的项目模板。

---

## 📦 包含的脚手架

### 1. SpringAI 智能体脚手架（Java）

基于 Spring Boot 3 + Spring AI 的 Java 智能体项目模板。

**特点：**
- ✅ ChatClient 对话客户端
- ✅ @Tool 工具调用注解
- ✅ RAG 检索增强生成
- ✅ 向量存储（SimpleVectorStore）
- ✅ REST API 接口
- ✅ 完整的分层结构（config/controller/service/tools/dto）

**使用方式：**

#### 方式一：Maven Archetype（推荐）

```bash
mvn archetype:generate \
  -DarchetypeGroupId=io.github.jhqxx \
  -DarchetypeArtifactId=springai-agent-archetype \
  -DarchetypeVersion=1.0.0 \
  -DgroupId=你的groupID \
  -DartifactId=项目名 \
  -Dpackage=你的完整包名 \
  -DinteractiveMode=false
```

#### 方式二：克隆模板项目

```bash
# 克隆 template 目录作为起点
git clone <仓库地址> my-project
# 然后使用 IDEA 的 Refactor → Rename 修改包名
```

#### 方式三：Python 脚本生成

```bash
python3 springai_scaffold.py 项目名 --group-id com.mycompany
```

---

### 2. Python 智能体脚手架

基于 LangChain 的 Python 智能体项目模板。

**使用方式：**

```bash
python3 scaffold.py 项目名
```

---

## 📁 目录结构

```
all-package/
├── maven-archetype/          # Maven Archetype 源码
│   ├── pom.xml
│   └── src/main/resources/
│       ├── META-INF/maven/
│       │   └── archetype-metadata.xml
│       └── archetype-resources/  # 模板文件
│           ├── pom.xml
│           └── src/
├── template/                 # 模板项目（克隆用）
│   ├── pom.xml
│   └── src/
├── demo-agent/               # 示例项目（可直接运行）
│   ├── pom.xml
│   └── src/
├── docs/                     # GitHub Pages 托管
│   ├── repo/                 # Maven 仓库（archetype jar）
│   ├── archetype-catalog.xml # Archetype 目录
│   └── index.html
├── springai_scaffold.py      # SpringAI 脚手架生成脚本
├── scaffold.py               # Python 脚手架生成脚本
├── build_and_publish.py      # 构建发布脚本
└── README.md
```

---

## 🚀 快速开始

### 生成 SpringAI 项目

```bash
mvn archetype:generate \
  -DarchetypeGroupId=io.github.jhqxx \
  -DarchetypeArtifactId=springai-agent-archetype \
  -DarchetypeVersion=1.0.0 \
  -DgroupId=com.example \
  -DartifactId=my-agent \
  -Dpackage=com.example.agent \
  -DinteractiveMode=false

cd my-agent

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 OPENAI_API_KEY

# 运行
./mvnw spring-boot:run
```

---

## 🔧 构建与发布（维护者用）

### 重新构建 Archetype

```bash
cd maven-archetype
mvn clean install
```

### 发布到 GitHub Pages

```bash
python3 build_and_publish.py
```

---

## 📚 技术栈

| 脚手架 | 技术栈 | 说明 |
|--------|--------|------|
| SpringAI 智能体 | Spring Boot 3 + Spring AI 1.0 | Java 生态智能体开发 |
| Python 智能体 | LangChain + FAISS | Python 生态智能体开发 |

---

## 📝 更新日志

### v1.0.0
- SpringAI 智能体脚手架发布
- Maven Archetype 支持
- Python 脚手架脚本支持
