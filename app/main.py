import argparse

from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.curator import CuratorAgent
from agents.strategist import StrategyAgent
from agents.writer import WriterAgent
from agents.critic import CriticAgent

from rag.vector_store import index_products


def main(topic):

    print("Indexing products...")
    index_products()

    planner = PlannerAgent("planner")
    retriever = RetrieverAgent()
    curator = CuratorAgent("curator")
    strategist = StrategyAgent("strategist")
    writer = WriterAgent("writer")
    # strategic_writer = StrategicWriterAgent("strategic_writer")
    critic = CriticAgent("critic")

    print("\nRunning Planner...")
    planner.run(topic)

    print("Retrieving products...")
    products = retriever.run(topic)

    print("Curating...")
    curated = curator.run(topic, products)

    print("Strategizing...")
    strategy = strategist.run(topic)

    print("Writing email...")
    email = writer.run(topic, curated, strategy)
    
    # print("Strategizing and Mail writer...")
    # email = strategic_writer.run(topic)

    print("Critiquing...")
    final_email = critic.run(email)

    print("\n====== FINAL EMAIL ======\n")
    print(final_email)


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--topic", required=True)
    # args = parser.parse_args()

    # main(args.topic)

    topic = input('Give the topic details here')
    main(topic)
    