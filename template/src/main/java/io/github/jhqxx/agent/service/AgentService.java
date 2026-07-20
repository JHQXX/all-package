package io.github.jhqxx.agent.service;

import io.github.jhqxx.agent.tools.CalculatorTool;
import io.github.jhqxx.agent.tools.DateTimeTool;
import io.github.jhqxx.agent.tools.WeatherTool;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

@Service
public class AgentService {

    private final ChatClient chatClient;

    public AgentService(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String simpleChat(String message) {
        return chatClient.prompt().user(message).call().content();
    }

    public String agentChat(String message) {
        return chatClient.prompt()
            .user(message)
            .tools(new WeatherTool(), new CalculatorTool(), new DateTimeTool())
            .call()
            .content();
    }

    public reactor.core.publisher.Flux<String> streamChat(String message) {
        return chatClient.prompt().user(message).stream().content();
    }
}