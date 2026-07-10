# DSA Problem Tracker API

A REST API built with FastAPI to track DSA problems during interview preparation.

## Features
- Add problems with topic, difficulty, status and personal notes
- Filter problems by topic, difficulty, or status
- Track revision progress — mark problems to revisit
- View stats — breakdown of solved/unsolved by topic

## Tech Stack
- Python
- FastAPI
- Pydantic

## Getting Started

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the server
```bash
fastapi dev main.py
```

### Access API docs
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /problems | Get all problems |
| GET | /problems/{id} | Get problem by id |
| GET | /problems/topic/{topic} | Filter by topic |
| GET | /problems/difficulty/{difficulty} | Filter by difficulty |
| GET | /problems/status/{status} | Filter by status |
| GET | /problems/stats | Get progress stats |
| POST | /problems | Add a new problem |
| PATCH | /problems/{id} | Update a problem |
| DELETE | /problems/{id} | Delete a problem |

## Topics Supported
arrays, hashing, two pointers, sliding window, binary search, 
linked list, trees, heaps, graphs, dp
