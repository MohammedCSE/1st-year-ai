from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
from database import save_claim
import os
import json


# -----------------------------------
# Load environment variables
# -----------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found")

client = Groq(api_key=api_key)


# -----------------------------------
# Create FastAPI app
# -----------------------------------

app = FastAPI()


# Allow our HTML/JavaScript frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Extract text from PDF
# -----------------------------------

def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# -----------------------------------
# Ask Groq to analyse policy
# -----------------------------------

def analyse_policy(text):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
You are an insurance document analyzer.

Read the insurance policy and extract the coverage rules.

Return ONLY valid JSON.

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

    ai_response = response.choices[0].message.content

    return json.loads(ai_response)


# -----------------------------------
# Claim checking
# -----------------------------------

def check_claim(claim_type, claim_amount, policy):

    if claim_type == "Med":

        limit = policy["medical_limit"]

        if claim_amount <= limit:
            return "Claim can be processed."

        return "Claim exceeds the medical coverage limit."

    elif claim_type == "Pres":

        limit = policy["prescription_limit"]

        if claim_amount <= limit:
            return "Claim can be processed."

        return "Claim exceeds the prescription coverage limit."

    elif claim_type == "Emergency":

        limit = policy["emergency_limit"]

        if claim_amount <= limit:
            return "Claim can be processed."

        return "Claim exceeds the emergency coverage limit."

    elif claim_type == "Dental":

        if policy["dental_covered"]:
            return "Claim can be processed."

        return "Dental treatment is not covered."

    else:

        return "Invalid claim type."


# -----------------------------------
# Claim endpoint
# -----------------------------------

@app.post("/claims")
async def create_claim(
    customer_name: str = Form(...),
    claim_type: str = Form(...),
    claim_amount: float = Form(...),
    policy_file: UploadFile = File(...)
):

    print("Customer:", customer_name)
    print("Claim type:", claim_type)
    print("Claim amount:", claim_amount)
    print("Uploaded file:", policy_file.filename)


    # -----------------------------------
    # Save uploaded PDF temporarily
    # -----------------------------------

    file_path = f"uploaded_{policy_file.filename}"

    with open(file_path, "wb") as f:
        f.write(await policy_file.read())


    # -----------------------------------
    # Extract PDF text
    # -----------------------------------

    policy_text = extract_text_from_pdf(file_path)

    print("\nPDF TEXT:")
    print(policy_text)


    # -----------------------------------
    # Ask Groq to analyse policy
    # -----------------------------------

    policy = analyse_policy(policy_text)

    print("\nAI POLICY:")
    print(policy)


    # -----------------------------------
    # Check claim
    # -----------------------------------

    result = check_claim(
        claim_type,
        claim_amount,
        policy
    )
    save_claim(
        customer_name,
        claim_type,
        claim_amount,
        result
    )


    # -----------------------------------
    # Return result
    # -----------------------------------

    return {
        "status": result,
        "customer_name": customer_name,
        "claim_type": claim_type,
        "claim_amount": claim_amount,
        "policy": policy,
        "file_name": policy_file.filename
    }