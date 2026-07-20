# ${artifactId}

基于 Spring Boot 3 + Spring AI 的 Java 智能体项目（由 Maven Archetype 生成）。

## 快速开始

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY
```

### 2. 编译运行

```bash
./mvnw spring-boot:run
# 或者
mvn spring-boot:run
```

### 3. 测试 API

```bash
# 简单对话
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你好"}'

# 智能体对话（带工具）
curl -X POST http://localhost:8080/api/agent \
  -H "Content-Type: application/json" \
  -d '{"message":"北京今天天气怎么样"}'

# RAG 问答
curl -X POST http://localhost:8080/api/rag \
  -H "Content-Type: application/json" \
  -d '{"message":"什么是 LangChain"}'
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| /api/chat | POST | 简单对话 |
| /api/agent | POST | 智能体对话（带工具）|
| /api/stream | POST | 流式对话（SSE）|
| /api/rag | POST | RAG 知识库问答 |
| /api/health | GET | 健康检查 |

## 添加知识库

把 `.txt` 文件放到 `src/main/resources/data/` 目录下，启动时会自动加载到向量库。

## 添加自定义工具

在 `${package}/tools/` 目录下创建工具类：

```java
@Component
public class MyTool {
    @Tool(description = "工具描述")
    public String myMethod(@ToolParam(description = "参数描述") String param) {
        return "结果";
    }
}
```

然后在 `AgentService.agentChat()` 中注册。