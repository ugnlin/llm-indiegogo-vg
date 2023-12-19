import os
from dataclasses import dataclass

from ..feature import EngineeredFeatures
from .rawdata import RawData
from ..llama_chat.llama_cpp_chat_completion_wrapper import Llama2ChatCompletionWrapper
from ..llama_chat.tokenizer import Tokenizer


@dataclass
class Project:
    # features go here
    raw: RawData
    features: EngineeredFeatures | None = None

    @classmethod
    def create(cls, **kwargs):
        return cls(raw=RawData.create(**kwargs))

    @classmethod
    def load_raw(cls, **kwargs):
        return cls(raw=RawData(**kwargs))

    def generate_features(self):
        llama_eval = Llama2ChatCompletionWrapper(
            model_path=os.environ['model_path'],
            tokenizer_encoder=Tokenizer(model_path=os.environ['tokenizer_path']).encode,
        )
        llama_eval.new_session("""You are an analyst who specialises in video game crowdfunding campaigns.
        You will answer questions directly, corresponding to the options provided to you, and not deviating from the point 
        or the request, succinctly and without extra detail. You are confident in your answers, and do not give reasoning for your answers. 
        You do not introduce yourself, you do not summarise your answers, and do not chat outside the bounds of fulfilling the request.""")

        llama_json = Llama2ChatCompletionWrapper(
            model_path=os.environ['model_path'],
            tokenizer_encoder=Tokenizer(model_path=os.environ['tokenizer_path']).encode,
        )
        llama_json.new_session("""You are an assistant who summaries info into jsons. You will return only the json
    in the format as prompted with nothing else. You will not, under any circumstances, change the format of the json.
    You do not give introductions or summaries, 
    and do not chat outside the bounds of fulfilling the request, 
    answering and stopping straight away with no extra notes, introductions, or thanks.""")

        self.features = EngineeredFeatures.create(
            raw_data=self.raw,
            llama_eval=llama_eval,
            llama_json=llama_json,
        )