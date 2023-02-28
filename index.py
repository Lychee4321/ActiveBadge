import requests
import json
import inspect
import sys
import time

from colorama  import Fore, Style

# 라쿠#7777 - https://idyllc.xyz
# 라쿠#7777 - https://idyllc.xyz
# 라쿠#7777 - https://idyllc.xyz
# 라쿠#7777 - https://idyllc.xyz

# 파이썬 버젼 오류 감지
if sys.version_info < (3, 8):
    exit("파이썬 3.8 버젼 이상을 사용해주세요.")

# disccord.py 오류 감지
try:
    from discord import app_commands, Intents, Client, Interaction
except ImportError:
    exit(
        "discord.py 관련 오류 감지됨"
        "( discord.py 를 재설치 하거나 높은 버젼의 파이썬을 이용해주세요. )"
    )


# 프로그램 안내 문구
print(inspect.cleandoc(f"""


    개발자 뱃지 받기 프로그램을 이용해주셔서 감사합니다.
    아래에 당신의 봇 토큰을 입력해주세요.

    토큰을 입력하기 전까진 이 프로그램을 닫지 마세요.
    서버에 봇을 초대하고 , 명령어를 입력하기 전에 이 프로그램을 닫지 마세요.
"""))

# config.json 오류 감지
try:
    with open("config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):

    config = {}

# config.json 토큰 감지
while True:
   
    token = config.get("token", None)
    if token:
        print(f"\n>>  토큰이 감지되었습니다. -> /config.json ( 이전에 실행때 저장됨. ) 에 저장된 토큰을 사용합니다 . \n")
    else:

        token = input("> ")

    # 기타 
    try:
        data = requests.get("https://discord.com/api/v10/users/@me", headers={
            "Authorization" : f"Bot {token}"
        }).json()
    except requests.exceptions.RequestException as e:
        
        # 네트워크 오류
        if e.__class__ == requests.exceptions.ConnectionError:
            exit(f"ConnectionError : 네트워크 연결 오류! 다른 네트워크를 사용해보세요.")

        # API 타임아웃
        elif e.__class__ == requests.exceptions.Timeout:
            exit(f"Timeout : API 타임아웃 감지. ( 오류 혹은 잠시후에 시도해주세요. )")

        # 파이썬 오류감지후 종료
        exit(f"알수 없는 오류가 발생했습니다. ( 오류 코드 :\n{e} )")

    # 올바른 토큰 감지후
    if data.get("id", None):
        break  # 루프 탈출

    # 토큰 틀릴 경우 에러
    # 토큰 다시 물어보기
    print(f"\n잘못된 토큰이 감지되었습니다. 올바른 토큰을 입력해주세요 .")

    # 다른 토큰 감지시 config.json 수정
    config.clear()


# config.json 에 저장하기
with open("config.json", "w") as f:
    config["token"] = token

    # 편-안
    json.dump(config, f, indent=2)


class FunnyBadge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """ nothing """
        await self.tree.sync()


# 안내 문구
client = FunnyBadge(intents=Intents.none())


@client.event
async def on_ready():
    """ 봇이 자동으로 연결되고 있습니다.
         봇이 자동으로 연결되고 난후 , 봇 초대 링크를 불러옵니다.
    """
    print(inspect.cleandoc(f"""
        {client.user} (ID: {client.user.id} 로 로그인됨)

        이 링크를 통해 {client.user} 을 초대하세요:
        https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot
    """), end="\n\n")
      
# 명령어
@client.tree.command()
async def setup(interaction: Interaction):
    """ 명령어를 입력하고 설정을 완료하세요! """
    # 콘솔에 알림
    print(f"> {interaction.user} 가 명령어를 사용하셨습니다.")

    # 채널에 알림
    await interaction.response.send_message(inspect.cleandoc(f"""
        **{interaction.user}** 님 , 제 프로그램을 이용해주셔서 감사합니다.

        > __**뱃지는 언제 얻을수 있나요?**__
        > `뱃지를 얻을 자격은 디스코드에서 시간을 두고 검토합니다,
        > 이러한 이유 때문에 사용자들은 최소 24시간에서 최대 몇일 까지 기다려야 할 수도 있습니다.`

        > __**24시간이 지난거 같아요 , 어디서 뱃지를 확인하죠?**__
        > `이미 24시간이 지난거 같다면 아래 링크를 통해 확인해보세요!
        > https://discord.com/developers/active-developer ( 들어가서 정보 채워넣기. )`

        > __**활성화된 봇 개발자 뱃지 관련 안내**__
        > `활성화된 봇 개발자 뱃지 관련 안내는 아래의 공식 디스코드 채널에서 확인해주세요.
        > 공식 서버 > https://discord.gg/discord-developers - #active-dev-badge .`
    """))

client.run(token)
