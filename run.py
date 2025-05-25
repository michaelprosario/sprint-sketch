#!/usr/bin/env python
# filepath: /workspaces/sprint-sketch/run.py

"""
Script to run the Blog application
"""

import uvicorn

if __name__ == "__main__":
    print("Starting Blog API...")
    print("Access the API documentation at http://localhost:8000/docs")
    print("Access the API at http://localhost:8000")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
