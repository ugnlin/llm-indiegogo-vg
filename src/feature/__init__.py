from dataclasses import dataclass, fields
import typing

from ..common.rawfeatures import RawFeatures


@dataclass
class EngineeredFeatures:
    # engineered features go here
    a: int

    @classmethod
    def create(cls, raw_data: RawFeatures):
        kwargs = {}
        for field in fields(cls):
            feature = field.type

            kwargs[field.name] = feature(raw_data)
        return cls(**kwargs)
