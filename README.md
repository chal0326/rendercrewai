# CrewAI API Wrapper

A FastAPI application that serves as an API wrapper for the CrewAI framework, designed for deployment on Render.com and integration with N8N.

## Overview

This application provides a RESTful API endpoint that allows external services like N8N to trigger CrewAI workflows. It handles the asynchronous execution of CrewAI crews and returns the results in a standardized format.

## Features

- FastAPI REST API with Pydantic validation
- Asynchronous CrewAI execution
- Environment variable configuration
- Ready for deployment on Render.com
- Placeholder CrewAI definitions for easy customization

## Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- CrewAI
- OpenAI Python SDK
- Python-dotenv (for local development)

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your API keys:
   ```
   cp .env.example .env
   ```
4. Start the server:
   ```
   uvicorn main:app --reload
   ```

## Usage

Send a POST request to `/trigger-crew` with a JSON body containing:

```json
{
  "topic": "Your research topic",
  "additional_context": {
    "optional_key": "optional_value"
  }
}
```

Example response:

```json
{
  "result": "Detailed research findings...",
  "execution_time": 12.34
}
```

## Customizing CrewAI Logic

Modify the `crew_definitions.py` file to customize:

1. Agent definitions (roles, goals, backstories)
2. Task definitions (descriptions, expected outputs)
3. Crew assembly and execution process

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your repository
3. Set the build command to: `pip install -r requirements.txt`
4. Set the start command to: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add your environment variables (OPENAI_API_KEY, etc.)

## N8N Integration

In N8N, create an HTTP Request node with:

- Method: POST
- URL: Your Render deployment URL + `/trigger-crew`
- Body: JSON data with your topic and any additional context

## License

[MIT License](LICENSE)