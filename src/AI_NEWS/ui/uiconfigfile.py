from configparser import ConfigParser
from pathlib import Path


class Config:
    def __init__(self):
        self.config = ConfigParser()

        config_path = Path(__file__).parent / "uiconfigfile.ini"

        self.config.read(config_path)

    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS")

    def get_usecase_options(self):
        return self.config["DEFAULT"].get("USECASE_OPTIONS")

    def get_groq_model_options(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(",")

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")