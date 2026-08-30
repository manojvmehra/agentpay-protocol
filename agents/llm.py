"""
LLM Interface for AgentPay
==========================
Uses Groq API (free tier) with Llama 3 for AI reasoning.
Handles all the "thinking" for the buyer agent.
"""

import asyncio
import json
import re
import httpx
from config import GROQ_API_KEY, GROQ_MODEL

MAX_RATE_LIMIT_RETRIES = 3


async def llm_reason(system_prompt: str, user_message: str, response_format: str = "json") -> dict | str:
    """
    Send a reasoning request to the LLM and get a structured response.
    
    Args:
        system_prompt: Instructions for the LLM
        user_message: The actual query/context
        response_format: "json" for structured output, "text" for free text
    
    Returns:
        Parsed JSON dict or text string
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    
    body = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.3,  # Low temperature for consistent reasoning
        "max_tokens": 2000,
    }
    
    if response_format == "json":
        body["response_format"] = {"type": "json_object"}
    
    async with httpx.AsyncClient(timeout=30) as client:
        for attempt in range(1, MAX_RATE_LIMIT_RETRIES + 1):
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=body,
            )
            if response.status_code == 429 and attempt < MAX_RATE_LIMIT_RETRIES:
                retry_after = response.headers.get("retry-after")
                if retry_after is None:
                    match = re.search(r"try again in ([\d.]+)s", response.text)
                    retry_after = match.group(1) if match else "5"
                await asyncio.sleep(float(retry_after) + 0.5)
                continue
            if response.status_code >= 400:
                raise httpx.HTTPStatusError(
                    f"{response.status_code} error from Groq: {response.text}",
                    request=response.request,
                    response=response,
                )
            data = response.json()
            break
    
    content = data["choices"][0]["message"]["content"]
    
    if response_format == "json":
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
            return {"error": "Failed to parse LLM response", "raw": content}
    
    return content


# Pre-built prompts for the buyer agent

PARSE_REQUEST_PROMPT = """You are the AI brain of a buyer agent in the AgentPay protocol.
Your job is to parse a natural language shopping request into structured requirements.

Given the user's request, extract:
1. What items/services they need (be specific about categories)
2. Quantities (exact or estimated)
3. Total budget
4. Any preferences (quality, brand, dietary, etc.)
5. Event context (what's the occasion)

Respond ONLY with a JSON object in this exact format:
{
    "event_name": "name of event",
    "event_size": number_of_attendees,
    "budget": total_budget_in_inr,
    "requirements": [
        {
            "category": "apparel|accessories|printing|signage|food|beverages|catering",
            "description": "what they need",
            "estimated_quantity": number,
            "max_price_per_unit": number_or_null,
            "preferences": ["any specific preferences"]
        }
    ],
    "priority": "cost|quality|speed"
}"""


NEGOTIATION_PROMPT = """You are the AI brain of a buyer agent negotiating with a merchant.
You must get the best deal possible while being fair.

Rules:
- Never exceed the buyer's budget
- Start by offering 15-20% below asking price
- Accept if the counter is within 10% of your target
- Use bulk discounts and combo deals to your advantage
- Be strategic: if a merchant won't budge, consider alternatives
- Maximum 3 negotiation rounds

Given the merchant's catalog, current prices, and buyer's budget, decide:

Respond ONLY with a JSON object:
{
    "action": "offer|accept|reject|skip",
    "items": [
        {
            "product_id": "id",
            "quantity": number,
            "target_unit_price": number
        }
    ],
    "offered_total": number,
    "reasoning": "why this offer makes sense",
    "upsell_interest": true/false,
    "combo_interest": "combo_name or null"
}"""


COMPARE_DEALS_PROMPT = """You are the AI brain of a buyer agent comparing deals from multiple merchants.
You've received quotes from different sellers and need to pick the best combination.

Rules:
- Total must stay within budget
- Prioritize value (price + quality balance)
- Prefer combo deals when they save money
- Consider all requirements are met
- If one merchant can't fulfill, split across merchants

Respond ONLY with a JSON object:
{
    "selected_orders": [
        {
            "merchant_id": "id",
            "merchant_name": "name",
            "items": [
                {
                    "product_id": "id",
                    "name": "product name",
                    "quantity": number,
                    "unit_price": number,
                    "total": number
                }
            ],
            "order_total": number,
            "reasoning": "why this merchant for these items"
        }
    ],
    "total_spend": number,
    "budget_remaining": number,
    "total_savings": number,
    "summary": "one-line summary of the deal"
}"""


FAILURE_ANALYSIS_PROMPT = """You are the AI brain of a buyer agent handling a failure.
Something went wrong during the transaction. Analyze and decide next steps.

Possible failures:
- Payment failed (retry? different method?)
- Merchant unresponsive (skip? retry?)
- Item out of stock (alternative? different merchant?)
- Budget exceeded (remove items? negotiate harder?)
- Negotiation failed (accept last offer? try another merchant?)

Respond ONLY with a JSON object:
{
    "failure_type": "payment|timeout|stock|budget|negotiation",
    "severity": "low|medium|high",
    "recovery_action": "retry|skip|alternative|abort",
    "details": "what went wrong",
    "recovery_plan": "step by step recovery plan",
    "user_notification": "what to tell the user"
}"""
