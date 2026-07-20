package ${package}.service;

import jakarta.annotation.PostConstruct;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.List;

/**
 * RAG 服务
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
            List<Document> documents = reader.get();
            TokenTextSplitter splitter = new TokenTextSplitter();
            List<Document> chunks = splitter.apply(documents);
            vectorStore.add(chunks);
        }
        System.out.println("Loaded " + files.length + " documents.");
    }

    public String askWithRetrieval(String question) {
        if (!initialized) {
            return "Knowledge base not initialized.";
        }
        List<Document> relevantDocs = vectorStore.similaritySearch(question);
        String context = relevantDocs.stream()
            .map(Document::getContent)
            .reduce("", (a, b) -> a + "\n" + b);

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