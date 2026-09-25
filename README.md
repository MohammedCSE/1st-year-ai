 AI-Powered Insurance Claim Processor

An intelligent web application that automates insurance claim processing by analyzing policy documents in real-time. Built with FastAPI, Groq AI (LLM), PyPDF, and MySQL, this system extracts coverage limits directly from uploaded PDF policy files and evaluates claims against extracted terms.

🚀 Key Features

📄 Automated PDF Parsing: Extracts text directly from uploaded policy documents using pypdf.

🧠 AI Rule Extraction: Uses Groq LLMs to analyze policy jargon and convert coverage rules into structured JSON data.

⚡ Real-Time Claim Assessment: Automatically verifies claim amounts against extracted medical, prescription, emergency, or dental policy limits.

💾 Persistent Database Storage: Saves all evaluated claims, user details, and assessment outcomes into a MySQL database.

🌐 Clean UI: Simple front-end interface built with HTML, CSS, and asynchronous JavaScript (fetch API).

🏗️ Architecture & Tech Stack

Frontend: HTML5, CSS3, JavaScript (ES6+ Fetch API)

Backend Framework: Python, FastAPI, Uvicorn

AI & Processing: Groq API (openai/gpt-oss-20b), PyPDF, python-dotenv

Database: MySQL Server, mysql-connector-python

📁 Repository Structure

.
├── database.py       # Handles MySQL database connections & record insertions
├── main.py           # FastAPI server, endpoints, business logic, & AI orchestration
├── pdf_reader.py     # Standalone PDF text extraction module
├── groqk.py          # Prototyping script for Groq API integration
├── index.html        # Main web user interface
├── script.js         # Client-side form submission & dynamic UI rendering
└── README.md         # Project documentation


⚙️ Setup and Installation

1. Prerequisites

Python 3.9+

MySQL Server installed and running locally

Groq API Key (obtainable from Groq Console)

2. Database Configuration

Start your MySQL service.

Create a database named insurance_claims.

Create a table named claims:

CREATE DATABASE insurance_claims;

USE insurance_claims;

CREATE TABLE claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    claim_type VARCHAR(100) NOT NULL,
    claim_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


Update your MySQL login credentials inside database.py if needed:

host="localhost",
port=3306,
user="root",
password="YOUR_MYSQL_PASSWORD",
database="insurance_claims"


3. Backend Setup

Clone the repository:

git clone https://github.com/your-username/insurance-claim-processor.git
cd insurance-claim-processor


Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install required Python packages:

pip install fastapi uvicorn groq pypdf mysql-connector-python python-dotenv


Create a .env file in the root directory and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here


Run the FastAPI server:

uvicorn main:app --reload


The backend API will run on http://127.0.0.1:8000.

🧪 Usage

Open index.html in your web browser (or serve it via a live server).

Enter the Customer Name, select a Claim Type, and enter the Claim Amount.

Upload an Insurance Policy PDF document.

Click Submit Claim.

View the real-time AI evaluation on screen. The claim decision will also be saved to your MySQL database.

