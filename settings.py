import os
from uuid import uuid4
from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """Workflow config"""

    # Run
    DEPLOY: str = os.environ.get("DEPLOY", "local")
    RUN_ID: str = os.environ.get("RUN_ID", str(uuid4()))

    # AWS
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID", "dummy-key-id")
    AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY", "dummy-key")

    # Minio
    BUCKET: str = os.environ.get("BUCKET", "dev-midas-news-scoring")

    # NewsAPI
    NEWS_KEYWORDS: str = os.environ.get("NEWS_KEYWORDS", "petrobras")
    NEWS_API_KEY: str = os.environ.get("NEWS_API_KEY", "dummy-key")

    # OpenAI
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "dummy-key")

    # Prompt
    MODEL_CONTEXT: str = f"""
    Preciso que você faça uma tarefa. É o seguinte, eu vou te dar um texto que é uma notícia sobre a empresa {NEWS_KEYWORDS}. Aí você vai me dizer se essa notícia é favorável ou não para aquela empresa. Vamos utilizar suas conclusões pra criar uma espécie de score para determinar se vale a pena ou não (ou se é o momento certo) para investir em determinada ação.
    Avalie a notícia e dê um score de 0 a 10 onde o score 0 seria algo como "a empresa vai falir amanhã" e o score 10 "o valor da ação vai subir 500% amanhã"
    O score da notícia deve estar especificado em um novo parágrafo no final da resposta no formato a seguir: "Score": "5"
    """
    NEWS_PROMPT_TEMPLATE: str = """
    Aqui está a notícia: {news_content}
    """

    # Twilio
    TWILIO_SID: str = os.environ.get("TWILIO_SID", "dummy-sid")
    TWILIO_TOKEN: str = os.environ.get("TWILIO_TOKEN", "dummy-token")
    TO_NUMBER: str = os.environ.get("TO_NUMBER", "123456789")
    FROM_NUMBER: str = os.environ.get("FROM_NUMBER", "123456789")

    # General
    REQUESTS_TIMEOUT: int = 5  # seconds
    LOGGER: str = "LOGGER"
