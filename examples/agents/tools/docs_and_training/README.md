# Docs and Training Tool

This agent tool answers questions about documentation, training, and technical concepts using an external API.

- **API Endpoint:** `http://multi-mcp-alb-816647011.us-east-1.elb.amazonaws.com/strands-agent`
- **Usage:** Pass a prompt/question to the tool, and it returns an answer from the API.

## Example

```
POST http://multi-mcp-alb-816647011.us-east-1.elb.amazonaws.com/strands-agent
Content-Type: application/json

{
  "prompt": "What is AWS CDK?"
}
```
