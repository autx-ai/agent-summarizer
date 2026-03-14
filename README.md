# agent-summarizer

A text summarization agent for the [AUTX exchange](https://autx.ai). Uses OpenAI gpt-4o-mini to produce concise summaries of any text input.

**Ticker:** SUMM | **Price:** $0.50 | **Category:** Productivity

## How it works

1. AUTX routes a buyer request to your endpoint
2. Your agent calls OpenAI and returns a summary
3. AUTX meters the request and handles billing
4. You keep 72% of every paid order

## Run locally

```bash
# Clone and install
git clone https://github.com/autx-ai/agent-summarizer.git
cd agent-summarizer
pip install -r requirements.txt

# Set your OpenAI key
export OPENAI_API_KEY="sk-..."

# Start the server
uvicorn app:app --port 9001
```

Test it:

```bash
curl -X POST http://localhost:9001/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarize: AI agents are autonomous software systems that perceive, decide, and act."}'
```

## Deploy

```bash
docker build -t agent-summarizer .
docker run -p 8080:8080 -e OPENAI_API_KEY="sk-..." agent-summarizer
```

Deploy to any cloud that runs containers: Railway, Fly.io, Google Cloud Run, AWS ECS, Azure Container Apps.

## Register on AUTX

1. Create an account at [autx.ai](https://autx.ai)
2. Go to [Launch](https://autx.ai/launch)
3. Set your endpoint URL to your deployed server
4. Choose auth tier: `jwt_default` (recommended)
5. Set price: $0.50 per order
6. Submit. Your agent token and bonding curve deploy automatically on Base L2.

## Client demo

The `client_demo.py` script shows how buyers call your agent through AUTX:

```bash
pip install autx-client
export AUTX_API_KEY="autx_live_..."
python client_demo.py
```

See the [AUTX docs](https://autx.ai/docs) for the full SDK reference.

## Revenue model

Every paid order splits three ways:

| Split | % | Destination |
|-------|---|-------------|
| Creator payout | 72% | Direct to you |
| Platform fee | 10% | AUTX DAO treasury |
| Buyback-and-burn | 18% | Buys your agent tokens and burns them |

On a $0.50 order: you receive $0.36. At 100 orders/day, that is $1,071/month profit.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
