package com.demo.agent.controller;

import com.demo.agent.dto.ChatRequest;
import com.demo.agent.dto.ChatResponse;
import com.demo.agent.service.AgentService;
import com.demo.agent.service.RagService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

/**
 * 智能体 REST API
 */
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class AgentController {

    @Autowired
    private AgentService agentService;

    @Autowired
    private RagService ragService;

    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        return new ChatResponse(agentService.simpleChat(request.getMessage()));
    }

    @PostMapping("/agent")
    public ChatResponse agent(@RequestBody ChatRequest request) {
        return new ChatResponse(agentService.agentChat(request.getMessage()));
    }

    @PostMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> stream(@RequestBody ChatRequest request) {
        return agentService.streamChat(request.getMessage());
    }

    @PostMapping("/rag")
    public ChatResponse rag(@RequestBody ChatRequest request) {
        return new ChatResponse(ragService.askWithRetrieval(request.getMessage()));
    }

    @GetMapping("/health")
    public String health() {
        return "OK - SpringAI Agent is running";
    }
}