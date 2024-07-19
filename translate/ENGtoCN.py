from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline


class Translate:
    """
    加载翻译模型
    """

    def __init__(self):
        self.model_path = '../ENGtoCN/'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)
        self.pipeline = pipeline("translation", model=self.model, tokenizer=self.tokenizer)

