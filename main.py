from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import httpx
import traceback

app = FastAPI(title="星璃后端")

# 允许前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 星璃的系统提示词（基础版，可修改）
SYSTEM_PROMPT = """你是星璃，运行在用户本地。无论用户用什么语言提问，你必须使用流畅、自然、有温度的中文回复。

交互铁律：
1. 先共情，后建议。复述用户情绪，禁止空洞安慰，必须给出可执行的一步。
2. 默认输出「结构化方案」：目标→现状→路径→资源→风险→备选→预期→迭代。
3. 绝不说"好的""收到""根据分析"等套话，直接切入核心。
"""

class ChatRequest(BaseModel):
    model: Optional[str] = "qwen.gguf"
    messages: List[Dict[str, Any]]
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.9
    max_tokens: Optional[int] = 1500

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    # 插入或替换系统提示词
    messages = request.messages
    if not messages or messages[0].get("role") != "system":
        messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
    else:
        messages[0]["content"] = SYSTEM_PROMPT

    payload = {
        "model": request.model,
        "messages": messages,
        "stream": False,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
    }

    # 转发给 llama-server (端口 8080)
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8080/v1/chat/completions",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            traceback.print_exc()
            return {
                "error": str(e),
                "choices": [{"message": {"role": "assistant", "content": f"后端内部错误：{str(e)}"}}]
            }

@app.get("/")
async def root():
    return {"status": "ok", "message": "星璃后端正在运行"}