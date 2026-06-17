# agent health monitor
import os
import anthropic
from langfuse import get_client

langfuse = get_client()

client = anthropic.Anthropic(
  api_key=os.environ["ANTHROPIC_API_KEY"]
)

agent_log = """
Agent: CustomerSupportBot
Runs: 100 | Successes: 30 | Errors: 45
Avg latency: 7.2s | Avg cost: $0.005/run
"""

with langfuse.start_as_current_observation(name="health-check-run") as span:
    response = client.messages.create(
      model="claude-sonnet-4-5",
      max_tokens=500,
      messages=[{"role": "user", "content":
        f"Rate agent health 0-100 and explain why:\n{agent_log}"}]
    )
    result = response.content[0].text
    langfuse.set_current_trace_io(output=result)

print("Health score result:\n", result)
langfuse.flush()
