# ServiceNow Chatbot Integration 

## Overview
This project demonstrates a **ServiceNow chatbot integration** using Python FastAPI.  
The chatbot helps users resolve IT issues efficiently by:

1. Searching Knowledge Base (KB) articles.
2. Searching past incidents.
3. Creating a new incident if no solution is found.

All ServiceNow data is **using JSON files**, so no real ServiceNow account is required.

---

## Features
- FastAPI backend with REST endpoints.
- Mock ServiceNow KB (`kb_articles.json`) and incidents (`incidents.json`).
- Combined chatbot endpoint `/chatbot/query`.
- Minimal frontend (`index.html`) to interact with the bot (optional).
- Fully testable locally and GitHub-ready.

---


