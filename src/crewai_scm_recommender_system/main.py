#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from crewai_scm_recommender_system.crews.recommender_crew.recommender_crew import RecommenderCrew


class RecommenderState(BaseModel):
    sentence_count: int = 1
    recommender: str = ""


class RecommenderFlow(Flow[RecommenderState]):

    @start()
    def generate_sentence_count(self):
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_recommender(self):
        print("Generating recommender")
        result = (
            RecommenderCrew()
            .crew()
            .kickoff(inputs={"sentence_count": self.state.sentence_count})
        )

        print("Recommender generated", result.raw)
        self.state.recommender = result.raw

    @listen(generate_recommender)
    def save_recommender(self):
        print("Saving recommender")
        with open("recommender.txt", "w") as f:
            f.write(self.state.recommender)


def kickoff():
    recommender_flow = RecommenderFlow()
    recommender_flow.kickoff()


def plot():
    recommender_flow = RecommenderFlow()
    recommender_flow.plot()


if __name__ == "__main__":
    kickoff()
