from dataclasses import dataclass

from . import mlfeatures
from . import rawfeatures


@dataclass
class Project:
    # features go here
    raw: rawfeatures.RawFeatures
    features: mlfeatures.EngineeredFeatures


