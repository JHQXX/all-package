package ${package}.config;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * AI Bean 配置
 */
@Configuration
public class AiConfig {

    @Bean
    public ChatClient chatClient(ChatModel chatModel) {
        return ChatClient.builder(chatModel)
            .defaultSystem("你是一个专业的助手，回答要简洁准确。")
            .build();
    }

    // 如果需要 RAG 向量存储，按需添加对应 starter 并启用下面的 Bean：
    //
    // <dependency>
    //   <groupId>org.springframework.ai</groupId>
    //   <artifactId>spring-ai-starter-vector-store-qdrant</artifactId>
    // </dependency>
    //
    // 然后引入：
    // import org.springframework.ai.vectorstore.VectorStore;
    // import org.springframework.ai.vectorstore.SimpleVectorStore;
    //
    // @Bean
    // public VectorStore vectorStore(EmbeddingModel embeddingModel) {
    //     return new SimpleVectorStore(embeddingModel);
    // }
}
