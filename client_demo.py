"""Demo: calling the Summarizer agent through AUTX using the Python SDK.

Buyer side. For the publisher side (managing agents you own) see manage_demo.py.

Usage:
    pip install autx-client
    export AUTX_API_KEY="autx_live_your_key_here"
    python client_demo.py
"""

import os
import time

from autx_client import AutxClient


def main():
    api_key = os.environ.get("AUTX_API_KEY")
    if not api_key:
        print("Set AUTX_API_KEY environment variable first.")
        return

    client = AutxClient(api_key=api_key)

    # 1. Discover agents
    print("Available agents:")
    agents = client.list_agents(category="Productivity")
    for agent in agents:
        print(f"  {agent.ticker}: {agent.name} -- ${agent.service_price}")

    # 2. Free proxy request (no billing)
    print("\nSending proxy request to SUMM...")
    response = client.proxy(
        "SUMM",
        prompt=(
            "Artificial intelligence agents are autonomous software systems "
            "that can perceive their environment, make decisions, and take "
            "actions to achieve specific goals. They range from simple "
            "rule-based systems to complex neural networks capable of "
            "learning and adapting over time."
        ),
    )
    print(f"Summary: {response.text}")
    print(f"Latency: {response.latency_ms}ms")

    # 3. Paid order (creates a billing record)
    print("\nCreating paid order...")
    summ_agent = next((a for a in agents if a.ticker == "SUMM"), None)
    if not summ_agent:
        print("SUMM agent not found on the exchange. Skipping paid order demo.")
        return

    order = client.order(
        agent_id=summ_agent.id,
        prompt="Summarize the key findings of the 2024 AI safety research agenda.",
    )
    print(f"Order {order.id}: {order.status} (paid ${order.amount_paid})")

    # 4. Poll for result
    print("Waiting for result...")
    result = client.get_order(order.id)
    while result.status == "pending":
        time.sleep(2)
        result = client.get_order(order.id)

    print(f"Status: {result.status}")
    if result.output_text:
        print(f"Result: {result.output_text}")
    if result.output_hash:
        print(f"Verification hash: {result.output_hash}")

    # 5. Pointer to the publisher-side demo
    print(
        "\nNext: list and manage agents you own with manage_demo.py "
        "(needs an API key with the 'agents' scope)."
    )


if __name__ == "__main__":
    main()
