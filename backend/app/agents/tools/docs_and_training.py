import requests
import json
from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from pydantic import BaseModel, Field

class DocsAndTrainingInput(BaseModel):
    prompt: str = Field(
        description="*************************'"
    )
    api_endpoint: str = Field(
        default="*****************************",
        description="The API endpoint for docs and training (optional, uses default if not provided)"
    )

def docs_and_training(
    arg: DocsAndTrainingInput, bot: BotModel | None, model: type_model_name | None
) -> dict:
    try:
        payload = {"prompt": arg.prompt}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            arg.api_endpoint,
            headers=headers,
            data=json.dumps(payload),
            timeout=90
        )
        if response.status_code == 200:
            try:
                response_data = response.json()
                return {
                    "status": "success",
                    "answer": response_data,
                    "source_name": "Docs and Training",
                    "source_link": arg.api_endpoint,
                    "content": f"Docs/Training Answer for: '{arg.prompt}'\n\n{json.dumps(response_data, indent=2)}"
                }
            except (json.JSONDecodeError, ValueError, Exception):
                response_text = response.text
                return {
                    "status": "success",
                    "answer": response_text,
                    "source_name": "Docs and Training",
                    "source_link": arg.api_endpoint,
                    "content": f"Docs/Training Answer for: '{arg.prompt}'\n\n{response_text}"
                }
        else:
            return {
                "status": "error",
                "error": f"API request failed with status code {response.status_code}",
                "details": response.text,
                "source_name": "Docs and Training",
                "content": f"Error: API returned status {response.status_code}"
            }
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": "Request timeout",
            "details": "The API request took too long to respond (>30 seconds)",
            "source_name": "Docs and Training",
            "content": "Error: Request timeout while fetching docs/training answer"
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "error": "Connection error",
            "details": f"Could not connect to the API endpoint: {arg.api_endpoint}",
            "source_name": "Docs and Training",
            "content": "Error: Could not connect to the docs/training API"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": "Unexpected error",
            "details": str(e),
            "source_name": "Docs and Training",
            "content": f"Unexpected error during docs/training query: {str(e)}"
        }

docs_and_training_tool = AgentTool(
    name="docs_and_training",
    description="Answer questions about documentation, training, and technical concepts using an external API.",
    args_schema=DocsAndTrainingInput,
    function=docs_and_training,
)
