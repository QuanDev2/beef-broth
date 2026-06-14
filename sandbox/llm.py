import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


def call_llm(prompt: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    print(message)
    return message.content[0].text


if __name__ == "__main__":
    response = call_llm("Describe Saigon in one sentence.")
    print("\n--- Response ---")
    print(response)

