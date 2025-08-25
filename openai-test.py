from openai import OpenAI
import os

# client = OpenAI()
message_input = "I killed my brother"

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = OPEN_AI_API_KEY)

assistant = client.beta.assistants.create(
  name="Poem Assistant",
  instructions="You are a poet that is told a secret. Write a short poem about the main themes in the secret",
  # tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo-preview",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content=message_input,
  )

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please write a poem about the secret the user submitted"
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages.data[0].content[0].text.value)
else:
  print(run.status)

# def create_assistant():
#   assistant = client.beta.assistants.create(
#     name="Poem Assistant",
#     instructions="You are a poet that writes poems about the secrets that the user tells you",
#     # tools=[{"type": "code_interpreter"}],
#     model="gpt-4-turbo-preview",
#   )
#   return assistant

# def generate_response(message_body):
#   thread = client.beta.threads.create()
#   thread_id = thread.id

#   message = client.beta.threads.messages.create(
#     thread_id=thread_id,
#     role="user",
#     content=message_body,
#   )

# message_body = "I am in love with someone who cant love me back"

# def run_assistant():
#   # Retrieves the assistant
#   assistant = client.beta.assistants.retrieve("")
#   thread = client.beta.threads.retrieve("")

#   # Runs the assistant
#   run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
#   )

#   # Waits for API
#   while run.status != "completed":
#     time.sleep(0.5)
#     run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

#   messages = client.beta.threads.messages.list(thread_id=thread.id)
#   new_message = messages.data[0].content[0].text.value
#   logging.info(f"Generated message: {new_message}")
#   return new_message

# new_message = run_assistant()