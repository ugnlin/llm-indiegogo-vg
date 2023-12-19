from ...common.rawfeatures import RawFeatures


class Title:
    def __init__(self, raw_data: RawFeatures):
        self.value = {
            'title_chars': len(raw_data.name),
        }

        res = llama(f"""
        Here is a crowdfunding campaign title: '{raw_data.name}'.
        
        What is the length of the title in words? Does it seem snappy? Does it include a tagline?
        """)

        formatted_res = llama(f"""
        Please format the following into json, and return the json only. The values should match that of the example
        format given, and if unsure, should occupy the string value 'null'.
        
        Format:
        {{
            'title_words': <number of words in the title>,
            'snappy': <bool>,
            'tagline: <bool>,
        }}
        
        Raw text:
        {res}
        
        Json:
        """)

        self.value.update(formatted_res)
