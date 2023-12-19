import json

from ...common.rawdata import RawData
from ...llama_chat.llama_cpp_chat_completion_wrapper import Llama2ChatCompletionWrapper


class Category:
    def __init__(self, raw_data: RawData,
                 llama_eval: Llama2ChatCompletionWrapper,
                 llama_json: Llama2ChatCompletionWrapper,
                 llama_params: dict):
        self.value = {}

        res = llama_eval(f"""
        Here is info about a crowdfunding campaign: 

        Description:
        '{raw_data.name}'.

        FAQs:
        '{raw_data.faqs}'
        
        From the following types of projects, what kind of project is this? 
        [Game Software , Game Hardware , Physical Game , Event , Other]
        
        If it is a game, what kind of genres is it?
        [Action, Board Game, Adventure, Card Game, Gacha Game, Horror, Puzzle, Role-playing, Fighting,
        Simulation, Strategy, Sports, Survival, MMO, Non-Game, Adult, VR, Other]
        
        If it is a game, what platforms does it come out on?
        [PC, Playstation, Xbox, Switch, Mobile, Other]
        
        How many platforms does it come out on?
        
        Does the game have a singleplayer mode? Does it have a multiplayer mode?
        
        Is the game developed by a single developer?
        
        """, params=llama_params)

        formatted_res = llama_json(f"""
        Please format the following into json, and return the json only. The values should match that of the example
        format given, and if unsure, should occupy the bool value False'.

        Example Format:
        {{
            "project_type_software": <bool>,
            "project_type_hardware": <bool>,
            "project_type_physical": <bool>,
            "project_type_event": <bool>,
            "project_type_other": <bool>,
            "game_genre_action": <bool>,
            "game_genre_board": <bool>,
            "game_genre_adventure": <bool>,
            "game_genre_card": <bool>,
            "game_genre_gacha": <bool>,
            "game_genre_horror": <bool>,
            "game_genre_puzzle": <bool>,
            "game_genre_rpg": <bool>,
            "game_genre_sim": <bool>,
            "game_genre_strategy": <bool>,
            "game_genre_sports": <bool>,
            "game_genre_survival": <bool>,
            "game_genre_mmo": <bool>,
            "game_genre_adult": <bool>,
            "game_genre_vr": <bool>,
            "game_platform_pc": <bool>,
            "game_platform_playstation": <bool>,
            "game_platform_xbox": <bool>,
            "game_platform_switch": <bool>,
            "game_platform_mobile": <bool>,
            "game_platform_other": <bool>,
            "number_of_platforms": <bool>,
            "singleplayer": <bool>
            "multiplayer": <bool>,
            "solo_developer: <bool>
        }}

        Raw text:
        {res}

        Json:
        """, params=llama_params).replace('\n', '')

        if formatted_res[-1] != '}':
            formatted_res += '}'

        if formatted_res[-2] == ',':
            formatted_res = formatted_res.rstrip(',')

        self.value.update(json.loads(formatted_res))
