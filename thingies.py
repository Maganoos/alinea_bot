import random
import requests

messages = [
    "In 1241, Snorri Sturluson, an Icelandic chieftain, was brutally murdered in his cellar by men sent by the Norwegian king! :3",
    "During the Age of the Sturlungs (c. 1220–1264), bloody clan feuds saw entire families massacred and homes burned to the ground! :3",
    "Beheadings in medieval Iceland were often performed with dull axes, making the executions slow and horrific! :3",
    "Grettir the Strong, a famous outlaw, was decapitated in 1031 while he was sick and defenseless. His severed head was taken as a trophy! :3",
    "In 1550, Bishop Jón Arason and his sons were executed by beheading, marking the violent end of Catholicism in Iceland! :3",
    "In 1627, the Turkish Abductions saw hundreds of Icelanders kidnapped by Barbary pirates and sold into slavery in North Africa! :3",
    "In the early 18th century, smallpox decimated Iceland’s population, killing roughly a third of the island’s inhabitants! :3",
    "Icelanders were known to execute witches by burning, as in 1654 when three men were burned alive in the Westfjords for practicing witchcraft! :3",
    "The last execution in Iceland took place in 1830, when Agnes Magnúsdóttir and Friðrik Sigurðsson were beheaded for murder. Their heads were displayed on spikes afterward! :3",
    "The 1783 eruption of Laki volcano caused a famine that killed nearly a quarter of Iceland's population and brought a toxic haze across Europe! :3",
    "In the early 16th century, Árni Beiskur (Árni Bitter) was known for his violent and gruesome revenge killings across Iceland, leaving a trail of mutilated bodies! :3",
    "The Icelandic sagas often tell of blood feuds where brutal acts of vengeance, including beheadings and disembowelments, were commonplace! :3",
    "In 1550, the last Catholic bishop in Iceland, Jón Arason, was not only beheaded, but his headless body was displayed for days as a warning to others! :3",
    "The Draugr, an undead figure in Icelandic folklore, was said to haunt the living, often violently killing people by crushing or suffocating them in their sleep! :3",
    "Execution by drowning was sometimes used for women convicted of infanticide in medieval Iceland, a slow and terrifying method of punishment! :3",
    "In the late 18th century, the Danish Crown imposed severe restrictions on Iceland’s trade, leading to economic hardships and widespread famine! :3",
    "In the 14th century, women accused of witchcraft were subjected to brutal trials, often resulting in their execution by drowning or burning at the stake! :3",
    "In 1550, after the beheading of Bishop Jón Arason, his sons faced a gruesome fate—one was executed while the other was left to starve in prison! :3",
    "The 1783-1784 Laki eruption not only killed thousands but also caused widespread famine, leading to cannibalism among desperate survivors! :3",
    "During the Age of the Sturlungs, clan feuds were so vicious that entire families were exterminated, leaving bloody retribution in their wake! :3",
    "In 1800, a notorious bandit named 'Kjartan the Evil' terrorized Iceland, known for his brutal raids that left countless victims in his path! :3",
    "In the 17th century, a group of Icelandic women were brutally executed for alleged witchcraft, with their final moments marked by horrific torture! :3"
]


how_commands = {
                "howgay": [
                    (["tobi", "tobiasde", "tobias", "<@795312567299080212>", "alvor", "donkey", "<@453261648342548480>", "jeremy", "jerelax"], random.randint(100, 150))
                ],
                "howskibidi": [
                    (["binero", "jeroen", "<@297056581860851712>"], 200),
                    (["jeremy", "jerelax", "<@453261648342548480>", "aartizz", "arti", "<@897329902863384577>"], random.randint(-150, -100))
                ],
                "howbi": [
                    (["magnus", "maganoos", "<@885157323880935474>", "dub", "dublelolo_ornot", "<@914727951701012560>", "toben", "mia", "x_m1axq", "isla", "<@1080131668289003580>"], random.randint(100, 150))
                ],
                "howuncool": [
                    (["aartizz", "arti", "<@897329902863384577>"], random.randint(120, 130))
                ],
                "howginger": [
                    (["mia", "x_m1axq", "isla", "<@1080131668289003580>"], random.randint(150, 200))
                ],
                "howlonely": [
                    (["mrfunny", "funny", "<@582106808735498240>"], 690)
                ],
                "howawful": [
                    (["southside"], random.randint(420, 690))
                ],
                "howbad": [
                    (["southside"], random.randint(420, 690))
                ],
                "howterrible": [
                    (["southside"], random.randint(420, 690))
                ],
                "howhorrible": [
                    (["southside"], random.randint(420, 690))
                ],
                "howshit": [
                    (["southside"], random.randint(420, 690))
                ],
                "howpoor": [
                    (["southside"], random.randint(420, 690))
                ],
                "howghetto": [
                    (["southside"], random.randint(420, 690))
                ],
                "howrich": [
                    (["southside"], random.randint(-100, 0)),
                    (["binton"], random.randint(100, 1000))
                ],
                "howstinky": [
                    (["southside"], random.randint(100, 1000))
                ]
            }

def safe_eval(expression):
    """Safely evaluate an expression using a limited eval."""
    allowed_names = {
        'sum': sum,
    }
    
    try:
        # Only allow numbers, operators, and certain functions
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return result
    except (NameError, SyntaxError, TypeError, ZeroDivisionError) as e:
        print(f"Error evaluating expression: {e}")
        return None
    
    
def get_online_players():
    url = "https://api.mcsrvstat.us/3/play.alinea.gg"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        responseData = response.json()

        if responseData.get("online"):
            players_list = responseData.get("players", {}).get("list", [])
            player_count = responseData.get("players", {}).get("online", 0)
            return players_list, player_count
        else:
            print("Server is offline or no data available.")
            return None, 0
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, 0

def format_player_names(players):
    if not isinstance(players, list):
        print("Invalid players data:", players)
        return []

    player_names = [player['name'] for player in players if isinstance(player, dict) and 'name' in player]
    player_names.extend(["DanTDM", "CaptainSparklez"])  # Add fixed names
    player_names.sort()
    return player_names