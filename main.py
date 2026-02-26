import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time
import os
import csv
from datetime import datetime
from itertools import product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Cấu hình giao diện (Từ constants.py) ---
BG_MAIN = "#1E1E2E"
BG_TEXT = "#313244"
TEXT_MAIN = "#CDD6F4"
TEXT_SUB = "#A6ADC8"
NAVER_GREEN = "#03c75a"

class NaverSEOProSingle:
    def __init__(self, root):
        self.root = root
        self.root.title("Naver SEO Pro - Single Stream")
        self.root.geometry("1100x750")
        self.root.configure(bg=BG_MAIN)
        
        self.driver = None
        self.is_searching = False
        self.stop_requested = False
        self.is_paused = False 
        self.current_csv_path = None
        
        self.create_widgets()

    def create_widgets(self):
        left_panel = tk.Frame(self.root, bg=BG_MAIN)
        left_panel.place(relx=0.01, rely=0.01, relwidth=0.48, relheight=0.97)

        gen_frame = tk.LabelFrame(left_panel, text=" 1. KEYWORD ENGINE (Brute-force) ", bg=BG_MAIN, fg=NAVER_GREEN, font=("Segoe UI", 11, "bold"))
        gen_frame.pack(fill="x", pady=5)
        
        grid_container = tk.Frame(gen_frame, bg=BG_MAIN)
        grid_container.pack(fill="both", padx=5, pady=5)

        self.inputs = {
            "addr": self.create_grid_input(grid_container, "(1) Địa chỉ (Bắt buộc)__ ADD", 0, 0),
            "feat1": self.create_grid_input(grid_container, "(2) Đặc điểm 1 __ F1", 0, 1),
            "food": self.create_grid_input(grid_container, "(3) Món ăn __ Food" , 1, 0),
            "feat2": self.create_grid_input(grid_container, "(4) Đặc điểm 2 __ F2", 1, 1),
            "sub_addr": self.create_grid_input(grid_container, "(5) Địa chỉ nhỏ __ SUB ADD", 2, 0),
            "feat3": self.create_grid_input(grid_container, "(6) Đặc điểm 3 __ F3", 2, 1),
        }
        
        tk.Button(gen_frame, text="GENERATE KEYWORDS ↓", bg=NAVER_GREEN, fg="white", 
                  font=("Segoe UI", 10, "bold"), command=self.generate_keywords).pack(pady=10)

        self.kw_list_area = scrolledtext.ScrolledText(left_panel, bg=BG_TEXT, fg=TEXT_MAIN, font=("Consolas", 10))
        self.kw_list_area.pack(fill="both", expand=True, pady=5)

        right_panel = tk.Frame(self.root, bg=BG_MAIN)
        right_panel.place(relx=0.51, rely=0.01, relwidth=0.48, relheight=0.97)

        meta_frame = tk.LabelFrame(right_panel, text=" 2. CAMPAIGN METADATA ", bg=BG_MAIN, fg="#3b82f6", font=("Segoe UI", 11, "bold"))
        meta_frame.pack(fill="x", pady=5)
        self.meta_link = self.create_meta_field(meta_frame, "🔗 Target Link:")
        self.meta_header = self.create_meta_field(meta_frame, "📋 Header Name:")
        self.meta_option = self.create_meta_field(meta_frame, "⚙️ Option/Note:")
        
        ctrl_frame = tk.Frame(right_panel, bg=BG_MAIN)
        ctrl_frame.pack(fill="x", pady=5)
        
        tk.Label(ctrl_frame, text="Target Brand:", bg=BG_MAIN, fg=TEXT_MAIN).pack(side="left")
        self.target_entry = tk.Entry(ctrl_frame, bg=BG_TEXT, fg=NAVER_GREEN, font=("Segoe UI", 11, "bold"), width=15)
        self.target_entry.pack(side="left", padx=5)

        btn_row = tk.Frame(right_panel, bg=BG_MAIN)
        btn_row.pack(fill="x", pady=5)
        
        for text, color, cmd in [("START", "#3b82f6", self.start_automation), ("PAUSE", "#f59e0b", self.pause_search), 
                                 ("RESUME", "#10b981", self.resume_search), ("STOP", "#ef4444", self.end_search)]:
            tk.Button(btn_row, text=text, bg=color, fg="white", width=8, font=("Segoe UI", 8, "bold"), command=cmd).pack(side="left", padx=2)

        data_btn_frame = tk.Frame(right_panel, bg=BG_MAIN)
        data_btn_frame.pack(fill="x", pady=10)

        tk.Button(data_btn_frame, text="📂 INIT CSV", bg="#4b5563", fg="white", font=("Segoe UI", 9, "bold"), width=15, command=self.init_csv).pack(side="left", padx=2)
        tk.Button(data_btn_frame, text="📊 LOG ALL DATA", bg="#0891b2", fg="white", font=("Segoe UI", 9, "bold"), width=15, command=self.log_full_system).pack(side="left", padx=2)
        
        btn_save_fix = tk.Button(data_btn_frame, text="💾 SAVE AFTER FIX", bg="#8b5cf6", fg="white", font=("Segoe UI", 9, "bold"), command=self.save_manually)
        btn_save_fix.pack(side="left", padx=2, expand=True, fill="x")

        tk.Label(right_panel, text="FINAL RESULT (EDITABLE):", bg=BG_MAIN, fg=NAVER_GREEN, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.final_output = scrolledtext.ScrolledText(right_panel, height=24, bg="#1e293b", fg="#4ade80", font=("Consolas", 11))
        self.final_output.pack(fill="x", pady=5)

        tk.Label(right_panel, text="System Log:", bg=BG_MAIN, fg=TEXT_SUB).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(right_panel, height=5, bg="#0f172a", fg="#94a3b8", font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True, pady=5)

    def generate_keywords(self):
        addr_list = [l.strip() for l in self.inputs["addr"].get("1.0", tk.END).split('\n') if l.strip()]
        food_list = [l.strip() for l in self.inputs["food"].get("1.0", tk.END).split('\n') if l.strip()]
        feat1_list = [l.strip() for l in self.inputs["feat1"].get("1.0", tk.END).split('\n') if l.strip()]
        feat2_list = [l.strip() for l in self.inputs["feat2"].get("1.0", tk.END).split('\n') if l.strip()]
        feat3_list = [l.strip() for l in self.inputs["feat3"].get("1.0", tk.END).split('\n') if l.strip()]
        sub_addr_list = [l.strip() for l in self.inputs["sub_addr"].get("1.0", tk.END).split('\n') if l.strip()]

        if not addr_list:
            messagebox.showwarning("Thiếu dữ liệu", "Địa chỉ phải có dữ liệu!")
            return

        def prepare_optional_list(lst):
            if not lst: return ['']
            res = list(lst)
            if '' not in res: res.append('')
            return res

        food, f1, f2, f3, sub = map(prepare_optional_list, [food_list, feat1_list, feat2_list, feat3_list, sub_addr_list])
        all_variations = list(product(addr_list, f1, food, f2, sub, f3))

        final_keywords = []
        for combo in all_variations:
            clean_kw = " ".join(" ".join(filter(None, combo)).split())
            if clean_kw and clean_kw not in final_keywords:
                final_keywords.append(clean_kw)

        self.kw_list_area.delete("1.0", tk.END)
        self.kw_list_area.insert(tk.END, "\n".join(final_keywords))
        self.log(f"Generated {len(final_keywords)} keywords.")

    def run_engine(self):
        kws = [l.strip() for l in self.kw_list_area.get("1.0", tk.END).split('\n') if l.strip()]
        target = self.target_entry.get().strip()
        if not kws or not target: 
            messagebox.showwarning("Cảnh báo", "Vui lòng tạo từ khóa và nhập Target Brand trước khi chạy.")
            self.is_searching = False
            return
        
        self.is_searching = True
        date_str = datetime.now().strftime("%y%m%d")
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.log("Browser started.")
            
            for i, kw in enumerate(kws):
                if self.stop_requested: break
                while self.is_paused: time.sleep(1)
                
                self.log(f"[{i+1}/{len(kws)}] Checking: {kw}")
                
                url = f"https://search.naver.com/search.naver?query={kw}"
                if i == 0: self.driver.get(url)
                else:
                    self.driver.execute_script(f"window.open('{url}', '_blank');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                
                time.sleep(2.5)
                
                target_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{target}')]")
                
                if target_elements:
                    el = target_elements[0]
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                    self.driver.execute_script("arguments[0].style.border = '5px solid red';", el)
                    
                    card_title = "Unknown"
                    try:
                        parent = el.find_element(By.XPATH, "./ancestor::*[contains(@class, 'bx') or contains(@class, 'card') or contains(@class, 'total')][1]")
                        title_el = parent.find_element(By.XPATH, ".//*[contains(@class, 'title') or contains(@class, 'tit') or contains(@class, 'api_txt_lines')]")
                        card_title = title_el.text.split('\n')[0].replace(" ", "")[:15]
                    except: pass
                    
                    res_line = f"{kw}_{card_title}_위 ({date_str})"
                    self.final_output.insert(tk.END, res_line + "\n")
                    self.log(f"-> Found: {kw} in {card_title}")
                else:
                    self.log(f"-> Not found: {kw}")
                    
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
            
            self.log("Job Finished!")
                
        except Exception as e: 
            self.log(f"Error: {e}")
        finally: 
            self.is_searching = False

    def init_csv(self):
        folder = os.path.join("SearchLog", f"Search_{datetime.now().strftime('%y%m%d')}")
        if not os.path.exists(folder): os.makedirs(folder)
        self.current_csv_path = os.path.join(folder, f"Result_{datetime.now().strftime('%H%M%S')}.csv")
        with open(self.current_csv_path, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Log Type", "Content", "Target", "Metadata"])
        self.log(f"CSV Ready: {self.current_csv_path}")
        messagebox.showinfo("CSV", "Đã khởi tạo file CSV!")

    def log_full_system(self):
        if not self.current_csv_path: self.init_csv()
        inputs_data = {k: v.get("1.0", tk.END).strip() for k, v in self.inputs.items()}
        meta_info = f"Link: {self.meta_link.get()} | Header: {self.meta_header.get()} | Opt: {self.meta_option.get()}"
        full_log = self.log_area.get("1.0", tk.END).strip()
        with open(self.current_csv_path, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime('%H:%M:%S'), "SNAPSHOT", str(inputs_data), self.target_entry.get(), meta_info])
            writer.writerow([datetime.now().strftime('%H:%M:%S'), "LOG", full_log, "", ""])
        self.log("Full system state logged.")

    def save_manually(self):
        if not self.current_csv_path: self.init_csv()
        content = self.final_output.get("1.0", tk.END).strip()
        if not content: return
        with open(self.current_csv_path, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime('%H:%M:%S'), "MANUAL_EDIT", content, self.target_entry.get(), "Final Report"])
        self.log("Manual fix saved to CSV.")
        messagebox.showinfo("Success", "Đã lưu kết quả!")

    def create_grid_input(self, parent, label, r, c):
        f = tk.Frame(parent, bg=BG_MAIN); f.grid(row=r, column=c, padx=5, pady=2, sticky="nsew")
        tk.Label(f, text=label, bg=BG_MAIN, fg=TEXT_SUB, font=("Segoe UI", 8)).pack(anchor="w")
        txt = tk.Text(f, height=4, width=30, bg=BG_TEXT, fg=TEXT_MAIN, font=("Segoe UI", 10)); txt.pack(fill="x")
        return txt

    def create_meta_field(self, parent, label):
        f = tk.Frame(parent, bg=BG_MAIN); f.pack(fill="x", padx=5, pady=2)
        tk.Label(f, text=label, bg=BG_MAIN, fg=TEXT_SUB, width=15, anchor="w").pack(side="left")
        ent = tk.Entry(f, bg=BG_TEXT, fg=TEXT_MAIN, font=("Segoe UI", 10))
        ent.pack(side="left", fill="x", expand=True); return ent

    def log(self, msg):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_area.see(tk.END); self.log_area.config(state="disabled")

    def start_automation(self):
        if self.is_searching: return
        self.stop_requested = False; self.is_paused = False
        threading.Thread(target=self.run_engine, daemon=True).start()

    def pause_search(self): 
        self.is_paused = True
        self.log("PAUSED")
            
    def resume_search(self): 
        self.is_paused = False
        self.log("RESUMED")
            
    def end_search(self): 
        self.stop_requested = True
        self.log("Stopping...")

if __name__ == "__main__":
    root = tk.Tk()
    app = NaverSEOProSingle(root)
    root.mainloop()
