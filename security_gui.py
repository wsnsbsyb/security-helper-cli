#!/usr/bin/env python3
"""
Security Cheat GUI - 图形化安全速查表工具
"""

import json
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import webbrowser

class SecurityCheatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Security Cheat GUI v1.0")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.data = []
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """设置用户界面"""
        # 顶部标题
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🔐 Security Cheat GUI", 
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # 搜索框区域
        search_frame = tk.Frame(self.root, bg='#f0f0f0')
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(search_frame, text="搜索:", font=('Arial', 12), bg='#f0f0f0').pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var,
            font=('Arial', 12),
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, padx=10)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 搜索",
            command=self.search_commands,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # 分类按钮区域
        category_frame = tk.Frame(self.root, bg='#f0f0f0')
        category_frame.pack(fill=tk.X, padx=20, pady=10)
        
        categories = ["Web安全", "网络安全", "系统安全", "所有命令"]
        for category in categories:
            btn = tk.Button(
                category_frame,
                text=category,
                command=lambda c=category: self.filter_by_category(c),
                bg='#95a5a6',
                fg='white',
                font=('Arial', 9)
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = tk.Frame(self.root, bg='#f0f0f0')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建树形视图显示结果
        columns = ("标题", "描述", "命令", "标签")
        self.tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.column("标题", width=200)
        self.tree.column("描述", width=250)
        self.tree.column("命令", width=300)
        self.tree.column("标签", width=150)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定双击事件
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
        # 底部按钮区域
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            button_frame,
            text="🔄 刷新数据",
            command=self.load_data,
            bg='#27ae60',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="➕ 添加命令",
            command=self.add_command,
            bg='#f39c12',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="❓ 帮助",
            command=self.show_help,
            bg='#9b59b6',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🚪 退出",
            command=self.root.quit,
            bg='#e74c3c',
            fg='white'
        ).pack(side=tk.RIGHT, padx=5)
    
    def load_data(self):
        """加载数据"""
        try:
            self.data = self.load_cheatsheets()
            self.display_results(self.data)
            messagebox.showinfo("成功", f"已加载 {len(self.data)} 条命令")
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败: {str(e)}")
    
    def load_cheatsheets(self):
        """安全加载速查表数据"""
        all_data = []
        data_dir = Path(__file__).parent / "cheatsheets"
        
        if not data_dir.exists():
            data_dir.mkdir(parents=True, exist_ok=True)
            # 创建示例数据
            self.init_sample_data()
            return self.load_cheatsheets()
        
        json_files = list(data_dir.glob("*.json"))
        
        for file in json_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_data.extend(data)
            except Exception as e:
                print(f"加载文件 {file} 时出错: {e}")
                continue
        
        return all_data
    
    def init_sample_data(self):
        """初始化示例数据"""
        data_dir = Path(__file__).parent / "cheatsheets"
        
        sample_data = [
            {
                "title": "SQL注入检测",
                "description": "使用sqlmap检测SQL注入漏洞",
                "tags": ["web", "sql", "安全"],
                "command": "sqlmap -u 'http://test.com?id=1' --batch",
                "category": "Web安全"
            },
            {
                "title": "Nmap端口扫描",
                "description": "基本端口和服务版本检测",
                "tags": ["网络", "扫描", "nmap"],
                "command": "nmap -sV -sC target.com",
                "category": "网络安全"
            },
            {
                "title": "Linux系统信息",
                "description": "查看系统基本信息",
                "tags": ["系统", "linux", "信息"],
                "command": "uname -a && cat /etc/os-release",
                "category": "系统安全"
            }
        ]
        
        with open(data_dir / "data.json", 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    def display_results(self, results):
        """显示结果到树形视图"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加新数据
        for item in results:
            self.tree.insert('', tk.END, values=(
                item.get('title', '无标题'),
                item.get('description', '无描述'),
                item.get('command', '无命令'),
                ', '.join(item.get('tags', []))
            ))
    
    def on_search(self, event=None):
        """实时搜索"""
        keyword = self.search_var.get().lower()
        if not keyword:
            self.display_results(self.data)
            return
        
        results = [
            item for item in self.data 
            if any(keyword in str(value).lower() for value in item.values())
        ]
        self.display_results(results)
    
    def search_commands(self):
        """搜索命令"""
        self.on_search()
    
    def filter_by_category(self, category):
        """按分类过滤"""
        if category == "所有命令":
            self.display_results(self.data)
        else:
            results = [item for item in self.data if item.get('category') == category]
            self.display_results(results)
    
    def on_item_double_click(self, event):
        """双击项目显示详细信息"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        # 创建详情窗口
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"详情 - {values[0]}")
        detail_window.geometry("600x400")
        
        # 创建文本框显示详细信息
        text_area = scrolledtext.ScrolledText(detail_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info_text = f"""标题: {values[0]}
描述: {values[1]}
命令: {values[2]}
标签: {values[3]}

使用方法:
1. 复制上方命令到终端执行
2. 根据实际情况修改参数
3. 注意遵守法律法规"""
        
        text_area.insert(tk.END, info_text)
        text_area.config(state=tk.DISABLED)
    
    def add_command(self):
        """添加新命令"""
        add_window = tk.Toplevel(self.root)
        add_window.title("添加新命令")
        add_window.geometry("500x400")
        
        # 创建表单
        tk.Label(add_window, text="标题:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        title_entry = tk.Entry(add_window, width=50)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="描述:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        desc_entry = tk.Entry(add_window, width=50)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="命令:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        cmd_entry = tk.Entry(add_window, width=50)
        cmd_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="标签(逗号分隔):").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tags_entry = tk.Entry(add_window, width=50)
        tags_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(add_window, text="分类:").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        category_var = tk.StringVar(value="Web安全")
        category_combo = ttk.Combobox(add_window, textvariable=category_var, 
                                    values=["Web安全", "网络安全", "系统安全", "其他"])
        category_combo.grid(row=4, column=1, padx=10, pady=5)
        
        def save_command():
            """保存命令"""
            new_command = {
                "title": title_entry.get(),
                "description": desc_entry.get(),
                "command": cmd_entry.get(),
                "tags": [tag.strip() for tag in tags_entry.get().split(',')],
                "category": category_var.get()
            }
            
            # 保存到文件
            data_dir = Path(__file__).parent / "cheatsheets"
            data_file = data_dir / "data.json"
            
            existing_data = []
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            existing_data.append(new_command)
            
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("成功", "命令已保存！")
            add_window.destroy()
            self.load_data()  # 刷新数据
        
        tk.Button(add_window, text="保存", command=save_command, bg='green', fg='white').grid(row=5, column=1, pady=10)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """Security Cheat GUI 使用说明

功能:
- 🔍 搜索: 在搜索框中输入关键词实时搜索
- 📁 分类: 点击分类按钮按类别筛选
- 📋 查看: 双击项目查看详细信息
- ➕ 添加: 点击添加命令按钮添加新命令
- 🔄 刷新: 点击刷新按钮重新加载数据

数据存储:
所有命令保存在 cheatsheets/data.json 文件中"""
        
        messagebox.showinfo("帮助", help_text)

def main():
    """主函数"""
    root = tk.Tk()
    app = SecurityCheatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()