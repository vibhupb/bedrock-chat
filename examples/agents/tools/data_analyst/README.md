# Data Analyst Assistant Tool

## Overview

The Data Analyst Assistant tool is a custom tool designed to connect with external data analysis APIs to provide comprehensive data insights. This tool enables users to ask complex data analysis questions and receive detailed responses including market trends, sales data, regional analysis, and other data-driven insights.

## Features

- **Flexible Query Processing**: Accepts natural language prompts for data analysis
- **Configurable API Endpoint**: Supports custom API endpoints for different data sources
- **Comprehensive Error Handling**: Handles timeouts, connection errors, and API failures gracefully
- **Multiple Response Formats**: Supports both JSON and text responses from the API
- **Rich Metadata**: Returns structured data with source information and links

## Example Use Cases

### Gaming Industry Analysis
- "What were the best selling games in the last 10 years and why?"
- "Analyze market trends for mobile gaming in 2024"
- "Show me sales data by region for action games"
- "Compare publisher performance across different genres"

### Market Research
- "Analyze gaming revenue trends by platform"
- "What genres are performing best in specific regions?"
- "Identify emerging trends in the gaming industry"

## API Integration

The tool is designed to work with the data analysis API:
```
POST http://CdkStr-Agent-DuMCKmPGRCa3-1106354629.us-east-1.elb.amazonaws.com/assistant-streaming
Content-Type: application/json

{
  "prompt": "Your data analysis question here"
}
```

## How to Enable This Tool

1. **Move the implementation file**: Move `data_analyst.py` to the `backend/app/agents/tools` directory.

2. **Update the imports**: In the moved file, uncomment the import statements and AgentTool instantiation:

```python
from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name

# ... (implementation code) ...

data_analyst_tool = AgentTool(
    name="analyze_data",
    description="Analyze data using an external data analysis API...",
    args_schema=DataAnalystInput,
    function=analyze_data,
)
```

3. **Register the tool**: Open `backend/app/agents/utils.py` and modify it:

```python
from app.agents.langchain import BedrockLLM
from app.agents.tools.base import BaseTool
from app.agents.tools.internet_search import internet_search_tool
+ from app.agents.tools.data_analyst import data_analyst_tool


def get_available_tools() -> list[BaseTool]:
    tools: list[BaseTool] = []
    tools.append(internet_search_tool)
+   tools.append(data_analyst_tool)

    return tools
```

4. **Deploy the changes**: Run `npx cdk deploy` to deploy your changes.

## Testing

Before deploying, you can test the tool functionality using the provided test script:

```bash
cd examples/agents/tools/data_analyst
python test_data_analyst.py
```

The test suite includes:
- Successful API responses (JSON and text)
- Error handling (API errors, timeouts, connection issues)
- Input validation
- Mock testing to avoid actual API calls during development

## Configuration

### Required Dependencies

The tool requires the `requests` library. If not already installed in your backend environment, add it to your requirements:

```
requests>=2.25.0
```

### Environment Considerations

- **Timeout**: The tool has a 30-second timeout for API requests
- **Error Handling**: Comprehensive error handling for network issues and API failures
- **Security**: Consider implementing authentication if required by your API endpoint

## Response Format

The tool returns structured data including:

- **status**: "success" or "error"
- **analysis**: The actual analysis results from the API
- **source_name**: "Data Analyst Assistant"
- **source_link**: The API endpoint used
- **content**: Formatted content for display in the chat interface

## Customization

You can customize the tool by:

1. **Changing the default API endpoint**: Modify the default value in `DataAnalystInput.api_endpoint`
2. **Adding authentication**: Extend the `analyze_data` function to include API keys or tokens
3. **Enhancing response processing**: Modify the response handling logic for specific API response formats
4. **Adding caching**: Implement response caching for frequently asked questions

## Security Considerations

- Validate API endpoints to prevent SSRF attacks
- Implement rate limiting if needed
- Consider adding authentication for production use
- Monitor API usage and costs

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the file is in the correct directory (`backend/app/agents/tools/`)
2. **API Connection**: Verify the API endpoint is accessible and running
3. **Timeout Issues**: Adjust the timeout value if needed for slower APIs
4. **Response Format**: Check that the API returns the expected response format

### Debug Mode

For debugging, you can add logging to the `analyze_data` function:

```python
import logging

def analyze_data(arg: DataAnalystInput, bot=None, model=None) -> dict:
    logging.info(f"Making request to: {arg.api_endpoint}")
    logging.info(f"Prompt: {arg.prompt}")
    # ... rest of the function
```
