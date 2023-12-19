import json

from ...common.rawdata import RawData
from ...llama_chat.llama_cpp_chat_completion_wrapper import Llama2ChatCompletionWrapper


class Date:
    def __init__(self, raw_data: RawData,
                 llama_eval: Llama2ChatCompletionWrapper,
                 llama_json: Llama2ChatCompletionWrapper,
                 llama_params: dict):
        self.value = {
            'title_chars': len(raw_data.name),
        }

        res = llama_eval(f"""
        Here is a crowdfunding campaign title: '{raw_data.name}'.
        
        What is the length of the title in words? Does it seem snappy? Does it include a tagline?
        """, params=llama_params)

        formatted_res = llama_json(f"""
        Please format the following into json, and return the json only. The values should match that of the example
        format given, and if unsure, should occupy the string value 'null'.
        
        Example Format:
        {{
            "title_words": <number of words in the title>,
            "snappy": <bool>,
            "tagline@: <bool>
        }}
        
        Raw text:
        {res}
        
        Json:
        """, params=llama_params).replace('\n', '')

        if formatted_res[-1] != '}':
            formatted_res += '}'

        self.value.update(json.loads(formatted_res))
