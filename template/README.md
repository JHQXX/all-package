# SpringAI Agent 模板项目

> 点击右上角的 **"Use this template"** 按钮即可基于此模板创建新项目

## 🚀 三步开始

### 1. 创建项目

点击本仓库的 **"Use this template" → "Create a new repository"**

### 2. 克隆到本地

```bash
git clone https://github.com/你的用户名/你的新项目名.git
cd 你的新项目名
```

### 3. 配置并运行

```bash
# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY

# 运行
./mvnw spring-boot:run
```

## 📚 包含内容

- Spring Boot 3.3 + Spring AI 1.0
- ChatClient Bean 配置
- 3 个示例工具：天气、计算器、时间
- RAG 服务（自动加载 `data/*.txt`）
- REST API：/api/chat, /api/agent, /api/rag, /api/stream

## 🔧 自定义包名

创建项目后，全局替换 `io.github.jhqxx.agent` 为你自己的包名。

## 📋 API 测试

```bash
# 简单对话
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你好"}'

# 智能体对话
curl -X POST http://localhost:8080/api/agent \
  -H "Content-Type: application/json" \
  -d '{"message":"北京今天天气怎么样"}'

# RAG 问答
curl -X POST http://localhost:8080/api/rag \
  -H "Content-Type: application/json" \
  -d '{"message":"什么是 LangChain"}'
```