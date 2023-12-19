from dataclasses import dataclass

from ..feature import EngineeredFeatures
from .rawfeatures import RawFeatures


@dataclass
class Project:
    # features go here
    raw: RawFeatures
    features: EngineeredFeatures | None = None

    @classmethod
    def create(cls, **kwargs):
        return cls(raw=RawFeatures.create(**kwargs))

