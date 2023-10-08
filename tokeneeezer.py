from transformers import GPT2Tokenizer, AutoTokenizer
import re


class Tokeeenizer:
    def __init__(self, model_name='DeepPavlov/rubert-base-cased', e_char='E'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.e_char = e_char

    def tokenize(self, text):
        data = self.tokenizer.encode(text, return_tensors="pt").tolist()[0]
        data = list(filter(lambda x: x != self.tokenizer.sep_token_id and x != self.tokenizer.cls_token_id, data))
        return data

    def detokenize(self, token_ids):
        return self.tokenizer.decode(token_ids)

    def number_to_string(self, number):
        digits = [int(digit) for digit in str(number)]
        return '-'.join([self.e_char * (digit + 1) for digit in digits])

    def string_to_number(self, string):
        substrings = string.split('-')
        number = int(''.join([str(len(substring) - 1) for substring in substrings]))
        return number

    def encode_text(self, text):
        paragraphs = text.split("\n")
        tokens_paragraphs = [self.tokenize(text) for text in paragraphs]
        return '\n'.join([
            ' '.join([self.number_to_string(token) for token in tokens])
            for tokens in tokens_paragraphs
            ])

    def decode_text(self, encoded_text):
        # Проверка на наличие недопустимых символов
        if not re.match(f"^[{self.e_char}\- \n]*$", encoded_text):
            raise ValueError("Encoded text contains invalid characters")
        
        paragraphs = encoded_text.split('\n')
        paragraphs = [paragraph.split(' ') for paragraph in paragraphs]
        tokens_paragraphs = [
            [self.string_to_number(token_string) for token_string in tokens_strings if token_string]
            for tokens_strings in paragraphs
            ]
        
        return "\n".join([self.detokenize(tokens) for tokens in tokens_paragraphs])
        