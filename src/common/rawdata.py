from datetime import datetime
from dataclasses import dataclass

@dataclass
class RawData:
    project_id: int
    name: str
    description: str
    faqs: list
    ended: bool
    open_date: datetime
    close_date: datetime
    goal: float
    raised: float
    currency: str

    @classmethod
    def create(cls, **kwargs):
        try:
            kwargs['open_date'] = datetime.fromisoformat(kwargs.pop('open_date'))
            kwargs['close_date'] = datetime.fromisoformat(kwargs.pop('close_date'))
            kwargs['ended'] = True if datetime.now(kwargs['close_date'].tzinfo) > kwargs['close_date'] else False
            kwargs['goal'] = kwargs['raised'] / kwargs.pop('raised_percent')
            return cls(**kwargs)
        except:
            raise RuntimeError('unhandled data exception')
