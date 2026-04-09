from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str
    redis_url: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str = "telemer-recordings"
    rabbitmq_url: str
    asr_url: str
    nlu_url: str
    tts_url: str
    sentiment_url: str
    llm_url: str
    llm_model: str = "tinyllama"
    fs_esl_host: str = "freeswitch"
    fs_esl_port: int = 8021
    fs_esl_password: str = "ClueCon"
    public_base_url: str = "http://localhost:8000"
    whatsapp_enabled: bool = False
    waba_provider: str = "whatsapp-web.js"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

settings = Settings()
