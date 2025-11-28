from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi import FastAPI

app = FastAPI(title="ServiceNow Chatbot Integration")

@app.get("/health")
def health_check():
    return {"status": "ok"}



import json
from pathlib import Path

# Load KB articles
KB_FILE = Path("data/kb_articles.json")
with open(KB_FILE, "r") as f:
    kb_articles = json.load(f)

@app.get("/kb/search")
def search_kb(query: str):
    """
    Search KB articles (mock) by checking if query is in title or content.
    """
    results = []
    for article in kb_articles:
        if query.lower() in article["title"].lower() or query.lower() in article["content"].lower():
            results.append(article)
    if results:
        return {"results": results}
    else:
        return {"results": [], "message": "No KB articles found"}


# Load incidents
INC_FILE = Path("data/incidents.json")
with open(INC_FILE, "r") as f:
    incidents = json.load(f)

@app.get("/incidents/search")
def search_incidents(query: str):
    """
    Search past incidents (mock) by checking if query is in short_description.
    """
    results = []
    for incident in incidents:
        if query.lower() in incident["short_description"].lower():
            results.append(incident)
    if results:
        return {"results": results}
    else:
        return {"results": [], "message": "No incidents found"}

from fastapi import Body
import uuid

@app.post("/incidents/create")
def create_incident(short_description: str = Body(...), details: str = Body(...)):
    """
    Create a new incident (mock) and add to incidents.json
    """
    new_incident = {
        "id": f"INC{str(uuid.uuid4())[:6].upper()}",
        "short_description": short_description,
        "resolution": details
    }
    incidents.append(new_incident)
    
    # Save back to JSON (mock persistence)
    with open(INC_FILE, "w") as f:
        json.dump(incidents, f, indent=4)
    
    return {"message": "Incident created", "incident": new_incident}


from fastapi import Body

@app.post("/chatbot/query")
def chatbot_query(query: str = Body(...)):
    """
    Main chatbot endpoint:
    - Search KB
    - Search past incidents
    - Create a new ticket if nothing found
    """
    # 1. Search KB
    kb_results = []
    for article in kb_articles:
        if query.lower() in article["title"].lower() or query.lower() in article["content"].lower():
            kb_results.append(article)
    
    if kb_results:
        return {"source": "kb", "results": kb_results}

    # 2. Search past incidents
    incident_results = []
    for incident in incidents:
        if query.lower() in incident["short_description"].lower():
            incident_results.append(incident)
    
    if incident_results:
        return {"source": "incident", "results": incident_results}

    # 3. Create new ticket
    new_incident = {
        "id": f"INC{str(uuid.uuid4())[:6].upper()}",
        "short_description": query,
        "resolution": "Ticket created for investigation"
    }
    incidents.append(new_incident)
    with open(INC_FILE, "w") as f:
        json.dump(incidents, f, indent=4)

    return {"source": "new_ticket", "incident": new_incident}
