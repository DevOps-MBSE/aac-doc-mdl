"""The AaC Document Model plugin AI utility implementation."""

import os
import httpx
from openai import (OpenAI, AzureOpenAI)

from aac.execute.aac_execution_result import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionMessage,
    MessageLevel,
)


def get_client(plugin_name: str):
    """Get the client for the AI model."""

    # returns client, model, error_bool, execution_result_if_error
    aac_ai_url = os.getenv("AAC_AI_URL")
    aac_ai_model = os.getenv("AAC_AI_MODEL")
    aac_ai_key = os.getenv("AAC_AI_KEY")
    aac_ai_type = os.getenv("AAC_AI_TYPE")
    aac_ai_api_version = os.getenv("AAC_AI_API_VERSION")

    aac_http_proxy = os.getenv("AAC_HTTP_PROXY")
    aac_https_proxy = os.getenv("AAC_HTTPS_PROXY")
    aac_ssl_verify = os.getenv("AAC_SSL_VERIFY")

    if (aac_ssl_verify is None or aac_ssl_verify == "" or aac_ssl_verify.lower() != "false"):
        aac_ssl_verify = True
    else:
        aac_ssl_verify = False

    use_az = False
    if aac_ai_type is not None and aac_ai_type.lower() == "azure":
        use_az = True
        if aac_ai_api_version is None or aac_ai_api_version == "":
            return None, None, True, ExecutionResult(
                plugin_name,
                "Shall statement quality",
                ExecutionStatus.GENERAL_FAILURE,
                [
                    ExecutionMessage(
                        "The AAC_AI_Type is Azure but AAC_AI_API_VERSION is not set. Must provide both environment variables to use Azure AI.",
                        MessageLevel.ERROR,
                        None,
                        None,
                    )
                ],
            )

    if ((aac_ai_url is None or aac_ai_url == "")
            or (aac_ai_model is None or aac_ai_model == "")
            or (aac_ai_key is None or aac_ai_key == "")):
        return None, None, True, ExecutionResult(
            plugin_name,
            "Shall statement quality",
            ExecutionStatus.CONSTRAINT_WARNING,
            [
                ExecutionMessage(
                    "The AAC_AI_URL, AAC_AI_MODEL, or AAC_AI_KEY environment variable is not set. Unable to evaluate the Shall statement quality constraint.",
                    MessageLevel.WARNING,
                    None,
                    None,
                )
            ],
        )

    if not aac_ssl_verify:
        print("WARNING: SSL verification is disabled.")

    if ((aac_http_proxy is not None and len(aac_http_proxy) > 0)
            or (aac_https_proxy is not None and len(aac_https_proxy) > 0)):

        # return client with proxy configuration
        print("INFO: Using proxy configuration.")
        proxies = {'http://': aac_http_proxy, 'https://': aac_https_proxy}
        http_client = httpx.Client(proxies=proxies, verify=aac_ssl_verify)
        if use_az:
            return AzureOpenAI(
                azure_endpoint=aac_ai_url,
                api_key=aac_ai_key,
                api_version=aac_ai_api_version,
                http_client=http_client), aac_ai_model, False, None
        else:
            return OpenAI(base_url=aac_ai_url, api_key=aac_ai_key, http_client=http_client), aac_ai_model, False, None

    # return client without proxy configuration
    if use_az:
        return AzureOpenAI(
            azure_endpoint=aac_ai_url,
            api_key=aac_ai_key,
            api_version=aac_ai_api_version), aac_ai_model, False, None
    else:
        return OpenAI(base_url=aac_ai_url, api_key=aac_ai_key), aac_ai_model, False, None


def generate(client, model, temp, prompt):
    """
    Generate AI response based on the given prompt.

    Args:
        client: The client for the AI model.
        model: The AI model to use for generating the response.
        temp:  The Gen AI temperature parameter to control variability (0-1) with lower values being less 'creative'.
        prompt: The input prompt for generating the response.

    Returns:
        The generated AI response.
    """
    response = "AI response goes here"
    r = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        temperature=temp,
    )
    response = r.choices[0].message.content
    return response
