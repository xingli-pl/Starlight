import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import time
import os

class VRAMManagerV2:
    def __init__(self, root):
        self.root = root
        self.root.title("星璃显存与内存管家 V2")
        self.root.geometry("550x520")
        self.root.configure(bg="#1e1e1e")
        
        self.log_text = None
        self.vram_label = None
        self.ram_label = None
        self.running = True

        self.setup_ui()
        self.update_monitor_loop()

    def setup_ui(self):
        # 顶部状态监控
        top_frame = tk.Frame(self.root, bg="#2d2d2d", pady=10)
        top_frame.pack(fill=tk.X)
        
        self.vram_label = tk.Label(top_frame, text="正在读取显存...", font=("微软雅黑", 12, "bold"), fg="#00ffcc", bg="#2d2d2d")
        self.vram_label.pack()
        
        self.ram_label = tk.Label(top_frame, text="正在读取内存...", font=("微软雅黑", 12, "bold"), fg="#00ffcc", bg="#2d2d2d")
        self.ram_label.pack()

        # 按钮区域 (使用网格布局，放6个按钮)
        btn_frame = tk.Frame(self.root, bg="#1e1e1e", pady=10)
        btn_frame.pack()

        tk.Button(btn_frame, text="🔪 一键释放显存 (关星璃)", font=("微软雅黑", 11, "bold"), bg="#d9534f", fg="white", command=self.kill_xingli, width=22, height=2).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="🚀 一键启动星璃", font=("微软雅黑", 11, "bold"), bg="#5cb85c", fg="white", command=self.start_xingli, width=22, height=2).grid(row=0, column=1, padx=5, pady=5)
        
        # 新增的“系统瘦身”按钮
        tk.Button(btn_frame, text="🧹 系统一键瘦身 (杀天禧/垃圾)", font=("微软雅黑", 11, "bold"), bg="#0275d8", fg="white", command=self.system_slim, width=22, height=2).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="🔄 刷新系统状态", font=("微软雅黑", 11, "bold"), bg="#f0ad4e", fg="white", command=self.manual_refresh, width=22, height=2).grid(row=1, column=1, padx=5, pady=5)

        # 日志输出
        log_frame = tk.LabelFrame(self.root, text="操作日志", bg="#1e1e1e", fg="#aaaaaa", padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, bg="#252526", fg="#cccccc", font=("Consolas", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log("星璃管家 V2 已启动。建议先点“系统一键瘦身”清理内存。")

    def log(self, msg):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.log_text.insert(tk.END, f"[{current_time}] {msg}\n")
        self.log_text.see(tk.END)

    def get_resources(self):
        # 显存
        try:
            res = subprocess.check_output("nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv,noheader,nounits", shell=True, stderr=subprocess.DEVNULL).decode().strip().split(', ')
            vram_total, vram_used, vram_free = int(res[0]), int(res[1]), int(res[2])
        except Exception:
            vram_total, vram_used, vram_free = 0, 0, 0
            
        # 内存 (通过 wmic 或 systeminfo 提取总内存和空闲内存)
        try:
            mem_output = subprocess.check_output("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value", shell=True, stderr=subprocess.DEVNULL).decode()
            mem_dict = dict(line.split('=') for line in mem_output.strip().split('\n') if '=' in line)
            ram_free = int(mem_dict.get('FreePhysicalMemory', 0)) // 1024 # MB
            ram_total = int(mem_dict.get('TotalVisibleMemorySize', 0)) // 1024 # MB
        except Exception:
            ram_total, ram_free = 0, 0
            
        return vram_total, vram_used, vram_free, ram_total, ram_free

    def update_monitor_loop(self):
        if not self.running: return
        
        vram_total, vram_used, vram_free, ram_total, ram_free = self.get_resources()
        
        if vram_total == 0:
            self.vram_label.config(text="显存: 无法读取", fg="#ff4444")
        else:
            v_percent = (vram_used / vram_total) * 100
            v_color = "#00ffcc" if v_percent < 50 else ("#ffaa00" if v_percent < 85 else "#ff4444")
            self.vram_label.config(text=f"显存: {vram_used}MB / {vram_total}MB (空闲: {vram_free}MB) [{v_percent:.0f}%]", fg=v_color)
            
        if ram_total == 0:
            self.ram_label.config(text="内存: 无法读取", fg="#ff4444")
        else:
            r_percent = ((ram_total - ram_free) / ram_total) * 100
            r_color = "#00ffcc" if r_percent < 70 else ("#ffaa00" if r_percent < 90 else "#ff4444")
            self.ram_label.config(text=f"内存: {(ram_total-ram_free)}MB / {ram_total}MB (空闲: {ram_free}MB) [{r_percent:.0f}%]", fg=r_color)
            
        self.root.after(3000, self.update_monitor_loop)

    def manual_refresh(self):
        self.log("手动刷新资源状态。")

    def run_task(self, cmd_str, log_msg):
        self.log(log_msg)
        try:
            subprocess.run(cmd_str, shell=True, capture_output=True)
            self.log(f"✅ 执行完毕: {cmd_str}")
        except Exception as e:
            self.log(f"❌ 执行失败: {e}")

    def system_slim(self):
        def task():
            self.log("========= 开始系统瘦身 =========")
            # 杀掉联想天禧AI和崩溃上报程序
            commands = [
                ("taskkill /F /IM LenovoTianxiAI.exe /T", "关闭天禧AI主进程"),
                ("taskkill /F /IM crashpad_handler.exe /T", "清理 crashpad 崩溃上报"),
                ("taskkill /F /IM 天禧AI.exe /T", "关闭天禧AI"),
                ("taskkill /F /IM 天禧个人超级智能体.exe /T", "关闭天禧智能体"),
            ]
            for cmd, msg in commands:
                self.run_task(cmd, msg)
            
            self.log("🎉 系统瘦身完毕！内存已释放。")
            self.log("=================================")
        threading.Thread(target=task, daemon=True).start()

    def kill_xingli(self):
        def task():
            self.run_task("taskkill /F /IM llama-server.exe /T", "正在关闭星璃推理引擎...")
            self.run_task("taskkill /F /IM python.exe /T", "正在关闭后端进程...")
            self.log("🎉 星璃已关闭，显存释放！现在可以去跑 GPT-SoVITS 了。")
        threading.Thread(target=task, daemon=True).start()

    def start_xingli(self):
        def task():
            self.log("正在启动推理引擎 (llama-server)...")
            cmd1 = 'start "星璃大脑" cmd /k "cd /d D:\\Xingli_Final\\llama-cpp\\build\\bin\\Release && llama-server.exe -m D:\\Xingli_Final\\models\\qwen.gguf -c 4096 -ngl 20 --port 8080"'
            os.system(cmd1)
            time.sleep(2)
            self.log("正在启动后端 (uvicorn)...")
            cmd2 = 'start cmd /k "cd /d D:\\Xingli_Final\\backend && uvicorn main:app --reload --port 8000"'
            os.system(cmd2)
            self.log("✅ 星璃启动完毕！双击 chat.html 即可开聊。")
        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = VRAMManagerV2(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (setattr(app, 'running', False), root.destroy()))
    root.mainloop()