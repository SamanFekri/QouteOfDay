import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import date
import yaml
import logging
from typing import Optional 

def getConfig(path: Optional[str]) -> dict:
  """
  Get the config file.

  Args:
    path (Union[str, None]): The path to the config file. If None, the default path "config.yaml" will be used.

  Returns:
    dict: The contents of the config file as a dictionary.
  """
  if path is None:
    path = "."
  path += "/config.yaml"
  with open(path, "r") as f:
    return yaml.load(f, Loader=yaml.FullLoader)

def getCurrentPath() -> str:
    """
    Get the current path
    """
    return os.path.dirname(os.path.realpath(__file__))

def askFromGpt(prompt: str) -> str:
    """
    Ask the GPT-3 model to generate a response based on the prompt
    """
    # get the client session
    client = OpenAI()

    # send the prompt to the API
    completion = client.chat.completions.create(
    model=config["gpt"]["model"],
    temperature=config["gpt"]["temperature"],
    max_tokens=config["gpt"]["max_tokens"],
    messages=[
        {"role": "user", "content": prompt}
    ],
    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "WARNING"))
    logging.info("Starting the program ...")
    # log the current path
    path = getCurrentPath()
    logging.info(f"Current path: {getCurrentPath()}")
    # load the config file
    config = getConfig(path=path)
    logging.info(f"Config file: \n{config}")

    # get today date
    today = date.today()

    # Ask for the the 3 events that happened in this date
    prompt = f"What are one event in usa this date? (date={today.strftime('%d %B')}) use bullet points"
    logging.info(f"Prompt: {prompt}")
    # ask the GPT model
    events = askFromGpt(prompt)

    # Ask for the quote of the day
    prompt = f"Give me a random positive quote of the day with emojies related to the quote change every day"
    logging.info(f"Prompt: {prompt}")
    # ask the GPT model
    quote = askFromGpt(prompt)

    # create the history file of events
    logging.info("Creating the history folder ...")
    os.makedirs(f"{path}/history", exist_ok=True)
    # create the folder of the current year
    logging.info("Creating the folder of the current year ...")
    os.makedirs(f"{path}/history/{today.year}", exist_ok=True)
    # create the file of the current month
    logging.info("Creating the file of the current month ...")
    with open(f"{path}/history/{today.year}/{today.strftime('%B')}.md", "a") as f:
        f.write(f"## {today.strftime('%A, %d %B, %Y')}\n")
        f.write(f"### Events\n")
        f.write(f"{events}\n")
        f.write(f"### Quote of the day\n")
        f.write(f"{quote}\n")
        f.write(f"-----\n")
    
    # create the README.md file
    logging.info("Creating the README.md file ...")
    with open(f"{path}/README.md", "w") as f:
        f.write(f"### 📅 {today.strftime('%A, %d %B, %Y')}\n")
        f.write(f"------\n")

        f.write(f"### Events\n")
        f.write(f"------\n")
        f.write(f"{events}\n")

        f.write(f"### Positive Qoute\n")
        f.write(f"------\n")
        f.write(f"{quote}\n")

    # commit the changes to the repo
    logging.info("Pulling from Git ...")
    os.system(f"git -C {path} pull" )
    logging.info("Done")
    
    logging.info("Add and commiting ...")
    os.system(f"git -C {path} add ." )
    os.system(f"git -C {path} commit -m 'update quote of the day for {today.strftime('%d %B, %Y')}'" )
    logging.info("Done")

    logging.info("Pushing the new commit to git ...")
    os.system(f"git -C {path} push" )
    logging.info("Done")
