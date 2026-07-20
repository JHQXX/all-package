package ${package}.dto;

public class ChatResponse {
    private String reply;
    private long timestamp = System.currentTimeMillis();

    public ChatResponse() {}
    public ChatResponse(String reply) { this.reply = reply; }

    public String getReply() { return reply; }
    public void setReply(String reply) { this.reply = reply; }

    public long getTimestamp() { return timestamp; }
    public void setTimestamp(long timestamp) { this.timestamp = timestamp; }
}