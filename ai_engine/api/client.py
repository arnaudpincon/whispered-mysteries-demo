from openai import AzureOpenAI


def create_azure_client(api_key, endpoint, api_version):
    """Create and configure the Azure OpenAI client"""
    return AzureOpenAI(
        api_key=api_key, api_version=api_version, azure_endpoint=endpoint
    )
