# src/research_crew/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
import os
from dotenv import load_dotenv
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from billy_crew.tools.custom_tool import SentimentAnalysisTool

# 加载环境变量
load_dotenv('.env')

# ========== 通义千问配置（Dashscope）==========
llm = LLM(
    model="dashscope/qwen-plus", # 可选：qwen-turbo / qwen-plus / qwen-max
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.4
)

@CrewBase
class BillyCrew():
    """BillyCrew crew"""

    """Research crew for comprehensive topic analysis and reporting"""
    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    print(f"当前LLM模型: {llm.model}")
    
    @agent
    def sales_rep_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sales_rep_agent'],  # type: ignore[index]
            verbose=True,
            native_tools=False,  # 新增这一行！关闭原生工具，不再强制调用OpenAI
            llm=llm
            # tools=[SerperDevTool()]
        )

    @agent
    def lead_sales_rep_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_sales_rep_agent'],  # type: ignore[index]
            native_tools=False,  # 新增这一行！关闭原生工具，不再强制调用OpenAI
            llm=llm,
            verbose=True
        )

    @task
    def lead_profiling_task(self) -> Task:
        return Task(
            # 要做什么事情
            config=self.tasks_config['lead_profiling_task'],
            # 配置对应的工具 框架内置工具
            # tools=[DirectoryReadTool(directory='./instructions'), FileReadTool(), SerperDevTool()],
            tools=[DirectoryReadTool(directory='./instructions'), FileReadTool()],
            # 给任务配置agent
            agent=self.sales_rep_agent()
        )

    @task
    def personalized_outreach_task(self) -> Task:
        return Task(
            config=self.tasks_config['personalized_outreach_task'],
            tools=[SentimentAnalysisTool(), SerperDevTool()],
            agent=self.lead_sales_rep_agent(),
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )