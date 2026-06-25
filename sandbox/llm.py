import anthropic
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel

load_dotenv()

client = anthropic.Anthropic()


def call_llm(messages: list[dict], temperature: float = 0, max_tokens: int = 256, system: Optional[str] = None) -> str:
    kwargs = dict(model="claude-haiku-4-5-20251001", max_tokens=max_tokens, messages=messages, temperature=temperature)
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)

    _report_cost(response.usage)

    return response.content[0].text

def call_llm_structured(messages: list[dict], schema: type[BaseModel], temperature: float = 0, max_tokens: int = 256, system: Optional[str] = None):
    kwargs = dict(model="claude-haiku-4-5-20251001", max_tokens=max_tokens, messages=messages, temperature=temperature, output_format=schema)
    if system:
        kwargs["system"] = system
    response = client.messages.parse(**kwargs)

    _report_cost(response.usage)

    return response.parsed_output

def _report_cost(usage) -> None:
    print("input tokens", usage.input_tokens)
    print("output tokens", usage.output_tokens)
    input_cost  = usage.input_tokens  * (0.80 / 1_000_000)
    output_cost = usage.output_tokens * (4.00 / 1_000_000)
    total_cost  = input_cost + output_cost
    print(f"cost in USD ${total_cost:.6f}")


class NoteSummary(BaseModel):
    summary: str
    tags: list[str]

if __name__ == "__main__":
    describe = [{
        "role": "user",
        "content": "Describe Saigon in one sentence"
    }]    
    print(call_llm(describe))

    notes = [{
        "role": "user",
        "content": (
            "Summarize these trip notes. Return JSON.\n"
            "- Arrive 5am Sunday, long immigration line.\n"
            "- Hot and humid. Streets crazy busy.\n"
            "- Food sooo good, pho amazing.\n"
            "- War Remnants Museum, heartbreaking.\n"
            "- Cafes and shopping in the evening."
        )
    }]
    result = call_llm_structured(notes, schema=NoteSummary)
    print(result)



