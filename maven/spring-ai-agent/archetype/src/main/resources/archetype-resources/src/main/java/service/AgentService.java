package ${package}.service;

import ${package}.tools.CalculatorTool;
import ${package}.tools.DateTimeTool;
import ${package}.tools.WeatherTool;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

/**
 * 智能体核心服务
 */
@Service
public class AgentService {

    private final ChatClient chatClient;

    public AgentService(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String simpleChat(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .call()
            .content();
    }

    public String agentChat(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .tools(new WeatherTool(), new CalculatorTool(), new DateTimeTool())
            .call()
            .content();
    }

    public reactor.core.publisher.Flux<String> streamChat(String userMessage) {
        return chatClient.prompt()
            .user(userMessage)
            .stream()
            .content();
    }
}