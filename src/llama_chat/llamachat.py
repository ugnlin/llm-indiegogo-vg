import os
from llama_cpp_chat_completion_wrapper import Llama2ChatCompletionWrapper, Message

USE_META_TOKENIZER_ENCODER = True

if USE_META_TOKENIZER_ENCODER:
    from tokenizer import Tokenizer


def console_print(message: Message) -> None:
    reset = "\033[00m"
    color_map = {
        "system": ("\033[1;35m", "\033[35m"),
        "user": ("\033[1;33m", "\033[33m"),
        "assistant": ("\033[1;31m", "\033[31m"),
        "assistant-before-post-process": ("\033[1;31m", "\033[31m"),
    }
    role_color, content_color = color_map[message["role"]]
    formatted_message = f"{role_color}{message['role'].upper()}{reset}> {content_color}{message['content']}{reset}"
    print(formatted_message)


def main():
    model_path = "../data/models/llama-2-7b-chat.Q5_K_S.gguf"

    params = {
        "temp": 0,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    if USE_META_TOKENIZER_ENCODER:
        # Download here: https://ai.meta.com/resources/models-and-libraries/llama-downloads/
        tokenizer_path = '../data/models/tokenizer.model'
        meta_tokenizer = Tokenizer(model_path=tokenizer_path)

    llm = Llama2ChatCompletionWrapper(
        model_path=model_path,
        callback=console_print,
        tokenizer_encoder=meta_tokenizer.encode if USE_META_TOKENIZER_ENCODER else None,
    )
    import time
    time_started = time.time()
    llm.new_session(system_content="""You are an analyst who specialises in video game crowdfunding campaigns.
    You will answer questions directly, corresponding to the options provided to you, and not deviating from the point 
    or the request, succinctly and without extra detail. You are confident in your answers, and do not give reasoning for your answers. 
    You do not introduce yourself, you do not summarise your answers, and do not chat outside the bounds of fulfilling the request.""")

    description = """
     A PREVIEW of our game is now available at 
     http://www.shiftjoy.com/kickstarterdemo.html 
     (You'll need Unity Webplayer, google it). 
     Latest video (will update) : 
     Hello everyone, thanks for visiting our post :).  We are ShiftJoy, and we are the team behind Predator Realm. We're all teenagers (I'm 14, don't laugh, read on) but we have lots of experience in gaming, game design and technology and have help from our families for all the legal and money stuff :3 
     I'm Sol. Don't underestimate me just because I'm 14 :P. I started learning Unity (the game engine I am using) nearly 2 years ago and now I have enough experience to start creating my own game. I have always been into technology and gaming: I'm also a good web designer, and I've picked up several clients in my town to design websites for. 
     I worked hard designing websites and making small games in Unity for 8 months, until I had enough money to buy my very own Macbook Pro :D. It's certainly my most prized possession! Now I am using it to develop Predator Realm, with the help of my family and friends for some graphics design, legal stuff and sorting out the money. 
     The rest of us have a similar sort of experience as me, and we make a great, hard-working team! 
     We're not the only teenagers who have made games. 
     Robert Nay created 'Bubble Ball' when he was 14, and that became the top App Store game (beating Angry Birds) in 2011. Harry Moran created 'PizzaBot' when he was 12 which became the top Mac App Store game in 2011, too. (Yes, I've done my research!). I'm sure there are many more... 
     Well, enough about me, and us. Don't worry, we're not the sort of people who give up easily, and we're aiming to update our group website ( 
     http://www.shiftjoy.com 
     ) with videos and snaps from development once a week at least :D. 
     Our workstation ^ 
     Predator Realm is an awesome third-person zombie shooter. It has more of a casual, arcade style compared to other FPS zombie games, but we are working on awesome graphics and different gamemodes to suit every PC gamer. 
     We're working on these game modes: 
     - Infinite Survival (Single Player) 
     - infinite waves of zombies, gets harder and harder, ends when you die 
     - Adventure (Single Player) 
     - progress through the levels 
     - Co-op Infinite Survival (2-4 Players) 
     - Same as Infinite Survival, but with your friends online 
     - Deathmatch (2-8 players) 
     - No zombies! Kill your rival players, the most kills wins! 
     (possibly a CTF gamemode too - thinking about it). 
     The main character is Zayn, a perfectly normal man, who is the only survivor of a mini-apocalypse in his hometown, up in the Heora Mountains. He must travel to the city and warn his fellow humans, and help them escape, before the whole area is taken over! 
     Currently Zayn has one weapon, an ACWR automatic rifle. It has a 26-round capacity and reloads in 1.5-2.5 seconds. We will, of course, be adding more weapons as the game progresses - one of the things we need the indiegogo money for is weapon design. 
     We're currently working on the Zombie AI and it is proving very successful. The zombie knows when to attack and will even attack other zombies if Zayn isn't close :P 
     We'll add a playable demo to our website ( 
     http://www.shiftjoy.com 
     ) once we've sorted the GUI. 
     The first release will be for Mac, Windows and Linux. 
     If we reach the stretch goal below, we'll also develop it for iOS :D 
     We're not sure whether to make the game freemium (free, but pay for extras), or charge a small amount. 
     Of course, we're a very small team so we rely a lot on the internet for models, animations and stuff like that. Unfortunately, this costs a lot>_>. 
     Here is a rough breakdown of where your kind donations will be going: 
     - £1000 = Unity Pro (yes, we're still using the free version), this will mean better graphics and much better performance for you! 
     - £70 - Mac App Store Licence for our first year publishing 
     - £200 - Animations, 3D models, weapon design and sound effects to make the game look better and feel better 
     - £80 - PayPal and IndieGogo fees 
     I am an OK musician (grade 5 piano, love Logic Pro and synthesisers) so we won't have to pay for music scoring, hopefully :) 
     In case you guys are ultra kind, 
     we've put together some stretch goals! 
     £1500 (+£150) = 3 more maps, 1 more gamemode 
     £2000 (+£650) = Game available to play FOR FREE ONLINE (pay for extras) 
     (this is expensive because we would need a server) 
     £3000 (+£1650) = iOS plus all above! 
     PLEASE CHECK OUT THE PERKS YOU CAN GET FOR PLEDGING! -----> 
     If you can't donate, you can also help by sharing the link above with your friends and family. It is much appreciated! 
     If you have any questions, feel free to email us at shift.joy.com@gmail.com OR live-chat with us on our website, 
     http://www.shiftjoy.com """

    prompt = f"""
            Here is info about a crowdfunding campaign: 

            Description:```
            '{description}'.
            ```

            From the following types of projects, what kind of project is this? 
            [Game Software , Game Hardware , Physical Game , Event , Other]

            If it is a game, what kind of genres is it?
            [Action, Board Game, Adventure, Card Game, Gacha Game, Horror, Puzzle, Role-playing, Fighting,
            Simulation, Strategy, Sports, Survival, MMO, Non-Game, Adult, VR, Other]

            If it is a game, what platforms does it come out on?
            [PC, Playstation, Xbox, Switch, Mobile, Other]

            How many platforms does it come out on?

            Does the game have a singleplayer mode? Does it have a multiplayer mode?

            Is the game developed by a single developer, or more?
            """

    answer = llm(prompt, params=params)

    llm.new_session(system_content="""You are an assistant who summaries info into jsons. You will return only the json
    in the format as prompted with nothing else. You do not give introductions or summaries, 
    and do not chat outside the bounds of fulfilling the request, 
    answering and stopping straight away with no extra notes, introductions, or thanks.""")

    answer2 = llm(f"""
            Please format the following into json, and return the json only. The values should match that of the example
            format given, and if unsure, should occupy the bool value False'.

            Example Format:
            {{
                'project_type_software': <bool>,
                'project_type_hardware': <bool>,
                'project_type_physical': <bool>,
                'project_type_event': <bool>,
                'project_type_other': <bool>,
                'game_genre_action': <bool>,
                'game_genre_board': <bool>,
                'game_genre_adventure': <bool>,
                'game_genre_card': <bool>,
                'game_genre_gacha': <bool>,
                'game_genre_horror': <bool>,
                'game_genre_puzzle': <bool>,
                'game_genre_rpg': <bool>,
                'game_genre_sim': <bool>,
                'game_genre_strategy': <bool>,
                'game_genre_sports': <bool>,
                'game_genre_survival': <bool>,
                'game_genre_mmo': <bool>,
                'game_genre_adult': <bool>,
                'game_genre_vr': <bool>,
                'game_platform_pc': <bool>,
                'game_platform_playstation': <bool>,
                'game_platform_xbox': <bool>,
                'game_platform_switch': <bool>,
                'game_platform_mobile': <bool>,
                'game_platform_other': <bool>,
                'number_of_platforms': <int>,
                'singleplayer': <bool>
                'multiplayer': <bool>,
                'solo_developer: <bool>,
            }}

            Raw text:
            {answer}

            Json:
            """, params=params)

    print(time.time() - time_started)


if __name__ == "__main__":
    main()