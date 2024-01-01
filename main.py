from openai import OpenAI
from dotenv import load_dotenv
from datetime import date

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

print(completion.choices[0].message.content)

template = f"""
# Quote of the day
### 📅 {date.today().strftime("%A, %B %d, %Y")}
------
{completion.choices[0].message.content}
"""

# write the respone to README.md
with open("README.md", "w") as f:
    f.write(completion.choices[0].message.content)
