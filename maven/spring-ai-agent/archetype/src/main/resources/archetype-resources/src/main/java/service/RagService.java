package ${package}.service;

import jakarta.annotation.PostConstruct;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

/**
 * RAG 服务（基础版：文档直接注入到 LLM 上下文）
 *
 * ⚠️ 这是一个轻量版的 RAG 实现，不依赖外部向量数据库。
 * 它在启动时把 src/main/resources/data/*.txt 的内容加载进内存，
 * 然后每次问答时把相关文档作为上下文传给 LLM。
 *
 * 适用场景：
 * - 小规模知识库（几百 KB 以内的 .txt 文档）
 * - 不需要持久化、重排序、混合检索
 *
 * 升级到完整 RAG：
 * 1. 在 pom.xml 添加具体 vector-store starter：
 *    <dependency>
 *      <groupId>org.springframework.ai</groupId>
 *      <artifactId>spring-ai-starter-vector-store-qdrant</artifactId>
 *    </dependency>
 * 2. 把下面的代码改成使用 VectorStore bean
 *
 * 详见：https://docs.spring.io/spring-ai/reference/api/vectordbs.html
 */
@Service
public class RagService {

    private final ChatClient chatClient;
    private String knowledgeBase = "";
    private boolean initialized = false;

    public RagService(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    @PostConstruct
    public void init() {
        try {
            loadKnowledgeBase();
            initialized = true;
            if (!knowledgeBase.isEmpty()) {
                System.out.println("[RagService] knowledge base loaded ("
                        + knowledgeBase.length() + " chars).");
            }
        } catch (Exception e) {
            System.err.println("[RagService] failed to load: " + e.getMessage());
        }
    }

    /**
     * 从 src/main/resources/data/*.txt 加载所有文档并合并
     */
    private void loadKnowledgeBase() throws IOException {
        // 优先使用 classpath:*（运行时能找到）
        PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        try {
            Resource[] resources = resolver.getResources("classpath:data/*.txt");
            StringBuilder all = new StringBuilder();
            for (Resource res : resources) {
                if (res.exists() && res.isReadable()) {
                    String content = new String(res.getInputStream().readAllBytes(),
                            java.nio.charset.StandardCharsets.UTF_8);
                    all.append(content).append("\n");
                }
            }
            if (all.length() > 0) {
                this.knowledgeBase = all.toString();
                System.out.println("[RagService] loaded "
                        + resources.length + " files from classpath.");
                return;
            }
        } catch (Exception e) {
            // fall through
        }

        // 备选：扫描文件系统中的 src/main/resources/data（开发期）
        File dataDir = new File("src/main/resources/data");
        if (!dataDir.exists()) {
            return;
        }
        File[] files = dataDir.listFiles((dir, name) -> name.endsWith(".txt"));
        if (files == null || files.length == 0) {
            return;
        }

        StringBuilder all = new StringBuilder();
        for (File file : files) {
            all.append(Files.readString(file.toPath(), java.nio.charset.StandardCharsets.UTF_8))
               .append("\n");
        }
        this.knowledgeBase = all.toString();
        System.out.println("[RagService] loaded " + files.length + " files from filesystem.");
    }

    /**
     * 用知识库增强的问答
     */
    public String askWithRetrieval(String question) {
        if (!initialized || knowledgeBase.isEmpty()) {
            return "知识库未初始化（请在 src/main/resources/data/ 放 .txt 文件）";
        }

        String promptText = String.format("""
            根据以下参考资料回答问题。如果资料中没有答案，请说"不知道"。

            参考资料：
            %s

            问题：%s

            答案：
            """, knowledgeBase, question);

        return chatClient.prompt()
            .user(promptText)
            .call()
            .content();
    }
}
