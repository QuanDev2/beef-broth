import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


def call_llm(messages: list[dict]) -> str:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=messages,
    )
    print("input tokens", response.usage.input_tokens)
    print("output tokens", response.usage.output_tokens)
    input_cost  = response.usage.input_tokens  * (0.80 / 1_000_000)
    output_cost = response.usage.output_tokens * (4.00 / 1_000_000)
    total_cost  = input_cost + output_cost
    print(f"cost in USD ${total_cost:.6f}")

    return response.content[0].text


if __name__ == "__main__":
    messages = [{
        "role": "user",
        "content": "Describe Saigon in one sentence."
    }]
    rep1 = call_llm(messages)
    print("\n--- Turn 1 ---")
    print(rep1)

    messages.append({"role": "assistant", "content": rep1})
    messages.append({"role": "user", "content": "make it more poetic"})
    rep2 = call_llm(messages)
    print("\n--- Turn 2 (with history) ---")
    print(rep2)



