import os
from crewai_scm_recommender_system.tools.database_query_tool import DatabaseQueryTool
from crewai_scm_recommender_system.tools.metric_calculator_tool import InventoryMetricsTool
from crewai_scm_recommender_system.tools.priority_tool import PriorityScoringTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class SupplyChainCrew:
    agents: List[BaseAgent]
    tasks: List[Task]
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyst'],  # type: ignore[index]
            tools=[DatabaseQueryTool()],
            verbose=True,
            allow_delegation=False,
            max_retry_limit=1,
        )
    
    @agent
    def inventory_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['inventory_strategist'],  # type: ignore[index]
            tools=[InventoryMetricsTool(), PriorityScoringTool()],
            verbose=True,
            allow_delegation=False,
            max_retry_limit=1,
        )
    
    @agent
    def business_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['business_advisor'],  # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            max_retry_limit=1,
        )

    @task
    def extract_and_analyze(self) -> Task:
        return Task(
            config=self.tasks_config['extract_and_analyze'],  # type: ignore[index]
            agent=self.data_analyst(),
        )
    
    @task
    def calculate_priorities(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_priorities'],  # type: ignore[index]
            agent=self.inventory_strategist()
        )
    
    @task
    def generate_recommendations(self) -> Task:
        return Task(
            config=self.tasks_config['generate_recommendations'],  # type: ignore[index]
            agent=self.business_advisor()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_log_file='crew_execution.log'
        )
