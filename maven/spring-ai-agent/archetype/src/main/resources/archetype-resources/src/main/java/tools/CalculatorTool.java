package ${package}.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

/**
 * 计算器工具
 */
@Component
public class CalculatorTool {

    @Tool(description = "数学计算器，支持加减乘除和括号运算")
    public String calculate(
            @ToolParam(description = "数学表达式") String expression) {
        try {
            javax.script.ScriptEngine engine = new javax.script.ScriptEngineManager()
                .getEngineByName("js");
            Object result = engine.eval(expression);
            return "计算结果：" + expression + " = " + result;
        } catch (Exception e) {
            return "计算错误：" + e.getMessage();
        }
    }
}