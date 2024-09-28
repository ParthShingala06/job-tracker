from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime, timezone
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv, find_dotenv
import uvicorn  # Ensure this is imported

load_dotenv(find_dotenv())

port = int(os.environ.get("PORT", 10000))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DB_ID = os.environ.get("DB_ID")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",  # Optional: update this to the latest version
}

class JobApplication(BaseModel):
    company: str
    position: str
    match: str

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DB_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    print(res.json())
    return res.json()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/add_job_application")
async def add_job_application(job: JobApplication):
    current_date = datetime.now(timezone.utc).isoformat()
    
    data = {
        "Company": {"title": [{"text": {"content": job.company}}]},
        "Date Applied": {"date": {"start": current_date, "end": None}},
        "Position": {"select": {"name": job.position}},
        "Match": {"select": {"name": job.match}},
    }
    print(data)
    response = create_page(data)
    
    if 'id' in response:
        return {"message": "Job application added successfully", "notion_page_id": response['id']}
    else:
        raise HTTPException(status_code=500, detail="Failed to add job application to Notion")
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
