from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# Connect to Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


# Read PDF
def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# Read our insurance PDF
text = extract_text_from_pdf("sample_insurance_policy.pdf")

print("PDF TEXT:")
print(text)


# Send PDF text to Groq
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": """
You are an insurance document analyzer.

Read the insurance policy and extract the coverage rules.

Return ONLY valid JSON.
Do not write anything before or after the JSON.

Use this exact format:

{
    "medical_limit": 500,
    "prescription_limit": 1000,
    "emergency_limit": 5000,
    "dental_covered": false
}
"""
        },
        {
            "role": "user",
            "content": text
        }
    ],
    response_format={"type": "json_object"}
)

# Get AI response
ai_response = response.choices[0].message.content

print("\nAI RESPONSE:")
print(ai_response)


ai_response = response.choices[0].message.content

print("\nAI RESPONSE:")
print(ai_response)

claim_data = json.loads(ai_response)

print("\nCLAIM DATA:")
print(claim_data)