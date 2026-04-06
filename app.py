import os
from dotenv import load_dotenv
from google import genai
from catalog import load_first_csv, get_dataset_metadata
from planner import generate_query_plan
from executor import execute_query_plan

load_dotenv(dotenv_path=".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("API KEY LOADED:", bool(os.getenv("GEMINI_API_KEY")))
df, file_name = load_first_csv()

if df is None:
    print("No CSV file found in current directory.")
    raise SystemExit

metadata = get_dataset_metadata(df, file_name)

user_question = input("Ask your question: ")

try:
    plan = generate_query_plan(client, user_question, metadata)
    print("\nGenerated Query Plan:\n")
    print(plan)

    answer = execute_query_plan(df, plan)
    print("\nFinal Answer:\n")
    print(answer)

except Exception as e:
    print("Error:", e)
