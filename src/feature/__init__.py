from dataclasses import dataclass, fields
import typing
from collections import defaultdict

from ..common.rawdata import RawData
from .features import *
from ..llama_chat.llama_cpp_chat_completion_wrapper import Llama2ChatCompletionWrapper


@dataclass
class EngineeredFeatures:
    # engineered features go here
    title: Title
    category: Category

    @classmethod
    def create(cls,
               raw_data: RawData,
               llama_eval: Llama2ChatCompletionWrapper,
               llama_json: Llama2ChatCompletionWrapper,
               llama_params : dict = {
                            "temp": 0,
                            "top_p": 1,
                            "frequency_penalty": 0,
                            "presence_penalty": 0,
                            }  # i hereby solemnly swear not to change this mutable
               ):
        kwargs = {}
        for field in fields(cls):
            feature = field.type

            kwargs[field.name] = feature(raw_data, llama_eval, llama_json, llama_params)
        return cls(**kwargs)
