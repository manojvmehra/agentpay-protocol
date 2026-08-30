import os
from dotenv import load_dotenv

load_dotenv()

# Razorpay Test Mode Keys
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_xxxxxxxxxxxxx")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "your_key_secret_here")

# Groq API (free tier - runs Llama/Mistral)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Agent Settings
MAX_NEGOTIATION_ROUNDS = 3
MAX_PAYMENT_RETRIES = 3
PAYMENT_RETRY_DELAY_SECONDS = 2
BUDGET_HARD_LIMIT = True  # Agent NEVER exceeds budget
