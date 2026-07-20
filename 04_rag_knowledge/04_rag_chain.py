"""
04 - RAG 问答链 (RAG Chain)

Java/SpringAI 对比：
- SpringAI: RetrievalAugmentedAdvisor / ChatClient + VectorStore
- LangChain: RetrievalQA / create_retrieval_chain
- RAG = Retrieval-Augmented Generation（检索增强生成）
- 核心流程：用户提问 → 检索相关文档 → 把文档 + 问题一起发给 LLM → 生成答案
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import is_config_ready, get_settings
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader


def get_llm():
    settings = get_settings()
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=0.3,
    )


def get_embeddings():
    settings = get_settings()
    return OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        model="text-embedding-ada-002",
    )


def build_sample_vector_store():
    """构建示例向量库（用知识库目录的文件）"""
    kb_path = Path(__file__).parent.parent / "data" / "knowledge_base"

    # 如果知识库目录为空，先创建示例文档
    if not any(kb_path.glob("*.txt")):
        import importlib
        loader_module = importlib.import_module("01_document_loader")
        # 实际上我们直接创建
        docs = [
            Document(
                page_content="""
LangChain 是一个用于构建大语言模型（LLM）应用的开发框架。
它的核心思想是将不同的组件链接（Chain）在一起。

LangChain 的核心组件：
1. Models: 各种 LLM 和嵌入模型
2. Prompts: 提示词模板、示例选择器
3. Chains: 将多个组件组合
4. Agents: 让 LLM 自主决策使用工具
5. Memory: 保存对话历史
6. Retrieval: 从知识库检索信息

LangChain 支持 Python 和 JavaScript，Python 版本功能最完善。
                """.strip(),
                metadata={"source": "langchain.txt"}
            ),
            Document(
                page_content="""
RAG（检索增强生成）是一种结合信息检索和文本生成的技术。
它可以让大语言模型基于私有知识库回答问题，而不需要重新训练模型。

RAG 的工作流程：
1. 文档加载：读取各种格式的文档
2. 文本分割：将长文档切分成小块
3. 向量化：用 Embedding 模型把文本转成向量
4. 存储：把向量存入向量数据库
5. 检索：用户提问时，找出最相关的文档片段
6. 生成：把相关文档和问题一起发给 LLM，生成答案

RAG 的优势：
- 可以使用私有数据
- 成本低，不需要微调
- 可以实时更新知识库
- 答案可溯源（可以引用具体文档）
                """.strip(),
                metadata={"source": "rag.txt"}
            ),
            Document(
                page_content="""
FAISS 是 Facebook AI Research 开发的向量相似度搜索库。
它能够高效地在大规模向量数据集中进行相似度搜索。

FAISS 的特点：
1. 速度快：针对大规模数据优化
2. 内存效率高：支持压缩存储
3. 灵活：支持多种索引类型
4. GPU 加速：可以使用 GPU 进一步提升速度

FAISS 在 RAG 系统中常用于存储和检索文档向量。
                """.strip(),
                metadata={"source": "faiss.txt"}
            ),
        ]
    else:
        # 从目录加载
        docs = []
        for txt_file in sorted(kb_path.glob("*.txt")):
            loader = TextLoader(str(txt_file), encoding="utf-8")
            loaded = loader.load()
            docs.extend(loaded)

    # 分割
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    # 创建向量库
    vector_store = FAISS.from_documents(chunks, get_embeddings())
    return vector_store


def basic_rag_chain():
    """基础 RAG 链"""
    print("=" * 60)
    print("1. 基础 RAG 问答链")
    print("=" * 60)

    vector_store = build_sample_vector_store()
    llm = get_llm()

    # 创建检索器 - 类似 Java 的 Retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # 返回最相关的 3 个
    )

    # 构建 RAG 提示词
    prompt = ChatPromptTemplate.from_template("""
你是一个知识问答助手。请根据以下参考资料回答用户的问题。
如果参考资料中没有相关信息，请如实回答"我不知道"，不要编造答案。

参考资料：
{context}

用户问题：{question}

请用简洁准确的语言回答：
""")

    # 构建 RAG 链（LCEL 方式）
    # 流程：
    # 1. 取出 question 用于检索
    # 2. 检索结果作为 context
    # 3. 把 context 和 question 传给提示词模板
    # 4. 发给 LLM
    # 5. 解析输出

    def format_docs(docs):
        """把检索到的文档格式化成字符串"""
        return "\n\n".join(f"[{i+1}] {doc.page_content}" for i, doc in enumerate(docs))

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 测试问题
    questions = [
        "什么是 RAG？",
        "LangChain 有哪些核心组件？",
        "FAISS 的特点是什么？",
        "火星上有外星人吗？",  # 测试"不知道"的情况
    ]

    for q in questions:
        print(f"\n❓ 问题: {q}")
        answer = rag_chain.invoke(q)
        print(f"💡 回答: {answer}")


def rag_with_sources():
    """带溯源的 RAG - 显示答案来自哪些文档"""
    print("\n" + "=" * 60)
    print("2. 带溯源的 RAG（显示答案来源）")
    print("=" * 60)

    vector_store = build_sample_vector_store()
    llm = get_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 这次我们不仅返回答案，还返回来源文档
    from langchain_core.runnables import RunnableParallel

    def format_docs(docs):
        return "\n\n".join(f"[{i+1}] {doc.page_content}" for i, doc in enumerate(docs))

    prompt = ChatPromptTemplate.from_template("""
根据以下参考资料回答问题。如果资料中没有答案，说"根据现有资料无法回答"。

参考资料：
{context}

问题：{question}

答案：
""")

    # 并行执行：同时得到检索结果和生成的答案
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=lambda x: format_docs(x["context"]))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    # 测试
    question = "RAG 的工作流程是什么？"
    print(f"❓ 问题: {question}\n")

    result = rag_chain_with_source.invoke(question)

    print(f"💡 回答: {result['answer']}\n")

    print(f"📚 参考资料（{len(result['context'])} 个）:")
    for i, doc in enumerate(result['context'], 1):
        print(f"\n  [{i}] 来源: {doc.metadata.get('source', '未知')}")
        print(f"      内容片段: {doc.page_content[:100]}...")


def retrieval_qa_chain():
    """使用 create_retrieval_chain（LangChain 封装好的）"""
    print("\n" + "=" * 60)
    print("3. 使用 create_retrieval_chain（封装好的 RAG 链）")
    print("=" * 60)

    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain

    vector_store = build_sample_vector_store()
    llm = get_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 创建文档组合链（把检索到的文档"塞"进提示词）
    system_prompt = """
你是一个知识问答助手。使用以下检索到的上下文来回答问题。
如果不知道答案，就说不知道。答案要简洁，不超过三句话。

上下文：{context}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)

    # 创建 RAG 链
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # 调用
    question = "LangChain 和 FAISS 是什么关系？"
    print(f"❓ 问题: {question}\n")

    result = rag_chain.invoke({"input": question})

    print(f"💡 回答: {result['answer']}\n")

    print(f"📚 检索到 {len(result['context'])} 个文档片段:")
    for i, doc in enumerate(result['context'], 1):
        print(f"  [{i}] {doc.metadata.get('source')}: {doc.page_content[:60]}...")


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        return

    try:
        basic_rag_chain()
        rag_with_sources()
        retrieval_qa_chain()
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 把你自己的文档加入知识库，试试 RAG 问答效果")
    print("2. 调整检索的 k 值，观察对答案质量的影响")
    print("3. 修改系统提示词，让 AI 用不同风格回答（比如更幽默、更专业）")
    print("=" * 60)


if __name__ == "__main__":
    main()
