import argparse

from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.curator import CuratorAgent
from agents.strategist import StrategyAgent
from agents.writer import WriterAgent
from agents.critic import CriticAgent

from rag.vector_store import index_products
# from app.campaign_email_sender import send_campaign_email
from app.email_renderer import send_campaign_email

# Halloween festival
# Valentines festival

def main(topic):

    # print("Indexing products...")
    # index_products()

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
    email_json = writer.run(topic, curated, strategy)
    
    # print("Strategizing and Mail writer...")
    # email = strategic_writer.run(topic)

    print("Critiquing...")
    final_email_json = critic.run(email_json)


    print("\n====== FINAL EMAIL ======\n")
    print(final_email_json)
    
    # write_email_to_files(
    #     subject=final_email_json["subject"],
    #     raw_text=email_text,
    #     html_text=email_html
    # )

    # send_campaign_email(
    #     final_email,
    #     to_email=["prajwal.sk@anko.com"],
    #     first_name="Customer"
    # )

    send_campaign_email(
        email_json=final_email_json,
        to_email=["prajwal.sk@anko.com"],
        first_name="Customer"
    )


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--topic", required=True)
    # args = parser.parse_args()

    # main(args.topic)

    topic = input('Topic for Campaign:\n')
    main(topic)
    