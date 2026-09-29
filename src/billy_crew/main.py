#!/usr/bin/env python
# src/research_crew/main.py
import os
from billy_crew.crew import BillyCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the research crew.
    """
    # 替换为您的输入内容，它将自动插值任务和代理信息
    inputs = {
        "lead_name": "MoPaas 魔泊云",
        "industry": "人工智能科技",
        "key_decision_maker": "鲁为民",
        "position": "创始人",
        "milestone": "吴文俊人工智能科学技术奖"
    }


    # Create and run the crew
    result = BillyCrew().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    run()