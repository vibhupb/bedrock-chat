import requests
import json
from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, Field


class DataAnalystInput(BaseModel):
    prompt: str = Field(
        description="The data analysis question or query you want to ask. "
                   "Examples: 'What is current stock price for provided company in prompt?', "
                   "'Analyze market trends for banking and financial sector in general', "
                   "'Analyze 10-Q and 10-K filing for provided company in prompt'"
    )
    api_endpoint: str = Field(
        
        default="http://***********", 
        description="The API endpoint for data analysis (optional, uses default if not provided)"
    )


def analyze_data(
    arg: DataAnalystInput, bot: BotModel | None, model: type_model_name | None
) -> dict:
    """
    Sends a data analysis request to the specified API endpoint and returns the response.
    
    Args:
        arg: DataAnalystInput containing the prompt and optional API endpoint
        bot: Bot model (unused in this implementation)
        model: Model name (unused in this implementation)
        
    Returns:
        dict: Analysis results from the API or error information
    """
    try:
        # Prepare the request payload
        payload = {
            "prompt": arg.prompt
        }
        
        # Set up headers
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Make the API request
        response = requests.post(
            arg.api_endpoint,
            headers=headers,
            data=json.dumps(payload),
            timeout=600  # 600 second timeout
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Try to parse as JSON first
            try:
                response_data = response.json()
                return {
                    "status": "success",
                    "analysis": response_data,
                    "source_name": "Data Analyst Assistant",
                    "source_link": arg.api_endpoint,
                    "content": f"Data Analysis Results for: '{arg.prompt}'\n\n{json.dumps(response_data, indent=2)}"
                }
            except (json.JSONDecodeError, ValueError, Exception):
                # If not JSON, return as text
                response_text = response.text
                return {
                    "status": "success", 
                    "analysis": response_text,
                    "source_name": "Data Analyst Assistant",
                    "source_link": arg.api_endpoint,
                    "content": f"Data Analysis Results for: '{arg.prompt}'\n\n{response_text}"
                }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status code {response.status_code}",
                "details": response.text,
                "source_name": "Data Analyst Assistant",
                "content": f"Error analyzing data: API returned status {response.status_code}"
            }
            
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": "Request timeout",
            "details": "The API request took too long to respond (>600 seconds)",
            "source_name": "Data Analyst Assistant",
            "content": "Error: Request timeout while analyzing data"
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "error": "Connection error",
            "details": f"Could not connect to the API endpoint: {arg.api_endpoint}",
            "source_name": "Data Analyst Assistant", 
            "content": "Error: Could not connect to the data analysis API"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": "Unexpected error",
            "details": str(e),
            "source_name": "Data Analyst Assistant",
            "content": f"Unexpected error during data analysis: {str(e)}"
        }


data_analyst_tool = AgentTool(
    name="analyze_data",
    description="Analyze data using an external data analysis API. This tool can answer questions about current financial news received from Yahoo Finance, CNBC, Federal Reserve, White House, WSJ etc., data, market trends, regional analysis, genre performance, and other data-driven insights. Perfect for queries about banking and financial sector news, market analysis, sales trends, and comparative data analysis.",
    args_schema=DataAnalystInput,
    function=analyze_data,
)
