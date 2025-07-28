


import json
from google.cloud import aiplatform_v1beta1
from google.oauth2 import service_account

# Load credentials and setup the Vertex AI client
def get_gemini_client():
    credentials = service_account.Credentials.from_service_account_file("key.json")
    client = aiplatform_v1beta1.PredictionServiceClient(credentials=credentials)
    return client

# Gemini model endpoint
MODEL_NAME = "projects/gmail-agent-v0-1/locations/us-central1/publishers/google/models/gemini-1.5-pro-preview-0409"

def extract_startup_info_with_gemini(email_body: str) -> dict:
    """Parse email body to structured startup info using Gemini."""

    prompt = f"""
You are a structured parser. From this email text, extract:
- Startup Name
- Sender Email (if mentioned)
- Startup Description
- Need (e.g. funding, technical help, hiring)

Return only a JSON object with:
"startup_name", "sender_email", "description", "need"

Email:
\"\"\"{email_body}\"\"\"
"""

    client = get_gemini_client()

    instance = {
        "prompt": prompt,
        "temperature": 0.2,
        "maxOutputTokens": 512
    }

    response = client.predict(
        endpoint=MODEL_NAME,
        instances=[instance],
        parameters={}
    )

    content = response.predictions[0]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse Gemini output as JSON:\n{content}")