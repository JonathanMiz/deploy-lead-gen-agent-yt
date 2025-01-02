import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings
import logging
import boto3
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('chromadb').setLevel(logging.WARNING)

load_dotenv()


def get_aws_secrets() -> Dict[str, Any]:
    """Fetch secrets from AWS Secrets Manager"""
    if os.getenv('IS_PROD', 'false').lower() == 'true':
        path: str = '/lead-gen-agent-yt'
        region: str = os.getenv("AWS_REGION")
        ssm = boto3.client('ssm', region_name=region)
        parameters = {}
        next_token = None

        while True:
            kwargs = {
                'Path': path,
                'Recursive': True,
                'WithDecryption': True
            }
            if next_token:
                kwargs['NextToken'] = next_token

            response = ssm.get_parameters_by_path(**kwargs)
            for param in response['Parameters']:
                simplified_name = param['Name'].replace(path, '').lstrip('/')
                parameters[simplified_name] = param['Value']
                os.environ[simplified_name] = param['Value']

            next_token = response.get('NextToken')
            if not next_token:
                break

        return parameters
    return {}


class Settings(BaseSettings):
    PORT: int = 3030
    IS_DOCKER: bool = False
    IS_PROD: bool = False
    AWS_REGION: str
    OPENAI_API_KEY: str
    AIRTABLE_API_KEY: str
    AIRTABLE_BASE_ID: str
    RESOURCES_PATH: str = "resources"
    DOCUMENTS_PATH: str = os.path.join(RESOURCES_PATH, "docs")
    CHROMA_PATH: str = os.path.join(RESOURCES_PATH, "chroma")

    class Config:
        @staticmethod
        def customise_sources(init_settings, env_settings, file_secret_settings):
            def ssm_settings_source(_: BaseSettings) -> Dict[str, Any]:
                return get_aws_secrets()
            return ssm_settings_source, init_settings, env_settings, file_secret_settings


settings = Settings()