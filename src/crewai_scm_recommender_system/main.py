#!/usr/bin/env python
import os
from crewai.flow import Flow, start, listen
from crewai_scm_recommender_system.crews.recommender_crew.crew import SupplyChainCrew

os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'

class ResearchFlow(Flow):

    @start()
    def start_method_of_research_flow(self):
        """
        Run the supply chain intelligence crew.
        """
        crew_instance = SupplyChainCrew()
        result = crew_instance.crew().kickoff(inputs={})

        print("\n" + "="*50)
        print("CREW EXECUTION COMPLETED")
        print("="*50)
        print(f"\nFinal Report:\n{result.raw}")
        print(f"\nReport saved to: supply_chain_recommendations.md")
        print(f"\nToken Usage: {result.token_usage}")
        
        return result.raw

def kickoff():
    research_flow = ResearchFlow()
    research_flow.kickoff()

def plot():
    research_flow = ResearchFlow()
    research_flow.plot()

if __name__ == "__main__":
    kickoff()
