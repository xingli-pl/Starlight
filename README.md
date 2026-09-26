# Starlight - Fully Local Offline AI Assistant

## 📖 Overview
Starlight is a fully local, offline AI assistant designed to run on consumer hardware (RTX 5060 Laptop 8GB VRAM, 16GB RAM) with no cloud dependency.

## ✨ Key Features
- **Local LLM Inference:** Optimized `llama.cpp` with CUDA acceleration, running a quantized Qwen2.5-7B-Instruct model (~4.6GB).
- **Voice Cloning & TTS:** Integrated GPT-SoVITS to train a personalized voice model from a 1-minute audio sample.
- **Real-time Chat:** FastAPI backend with a lightweight HTML frontend.
- **GPU Resource Scheduling:** Implemented time-sliced GPU scheduling to handle VRAM contention between LLM and voice synthesis on a single 8GB GPU.

## 🛠️ Tech Stack
- **Model:** Qwen2.5-7B-Instruct (Q4_K_M)
- **Framework:** llama.cpp, FastAPI, Uvicorn
- **Audio:** GPT-SoVITS, Audacity
- **Frontend:** HTML

## 🚀 Future Plans
- Knowledge retrieval (RAG)
- Tool calling
- Experience-based memory

## 📬 Contact
- **Developer:** Yang Zeyu (杨泽宇)
- **Email:** ku2062893332@qq.com
- **GitHub:** [@xingli-pl](https://github.com/xingli-pl)
