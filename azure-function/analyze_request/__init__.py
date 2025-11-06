import logging
import json
import azure.functions as func
import os
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Analyzes IT asset requests using Azure AI Foundry (Azure OpenAI) to determine category and priority.
    
    This function is called by Power Automate via a custom connector whenever a new
    asset request is created in Dataverse. It uses GPT-4 to intelligently categorize
    the request and assign an urgency level.
    """
    logging.info('Processing IT asset request analysis.')

    # Validate environment variables - these should be set in Azure Function configuration
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_KEY")
    model = os.getenv("AZURE_OPENAI_MODEL")
    
    if not endpoint or not api_key or not model:
        logging.error("Azure AI Foundry configuration missing.")
        return func.HttpResponse(
            "Missing Azure AI Foundry configuration.",
            status_code=500,
            headers={"Access-Control-Allow-Origin": "*"}
        )

    try:
        req_body = req.get_json()
        request_text = req_body.get('requestText')
        
        if not request_text or not isinstance(request_text, str):
            logging.warning("Invalid request body received.")
            return func.HttpResponse(
                json.dumps({"error": "Please provide requestText (string) in the request body."}),
                mimetype="application/json",
                status_code=400,
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # Initialize Azure OpenAI client (works with Azure AI Foundry deployments)
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_version="2023-05-15",
            api_key=api_key
        )

        # Construct prompt with clear instructions for consistent output
        prompt = (
            "Analyze the following IT request. Return a JSON object with two keys: "
            "'category' (must be exactly one of: 'Hardware', 'Software', 'Access', 'Network', 'Other') "
            "and 'priority' (a number from 1 to 5, where 5 is highest urgency).\n"
            f"Request: {request_text}"
        )

        # Call Azure AI Foundry (Azure OpenAI) for intelligent analysis
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an IT request analyzer."},
                {"role": "user", "content": prompt}
            ]
        )

        # Parse and validate the AI response
        try:
            analysis = json.loads(response.choices[0].message.content)
            
            # Ensure the response matches our expected schema
            valid_categories = {"Hardware", "Software", "Access", "Network", "Other"}
            if (
                "category" not in analysis or
                analysis["category"] not in valid_categories or
                "priority" not in analysis or
                not isinstance(analysis["priority"], int) or
                not (1 <= analysis["priority"] <= 5)
            ):
                raise ValueError("Invalid AI response format.")
                
        except Exception as e:
            logging.error(f"AI response parsing error: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": "AI response parsing error."}),
                mimetype="application/json",
                status_code=500,
                headers={"Access-Control-Allow-Origin": "*"}
            )

        return func.HttpResponse(
            json.dumps(analysis),
            mimetype="application/json",
            status_code=200,
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Error processing request: {str(e)}"}),
            mimetype="application/json",
            status_code=500,
            headers={"Access-Control-Allow-Origin": "*"}
        )
