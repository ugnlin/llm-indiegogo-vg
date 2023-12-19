from ...common.rawfeatures import RawFeatures


class Title:
    def __init__(self, raw_data: RawFeatures):
        self.value = {
            'title_chars': len(raw_data.name),
        }
        llama(raw_data.name)