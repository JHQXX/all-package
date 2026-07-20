package io.github.jhqxx.agent.controller;

import io.github.jhqxx.agent.dto.ChatRequest;
import io.github.jhqxx.agent.dto.ChatResponse;
import io.github.jhqxx.agent.service.AgentService;
import io.github.jhqxx.agent.service.RagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class AgentController {

    @Autowired private AgentService agentService;
    @Autowired private RagService ragService;

    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest req) {
        return new ChatResponse(agentService.simpleChat(req.getMessage()));
    }

    @PostMapping("/agent")
    public ChatResponse agent(@RequestBody ChatRequest req) {
        return new ChatResponse(agentService.agentChat(req.getMessage()));
    }

    @PostMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> stream(@RequestBody ChatRequest req) {
        return agentService.streamChat(req.getMessage());
    }

    @PostMapping("/rag")
    public ChatResponse rag(@RequestBody ChatRequest req) {
        return new ChatResponse(ragService.askWithRetrieval(req.getMessage()));
    }

    @GetMapping("/health")
    public String health() {
        return "OK - SpringAI Agent is running";
    }
}