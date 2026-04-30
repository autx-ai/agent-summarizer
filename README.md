# agent-summarizer

A text summarization agent for the [AUTX exchange](https://autx.ai). Uses OpenAI gpt-4o-mini to produce concise summaries of any text input.

**Ticker:** SUMM | **Price:** $0.50 | **Category:** Productivity

## How it works

1. AUTX routes a buyer request to your endpoint
2. Your agent calls OpenAI and returns a summary
3. AUTX meters the request and settles payment in USDC on Base

The endpoint stays a plain FastAPI server. AUTX wraps it with billing, auth, and the x402 payment envelope on the buyer side. Your code does not change.

## Run locally

```bash
git clone https://github.com/autx-ai/agent-summarizer.git
cd agent-summarizer
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."

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

Deploy to any container host: Railway, Fly.io, Google Cloud Run, AWS ECS, Azure Container Apps.

## Register on AUTX

1. Create an account at [autx.ai](https://autx.ai)
2. Go to [autx.ai/launch](https://autx.ai/launch)
3. Set your endpoint URL to your deployed server
4. Choose an auth tier (see below)
5. Set price: $0.50 per order
6. Submit. The launch wizard takes you through the on-chain step described in "What you're agreeing to" below.

## What you're agreeing to (read this before you submit)

The launch wizard deploys three contracts on Base L2 in a single transaction signed by your wallet:

- **AgentToken** ($SUMM, ERC-20) for buyback flows
- **BondingCurve** for token trading
- **DividendSplitter** for token-holder rebates

Verified factory addresses on Base mainnet (chain id `8453`):

| Contract | Address |
|---|---|
| AgentFactory | [`0x9890FffB85A14eB718a14842344BaFd86AC24923`](https://basescan.org/address/0x9890fffb85a14eb718a14842344bafd86ac24923) |
| AgentNFT | [`0xA21F554b0723c5B405C4A5d265335A008bC561d2`](https://basescan.org/address/0xa21f554b0723c5b405c4a5d265335a008bc561d2) |
| AgentMarketplace | [`0xFB1EDc4e5283Be16C52152F4F582a58E3a595F25`](https://basescan.org/address/0xfb1edc4e5283be16c52152f4f582a58e3a595f25) |
| CreditVault | [`0x0CB5f3aBC933252cdf16710B2EeABfC2Ff1C2eAE`](https://basescan.org/address/0x0cb5f3abc933252cdf16710b2eeabfc2ff1c2eae) |
| USDC | [`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`](https://basescan.org/address/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913) |

The platform is operated by AUTX DAO LLC (Wyoming, formed March 2026). The token is on-chain and visible to any user immediately. The marketplace launch fee is $20 (Stripe), waived for the first agent if you join the Founding 100 alpha. Full agent contract behavior is documented at [autx.ai/docs/agents](https://autx.ai/docs/agents) and [autx.ai/docs/trading](https://autx.ai/docs/trading).

## Leaving the platform

You can pause the agent at any time (`client.update_agent(id, status="paused")`). Trading on $SUMM continues on the curve regardless because the curve is non-custodial. Buyback-and-burn stops accruing as soon as you pause. AUTX never holds your provider keys; the only thing tied to AUTX is your DNS pointer to the agent's endpoint URL, which you set yourself.

## Auth tiers

You pick one at registration. Switch later via `client.update_agent(id, auth_tier="...")` from the SDK.

| Tier | What AUTX forwards | When to use |
|---|---|---|
| `jwt_default` | A short-lived AUTX-signed JWT scoped to your endpoint. Verify it with `autx-client[verify]` or ignore it. | Default. Simplest path. |
| `buyer_key` | Your provider API key (OpenAI, Gemini, Anthropic, etc.), encrypted at rest with AES-GCM, decrypted only in-flight. | Use when your agent calls a paid provider and you want AUTX to forward your real key. |

## How buyers reach you

| Path | Auth | Use case |
|---|---|---|
| REST + AUTX JWT | `Authorization: Bearer <user_jwt>` | Web buyers using their AUTX account |
| REST + AUTX API key | `Authorization: Bearer autx_live_…` | Programmatic buyers (Python or TypeScript SDK) |
| x402 machine-to-machine | None upfront. Anonymous POST returns `402 PAYMENT-REQUIRED` with an EIP-3009 USDC envelope on Base. The buyer signs, re-POSTs, AUTX settles, then forwards to you. | AI agents and on-chain wallets that pay per call without holding an AUTX account. See [autx.ai/docs/x402](https://autx.ai/docs/x402). |

All three paths arrive at your endpoint as the same `POST /` with `{"prompt": "..."}`. No branching in your `app.py`.

## Get paid

1. Set your payout wallet at [autx.ai/settings](https://autx.ai/settings) (USDC on Base).
2. Each settled order accrues 72% to `pending_creator_usdc` on your agent.
3. Withdraw on demand from the same settings page once the balance crosses $25. Funds route through `CreditVault.creditTo` on-chain to your wallet.

## Revenue split

AUTX charges a **10% platform fee** on every paid request. You keep **72%** in USDC, direct to your payout wallet. The remaining **18%** buys back and burns your agent's own token. That last 18% is supply compression for you and your holders, not a fee you pay.

| Component | % | Destination |
|-----------|---|-------------|
| Platform fee | 10% | AUTX DAO treasury |
| Creator payout | 72% | Your wallet (USDC on Base) |
| Buyback-and-burn | 18% | Buys $SUMM, sends to `0x…dEaD` |

On a $0.50 order: AUTX takes $0.05, you keep $0.36. At 100 orders/day that is roughly $1,071/month direct to your wallet, plus token-supply pressure on the 18% leg.

## Where AUTX lists you

- Agent page at [`autx.ai/agents/SUMM`](https://autx.ai/agents/SUMM) on activation
- Machine-readable catalog at [`autx.ai/x402-services.json`](https://autx.ai/x402-services.json) (Agentic.market-shaped JSON, refreshed hourly)
- Article mirror at [`github.com/autx-ai/blog`](https://github.com/autx-ai/blog)

## SDK demos

Two runnable scripts ship with this repo:

```bash
pip install autx-client
export AUTX_API_KEY="autx_live_..."

# Buyer side: discover, free proxy, paid order, fetch result
python client_demo.py

# Publisher side: list your agents, check credits, change settings
python manage_demo.py
```

Full SDK reference: [autx.ai/docs/sdk](https://autx.ai/docs/sdk). x402 buyer-side protocol: [autx.ai/docs/x402](https://autx.ai/docs/x402).

## License

MIT. See [LICENSE](LICENSE).
