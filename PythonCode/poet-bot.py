import time
from openai import OpenAI
import os

client = OpenAI()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = OPEN_AI_API_KEY)

def create_assistant():
  assistant = client.beta.assistants.create(
    name="Poem Assistant",
    instructions="You are a poet that writes poems about the secrets that the user tells you",
    # tools=[{"type": "code_interpreter"}],
    model="gpt-4-turbo-preview",
  )
  return assistant

def generate_response(message_body):
  thread = client.beta.threads.create()

  message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=message_body,
  )

message_body = "I accidently murdered my brother when I was a kid"

def run_assistant():
  # Retrieves the assistant
  assistant = client.beta.assistants.retrieve("")
  thread = client.beta.threads.retrieve("")

  # Runs the assistant
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
  )

  # Waits for API
  while run.status != "completed":
    time.sleep(0.5)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

  messages = client.beta.threads.messages.list(thread_id=thread.id)
  new_message = messages.data[0].content[0].text.value
  logging.info(f"Generated message: {new_message}")
  return new_message

new_message = run_assistant()
