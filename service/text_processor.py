from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from config.settings import EN_TO_ZH_MODEL_PATH


class TextProcessor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(EN_TO_ZH_MODEL_PATH)

        self.model = AutoModelForSeq2SeqLM.from_pretrained(EN_TO_ZH_MODEL_PATH)

    def translate(self, text):
        translation = pipeline("translation_en_to_zh", model=self.model, tokenizer=self.tokenizer)
        result = translation(text)[0]['translation_text']

        return result

