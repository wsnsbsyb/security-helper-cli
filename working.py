#!/usr/bin/env python3
import sys
import json
import os

print("=== Security Cheat CLI 工作版本 ===")
print(f"参数: {sys.argv}")

# 简单数据
data = [
    {"title": "SQL Injection Test", "command": "sqlmap -u test.com"},
    {"title": "Nmap Scan", "command": "nmap -sV target.com"}
]

if len(sys.argv) > 1:
    cmd = sys.argv[1]
    
    if cmd == "list":
        print(f"📚 找到 {len(data)} 条记录:")
        for i, item in enumerate(data, 1):
            print(f"{i}. {item['title']}")
    
    elif cmd == "search" and len(sys.argv) > 2:
        keyword = sys.argv[2]
        found = [item for item in data if keyword.lower() in item['title'].lower()]
        
        if found:
            print(f"🔍 找到 {len(found)} 条结果:")
            for item in found:
                print(f"  • {item['title']}: {item['command']}")
        else:
            print(f"❌ 无结果: {keyword}")
    
    elif cmd == "init":
        print("✅ 数据库已初始化")
        with open("test_data.json", "w") as f:
            json.dump(data, f, indent=2)
    
    elif cmd in ["help", "-h", "--help"]:
        print("命令: list, search <词>, init, help")
    
    else:
        print(f"未知命令: {cmd}")

else:
    print("使用: python working.py [list|search|init|help]")

print("-" * 40)
input("按回车退出...")