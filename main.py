import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import date

load_dotenv()

client = OpenAI()
# reset session of client

# Define the prompt for the quote of the day
prompt = "Give me a random positive quote of the day with emojies related to the quote based on event of the day" 

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
### 📅 {date.today().strftime("%A, %d %B, %Y")}
------
{completion.choices[0].message.content}
"""

# write the respone to README.md
with open("README.md", "w") as f:
    f.write(template)

# commit the changes to the repo
repo_path = os.getenv("REPO_PATH") # path to the repo
print("Pulling from Git ...")
os.system(f"git -C {repo_path} pull" )
print("Done")
print()

print("Add and commiting ...")
os.system(f"git -C {repo_path} add ." )
os.system(f"git -C {repo_path} commit -m 'update quote of the day for {date.today().strftime('%d %B, %Y')}'" )
print("Done")
print()

print("Pushing the new commit to git ...")
os.system(f"git -C {repo_path} push" )
print("Done")
print()