#!/usr/bin/env python3
"""
Security Cheat CLI - 命令行安全速查表工具
"""

import json
import os
import sys
from pathlib import Path


def load_cheatsheets():
    """安全加载速查表数据"""
    all_data = []
    data_dir = Path(__file__).parent / "cheatsheets"

    if not data_dir.exists():
        print("📁 创建数据目录...")
        data_dir.mkdir(parents=True, exist_ok=True)
        return []

    json_files = list(data_dir.glob("*.json"))

    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
        except:
            continue

    return all_data


def main():
    """主函数"""
    print("🔐 Security Cheat CLI")

    if len(sys.argv) < 2:
        print("用法: python main.py [list|search|init|help]")
        return

    command = sys.argv[1]

    if command == "list":
        data = load_cheatsheets()
        if data:
            print(f"📚 找到 {len(data)} 条速查表:")
            for i, item in enumerate(data, 1):
                print(f"{i}. {item.get('title', '无标题')}")
        else:
            print("📭 没有数据，请先运行: python main.py init")

    elif command == "search" and len(sys.argv) >= 3:
        keyword = sys.argv[2]
        data = load_cheatsheets()
        results = [item for item in data if keyword.lower() in str(item).lower()]

        if results:
            print(f"🔍 找到 {len(results)} 条结果:")
            for item in results:
                print(f"\n• {item.get('title')}")
                if item.get('command'):
                    print(f"  命令: {item.get('command')}")
        else:
            print(f"❌ 没有找到 '{keyword}' 相关的内容")

    elif command == "init":
        data_dir = Path(__file__).parent / "cheatsheets"
        data_dir.mkdir(exist_ok=True)

        sample_data = [
            {
                "title": "SQL注入检测",
                "description": "SQL注入漏洞检测",
                "tags": ["sql", "安全"],
                "command": "sqlmap -u 'http://test.com?id=1'"
            },
            {
                "title": "Nmap扫描",
                "description": "端口扫描",
                "tags": ["nmap", "网络"],
                "command": "nmap -sV target.com"
            }
        ]

        with open(data_dir / "data.json", 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)

        print("✅ 已初始化数据库")
        print(f"📁 数据目录: {data_dir}")

    elif command in ["help", "--help", "-h"]:
        print("命令列表:")
        print("  list              显示所有速查表")
        print("  search <关键词>   搜索速查表")
        print("  init              初始化数据库")
        print("  help              显示帮助")

    else:
        print(f"❌ 未知命令: {command}")
        print("使用 'python main.py help' 查看帮助")


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
    