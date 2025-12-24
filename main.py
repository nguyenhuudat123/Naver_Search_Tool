"""
Project: Naver SEO Automation Helper
Author: Nguyen Huu Dat
Description: A semi-automatic tool to check keyword rankings on Naver.
Features: Keyword Generation, Auto-searching, Manual Rank Entry, Multi-tab management.
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- UI CONFIGURATION ---
BG_MAIN = "#1E1E2E"
BG_TEXT = "#313244"
TEXT_MAIN = "#CDD6F4"
TEXT_SUB = "#A6ADC8"
NAVER_GREEN = "#03c75a"

class NaverSEOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Naver SEO Helper - Premium Edition")
        self.root.geometry("1200x900")
        self.root.configure(bg=BG_MAIN)
        
        self.driver = None
        self.is_searching = False
        self.stop_requested = False
        self.is_paused = False 
        
        self.init_ui()

    def init_ui(self):
        """Initialize User Interface components"""
        # 1. KEYWORD GENERATOR SECTION
        gen_frame = tk.LabelFrame(self.root, text=" 1. KEYWORD GENERATOR ", bg=BG_MAIN, fg=NAVER_GREEN, font=("Segoe UI", 11, "bold"))
        gen_frame.place(relx=0.01, rely=0.01, relwidth=0.48, relheight=0.35)
        
        grid = tk.Frame(gen_frame, bg=BG_MAIN)
        grid.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.txt_address = self.create_input_box(grid, "🏠 Address (Main)", 0, 0)
        self.txt_food = self.create_input_box(grid, "🥘 Food/Service", 0, 1)
        self.txt_feature = self.create_input_box(grid, "✨ Feature 1", 1, 0)
        self.txt_sub_addr = self.create_input_box(grid, "🏘 Sub-Address", 1, 1)
        self.txt_feature2 = self.create_input_box(grid, "🔸 Feature 2", 2, 0) 
        
        tk.Button(gen_frame, text="GENERATE LIST ↓", bg=NAVER_GREEN, fg="white", 
                  font=("Segoe UI", 9, "bold"), command=self.generate_keywords).pack(pady=5)

        # 2. KEYWORDS QUEUE
        list_frame = tk.LabelFrame(self.root, text=" 2. SEARCH QUEUE ", bg=BG_MAIN, fg="#3b82f6", font=("Segoe UI", 11, "bold"))
        list_frame.place(relx=0.01, rely=0.37, relwidth=0.48, relheight=0.61)
        
        self.keywords_text = scrolledtext.ScrolledText(list_frame, bg=BG_TEXT, fg=TEXT_MAIN, font=("Consolas", 10))
        self.keywords_text.pack(fill="both", expand=True, padx=10, pady=5)

        # 3. CONTROL & OUTPUT
        right_frame = tk.Frame(self.root, bg=BG_MAIN)
        right_frame.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.97)

        # Control Row
        ctrl_row = tk.Frame(right_frame, bg=BG_MAIN)
        ctrl_row.pack(fill="x", pady=5)
        
        tk.Label(ctrl_row, text="Target Brand:", bg=BG_MAIN, fg=TEXT_MAIN).pack(side="left")
        self.target_entry = tk.Entry(ctrl_row, bg=BG_TEXT, fg=NAVER_GREEN, font=("Segoe UI", 11, "bold"), width=12)
        self.target_entry.pack(side="left", padx=5)
        
        # Action Buttons
        btns = [("START", "#3b82f6", self.start_search), ("PAUSE", "#f59e0b", self.toggle_pause), 
                ("RESUME", "#10b981", self.toggle_resume), ("STOP", "#ef4444", self.stop_search)]
        for txt, clr, cmd in btns:
            tk.Button(ctrl_row, text=txt, bg=clr, fg="white", font=("Segoe UI", 8, "bold"), width=7, command=cmd).pack(side="left", padx=2)

        # Final String Output
        tk.Label(right_frame, text="FINAL RESULTS (Add Rank Manually):", bg=BG_MAIN, fg=NAVER_GREEN, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.final_output = scrolledtext.ScrolledText(right_frame, height=12, bg="#1e293b", fg="#4ade80", font=("Consolas", 11))
        self.final_output.pack(fill="x", pady=5)

        # Log Area
        tk.Label(right_frame, text="System Log:", bg=BG_MAIN, fg=TEXT_SUB).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(right_frame, bg="#0f172a", fg="#94a3b8", font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True, pady=5)

    def create_input_box(self, parent, label, r, c):
        f = tk.Frame(parent, bg=BG_MAIN); f.grid(row=r, column=c, padx=5, pady=2, sticky="nsew")
        tk.Label(f, text=label, bg=BG_MAIN, fg=TEXT_SUB, font=("Segoe UI", 9)).pack(anchor="w")
        txt = tk.Text(f, height=2, bg=BG_TEXT, fg=TEXT_MAIN, font=("Segoe UI", 10)); txt.pack(fill="x")
        return txt

    def log(self, msg):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_area.see(tk.END); self.log_area.config(state="disabled")

    def generate_keywords(self):
        """Cross-combine inputs to create keyword list"""
        try:
            get_input = lambda x: [l.strip() for l in x.get("1.0", tk.END).split('\n') if l.strip()]
            addrs, foods = get_input(self.txt_address), get_input(self.txt_food)
            feats, subs, feats2 = get_input(self.txt_feature), get_input(self.txt_sub_addr), get_input(self.txt_feature2)
            
            if not addrs or not foods: return
            
            res = []
            for a in addrs:
                for f in foods:
                    base = f"{a} {f}"
                    res.append(base)
                    for x in feats + subs + feats2: res.append(f"{base} {x}")
            
            res = list(dict.fromkeys(res)) # Remove duplicates
            self.keywords_text.delete("1.0", tk.END)
            self.keywords_text.insert(tk.END, "\n".join(res))
            self.log(f"Generated {len(res)} keywords.")
        except Exception as e:
            self.log(f"Gen Error: {e}")

    # --- CONTROL METHODS ---
    def toggle_pause(self): self.is_paused = True; self.log("PAUSED.")
    def toggle_resume(self): self.is_paused = False; self.log("RESUMED.")
    def stop_search(self): self.stop_requested = True; self.is_paused = False; self.log("Stopping...")

    def start_search(self):
        if self.is_searching: return
        threading.Thread(target=self.run_automation, daemon=True).start()

    def run_automation(self):
        """Main automation logic using Selenium"""
        kws = [l.strip() for l in self.keywords_text.get("1.0", tk.END).split('\n') if l.strip()]
        target = self.target_entry.get().strip()
        if not kws or not target: return
        
        self.is_searching, self.stop_requested = True, False
        date_str = datetime.now().strftime("%y%m%d")
        
        opts = Options()
        opts.add_argument("--start-maximized")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])

        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
            
            for i, kw in enumerate(kws):
                if self.stop_requested: break
                while self.is_paused and not self.stop_requested: time.sleep(1)
                
                self.log(f"Checking: {kw}")
                
                # Tab Management
                if i == 0: self.driver.get(f"https://search.naver.com/search.naver?query={kw}")
                else:
                    self.driver.execute_script(f"window.open('https://search.naver.com/search.naver?query={kw}', '_blank');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                
                time.sleep(2.5) # Allow page to load

                # Search for target text
                targets = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{target}')]")
                
                if targets:
                    # Highlight target
                    el = targets[0]
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                    self.driver.execute_script("arguments[0].style.border = '5px solid red';", el)
                    
                    # Extract Card Name
                    card_title = "Unknown"
                    try:
                        parent = el.find_element(By.XPATH, "./ancestor::*[contains(@class, 'bx') or contains(@class, 'card') or contains(@class, 'total')][1]")
                        title_el = parent.find_element(By.XPATH, ".//*[contains(@class, 'title') or contains(@class, 'tit') or contains(@class, 'api_txt_lines')]")
                        card_title = title_el.text.split('\n')[0].replace(" ", "")[:15]
                    except: pass
                    
                    # Push to Result Area
                    self.final_output.insert(tk.END, f"{kw}_{card_title}_위 ({date_str})\n")
                    self.log(f"-> Found: {kw}")
                else:
                    # Close tab if not found to save memory
                    self.log(f"-> Not found: {kw}. Closing tab.")
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                    else: self.driver.get("about:blank")

            self.log("Job Finished!")
        except Exception as e: self.log(f"Critical Error: {e}")
        finally: self.is_searching = False

if __name__ == "__main__":
    root = tk.Tk()
    app = NaverSEOApp(root)
    root.mainloop()