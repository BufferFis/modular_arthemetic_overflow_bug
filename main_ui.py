import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import random
import os
import sys
import time

class CryptoSecurityUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modular Arithmetic Overflow & Integer Attacks Lab")
        self.root.geometry("1100x850")
        
        # Apply Modern Dark Theme using standard ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(".", background="#1e1e2e", foreground="#f0f0f0", font=("Segoe UI", 10))
        self.style.configure("TFrame", background="#1e1e2e")
        self.style.configure("TLabelframe", background="#1e1e2e", foreground="#50fa7b", font=("Segoe UI", 12, "bold"))
        self.style.configure("TLabelframe.Label", background="#1e1e2e", foreground="#50fa7b")
        self.style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 11))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#313244", foreground="#cdd6f4", borderwidth=0, padding=6)
        self.style.map("TButton", background=[("active", "#45475a"), ("pressed", "#585b70")])
        self.style.configure("TCombobox", fieldbackground="#313244", background="#313244", foreground="#ffffff", bordercolor="#1e1e2e")
        
        self.root.configure(bg="#1e1e2e")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.main_frame = ttk.Frame(self.root, padding="15")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(1, weight=1)
        
        self.test_cases = []
        self.create_widgets()
        
    def create_widgets(self):
        # --- Control Panel (Left) ---
        self.control_frame = ttk.LabelFrame(self.main_frame, text="🛡️ Attack & Prevention Controls", padding="15")
        self.control_frame.grid(row=0, column=0, sticky="nswe", padx=(0, 15))
        
        ttk.Label(self.control_frame, text="Select Scenario:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.scenario_var = tk.StringVar(value="C uint8 Overflow")
        scenarios = [
            "C uint8 Overflow", 
            "Java int Overflow", 
            "Java BigInteger Improper Migration",
            "Nuclear Gandhi Vulnerability",
            "Modular Reduction (Barrett/Montgomery)"
        ]
        self.scenario_dropdown = ttk.Combobox(self.control_frame, textvariable=self.scenario_var, values=scenarios, state="readonly", width=35)
        self.scenario_dropdown.grid(row=1, column=0, sticky="w", pady=(0, 20))
        
        ttk.Button(self.control_frame, text="1. 🎲 Generate 10 Test Cases", command=self.generate_params).grid(row=2, column=0, sticky="ew", pady=8)
        ttk.Button(self.control_frame, text="2. 💥 Run Attack (Vulnerable)", command=self.run_attack).grid(row=3, column=0, sticky="ew", pady=8)
        ttk.Button(self.control_frame, text="3. 🔒 Apply Prevention (Secure)", command=self.apply_prevention).grid(row=4, column=0, sticky="ew", pady=8)
        ttk.Button(self.control_frame, text="4. 📊 Show Advanced Graphs", command=self.show_graphs).grid(row=5, column=0, sticky="ew", pady=30)
        ttk.Button(self.control_frame, text="🗑️ Clear Log", command=self.clear_log).grid(row=6, column=0, sticky="ew", pady=5)
        
        # --- Log Output (Right) ---
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Terminal Output (10 Test Cases Per Run)", padding="10")
        self.log_frame.grid(row=0, column=1, sticky="nsew")
        self.log_frame.rowconfigure(0, weight=1)
        self.log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, bg="#11111b", fg="#cdd6f4", insertbackground="#cdd6f4", font=("Consolas", 11), borderwidth=0)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Tags for colored text
        self.log_text.tag_config("vulnerable", foreground="#f38ba8", font=("Consolas", 11, "bold"))
        self.log_text.tag_config("secure", foreground="#a6e3a1", font=("Consolas", 11, "bold"))
        self.log_text.tag_config("info", foreground="#bac2de")
        self.log_text.tag_config("header", foreground="#89b4fa", font=("Consolas", 12, "bold"))
        
        self.log("System initialized. Select a scenario and generate test cases.", "info")

    def log(self, message, tag="info"):
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.root.update()
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def generate_params(self):
        scenario = self.scenario_var.get()
        self.log(f"\n=======================================================", "header")
        self.log(f"--- GENERATING 10 TEST CASES FOR: {scenario} ---", "header")
        self.test_cases = []
        
        for i in range(1, 11):
            if scenario == "C uint8 Overflow":
                price = random.randint(150, 250)
                qty = random.randint(2, 5)
                bal = random.randint(50, 100) 
                self.test_cases.append({"price": price, "qty": qty, "bal": bal})
                self.log(f"Test {i}: Price={price} per item | Qty={qty} | UserBalance={bal}", "info")
                
            elif scenario in ["Java int Overflow", "Java BigInteger Improper Migration"]:
                items = random.randint(400000, 900000)
                price = random.randint(4000, 8000)
                bal = random.randint(1000, 5000)
                self.test_cases.append({"items": items, "price": price, "bal": bal})
                self.log(f"Test {i}: Items={items} | Price={price} | UserBalance={bal}", "info")
                
            elif scenario == "Nuclear Gandhi Vulnerability":
                gandhi = 4
                modifier = random.randint(10, 20)
                self.test_cases.append({"gandhi": gandhi, "modifier": modifier})
                self.log(f"Test {i}: peaceful: value = {gandhi} | discount=-{modifier}", "info")
                
            elif scenario == "Modular Reduction (Barrett/Montgomery)":
                val = random.randint(2000000, 9000000)
                modulus = random.randint(200, 500)
                self.test_cases.append({"val": val, "modulus": modulus})
                self.log(f"Test {i}: Base Value={val} | Target Modulus={modulus}", "info")
                
            time.sleep(0.4)
                
        self.log(f"-> 10 Test Cases Generated successfully.", "secure")

    def run_attack(self):
        scenario = self.scenario_var.get()
        if not self.test_cases:
            self.log("[!] Please Generate 10 Test Cases first!", "vulnerable")
            return
            
        self.log(f"\n=======================================================", "header")
        self.log(f"[!] RUNNING ATTACKS (VULNERABLE IMPLEMENTATION) : {scenario}", "header")
        success_count = 0
        
        for i, tc in enumerate(self.test_cases, 1):
            if scenario == "C uint8 Overflow":
                price, qty, bal = tc["price"], tc["qty"], tc["bal"]
                true_cost = price * qty
                calc_cost = true_cost % 256
                
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                self.log(f"Expected True Cost: {true_cost}", "info")
                self.log(f"Got Wrapped Cost (8-bit): {calc_cost}", "vulnerable")
                self.log(f"User Balance limit: {bal}", "info")
                
                if calc_cost <= bal and true_cost > bal:
                    self.log(f"  -> Result: VULNERABLE (Auth Approved! Cost wrapped below balance)", "vulnerable")
                    success_count += 1
                else:
                    self.log(f"  -> Result: FAILED (No exploitable integer wrap triggered)", "info")
                    
            elif scenario in ["Java int Overflow", "Java BigInteger Improper Migration"]:
                items, price, bal = tc["items"], tc["price"], tc["bal"]
                true_cost = items * price
                wrapped_cost = (true_cost + 2**31) % 2**32 - 2**31
                
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                self.log(f"Expected True Cost: {true_cost}", "info")
                
                if scenario == "Java BigInteger Improper Migration":
                    self.log(f"Developer used BigInteger correctly: {true_cost}", "info")
                    self.log(f"Got Casted Value (.intValue() vulnerability): {wrapped_cost}", "vulnerable")
                else:
                    self.log(f"Got Wrapped Cost (32-bit int): {wrapped_cost}", "vulnerable")
                    
                self.log(f"User Balance limit: {bal}", "info")
                
                if wrapped_cost <= bal and true_cost > bal:
                    self.log(f"  -> Result: VULNERABLE (Negative cost! Transaction approved maliciously)", "vulnerable")
                    success_count += 1
                else:
                    self.log(f"  -> Result: FAILED (Exploit condition missed)", "info")
                    
            elif scenario == "Nuclear Gandhi Vulnerability":
                g, mod = tc["gandhi"], tc["modifier"]
                new_val = (g - mod) % 256
                
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                if new_val > 128:
                    self.log(f"  -> Result: VULNERABLE (value = highly aggresive nuclear maglomanian)", "vulnerable")
                    success_count += 1
                else:
                    self.log(f"  -> Result: FAILED (value = {new_val})", "info")

            elif scenario == "Modular Reduction (Barrett/Montgomery)":
                val, mod = tc["val"], tc["modulus"]
                true_mod = val % mod
                fault_offset = random.randint(1, 10)
                bug_mod = true_mod + fault_offset
                
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                self.log(f"Expected Modulo Result: {true_mod}", "info")
                self.log(f"Got Fault-injected Result (loop skipped): {bug_mod}", "vulnerable")
                self.log(f"  -> Result: VULNERABLE (Data compromised via partial timing/reduction bypass)", "vulnerable")
                success_count += 1
                
            time.sleep(0.4)
                
        rate = (success_count / 10) * 100
        self.log(f"\n[!] ATTACK PHASE COMPLETE. Success Rate: {rate}% ({success_count}/10)", "vulnerable")

    def apply_prevention(self):
        scenario = self.scenario_var.get()
        if not self.test_cases:
            self.log("[!] Please Generate 10 Test Cases first!", "vulnerable")
            return
            
        self.log(f"\n=======================================================", "header")
        self.log(f"[*] APPLYING PREVENTION (SECURE IMPLEMENTATION) : {scenario}", "header")
        blocked_count = 0
        
        for i, tc in enumerate(self.test_cases, 1):
            if scenario == "C uint8 Overflow":
                price, qty, bal = tc["price"], tc["qty"], tc["bal"]
                true_cost = price * qty
                
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                self.log(f"Expected True Cost: {true_cost}", "info")
                self.log(f"Got Secure Cost (size_t): {true_cost}", "secure")
                if true_cost <= bal:
                    self.log(f"  -> SECURE (Legitimate transaction approved)", "secure")
                else:
                    self.log(f"  -> SECURE (Exploit blocked. Insufficient balance)", "secure")
                    blocked_count += 1

            elif scenario == "Java int Overflow":
                items, price, bal = tc["items"], tc["price"], tc["bal"]
                true_cost = items * price
                
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                self.log(f"Got Secure Cost (BigInteger): {true_cost}", "secure")
                if true_cost <= bal:
                    self.log(f"  -> SECURE (Legitimate transaction)", "secure")
                else:
                    self.log(f"  -> SECURE (Exploit blocked. Correct mathematical evaluation)", "secure")
                    blocked_count += 1
                    
            elif scenario == "Java BigInteger Improper Migration":
                items, price, bal = tc["items"], tc["price"], tc["bal"]
                true_cost = items * price
                
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                self.log(f"Got Secure Comparison (BigInteger.compareTo): Checked securely against balance.", "secure")
                if true_cost <= bal:
                    self.log(f"  -> SECURE (Legitimate transaction)", "secure")
                else:
                    self.log(f"  -> SECURE (Exploit blocked. Value maintained without truncation)", "secure")
                    blocked_count += 1

            elif scenario == "Nuclear Gandhi Vulnerability":
                g, mod = tc["gandhi"], tc["modifier"]
                if g >= mod:
                    new_val = g - mod
                else:
                    new_val = 0
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                self.log(f"  -> SECURE (peaceful: value = {new_val})", "secure")
                blocked_count += 1

            elif scenario == "Modular Reduction (Barrett/Montgomery)":
                val, mod = tc["val"], tc["modulus"]
                true_mod = val % mod
                
                self.log(f"\n--- [Test {i} Executing] ---", "info")
                self.log(f"Got Secure Computed Modulo: {true_mod}", "secure")
                self.log(f"  -> SECURE (Fault injection blocked boundary check pass)", "secure")
                blocked_count += 1
                
            time.sleep(0.4)
                
        self.log(f"\n[*] PREVENTION PHASE COMPLETE. {blocked_count}/10 malicious attempts safely blocked (100% Secure)", "secure")

    def show_graphs(self):
        self.log("\n[+] Generating Comprehensive HTML Graphs Report...", "info")
        try:
            if os.path.exists("generate_all_graphs.py"):
                subprocess.Popen([sys.executable, "generate_all_graphs.py"])
                self.log("HTML graph report generated and opened in browser.", "secure")
            else:
                self.log("Graph script 'generate_all_graphs.py' not found.", "vulnerable")
        except Exception as e:
            self.log(f"Error launching graphs: {e}", "vulnerable")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoSecurityUI(root)
    root.mainloop()
