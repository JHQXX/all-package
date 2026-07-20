package io.github.jhqxx.agent.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class WeatherTool {

    @Tool(description = "查询指定城市的实时天气信息")
    public String getWeather(@ToolParam(description = "城市名称") String city) {
        Map<String, String> weatherData = Map.of(
            "北京", "北京今天晴，温度 25°C",
            "上海", "上海今天多云，温度 28°C",
            "广州", "广州今天雷阵雨，温度 32°C",
            "深圳", "深圳今天晴转多云，温度 30°C"
        );
        return weatherData.getOrDefault(city, "抱歉，暂时不支持查询 " + city + " 的天气");
    }
}