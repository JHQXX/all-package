package io.github.jhqxx.agent.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Component
public class DateTimeTool {

    @Tool(description = "获取当前的日期和时间")
    public String getCurrentTime() {
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH:mm:ss");
        String[] days = {"周一", "周二", "周三", "周四", "周五", "周六", "周日"};
        return "当前时间：" + now.format(formatter) + " " + days[now.getDayOfWeek().getValue() - 1];
    }
}