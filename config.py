import os
from dotenv import load_dotenv

load_dotenv()

# Razorpay Test Mode Keys
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_xxxxxxxxxxxxx")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "your_key_secret_here")

# Groq API (free tier - runs Llama/Mistral)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
# Model for latency/rate-limit-sensitive calls (e.g. one call per negotiation
# round). Defaults to GROQ_MODEL itself — as of writing this Groq account has
# no meaningfully smaller general-purpose chat model available; override via
# env if one becomes available.
GROQ_MODEL_FAST = os.getenv("GROQ_MODEL_FAST", GROQ_MODEL)

# ElevenLabs Conversational AI (voice mode) — agent id is safe for the frontend,
# the API key is server-only and must never be sent to the browser.
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Agent Settings
MAX_NEGOTIATION_ROUNDS = 3
MAX_PAYMENT_RETRIES = 3
PAYMENT_RETRY_DELAY_SECONDS = 2
BUDGET_HARD_LIMIT = True  # Agent NEVER exceeds budget
