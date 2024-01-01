from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# Define the prompt for the quote of the day
prompt = "Give me a random positive quote of the day with emojies"

# send the prompt to the API
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": prompt}
  ]
)


