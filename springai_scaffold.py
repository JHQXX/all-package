"""
SpringAI 智能体项目脚手架生成器
================================

一键生成基于 Spring Boot + Spring AI 的 Java 智能体项目。

使用方法：
    python springai_scaffold.py <项目名称>

示例：
    python springai_scaffold.py my-springai-agent
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


# ========== Maven POM 文件 ==========

POM_XML_CONTENT = r'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.0</version>
        <relativePath/>
    </parent>

    <groupId>{group_id}</groupId>
    <artifactId>{artifact_id}</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>{project_name}</name>
    <description>SpringAI Agent Project</description>

    <properties>
        <java.version>17</java.version>
        <spring-ai.version>1.0.0-M6</spring-ai.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring AI OpenAI 启动器（兼容 OpenAI API 格式的其他模型）-->
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-openai-spring-boot-starter</artifactId>
        </dependency>

        <!-- Spring AI 向量存储 -->
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-vector-store-spring-boot-starter</artifactId>
        </dependency>

        <!-- Spring Boot 配置处理器 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-configuration-processor</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- 测试 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.ai</groupId>
                <artifactId>spring-ai-bom</artifactId>
                <version>${spring-ai.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
            <snapshots><enabled>false</enabled></snapshots>
        </repository>
    </repositories>
</project>
'''

# ========== 启动类 ==========

APP_JAVA_CONTENT = '''package {base_package};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * SpringAI 智能体启动类
 */
@SpringBootApplication
public class AgentApplication {

    public static void main(String[] args) {
        SpringApplication.run(AgentApplication.class, args);
        System.out.println("\\n" +
            "========================================\\n" +
            "  🚀 SpringAI 智能体启动成功！\\n" +
            "  访问: http://localhost:8080\\n" +
            "========================================\\n"
        );
    }
}
'''

# ========== AI 配置类 ==========

AI_CONFIG_JAVA = '''package {base_package}.config;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * AI 相关 Bean 配置
 *
 * 类似 Python LangChain 中的:
 *   llm = ChatOpenAI(model=..., api_key=..., base_url=...)
 *
 * 但在 Spring 中，Bean 由容器管理，更符合企业级开发习惯。
 */
@Configuration
public class AiConfig {

    /**
     * ChatClient Bean - 对话客户端
     * 类似 LangChain 的: prompt | llm | parser 组合
     */
    @Bean
    public ChatClient chatClient(ChatModel chatModel) {
        return ChatClient.builder(chatModel)
            .defaultSystem("你是一个专业的助手，回答要简洁准确。")
            .build();
    }

    /**
     * 简单向量存储 Bean（内存版，适合学习和测试）
     * 生产环境建议使用 PgVector、Milvus 等
     */
    @Bean
    public VectorStore vectorStore(EmbeddingModel embeddingModel) {
        return new SimpleVectorStore(embeddingModel);
    }
}
'''

# ========== 应用配置 ==========

APP_PROPERTIES_JAVA = '''package {base_package}.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * 应用配置属性
 * 类似 Python 的 pydantic Settings 类
 */
@Configuration
@ConfigurationProperties(prefix = "app")
public class AppProperties {

    private String name = "SpringAI Agent";
    private String version = "1.0.0";
    private boolean debug = false;

    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }

    public boolean isDebug() { return debug; }
    public void setDebug(boolean debug) { this.debug = debug; }
}
'''

# ========== 工具类 ==========

WEATHER_TOOL_JAVA = '''package {base_package}.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * 天气查询工具
 *
 * Spring AI 中通过 @Tool 注解定义工具，类似 LangChain 的 @tool 装饰器。
 * docstring 在 Java 中是 javadoc，会被 Spring AI 提取作为工具描述。
 */
@Component
public class WeatherTool {

    /**
     * 查询指定城市的天气信息
     *
     * @param city 城市名称，例如：北京、上海
     * @return 天气详情
     */
    @Tool(description = "查询指定城市的实时天气信息，支持北京、上海、广州、深圳等城市")
    public String getWeather(
            @ToolParam(description = "城市名称") String city) {

        // 模拟天气数据（实际项目调用真实 API）
        Map<String, String> weatherData = Map.of(
            "北京", "北京今天晴，温度 25°C，湿度 45%",
            "上海", "上海今天多云，温度 28°C，湿度 65%",
            "广州", "广州今天雷阵雨，温度 32°C，湿度 80%",
            "深圳", "深圳今天晴转多云，温度 30°C，湿度 70%"
        );

        return weatherData.getOrDefault(city,
            "抱歉，暂时不支持查询 " + city + " 的天气");
    }
}
'''

CALCULATOR_TOOL_JAVA = '''package {base_package}.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

/**
 * 计算器工具
 */
@Component
public class CalculatorTool {

    /**
     * 计算数学表达式
     *
     * @param expression 数学表达式，例如 (2+3)*4
     * @return 计算结果
     */
    @Tool(description = "数学计算器，支持加减乘除和括号运算")
    public String calculate(
            @ToolParam(description = "数学表达式字符串") String expression) {
        try {
            // 简单的安全计算（生产环境不要直接用 ScriptEngine 评估用户输入）
            javax.script.ScriptEngine engine = new javax.script.ScriptEngineManager()
                .getEngineByName("js");
            Object result = engine.eval(expression);
            return "计算结果：" + expression + " = " + result;
        } catch (Exception e) {
            return "计算错误：" + e.getMessage();
        }
    }
}
'''

DATETIME_TOOL_JAVA = '''package {base_package}.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * 日期时间工具
 */
@Component
public class DateTimeTool {

    /**
     * 获取当前日期和时间
     *
     * @return 当前时间字符串
     */
    @Tool(description = "获取当前的日期和时间，包括星期几")
    public String getCurrentTime() {
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH:mm:ss");
        String weekDay = getChineseWeekDay(now.getDayOfWeek().getValue());
        return "当前时间：" + now.format(formatter) + " " + weekDay;
    }

    private String getChineseWeekDay(int day) {
        String[] days = {"周一", "周二", "周三", "周四", "周五", "周六", "周日"};
        return days[day - 1];
    }
}
'''

# ========== 智能体服务 ==========

AGENT_SERVICE_JAVA = '''package {base_package}.service;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 智能体核心服务
 *
 * 类似 LangChain 中的 AgentExecutor，但更符合 Java 的依赖注入风格。
 */
@Service
public class AgentService {

    private final ChatClient chatClient;
    private final List<ToolCallback> tools;

    @Autowired
    public AgentService(ChatClient chatClient,
                        WeatherToolCallbackProvider weatherProvider,
                        CalculatorToolCallbackProvider calcProvider,
                        DateTimeToolCallbackProvider timeProvider) {
        this.chatClient = chatClient;
        // 实际工具回调会在下面创建
        this.tools = List.of();
    }

    /**
     * 简单对话（不带工具）
     */
    public String simpleChat(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .call()
            .content();
    }

    /**
     * 带工具的智能体对话
     */
    public String agentChat(String userMessage) {
        ChatResponse response = chatClient.prompt()
            .user(userMessage)
            .tools(new {base_package}.tools.WeatherTool(),
                   new {base_package}.tools.CalculatorTool(),
                   new {base_package}.tools.DateTimeTool())
            .call()
            .chatResponse();

        return response.getResult().getOutput().getContent();
    }

    /**
     * 流式对话
     */
    public reactor.core.publisher.Flux<String> streamChat(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .stream()
            .content();
    }
}
'''

# 为了简化，我们用更直接的实现

AGENT_SERVICE_SIMPLE_JAVA = '''package {base_package}.service;

import {base_package}.tools.CalculatorTool;
import {base_package}.tools.DateTimeTool;
import {base_package}.tools.WeatherTool;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

/**
 * 智能体核心服务
 *
 * 类似 LangChain 中的 AgentExecutor
 * 这里直接组合 ChatClient + 多个工具
 */
@Service
public class AgentService {

    private final ChatClient chatClient;

    public AgentService(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    /**
     * 简单对话（不带工具）
     */
    public String simpleChat(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .call()
            .content();
    }

    /**
     * 带工具的智能体对话
     *
     * 类似 Python 的:
     *   agent_executor = AgentExecutor(agent, tools)
     *   agent_executor.invoke({"input": userMessage})
     */
    public String agentChat(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .tools(
                new WeatherTool(),
                new CalculatorTool(),
                new DateTimeTool()
            )
            .call()
            .content();
    }

    /**
     * 流式对话（SSE）
     */
    public reactor.core.publisher.Flux<String> streamChat(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .stream()
            .content();
    }
}
'''

# ========== RAG 服务 ==========

RAG_SERVICE_JAVA = '''package {base_package}.service;

import jakarta.annotation.PostConstruct;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.File;
import java.nio.file.Files;
import java.util.List;

/**
 * RAG（检索增强生成）服务
 *
 * 类似 Python LangChain 的:
 *   loader = TextLoader(...)
 *   splitter = RecursiveCharacterTextSplitter(...)
 *   vector_store = FAISS.from_documents(chunks, embeddings)
 *   retriever = vector_store.as_retriever()
 *   rag_chain = prompt | llm | parser
 */
@Service
public class RagService {

    private final ChatClient chatClient;
    private final VectorStore vectorStore;
    private boolean initialized = false;

    public RagService(ChatClient chatClient, VectorStore vectorStore) {
        this.chatClient = chatClient;
        this.vectorStore = vectorStore;
    }

    /**
     * 启动时自动加载知识库
     */
    @PostConstruct
    public void init() {
        try {
            loadKnowledgeBase();
            initialized = true;
            System.out.println("✅ RAG 知识库加载完成");
        } catch (Exception e) {
            System.err.println("⚠️  知识库加载失败: " + e.getMessage());
        }
    }

    /**
     * 加载知识库文件
     */
    private void loadKnowledgeBase() throws Exception {
        // 从 resources/data 目录加载
        File dataDir = new File("src/main/resources/data");
        if (!dataDir.exists()) {
            return;
        }

        File[] files = dataDir.listFiles((dir, name) -> name.endsWith(".txt"));
        if (files == null || files.length == 0) {
            return;
        }

        for (File file : files) {
            // 读取文档
            TextReader reader = new TextReader(file.toURI().toURL());
            List<Document> documents = reader.get();

            // 文本分割
            TokenTextSplitter splitter = new TokenTextSplitter();
            List<Document> chunks = splitter.apply(documents);

            // 存入向量库
            vectorStore.add(chunks);
        }

        System.out.println("📚 已加载 " + files.length + " 个文档");
    }

    /**
     * RAG 问答
     */
    public String ask(String question) {
        if (!initialized) {
            return "知识库未初始化，请先添加文档到 src/main/resources/data/";
        }

        return chatClient.prompt()
            .user(question)
            .call()
            .content();
    }

    /**
     * 带检索的 RAG 问答（显式指定检索）
     */
    public String askWithRetrieval(String question) {
        // 检索相关文档
        List<Document> relevantDocs = vectorStore.similaritySearch(question);
        String context = relevantDocs.stream()
            .map(Document::getContent)
            .reduce("", (a, b) -> a + "\\n" + b);

        // 构建提示词
        String promptText = String.format("""
            根据以下参考资料回答问题。如果资料中没有答案，请说"不知道"。

            参考资料：
            %s

            问题：%s

            答案：
            """, context, question);

        return chatClient.prompt()
            .user(promptText)
            .call()
            .content();
    }
}
'''

# ========== Controller ==========

AGENT_CONTROLLER_JAVA = '''package {base_package}.controller;

import {base_package}.dto.ChatRequest;
import {base_package}.dto.ChatResponse;
import {base_package}.service.AgentService;
import {base_package}.service.RagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

/**
 * 智能体 REST API 控制器
 */
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class AgentController {

    @Autowired
    private AgentService agentService;

    @Autowired
    private RagService ragService;

    /**
     * 简单对话
     * POST /api/chat
     * Body: {"message": "你好"}
     */
    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        String reply = agentService.simpleChat(request.getMessage());
        return new ChatResponse(reply);
    }

    /**
     * 智能体对话（带工具）
     * POST /api/agent
     * Body: {"message": "北京今天天气怎么样？"}
     */
    @PostMapping("/agent")
    public ChatResponse agent(@RequestBody ChatRequest request) {
        String reply = agentService.agentChat(request.getMessage());
        return new ChatResponse(reply);
    }

    /**
     * 流式对话（SSE）
     * POST /api/stream
     */
    @PostMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> stream(@RequestBody ChatRequest request) {
        return agentService.streamChat(request.getMessage());
    }

    /**
     * RAG 问答
     * POST /api/rag
     * Body: {"message": "什么是 LangChain？"}
     */
    @PostMapping("/rag")
    public ChatResponse rag(@RequestBody ChatRequest request) {
        String reply = ragService.askWithRetrieval(request.getMessage());
        return new ChatResponse(reply);
    }

    /**
     * 健康检查
     */
    @GetMapping("/health")
    public String health() {
        return "OK - SpringAI Agent is running";
    }
}
'''

# ========== DTO ==========

CHAT_REQUEST_JAVA = '''package {base_package}.dto;

/**
 * 聊天请求 DTO
 */
public class ChatRequest {
    private String message;

    public ChatRequest() {}

    public ChatRequest(String message) {
        this.message = message;
    }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
}
'''

CHAT_RESPONSE_JAVA = '''package {base_package}.dto;

/**
 * 聊天响应 DTO
 */
public class ChatResponse {
    private String reply;
    private long timestamp = System.currentTimeMillis();

    public ChatResponse() {}

    public ChatResponse(String reply) {
        this.reply = reply;
    }

    public String getReply() { return reply; }
    public void setReply(String reply) { this.reply = reply; }

    public long getTimestamp() { return timestamp; }
    public void setTimestamp(long timestamp) { this.timestamp = timestamp; }
}
'''

# ========== 配置文件 ==========

APPLICATION_YML = r'''# SpringAI 智能体配置
server:
  port: 8080
  servlet:
    context-path: /

spring:
  application:
    name: {project_name}

  # AI 配置
  ai:
    # OpenAI 兼容接口配置（支持国内模型）
    openai:
      api-key: ${OPENAI_API_KEY:your_api_key_here}
      base-url: ${OPENAI_BASE_URL:https://api.openai.com/v1}
      chat:
        options:
          model: ${LLM_MODEL:gpt-3.5-turbo}
          temperature: 0.7
      embedding:
        options:
          model: text-embedding-ada-002

# 应用自定义配置
app:
  name: {project_name}
  version: 1.0.0
  debug: false

# 日志
logging:
  level:
    root: INFO
    {base_package}: DEBUG
    org.springframework.ai: INFO
'''

APPLICATION_DEV_YML = '''# 开发环境配置
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      base-url: ${OPENAI_BASE_URL:https://api.openai.com/v1}

logging:
  level:
    {base_package}: DEBUG
'''

# ========== 系统提示词 ==========

SYSTEM_PROMPT_ST = '''你是一个专业的 AI 助手，名字叫 {agent_name}。

你的能力：
1. 回答各种问题
2. 调用工具获取实时信息（天气、计算、时间等）
3. 基于知识库回答专业问题

回答规则：
- 用中文回答
- 简洁准确，重点突出
- 不确定的事情如实告知
- 必要时主动使用工具
'''

# ========== 测试类 ==========

TEST_JAVA = '''package {base_package};

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class AgentApplicationTests {

    @Test
    void contextLoads() {
        // 测试 Spring 上下文能否正常加载
    }
}
'''

# ========== 知识库示例 ==========

SAMPLE_KB_CONTENT = '''# LangChain 知识库

## 什么是 LangChain？

LangChain 是一个用于构建大语言模型（LLM）应用的开发框架。
它由 Harrison Chase 于 2022 年创建，核心思想是将不同的组件"链"在一起。

## 核心组件

1. Models（模型）：各种 LLM 和嵌入模型
2. Prompts（提示词）：模板化提示词管理
3. Chains（链）：组合多个步骤
4. Agents（智能体）：让 LLM 自主决策
5. Memory（记忆）：保存对话历史
6. Retrieval（检索）：从知识库检索

## Spring AI 对应

Spring AI 是 Java 生态对应的 AI 框架：
- ChatClient ≈ Python 的 ChatOpenAI
- @Tool 注解 ≈ Python 的 @tool 装饰器
- VectorStore ≈ FAISS / Chroma
- ChatMemory ≈ ConversationBufferMemory
'''

# ========== 其他辅助文件 ==========

GITIGNORE_CONTENT = '''# Java
target/
*.class
*.jar
*.war

# IDE
.idea/
.vscode/
*.iml
.project
.classpath
.settings/

# 环境变量
.env
.env.local

# 系统
.DS_Store
'''

ENV_EXAMPLE_CONTENT = '''# LLM 配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo

# 服务端口
SERVER_PORT=8080
'''

README_CONTENT = '''# {project_name}

基于 Spring Boot 3 + Spring AI 的 Java 智能体项目脚手架。

## 技术栈

- Spring Boot 3.3
- Spring AI 1.0
- Java 17
- Maven

## 快速开始

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的 OPENAI_API_KEY
```

### 2. 编译运行

```bash
# 使用 Maven
./mvnw spring-boot:run

# 或编译后运行
./mvnw clean package
java -jar target/{artifact_id}-0.0.1-SNAPSHOT.jar
```

### 3. 测试 API

```bash
# 简单对话
curl -X POST http://localhost:8080/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{{"message":"你好"}}'

# 智能体对话（带工具）
curl -X POST http://localhost:8080/api/agent \\
  -H "Content-Type: application/json" \\
  -d '{{"message":"北京今天天气怎么样"}}'

# RAG 问答
curl -X POST http://localhost:8080/api/rag \\
  -H "Content-Type: application/json" \\
  -d '{{"message":"什么是 LangChain"}}'
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| /api/chat | POST | 简单对话 |
| /api/agent | POST | 智能体对话（带工具）|
| /api/stream | POST | 流式对话（SSE）|
| /api/rag | POST | RAG 知识库问答 |
| /api/health | GET | 健康检查 |

## 添加工具

在 `tools/` 目录下创建新类：

```java
@Component
public class MyTool {{
    @Tool(description = "工具描述")
    public String myMethod(
            @ToolParam(description = "参数描述") String param) {{
        return "结果";
    }}
}}
```

然后在 `AgentService.agentChat()` 中注册：
```java
.tools(new MyTool())
```

## 添加知识库

把 `.txt` 文件放到 `src/main/resources/data/` 目录下，启动时会自动加载。
'''

# ========== 脚手架生成器 ==========

def create_springai_scaffold(project_name: str, group_id: str = "io.github.jhqxx"):
    """创建 SpringAI 脚手架"""

    artifact_id = project_name.lower().replace(" ", "-").replace("_", "-")
    base_package = f"{group_id}.agent"
    agent_name = project_name.replace("-", " ").title()

    project_root = Path(project_name)

    print(f"🚀 创建 SpringAI 脚手架: {project_name}")
    print(f"📁 目录: {project_root.absolute()}")
    print(f"📦 Maven GroupId: {group_id}")
    print(f"📦 包名: {base_package}\n")

    # 创建目录
    package_path = base_package.replace(".", "/")
    dirs = [
        project_root / "src/main/java" / package_path / "config",
        project_root / "src/main/java" / package_path / "controller",
        project_root / "src/main/java" / package_path / "service",
        project_root / "src/main/java" / package_path / "tools",
        project_root / "src/main/java" / package_path / "dto",
        project_root / "src/main/resources/prompts",
        project_root / "src/main/resources/data",
        project_root / "src/test/java" / package_path,
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  📂 {d.relative_to(project_root)}")

    # 文件映射
    files = {
        "pom.xml": POM_XML_CONTENT
            .replace("{group_id}", group_id)
            .replace("{project_name}", project_name)
            .replace("{artifact_id}", artifact_id),
        ".gitignore": GITIGNORE_CONTENT,
        ".env.example": ENV_EXAMPLE_CONTENT,
        "README.md": README_CONTENT.format(
            project_name=project_name,
            artifact_id=artifact_id,
        ),

        # 启动类
        f"src/main/java/{package_path}/AgentApplication.java":
            APP_JAVA_CONTENT,

        # 配置类
        f"src/main/java/{package_path}/config/AiConfig.java":
            AI_CONFIG_JAVA,
        f"src/main/java/{package_path}/config/AppProperties.java":
            APP_PROPERTIES_JAVA,

        # 工具类
        f"src/main/java/{package_path}/tools/WeatherTool.java":
            WEATHER_TOOL_JAVA,
        f"src/main/java/{package_path}/tools/CalculatorTool.java":
            CALCULATOR_TOOL_JAVA,
        f"src/main/java/{package_path}/tools/DateTimeTool.java":
            DATETIME_TOOL_JAVA,

        # 服务类
        f"src/main/java/{package_path}/service/AgentService.java":
            AGENT_SERVICE_SIMPLE_JAVA,
        f"src/main/java/{package_path}/service/RagService.java":
            RAG_SERVICE_JAVA,

        # Controller
        f"src/main/java/{package_path}/controller/AgentController.java":
            AGENT_CONTROLLER_JAVA,

        # DTO
        f"src/main/java/{package_path}/dto/ChatRequest.java":
            CHAT_REQUEST_JAVA,
        f"src/main/java/{package_path}/dto/ChatResponse.java":
            CHAT_RESPONSE_JAVA,

        # 资源文件
        "src/main/resources/application.yml":
            APPLICATION_YML.replace("{project_name}", project_name),
        "src/main/resources/application-dev.yml":
            APPLICATION_DEV_YML,
        "src/main/resources/prompts/system-prompt.st":
            SYSTEM_PROMPT_ST.format(agent_name=agent_name),
        "src/main/resources/data/langchain-intro.txt":
            SAMPLE_KB_CONTENT,

        # 测试
        f"src/test/java/{package_path}/AgentApplicationTests.java":
            TEST_JAVA,
    }

    # 写入文件
    for filepath, content in files.items():
        full_path = project_root / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # 替换 Java 文件中的包名占位符
        if filepath.endswith(".java"):
            content = content.replace("{base_package}", base_package)

        full_path.write_text(content, encoding="utf-8")
        print(f"  📄 {filepath}")

    print(f"\n✅ SpringAI 脚手架创建完成！\n")
    print("=" * 50)
    print("📋 下一步操作：")
    print("=" * 50)
    print(f"""
  cd {project_name}

  # 配置环境变量
  cp .env.example .env
  # 编辑 .env 填入你的 OPENAI_API_KEY

  # 运行（需要 Java 17+ 和 Maven）
  ./mvnw spring-boot:run

  # 测试
  curl -X POST http://localhost:8080/api/chat \\
    -H "Content-Type: application/json" \\
    -d '{{"message":"你好"}}'
""")


def main():
    parser = argparse.ArgumentParser(description="SpringAI 脚手架生成器")
    parser.add_argument("project_name", help="项目名称")
    parser.add_argument(
        "--group-id",
        default="io.github.jhqxx",
        help="Maven groupId（默认: io.github.jhqxx）"
    )

    args = parser.parse_args()
    create_springai_scaffold(args.project_name, args.group_id)


if __name__ == "__main__":
    main()