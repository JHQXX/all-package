package io.github.jhqxx.agent.service;

import jakarta.annotation.PostConstruct;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.List;

@Service
public class RagService {

    private final ChatClient chatClient;
    private final VectorStore vectorStore;
    private boolean initialized = false;

    public RagService(ChatClient chatClient, VectorStore vectorStore) {
        this.chatClient = chatClient;
        this.vectorStore = vectorStore;
    }

    @PostConstruct
    public void init() {
        try {
            loadKnowledgeBase();
            initialized = true;
            System.out.println("RAG knowledge base loaded.");
        } catch (Exception e) {
            System.err.println("Failed to load knowledge base: " + e.getMessage());
        }
    }

    private void loadKnowledgeBase() throws Exception {
        File dataDir = new File("src/main/resources/data");
        if (!dataDir.exists()) return;
        File[] files = dataDir.listFiles((dir, name) -> name.endsWith(".txt"));
        if (files == null || files.length == 0) return;
        for (File file : files) {
            TextReader reader = new TextReader(file.toURI().toURL());
            List<Document> docs = reader.get();
            vectorStore.add(new TokenTextSplitter().apply(docs));
        }
        System.out.println("Loaded " + files.length + " documents.");
    }

    public String askWithRetrieval(String question) {
        if (!initialized) return "Knowledge base not initialized.";
        List<Document> docs = vectorStore.similaritySearch(question);
        String context = docs.stream().map(Document::getContent).reduce("", (a, b) -> a + "\n" + b);
        String prompt = String.format("根据以下参考资料回答问题。\n\n%s\n\n问题：%s\n\n答案：", context, question);
        return chatClient.prompt().user(prompt).call().content();
    }
}