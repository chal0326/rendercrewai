import os
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio

# Import CrewAI related functions
from crew_definitions import create_musical_theater_crew

# Load environment variables from .env file for local development
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Musical Theater CrewAI API",
    description="API wrapper for Musical Theater CrewAI framework",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if required environment variables are set
def verify_api_keys():
    required_keys = ["OPENAI_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        error_msg = f"Missing required environment variables: {', '.join(missing_keys)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    
    return True

# Request model
class CrewRequest(BaseModel):
    production_name: str = Field(..., description="The name of the musical theater production")
    additional_context: Dict[str, Any] = Field(
        default={}, description="Optional additional context for the production"
    )

# Response model
class CrewResponse(BaseModel):
    result: str = Field(..., description="The result from CrewAI execution")
    execution_time: float = Field(..., description="Execution time in seconds")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Musical Theater CrewAI API is running"}

@app.post("/trigger-crew", response_model=CrewResponse)
async def trigger_crew(request: CrewRequest, api_keys: bool = Depends(verify_api_keys)):
    """
    Trigger a Musical Theater CrewAI process
    
    This endpoint accepts a production name and additional context, then:
    1. Creates a musical theater crew with the appropriate agents and tasks
    2. Executes the crew asynchronously
    3. Returns the result
    """
    try:
        logger.info(f"Received request for production: {request.production_name}")
        
        # Create the musical theater crew
        crew = create_musical_theater_crew(request.production_name)
        
        # Start timing the execution
        start_time = asyncio.get_event_loop().time()
        
        # Execute the crew asynchronously and wait for the result
        inputs = {"production_name": request.production_name, **request.additional_context}
        result = await crew.kickoff_async(inputs=inputs)
        
        # Calculate execution time
        execution_time = asyncio.get_event_loop().time() - start_time
        logger.info(f"CrewAI execution completed in {execution_time:.2f} seconds")
        
        return CrewResponse(result=result, execution_time=execution_time)
    
    except Exception as e:
        logger.error(f"Error during CrewAI execution: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during CrewAI execution: {str(e)}",
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)