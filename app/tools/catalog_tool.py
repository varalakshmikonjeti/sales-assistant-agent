import json


def search_catalog(query: str):
    with open("catalog.json", "r") as f:
        catalog = json.load(f)

    query = query.lower()

    for plan in catalog["plans"]:
        if plan["name"].lower() in query:
            return {
                "plan": plan["name"],
                "response": (
                    f"{plan['name']} costs {plan['price']} "
                    f"and includes {', '.join(plan['features'])}"
                )
            }

    return None


def get_plan_by_name(plan_name: str):
    with open("catalog.json", "r") as f:
        catalog = json.load(f)

    for plan in catalog["plans"]:
        if plan["name"].lower() == plan_name.lower():
            return plan

    return None