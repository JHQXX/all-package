package io.github.jhqxx.agent;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AgentApplication {

    public static void main(String[] args) {
        SpringApplication.run(AgentApplication.class, args);
        System.out.println("\n" +
            "========================================\n" +
            "  SpringAI Agent started successfully!\n" +
            "  URL: http://localhost:8080\n" +
            "========================================\n"
        );
    }
}