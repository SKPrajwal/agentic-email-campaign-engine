from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.curator import CuratorAgent
from agents.strategist import StrategyAgent
from agents.writer import WriterAgent
from agents.critic import CriticAgent

# from rag.vector_store import index_products
# from app.campaign_email_sender import send_campaign_email
from app.email_renderer import send_campaign_email

# Halloween festival
# Valentines festival

def main(topic, to_email='prajwal.sk@anko.com'):

    planner = PlannerAgent("planner")
    retriever = RetrieverAgent()
    curator = CuratorAgent("curator")
    strategist = StrategyAgent("strategist")
    writer = WriterAgent("writer")
    critic = CriticAgent("critic")

    agents = {
        "retrieve": retriever,
        "curate": curator,
        "strategize": strategist,
        "write": writer,
        "critic": critic
    }

    context = {"topic": topic}

    print("\nRunning Planner...")
    plan = planner.run(topic)

    print(plan)

    for step in plan["execution_plan"]:

        step_name = step["step"]
        print(f"\nExecuting {step_name}...")

        if step_name == "retrieve":
            context["products"] = agents[step_name].run(topic)

        elif step_name == "curate":
            context["curated"] = agents[step_name].run(topic, context["products"])

        elif step_name == "strategize":
            context["strategy"] = agents[step_name].run(topic)

        elif step_name == "write":
            context["email"] = agents[step_name].run(
                topic,
                context["curated"],
                context["strategy"]
            )

        elif step_name == "critic":
            context["final_email"] = agents[step_name].run(context["email"])

    print("\n====== FINAL EMAIL ======\n")
    print(context["final_email"])
    
    send_campaign_email(
        email_json=context["final_email"],
        to_email=["prajwal.sk@anko.com"],
        first_name="Customer"
    )


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--topic", required=True)
    # args = parser.parse_args()

    # main(args.topic)

    topic = input('Topic for Campaign:\n')
    to_email = input('Enter TO EMAIL for campaign:\n')
    main(topic, to_email)
    