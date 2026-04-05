import json
from prompts import build_query_plan_prompt


def generate_query_plan(client, user_question, metadata):
    prompt = build_query_plan_prompt(user_question, metadata)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()

    return json.loads(text)
