"""
智能体项目脚手架生成器
======================

一行命令快速生成一个完整的 Python 智能体项目脚手架。

使用方法：
    python scaffold.py <项目名称>

示例：
    python scaffold.py my-chatbot
    python scaffold.py my-rag-system --with-rag
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


# ========== 模板文件内容 ==========

GITIGNORE_CONTENT = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
venv/
env/

# 环境变量
.env
.env.local

# IDE
.idea/
.vscode/

# 数据
data/faiss_index/
*.db

# 系统
.DS_Store
"""

REQUIREMENTS_CONTENT = """# LangChain 核心
langchain>=0.3.0
langchain-core>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
langchain-text-splitters>=0.3.0

# 向量数据库
faiss-cpu>=1.8.0

# 工具
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
"""

ENV_EXAMPLE_CONTENT = """# LLM 配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo

# 向量库
VECTOR_STORE_PATH=./data/faiss_index
"""

SETTINGS_PY_CONTENT = '''"""
配置管理
"""
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-3.5-turbo"
    VECTOR_STORE_PATH: str = "./data/faiss_index"

    class Config:
        env_file = ".env"


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
'''

SETTINGS_INIT_CONTENT = '''"""配置模块"""
from .settings import get_settings

__all__ = ["get_settings"]
'''

LLM_HELPER_CONTENT = '''"""
LLM 辅助函数 - 统一获取 LLM 实例
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import get_settings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


def get_llm(temperature: float = 0.7):
    """获取 LLM 实例"""
    settings = get_settings()
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=temperature,
    )


def simple_chat(prompt: str, system: str = None) -> str:
    """简单对话"""
    llm = get_llm()
    messages = []
    if system:
        messages.append(SystemMessage(content=system))
    messages.append(HumanMessage(content=prompt))
    response = llm.invoke(messages)
    return response.content


if __name__ == "__main__":
    # 测试
    settings = get_settings()
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_api_key_here":
        print("❌ 请先配置 .env 中的 OPENAI_API_KEY")
    else:
        answer = simple_chat("用一句话介绍你自己")
        print(f"AI: {answer}")
'''

SIMPLE_AGENT_CONTENT = '''"""
简单智能体示例
===============
这是你的第一个智能体！包含 3 个示例工具。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from llm_helper import get_llm
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor


# ========== 工具定义 ==========

@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculator(expression: str) -> str:
    """
    数学计算器，支持加减乘除和括号。

    Args:
        expression: 数学表达式，例如：(2+3)*4
    """
    try:
        allowed = set("0123456789+-*/().")
        if not all(c in allowed for c in expression):
            return "错误：包含非法字符"
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"计算错误: {e}"


@tool
def string_length(text: str) -> str:
    """
    计算字符串长度。

    Args:
        text: 要计算的字符串
    """
    return f"字符串 "{text}" 的长度是 {len(text)}"


# ========== 构建智能体 ==========

def build_agent(verbose: bool = True) -> AgentExecutor:
    """构建智能体"""
    llm = get_llm(temperature=0.3)
    tools = [get_current_time, calculator, string_length]

    prompt = ChatPromptTemplate.from_template("""
你是一个智能助手，可以使用以下工具回答问题。

可用工具:
{tools}

工具名称: {tool_names}

使用格式:
Thought: <思考>
Action: <工具名>
Action Input: <工具参数>
Observation: <工具结果>
... (可重复)
Thought: 我知道答案了
Final Answer: <最终答案>

问题: {input}
{agent_scratchpad}
""")

    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        handle_parsing_errors=True,
    )


def main():
    print("🤖 简单智能体启动")
    print("输入 'quit' 退出\\n")

    agent = build_agent(verbose=False)

    while True:
        try:
            user_input = input("你: ").strip()
            if user_input.lower() in ["quit", "exit", "退出"]:
                print("再见！")
                break
            if not user_input:
                continue

            result = agent.invoke({"input": user_input})
            print(f"AI: {result['output']}\\n")

        except KeyboardInterrupt:
            print("\\n再见！")
            break
        except Exception as e:
            print(f"出错了: {e}\\n")


if __name__ == "__main__":
    main()
'''

RAG_BASIC_CONTENT = '''"""
基础 RAG 示例
=============
演示如何用 LangChain 构建 RAG 问答系统。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from llm_helper import get_llm
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config.settings import get_settings


def build_vector_store():
    """构建向量库"""
    settings = get_settings()
    embeddings = OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )

    kb_path = Path(__file__).parent.parent / "data" / "knowledge_base"
    kb_path.mkdir(parents=True, exist_ok=True)

    # 加载所有 txt 文件
    docs = []
    for txt_file in kb_path.glob("*.txt"):
        loader = TextLoader(str(txt_file), encoding="utf-8")
        docs.extend(loader.load())

    if not docs:
        print(f"⚠️  知识库为空，请在 {kb_path} 目录下添加 .txt 文件")
        return None

    # 分割
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(docs)

    # 向量化
    vector_store = FAISS.from_documents(chunks, embeddings)
    print(f"✅ 向量库构建完成，共 {len(chunks)} 个片段")
    return vector_store


def build_rag_chain(vector_store):
    """构建 RAG 链"""
    llm = get_llm(temperature=0.3)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template("""
根据以下参考资料回答问题。如果资料中没有答案，说"不知道"。

参考资料:
{context}

问题: {question}

答案:
""")

    def format_docs(docs):
        return "\\n\\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def main():
    print("📚 RAG 问答系统")
    print("输入 'quit' 退出\\n")

    vector_store = build_vector_store()
    if not vector_store:
        return

    rag_chain = build_rag_chain(vector_store)

    while True:
        try:
            question = input("问题: ").strip()
            if question.lower() in ["quit", "exit", "退出"]:
                print("再见！")
                break
            if not question:
                continue

            answer = rag_chain.invoke(question)
            print(f"\\n答案: {answer}\\n")

        except KeyboardInterrupt:
            print("\\n再见！")
            break
        except Exception as e:
            print(f"出错了: {e}\\n")


if __name__ == "__main__":
    main()
'''

PROJECT_RULES_CONTENT = """# {project_name} - 项目规则

## 项目结构
```
{project_slug}/
├── llm_helper.py        # LLM 辅助函数
├── main.py              # 主入口
├── rag_basic.py         # RAG 示例
├── config/              # 配置
├── data/knowledge_base/ # 知识库
├── requirements.txt
├── .env.example
└── README.md
```

## 开发流程

### 1. 环境搭建
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入 API Key
```

### 2. 运行示例
```bash
python llm_helper.py   # 测试 LLM
python main.py         # 运行智能体
python rag_basic.py    # 运行 RAG
```

## 编码规范
- 函数/变量用 snake_case
- 类名用 PascalCase
- 所有配置通过环境变量
- 工具必须有完整 docstring

## 后续扩展
- 添加更多工具到 main.py
- 用 Streamlit 做 Web 界面
- 加入 LangGraph 实现多智能体
"""

README_CONTENT = """# {project_name}

基于 LangChain 的 Python 智能体项目脚手架。

## 快速开始

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY

# 4. 运行
python llm_helper.py   # 测试 LLM 连接
python main.py         # 智能体对话
python rag_basic.py    # RAG 问答
```

## 文件说明

- `llm_helper.py` - LLM 统一调用接口
- `main.py` - 智能体主程序（带工具调用）
- `rag_basic.py` - RAG 知识库问答示例
- `config/settings.py` - 配置管理
- `data/knowledge_base/` - 知识库目录（放入 txt 文件）

## 添加新工具

在 `main.py` 中添加：
```python
@tool
def my_tool(param: str) -> str:
    \"\"\"工具描述\"\"\"
    return f"结果: {{param}}"
```

然后添加到 tools 列表。

## 推送到 GitHub

```bash
git init
git add .
git commit -m "feat: 初始化项目"
git remote add origin <your-repo-url>
git push -u origin main
```
"""

SAMPLE_KB_CONTENT = """# 项目知识库示例

## 什么是 LangChain？

LangChain 是一个用于构建大语言模型应用的开发框架。
它提供了链、智能体、工具等核心组件。

## LangChain 的主要功能

1. 模型集成：支持 OpenAI、Anthropic 等多种 LLM
2. 提示词工程：模板化、动态生成
3. 链式调用：组合多个步骤形成复杂流程
4. 智能体：让 LLM 自主决策使用工具
5. RAG：基于私有知识库的问答

## 如何学习 LangChain？

1. 先掌握 Python 基础
2. 了解 LLM 的基本概念
3. 从简单 Chain 开始
4. 学习工具调用
5. 实践 RAG 应用
6. 探索多智能体（LangGraph）
"""


# ========== 脚手架生成器 ==========

def create_scaffold(project_name: str, with_rag: bool = True):
    """创建脚手架"""

    # 项目名处理
    project_slug = project_name.lower().replace(" ", "-").replace("_", "-")
    project_root = Path(project_name)

    print(f"🚀 创建项目脚手架: {project_name}")
    print(f"📁 目录: {project_root.absolute()}\n")

    # 目录结构
    dirs = [
        project_root / "config",
        project_root / "data" / "knowledge_base",
    ]

    if with_rag:
        dirs.append(project_root / "examples")

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  📂 {d.relative_to(project_root)}")

    # 文件映射
    files = {
        ".gitignore": GITIGNORE_CONTENT,
        "requirements.txt": REQUIREMENTS_CONTENT,
        ".env.example": ENV_EXAMPLE_CONTENT,
        "config/settings.py": SETTINGS_PY_CONTENT,
        "config/__init__.py": SETTINGS_INIT_CONTENT,
        "llm_helper.py": LLM_HELPER_CONTENT,
        "main.py": SIMPLE_AGENT_CONTENT,
        "PROJECT_RULES.md": PROJECT_RULES_CONTENT.format(
            project_name=project_name,
            project_slug=project_slug,
        ),
        "README.md": README_CONTENT.format(project_name=project_name),
        "data/knowledge_base/sample.txt": SAMPLE_KB_CONTENT,
    }

    if with_rag:
        files["examples/rag_basic.py"] = RAG_BASIC_CONTENT

    # 写入文件
    for filepath, content in files.items():
        full_path = project_root / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        print(f"  📄 {filepath}")

    # 完成提示
    print(f"\n✅ 脚手架创建完成！\n")
    print("=" * 50)
    print("📋 下一步操作：")
    print("=" * 50)
    print(f"\n  cd {project_name}")
    print("  python3 -m venv venv")
    print("  source venv/bin/activate")
    print("  pip install -r requirements.txt")
    print("  cp .env.example .env")
    print("  # 编辑 .env 填入你的 API Key")
    print("  python llm_helper.py  # 测试一下")
    print()


def main():
    parser = argparse.ArgumentParser(description="智能体项目脚手架生成器")
    parser.add_argument("project_name", help="项目名称")
    parser.add_argument("--with-rag", action="store_true", default=True,
                        help="包含 RAG 示例（默认开启）")
    parser.add_argument("--no-rag", dest="with_rag", action="store_false",
                        help="不包含 RAG 示例")

    args = parser.parse_args()
    create_scaffold(args.project_name, args.with_rag)


if __name__ == "__main__":
    main()