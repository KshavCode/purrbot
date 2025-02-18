#IMPORTING
import discord
from discord import app_commands
from discord.ext import commands, tasks
import random, pandas as pd, requests, asyncio, typing, math, json, FunctionFiles as ff
from itertools import cycle
from fractions import Fraction

pd.options.mode.chained_assignment = None

@tasks.loop(seconds=120)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@tasks.loop(seconds=30)
async def generate_question():
  server_channel = 1283774140783919125
  channel = client.get_channel(server_channel)
  difficultyChoice = random.choice(["EASY", "EASY", "EASY", "MEDIUM"])
  n = 200
  while True:
    try:
      rn = random.randint(1,n)
      url = f"https://alfa-leetcode-api.onrender.com/problems?difficulty={difficultyChoice}&limit={n}"
      r = requests.get(url).json()["problemsetQuestionList"][rn]
      title = r["title"]
      problemId = r["questionFrontendId"]
      isPaid = r["isPaidOnly"]
      acceptanceRate = r["acRate"]
      tags = [f"`{x["name"]}`" for x in r["topicTags"]]
      hasSolution = "Not Available" if not r["hasSolution"] else "Available"
      # Getting the direct link
      r2 = requests.get(f"https://leetcode-api-pied.vercel.app/problem/{problemId}").json()
      category = r2["categoryTitle"]
      urlQuestion = r2["url"]
      
      break
    except IndexError:
      n -= 100
      continue
    except KeyError:
      continue

  em = discord.Embed(title=f"LeetCode Problem #{problemId}", color=discord.Color.random())
  em.add_field(name="Problem name", value=title, inline=False)
  em.add_field(name="Difficulty", value=difficultyChoice.title(), inline=False)
  em.add_field(name="Paid?", value=isPaid, inline=False)
  em.add_field(name="Solution", value=hasSolution, inline=False)
  em.add_field(name="Category", value=category, inline=False)
  em.add_field(name="Acceptance Rate", value=f"{int(acceptanceRate)}%", inline=False)
  em.add_field(name="Tags", value="  ".join(tags), inline=False)
  em.add_field(name="Problem Link", value=urlQuestion ,inline=False)
  em.set_thumbnail(url=client.user.avatar)
  await channel.send(embed=em)

# r = requests.head(url="https://discord.command/api/v1")
# try:
#   print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
# except:
#   print("No rate limit")

# INITIALIZATION
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=['purr ', 'Purr ', 'PURR '], intents=intents, case_insensitive=True)
client.remove_command('help')

# EVENTS
@client.event
async def on_ready():
  change_status.start()
  generate_question.start()
  print("Bot Launched")
  try:
    client.tree.add_command(maths)
    client.tree.add_command(edit)
    await client.tree.sync()
    print("Syncing successful!")
  except Exception as e:
    print(e)

@client.event
async def on_guild_join(g):
  success = False
  i = 0
  while not success:
    try:
      success = True
      await g.channels[i].send("Thanks for inviting me here. Check my available commands by using `/help`! More commands are yet to come.")
    except (discord.Forbidden, AttributeError):
      i += 1
    except :
      break

#________LIST/DICTIONARY_______

answer_me = [
  "Yes!", "No!", "Certainely", "Not Certain", "Maybe Yes!", "Maybe No!",
  "Hard to say but Yes!", "Hard to think about it but it is a no from my side",
  "Definitely Yes", "I don't think so", "Yup!", "Nope", "Can't decide xD",
  "Both Yes and No", "Idk", "Undoubtelly", "Can't Decide",
  "It would not fit in", "Damn YES!", "Hard to say", "I think, no",
  "No from me"
]

status = cycle([
  "Purrbot v2", "/feedback", "and collecting Purrcoins", "the fish game", "Heads or Tails", "/logs",
  "some songs", "with different shapes", "with my profile using /profile", "with new commands", " the music in my hood"
])

encode_characters = {'a': '𓂅', 'b': '✦', 'c': '𝖄', 'd': '⊹', 'e': '⋆', 'f': '⌕', 'g': 'ꗃ', 'h': '𝕯', 'i': 'ഒ', 'j': '୨', 'k': '୧', 'l': '⌯', 'm': '﹅', 'n': '﹆', 'o': 'ଘ', 'p': 'ꕤ', 'q': 'ꔛ', 'r': '𓏲', 's': 'ָ', 't': 'ǂ', 'u': '𓍼', 'v': '⋈', 'w': 'ꮺ', 'x': '⌗', 'y': 'ꉂ', 'z': 'ᨒ', '1': '๑', '2': '∇', '3': 'θ', '4': 'Λ', '5': 'Γ', '6': 'Ξ', '7': 'ω', '8': 'ξ', '9': 'δ', '0': 'ε', 'A': 'ζ', 'B': 'η', 'C': '𝕬', 'D': '⊷', 'E': '⋭', 'F': '≟', 'G': '≲', 'H': '⍤', 'I': '⨒', 'J': '⊿', 'K': '𝟃', 'L': '⋴', 'M': '⊎', 'N': '⊅', 'O': '⋓', 'P': 'ӫ', 'Q': '옻', 'R': 'ഋ', 'S': '∵', 'T': '⋠', 'U': '≢', 'V': '≭', 'W': '⩲', 'X': '∔', 'Y': '⊖', 'Z': '₪', ' ': '✧', '.': '↢', ',': '↡', "'": '↺', '/': '↻', '?': '↼', '!': '↾', '@': '↳', '#': '↲', '$': '↸', '%': '↹', '^': '⇏', '&': '⇪', '*': '⇫', '(': '⇬', ')': '⇭', '_': '⇮', '+': '⇯', '=': '⇻', '-': '⇺', '~': '⇹', '`': '⇸', '|': '⇷', '<': '⇾', '>': '⇽', ';': '⇲', ':': '⇱', '{': '⇰', '}': 'ↇ', '[': 'Ⅰ', ']': '円'}
decode_characters = {v: k for k, v in encode_characters.items()}


itemdesc = {"Bait": "Basic is a common item. It can be used to catch fishes."}


wallpapers = {
  "Not Set" : "https://media.discordapp.net/attachments/1159490904990691338/1159792379172225107/wall.png?ex=658e98d3&is=657c23d3&hm=bb4577524e5dcf18e294102ab108a8388f803965004416ba64c4d82f1def9b0f&=&format=webp&quality=lossless&width=441&height=441",

  "Christmas Wallpaper" : "https://media.discordapp.net/attachments/1159490904990691338/1184135646558814330/images_6.jpeg?ex=658adf42&is=65786a42&hm=7771380eacb743872d0c27ac77f5f599e1832801267caf98a74259d44f2f960d&=&format=webp", 

  "Purrbot Wallpaper" : "https://media.discordapp.net/attachments/1159490904990691338/1184135646076485742/images_8.jpeg?ex=658adf42&is=65786a42&hm=a26649943540af6c6ad8bbddaabec82cf123b9aa04de195f31a739d0b7c7cf00&=&format=webp", 

  "Anime Wallpaper" : "https://media.discordapp.net/attachments/1159490904990691338/1184135649377402951/images.jpeg?ex=658adf42&is=65786a42&hm=f2a6d78b766957bc3deb0bcd54712d4a2cb3e98c199d197968365407da41af9a&=&format=webp", 

  "Batman Wallpaper" : "https://media.discordapp.net/attachments/1159490904990691338/1173598422570381382/AVvXsEgWfhmsqwj-sGb6R5EpSCdseX2h3P5MkgxBsWuXjO4vyOc-Nb2S3NPY4-Ot96VgnYUxH0vsdGT_cdg-fJgCo1Vktl9uhmXqVNGYxb8OQW_wNRzTBnwyCV4BBIC20-CJBjrP8g4FBRvBPtdZuy7lIrvID16eL05bsRKQKK6hUg7UJgLhZu9j1kG6KrAL0uhNs16000-rw.png?ex=658973b4&is=6576feb4&hm=955d7098d7e1751d70353cc0b8b279732e5c11febd8db46fc9f52357aed5804f&=&format=webp&quality=lossless&width=783&height=440", 

  "Superman Wallpaper" : "https://media.discordapp.net/attachments/1159490904990691338/1173600170093580320/1095250.png?ex=65897554&is=65770054&hm=d0dd9fd511d9fc118a16b23d7337fea5908d34c451852b41ea6c5225d1793343&=&format=webp&quality=lossless&width=783&height=440", 

  "Spiderman Wallpaper" : "https://media.discordapp.net/attachments/1159490904990691338/1173598534826733679/thumb-1920-844967.png?ex=658973cf&is=6576fecf&hm=72846e81f2c5a5a0f7e338d9940d174bb802c6505f81ba8ab36015dcb927417d&=&format=webp&quality=lossless&width=783&height=440", 

  "Ironman Wallpaper" : "https://media.discordapp.net/attachments/1159490904990691338/1173598641584357386/319903-3840x2160-desktop-4k-iron-man-wallpaper.png?ex=658973e8&is=6576fee8&hm=1b667914bea14d654df24496c5c10caac6510217562eeec63566ae6d4346b12f&=&format=webp&quality=lossless&width=783&height=440", 

  "Landscape Wallpaper" : "https://media.discordapp.net/attachments/1159490904990691338/1173600276515663882/vector-forest-sunset-forest-sunset-forest-wallpaper-preview.png?ex=6589756e&is=6577006e&hm=fcde258228105a9621e43c11975a9c1f233126b8010f7c54837ca31909e6c11c&=&format=webp&quality=lossless", 

  "Valentines Wallpaper1" : "https://media.discordapp.net/attachments/1159490904990691338/1173598769519013998/Valentine-Day-Wallpaper_beautiful-photos-hd-wide-wallpapers1.png?ex=65897407&is=6576ff07&hm=079463d583752878710495ae65e22f80599878951cd9c1fd73ce166d35d2f41d&=&format=webp&quality=lossless&width=705&height=441", 

  "Valentines Wallpaper2" :  "https://media.discordapp.net/attachments/1159490904990691338/1173598860581556224/valentines_wallpaper_banner-800x457.png?ex=6589741c&is=6576ff1c&hm=c4acb8f512c77063eaa004848ae7a22dc8e8fd2b15d99aa667aedf96146016a5&=&format=webp&quality=lossless&width=772&height=441"
}

fish_price = {"basic": 10, "regular": 50, "elite": 100, "premium": 250, "epic": 800, "supreme":2500}

#--------------------------------------------------------------------------------------

#____________________________________BUTTON/MODALS_______________________________________


class Invitebutton(discord.ui.View):
  def __init__(self, inv: str):
    super().__init__()
    self.inv = inv
    self.add_item(discord.ui.Button(label="Invite Me!", url=self.inv))

  @discord.ui.button(label="Invite link", style=discord.ButtonStyle.blurple)
  async def invite(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_message(self.inv, ephemeral=False)

class Feedback(discord.ui.Modal, title="Send us your feedback!") : 
  fb = discord.ui.TextInput(style=discord.TextStyle.long, label="Feedback :", required=True, placeholder="Your experience with Purrbot.....")
  sug = discord.ui.TextInput(style=discord.TextStyle.long, label="Suggestions :", required=False, placeholder="Ideas for new command (Optional)")

  async def on_submit(self, interaction=discord.Interaction) : 
    with open("feedback.txt", "a") as u :
      if self.sug != None : 
        u.write(f"Feedback : {self.fb.value}\nSuggestions : {self.sug.value}\nBy : {self.user}\n\n")
      else : 
        u.write(f"Feedback : {self.fb.value}\nBy : {self.user}\n\n")
      await interaction.response.send_message("Your feedback has been submitted. Thank you for your precious time! Have a nice day!")


class RiddAns(discord.ui.View) :
  def __init__(self, ans:str) : 
    super().__init__()
    self.ans = ans

  @discord.ui.button(label="Answer", style=discord.ButtonStyle.green)
  async def answ(self, interaction:discord.Interaction, button:discord.ui.Button):
    await interaction.response.send_message(self.ans, ephemeral=False)


# CLASSES AND PARENTS
#_____________________________________MATH____________________________________
class Maths(app_commands.Group):
  ...
maths = Maths(name="math", description="Performs various calculations")

class editprofile(app_commands.Group) : 
  ...
edit = editprofile(name="editprofile", description="Edit your profile")



#____________________________________________________________________________________

#----------------------------------COMMANDS------------------------------------------
@client.command()
async def ban(ctx, member: discord.Member, reason=None):
  if ctx.author.guild_permissions.manage_channels:
    await ctx.send(f"{member} has been banned.")
    await member.ban(reason=reason)
  else:
    await ctx.send("You don't have permission to ban anyone.")


@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")
  for ban_entry in banned_users:
    user = ban_entry.user
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"{user.name}#{user.discriminator} has been unbanned!")


#----------------------------------HELP--------------------------------------

@client.tree.command(name="help", description="lists out all the available commands of the Purrbot")
@discord.app_commands.describe(command="enter the command name, which you want help with")
async def help(interaction: discord.Interaction, command:typing.Optional[str]):
  em = discord.Embed(title="HELP", color=interaction.user.color)
  if not command:
    em.add_field(name="<:commands:1103517903166382091>Normal Commands",
                 value="`logs`  `pfp`  `info`  `encode`  `decode`  `feedback`  `invite`  `userinfo`  `serverinfo`  `remindme`\n", inline=False)
    em.add_field(name="<:commands:1103517903166382091>Game Commands", 
                 value="`profile`  `edit`  `dailylogin`  `research`  `balance`  `search`  `steal`  `shop`  `buy`  `inventory`  `use`  `share`  `gamble`  `fish`  `bucket`  `sellfish`  `fishinfo`  `leaderboard`\n", inline=False)
    em.add_field(name="<:commands:1103517903166382091>Fun Commands",
                 value="`fact`  `riddle`  `echo`  `spam`  `spamstop`  `rate`  `toss`  `diceroll`  `8ball`  `pet`  `pick1`  `randomnum`  `hiddendm`", inline=True)
    em.add_field(name="<:commands:1103517903166382091>Roleplay Commands",
                 value="`pat`  `slap` `wish`", inline=False)
    em.add_field(name="<:commands:1103517903166382091>Mathematical Commands",
                 value="`factorial`  `add`  `subtract`  `multiply`  `divide`  `exponent`  `log10`  `shapes`  `sqroot`", inline=False)
    em.add_field(name="<:commands:1103517903166382091>Moderation Commands",
                 value="`kick`  `purge`  `kaboom`  `poll`", inline=False)

  elif command :
    with open("data/help.json") as f:
      help_dict, help_args = json.load(f)
    command = command.lower()
    em.add_field(name=f"<a:symbol:1103534543895531610> {command}", value=help_dict[command], inline=False)
    em.add_field(name="Arguments Required :", value=help_args[command], inline=False)

  elif command.lower() not in help_dict: 
    em.add_field(name="INVALID COMMAND", value="Either the command is unavailable in Purrbot or you must have made a spelling error.")

  await interaction.response.send_message(embed=em, ephemeral=False)


#____________________________________NORMAL_______________________________________

@client.tree.command(name="logs", description="Tells you about the recent updates and fixes")
async def log(interaction: discord.Interaction):
  em = discord.Embed(title="PurrBot Logs, 11 February 2025", description="*Due to financial reasons, Purrbot was shut down. But now, it has been revived again and will be programmed actively. Sorry for inconvinience the bot will work as expected and in a much smoother way!*\n*If you contact any kind of error from the bot, you can always use the `/feedback` command which will notify the developer.*", color = 0x3498db)
  #<a:star_2:1085488210064461955> for updates
  em.add_field(name="Updates <a:blu_glitter:1161309978099986492>", value="<a:star_2:1085488210064461955> __New Commands__ -> `leetcodestats`\n<a:star_2:1085488210064461955> __Removed Commands__ -> `spamstart` `spamstop`", inline=False)
  #<:wren:1105395863955714059> for fixes
  em.add_field(name="Fixes", value="Slight error in `fact` and `riddle`.")
  em.set_footer(text="You can send feedbacks using /feedback.", icon_url=client.user.avatar)
  await interaction.response.send_message(embed=em, ephemeral=False)

@client.tree.command(name="info", description="Gives information regarding the Bot Status")
async def info(interaction: discord.Interaction):
  try:
    user = await client.fetch_user("781419439160688660")
  except:
    user = 'purrfectkun'
  total_servers = str(len(client.guilds))
  with open("data/help.json") as f:
    NumberOfCommands = len(json.load(f)[0])
  em = discord.Embed(title=client.user, description="ID = 863490119976878090", color=0xffb6e4)
  em.add_field(name="<:person:1085489445584785508> Owner :", value = user.mention, inline=False)
  em.add_field(name="<a:coding:1085489342551695371> Version :", value="PurrBot v2", inline=False)
  em.add_field(name="<a:Discord:1085489545258217542> Library : ", value="discord.py 2.0")
  em.add_field(name="<:server:1085489879401639976> No. of Servers : ", value=total_servers, inline=False)
  em.add_field(name="<:Cool:912744704460857375> No. of Commands : ", value=NumberOfCommands, inline=False)
  em.add_field(name="<:people:1085588661980102671> Bot Users :", value=str(len({m.id for m in client.get_all_members()})), inline=False)
  em.add_field(name="<a:Errorr:1085489721926496346> Errors :", value="2 Errors", inline=False)
  em.add_field(name="<:thinking_cat_face:937049263509225502> Since :", value="Sunday, 11 July 2021", inline=False)
  em.set_thumbnail(url="https://i.pinimg.command/564x/39/69/7f/39697f5042715e373aa7144caf3f4795.jpg")
  await interaction.response.send_message(embed=em, ephemeral=False)

@client.tree.command(name="pfp", description="shows avatar of the member you mentioned or yours if not mentioned")
@discord.app_commands.describe(member="leave it blank if you want your pfp to be displayed")
async def pfp(interaction: discord.Interaction, member: discord.Member = None):
  if not member:
    member = interaction.user
  em = discord.Embed(title=f"__Avatar of {member}__", color=interaction.user.color)
  em.set_image(url=member.avatar)
  em.set_footer(text=f"~requsted by {interaction.user.name}")
  await interaction.response.send_message(embed=em, ephemeral=False)


@client.tree.command(name="invite", description="Invite the bot in your server!")
async def inv(interaction: discord.Interaction):
  inv = "https://bit.ly/3q7hDBB"
  await interaction.response.send_message("Here is the link my friend!", view=Invitebutton(str(inv)), ephemeral=False)

@client.tree.command(name="encode", description="turns your texts into a passcode language")
@discord.app_commands.describe(text="here comes the text that will be encoded")
async def enc(interaction:discord.Interaction, text:str) : 
  global encode_characters
  textList = list(text)
  for index in range(len(textList)):
    try : 
      textList[index] = encode_characters[textList[index]]
    except KeyError: 
      continue
  await interaction.response.send_message("".join(textList), ephemeral=False)

@client.tree.command(name="decode", description="turns the code back to the original text")
@discord.app_commands.describe(code="type the code here (only works if encoded using Purrbot)")
async def dec(interaction:discord.Interaction, code:str) : 
  codeList = list(code)
  for index in range(len(codeList)):
    try : 
      codeList[index] = decode_characters[codeList[index]]
    except KeyError: 
      continue
  await interaction.response.send_message("".join(codeList), ephemeral=False)

@client.tree.command(name="feedback", description="tell the bot owner about your experience with the Purrbot.")
async def fedback(interaction:discord.Interaction) : 
  feedback_modal = Feedback()
  feedback_modal.user = interaction.user
  await interaction.response.send_modal(feedback_modal)

@client.tree.command(name="userinfo", description="shows the information regarding a member")
@discord.app_commands.describe(member="mention a member. Will show your info if none")
async def userinfo(interaction:discord.Interaction, member:discord.Member=None) : 
  botpfp = client.user.avatar
  user = member or interaction.user
  roles = [str(role.mention) for role in user.roles]
  userColorCode = user.color 
  userId = user.id
  userNickname = user.nick or "No nickname set"
  userCreatedAccountDate = user.created_at.strftime("%A, %B %d %Y, %I:%M:%S %p")
  userJoinedServerDate = user.joined_at.strftime("%A, %B %d %Y, %I:%M:%S %p")
  avatar_url = user.display_avatar
  checkIfBot = "not a bot" if not user.bot else "a bot"
  numberOfRoles = len(user.roles)
  roles = " | ".join(roles)
  if roles > 1024:
    roles = "Too many to display"
  else : 
    roles = " | ".join(roles)

  em = discord.Embed(title="User Information", description=f"ID = {userId}", color=userColorCode)
  em.set_thumbnail(url=avatar_url)
  em.add_field(name="", value="")
  em.add_field(name="Member name : ", value=f"{user}", inline=False)
  em.add_field(name="Nickname : ", value=f"{userNickname}", inline=False)
  em.add_field(name="Created on :", value=f"{userCreatedAccountDate}", inline=False)
  em.add_field(name="Joined on :", value=f"{userJoinedServerDate}", inline=False)
  em.add_field(name=f"Roles ({numberOfRoles}) :", value=f"{roles}", inline=False)
  em.set_footer(text=f"{user} is {checkIfBot}", icon_url=botpfp)
  await interaction.response.send_message(embed=em)

@client.tree.command(name="serverinfo", description="shows the information about the current server.")
async def svinfo(interaction:discord.Interaction) : 
  sv = interaction.guild
  serverId = sv.id
  serverName = sv.name 
  serverCreatedTime = sv.created_at.strftime("%A, %B %d %Y, %I:%M:%S %p")
  serverOwner = sv.owner
  serverMemberCount = sv.member_count
  serverTextChannelCount = len(sv.text_channels)
  serverVoiceChannelCount = len(sv.voice_channels)
  serverImage = sv.icon
  serverEmojis = len(sv.emojis)

  em = discord.Embed(title=serverName, description=f"Server ID : {serverId}", color=interaction.user.color)
  em.add_field(name=f"__Owner__ : *{serverOwner}*", value="", inline=False)
  em.add_field(name=f"__Total Members__ : *{serverMemberCount}*", value="", inline=False)
  em.add_field(name=f"__Created At__ : *{serverCreatedTime}*", value="", inline=False)
  em.add_field(name=f"__Text Channels__ : *{serverTextChannelCount}*", value="", inline=False)
  em.add_field(name=f"__Voice Channels__ : *{serverVoiceChannelCount}*", value="", inline=False)
  em.add_field(name=f"__Emojis__ : *{serverEmojis}*", value="", inline=False)
  em.set_thumbnail(url=serverImage)
  await interaction.response.send_message(embed=em)


@client.tree.command(name="remindme", description="reminds you about certain task according to the time you have given.")
@discord.app_commands.describe(message="A text which needs to be sent when reminding", time="To remind after? Seconds and minutes only (3s, 5m, 25m, etc.)!")
async def remind(interaction:discord.Interaction, message:str, time:str) :
  user = interaction.user
  try: 
    if time.lower()[-1] == "m" : 
      time = map(str, time)
      time = list(time)
      time.pop()
      timenum = "".join(time)
      if timenum.isdigit() == True : 
        await interaction.response.send_message(f"Purrbot will remind you about your message in about {timenum} minute(s)!")
        time = int(timenum)
        time = time*60
        await asyncio.sleep(time)
        for i in range(10) : 
          await user.send(f"Hey, you put a reminder for ||**{message}**||!")    
      else : 
        await interaction.response.send_message("A wrong syntax again. Only *s* and *m* allowed!")
          
    elif time.lower()[-1] == "s" :
      timemap = map(str, time)
      timemap = list(timemap)
      timemap.pop()
      timenum = "".join(timemap)
      if timenum.isdigit() == True : 
        await interaction.response.send_message(f"Purrbot will remind you about your message in about {timenum} second(s)!")
        time = int(timenum)
        await asyncio.sleep(time)
        for i in range(10) : 
          await user.send(f"Hey, you put a reminder for ||**{message}**||!")
      else : 
        await interaction.response.send_message("A wrong syntax again. Only *s* and *m* allowed!")

    else : 
      await interaction.response.send_message("Invalid time definition :(\nWhy not check the syntax using the help command?")

  except : 
    await interaction.channel.send("I think you wrote wrong syntax. If it's right, then I apologize, they may be some error going to with me :(\nYou can report it using the feedback command if it didn't work correctly.")

@client.tree.command(name="leetcodestats", description="Returns the leetcode stats of a user")
async def lcstats(interaction:discord.Interaction, username:str) :
  url = f"https://leetcode-stats-api.herokuapp.com/{username}"
  try:
    r = requests.get(url).json()
    if r["status"] != "success":
      await interaction.response.send_message("Kindly check if you provided the correct username, otherwise, this might just be an issue from the other side (It'll be fixed soon, else use `/feedback` to notify the creator).")
    if int(r["totalSolved"]) == 0:
      await interaction.response.send_message("Kindly provide the correct username.")
    else : 
      em = discord.Embed(title=f"LeetCode stats ({username})", color=interaction.user.color)
      em.add_field(name="Total Solved", value=f"{r["totalSolved"]} / {r["totalQuestions"]}", inline=False)
      em.add_field(name="Easy Solved:", value=r["easySolved"], inline=False)
      em.add_field(name="Medium Solved:", value=r["mediumSolved"], inline=False)
      em.add_field(name="Hard Solved:", value=r["hardSolved"], inline=False)
      em.add_field(name="Acceptance Rate:", value=r["acceptanceRate"], inline=False)
      em.add_field(name="Rank:", value=r["ranking"], inline=False)
      em.set_footer(text=f"Requested by {interaction.user.display_name}",icon_url=interaction.user.avatar)
      await interaction.response.send_message(embed=em)
  except Exception as e:
    print(e)
    await interaction.response.send_message("There might be some small issue from the server side. Kindly try again for a few times.")
    

#________________________________________________________________________________

# GAME COMMANDS
@app_commands.checks.cooldown(1, 3600*24, key=lambda i: (i.user.id))
@client.tree.command(name="dailylogin", description="Gives you currency every day")
async def dailylogin(interaction:discord.Interaction):
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  lvl = df.loc[place, "dailylevel"]
  extramess = ""
  if int(lvl/5) > 0 :
    df.loc[place, "purrgems"] += int(lvl/5)
    extramess = f"<:purrgem:1163086619348303902> Your daily level is {lvl}! You received **{int(lvl/5)}** gem(s)."
  df.loc[place, "purrcoins"] += 100+(lvl*10)
  df.to_csv("userdata/users.csv", index=False)
  await interaction.response.send_message(f"<:purrcoin:1163085791401103471> You got **{100+(lvl*10)}** purrcoins from your daily login!\n{extramess}")


@client.tree.command(name="profile", description="Shows your profile")
async def profile(interaction: discord.Interaction, member:typing.Optional[discord.Member]) : 
  if not member :
    member = interaction.user
  if member.bot : 
    await interaction.response.send_message("Bots cannot have profiles.", ephemeral=True)
  ff.setup(member.id, member.name)
  global wallpapers
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(member.id)
  df.loc[place, "username"] = member.name
  nn = df.loc[place, "nickname"]
  age = df.loc[place, "age"]
  gender = df.loc[place, "gender"]
  favpet = df.loc[place, "favpet"]
  bio = df.loc[place, "bio"]
  tfish = df.loc[place, "totalfishes"]
  wal = df.loc[place, "wallpaper"]
  col = int(df.loc[place, "embcolor"])
  dl = df.loc[place, "dailylevel"]
  fl = df.loc[place, "fishlevel"]

  em = discord.Embed(title="Profile", color=col)
  em.add_field(name="__User Name__", value=member.name, inline=False)
  em.add_field(name="__Nickname__", value=f"*{nn}*", inline=False)
  em.add_field(name="__Age__", value=f"*{age}*", inline=False)
  em.add_field(name="__Gender__", value=f"*{gender}*", inline=False)
  em.add_field(name="__Level__", value=f"*DailyLevel: {dl}\nFishLevel: {fl} *", inline=False)
  em.add_field(name="__Total Fishes caught__", value=f"*{tfish}*", inline=False)
  em.add_field(name="__Favorite Pet__", value=f"*{favpet}*", inline=False)
  em.add_field(name="__About Me__", value=f"*{bio}*", inline=False)
  em.set_image(url=wallpapers[wal])
  em.set_footer(text="You can change your details using /edit",icon_url=client.user.avatar)
  await interaction.response.send_message(embed=em)


@edit.command(name="nick", description="Use this command to edit your nickname in your profile")
@discord.app_commands.describe(val="New value to change the existing one")
async def chgname(interaction:discord.Interaction, val:str) : 
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  if len(val) > 20 : 
    await interaction.response.send_message("Your nickname cannot have more than 20 characters!", ephemeral=True)
  elif len(val) <= 2 : 
    await interaction.response.send_message("Your nickname is too short!", ephemeral=True)
  else : 
    df.loc[place, "nickname"] = val
    df.to_csv("userdata/users.csv", index=False)
    await interaction.response.send_message("Overwriting of data successful!", ephemeral=True)


@edit.command(name="age", description="Use this command to edit your age in your profile")
@discord.app_commands.describe(val="New value to change the existing one")
async def chgage(interaction:discord.Interaction, val:int) : 
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  if val <= 9 : 
    await interaction.response.send_message("Are you really that small? Stay away from discord if I suggest.", ephemeral=True)
  elif val >= 60 : 
    await interaction.response.send_message("Woah, woah. Are you a grandparent? Enter your real age if you are wanting to change it.", ephemeral=True)
  else : 
    df.loc[place, "age"] = val
    df.to_csv("userdata/users.csv", index=False)
    await interaction.response.send_message("Overwriting of data successful!", ephemeral=True)


@edit.command(name="about", description="Use this command to edit your about section in your profile")
@discord.app_commands.describe(val="New value to change the existing one")
async def chgabout(interaction:discord.Interaction, val:str) : 
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  if len(val) > 100 : 
    await interaction.response.send_message("Isn't it too lengthy? Don't go on typing your autobiography.", ephemeral=True)
  elif len(val) <= 2 : 
    await interaction.response.send_message("Why are you even bothering to type that :skull:. At least type something more about yourself.", ephemeral=True)
  else : 
    df.loc[place, "bio"] = val
    df.to_csv("userdata/users.csv", index=False)
    await interaction.response.send_message("Overwriting of data successful!", ephemeral=True)


@edit.command(name="pet", description="Use this command to edit your fav pet in Purrbot")
@discord.app_commands.describe(val="New value to change the existing one")
@app_commands.choices(val=[
  app_commands.Choice(name="Rabbit", value=1),
  app_commands.Choice(name="Cat", value=2),
  app_commands.Choice(name="Panda", value=3),
  app_commands.Choice(name="Hamster", value=4),
  app_commands.Choice(name="Dog", value=5)
])
async def chgpet(interaction:discord.Interaction, val:discord.app_commands.Choice[int]):
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  df.loc[place, "favpet"] = val.name
  df.to_csv("userdata/users.csv", index=False)
  await interaction.response.send_message("Overwriting of data successful!", ephemeral=True)


@edit.command(name="gender", description="Change the gender value in your profile")
@discord.app_commands.describe(val="New value to change the existing one")
@app_commands.choices(val=[
  app_commands.Choice(name="Male", value=1),
  app_commands.Choice(name="Female", value=2),
  app_commands.Choice(name="Prefer not to say", value=3)
])
async def chggen(interaction:discord.Interaction, val:discord.app_commands.Choice[int]) :
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  df.loc[place, "gender"] = val.name
  df.to_csv("userdata/users.csv", index=False)
  await interaction.response.send_message("Overwriting of data successful!", ephemeral=True)


@edit.command(name="picture", description="Change the wallpaper of your profile")
@discord.app_commands.describe(val="New value to change the existing one")
@app_commands.choices(val=[
  app_commands.Choice(name="Default", value=1),
  app_commands.Choice(name="Christmas Wallpaper", value=2),
  app_commands.Choice(name="Purrbot Wallpaper", value=3),
  app_commands.Choice(name="Anime Wallpaper", value=4),
  app_commands.Choice(name="Batman Wallpaper", value=5),
  app_commands.Choice(name="Superman Wallpaper", value=6),
  app_commands.Choice(name="Spiderman Wallpaper", value=7),
  app_commands.Choice(name="Ironman Wallpaper", value=8),
  app_commands.Choice(name="Landscape Wallpaper", value=9),
  app_commands.Choice(name="Valentines Wallpaper1", value=10),
  app_commands.Choice(name="Valentines Wallpaper2", value=11)
])
async def chgwall(interaction:discord.Interaction, val:discord.app_commands.Choice[int]) : 
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  if val.name == "Default" : 
    df.loc[place, "wallpaper"] = "Not Set"
  else : 
    inv = ff.openinv(interaction.user.id)
    if val.name in inv : 
      df.loc[place, "wallpaper"] = val.name
      await interaction.response.send_message("Overwriting of data successful!", ephemeral=True)
    else : 
      await interaction.response.send_message("You don't have this wallpaper in your inventory! Buy it from the shop please.", ephemeral=True)
  df.to_csv("userdata/users.csv", index=False)


@edit.command(name="color", description="Change the embed color of your profile")
@discord.app_commands.describe(val="New value to change the existing one")
@app_commands.choices(val=[
  app_commands.Choice(name="black", value=0),
  app_commands.Choice(name="green", value=0x2ecc71),
  app_commands.Choice(name="blue", value=0x3498db),
  app_commands.Choice(name="purple", value=0x9b59b6),
  app_commands.Choice(name="gold", value=0xf1c40f),
  app_commands.Choice(name="orange", value=0xe67e22),
  app_commands.Choice(name="red", value=0xe74c3c),
  app_commands.Choice(name="grey", value=0x95a5a6),
  app_commands.Choice(name="teal", value=1752220),  
  app_commands.Choice(name="darkgreen", value=0x1f8b4c),
  app_commands.Choice(name="darkred", value=10038562),
  app_commands.Choice(name="magenta", value=0xe91e63),
  app_commands.Choice(name="darkblue", value=0x206694), 
  app_commands.Choice(name="darkgrey", value=0x546e7a)
])
async def chgcol(interaction:discord.Interaction, val:discord.app_commands.Choice[int]) :
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  df.loc[place, "embcolor"] = val.value
  df.to_csv("userdata/users.csv", index=False)
  await interaction.response.send_message("Overwriting of data successful!", ephemeral=True)


@client.tree.command(name="balance", description="Shows your balance")
async def balance(interaction:discord.Interaction):
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  coins = df.loc[place, "purrcoins"]
  gems = df.loc[place, "purrgems"]

  em = discord.Embed(title="BALANCE", description=f"<:purrcoin:1163085791401103471> **Purrcoins** : {coins}\n\n<:purrgem:1163086619348303902> **Purrgems** : {gems}", color=interaction.user.color)
  await interaction.response.send_message(embed=em)


@client.tree.command(name="leaderboard", description= "Shows the top 20 leaderboard on 'basis' globally.")
@app_commands.choices(basis=[
  app_commands.Choice(name="dailylevel", value=1),
  app_commands.Choice(name="purrgems", value=2),
  app_commands.Choice(name="purrcoins", value=3),
  app_commands.Choice(name="fishlevel", value=4),
  app_commands.Choice(name="totalfishes", value=5),
  app_commands.Choice(name="supreme", value=6),
  app_commands.Choice(name="epic", value=7),
  app_commands.Choice(name="premium", value=8),
])
async def leaderboard(interaction:discord.Interaction, basis:app_commands.Choice[int]) :
  df = pd.read_csv("userdata/users.csv") 
  board = df.sort_values(by=basis.name, ascending=False).head(10)
  board = board[["username", basis.name]].to_string(index=False)
  await interaction.response.send_message(f"`{board}`")


@app_commands.checks.cooldown(1, 30, key=lambda i: (i.user.id))
@client.tree.command(name="search", description="Search for some purrcoins")
async def search(interaction:discord.Interaction):
  chances = [20, 30, 50, 20, 0, 0, 20, 30, 0]
  chance = random.choice(chances)
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  if chance == 0 :
    await interaction.response.send_message("You searched and found nothing :(")
  else : 
    await interaction.response.send_message(f"<:purrcoin:1163085791401103471> You searched and found **{chance}** purrcoins! <:purrcoin:1163085791401103471>")
    df.loc[place, "purrcoins"] += chance
    df.to_csv("userdata/users.csv", index=False)


@app_commands.checks.cooldown(1, 5, key=lambda i: (i.user.id))
@client.tree.command(name="steal", description="You get 50% more purrcoins but have a chance to lose some.")
async def steal(interaction:discord.Interaction):
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)

  if df.loc[place, "purrcoins"] > 50 : 
    chances = [60,70,-80,60,-60,60,70,80,90,90,100,-50,-50,70,80,-70,-90]
    chance = random.choice(chances)
    df.loc[place, "purrcoins"] += chance
    df.to_csv("userdata/users.csv", index=False)
    if chance < 0 : 
      await interaction.response.send_message(f"<:purrcoin:1163085791401103471> You tried to steal but got caught and lost **{chance}** purrcoins <:purrcoin:1163085791401103471>")
    else : 
      await interaction.response.send_message(f"<:purrcoin:1163085791401103471> You slyly stole **{chance}** purrcoins! <:purrcoin:1163085791401103471>")
  else : 
    await interaction.response.send_message("You should have at least 50 purrcoins to steal!", ephemeral=True)


@app_commands.checks.cooldown(1, 30, key=lambda i: (i.user.id))
@client.tree.command(name="research", description="Research on new techniques to get more purrcoins in daily login or get more fishes.")
@app_commands.choices(leveltype=[
  app_commands.Choice(name="dailylevel", value=1),
  app_commands.Choice(name="fishlevel", value=2)
])
async def research(interaction:discord.Interaction, leveltype:discord.app_commands.Choice[int]):
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  money = df.loc[place, "purrcoins"]
  level = df.loc[place, leveltype.name]
  if leveltype.name == "dailylevel" : 
    cost = int(1000*0.5*level)
    if money < cost :
      await interaction.response.send_message(f"You don't have enough purrcoins to research! Earn {cost} then you can research to level up your daily.")
    elif money > cost : 
      chance = bool(random.randint(0, 1))
      df.loc[place, "purrcoins"] -= cost
      if not chance : 
        df.to_csv("userdata/users.csv", index=False)
        await interaction.response.send_message("You researched but found nothing sadly.......")
      else: 
        df.loc[place, "dailylevel"] += 1
        df.to_csv("userdata/users.csv", index=False)
        await interaction.response.send_message(f"The research is a success! Your daily level has been upgraded to **Level {level+1}**")
  else : 
    cost = int(1000*1.5*level)
    if money < cost :
      await interaction.response.send_message(f"You don't have enough purrcoins to research! Earn {cost} then you can research to level up your fishing.")
    elif money > cost : 
      df.loc[place, "purrcoins"] -= cost
      df.loc[place, "fishlevel"] += 1
      df.to_csv("userdata/users.csv", index=False)
      await interaction.response.send_message(f"You researched with the cost of {cost} purrcoins! Your fishing level has been upgraded to **Level {level+1}**")


@client.tree.command(name="shop", description="Check available items to buy")  
async def shop(interaction:discord.Interaction):
  with open("data/shop.json") as f:
    items = json.load(f)
  col = discord.Color.random()
  em1 = discord.Embed(title="Shop", color=col)
  if len(items) > 25 :
    for i in range(25) : 
      em1.add_field(name=str(i)+". "+items[i]["itemname"], value=f"<:purrcoin:1163085791401103471> **{items[i]["price"]}**", inline=False)
    await interaction.response.send_message(embed=em1)

    em1 = discord.Embed(color=col)
    for i in range(25, len(items["name"])) : 
      em1.add_field(name=str(i)+". "+items[i]["itemname"], value=f"<:purrcoin:1163085791401103471> **{items[i]["price"]}**", inline=False)
    await interaction.channel.send(embed=em1)
  else :
    for i in range(len(items)) : 
      em1.add_field(name=str(i)+". "+items[i]["itemname"], value=f"<:purrcoin:1163085791401103471> **{items[i]["price"]}**", inline=False)
    await interaction.response.send_message(embed=em1)

@client.tree.command(name="buy", description="Buy an item from the shop")
async def buyitem(interaction:discord.Interaction, itemid:int, quantity:typing.Optional[int]=1) : 
  if quantity <=0:
    await interaction.response.send_message("Quantity must be greater than 0.")
    return
  elif quantity > 1000 : 
    await interaction.response.send_message("Quantity should be lower than 1000 -.-")
  elif itemid<0:
    await interaction.response.send_message("Negative itemID provided!")
  try : 
    with open("data/shop.json") as f :
      items = json.load(f)
      itemname = items[itemid]["itemname"]
    itemlist = ff.openinv(interaction.user.id)
    if itemname in itemlist : 
      await interaction.response.send_message(f"You already have {itemname} in your inventory!")
    
    df = pd.read_csv("userdata/users.csv")
    place = ff.userindex(interaction.user.id)
    money = df.loc[place, "purrcoins"]
    if "Wallpaper" in itemname and quantity != 1 : 
      quantity = 1
      sen = f"Wallpapers are bought only once. Hence, you only bought 1 {itemname} for <:purrcoin:1163085791401103471> **{itemcost}**!" 

    itemcost = items[itemid]["price"]*quantity
    if money < itemcost :
      await interaction.response.send_message(f"You need {itemcost-money} purrcoins to buy {quantity} {itemname}!")

    else :
      sen = f"You bought {quantity} {itemname} for <:purrcoin:1163085791401103471> **{itemcost}**!"
      df.loc[place, "purrcoins"] -= itemcost
      if itemid == 0 : 
        df.loc[place, "baits"] += quantity
        df.to_csv("userdata/users.csv", index=False)
      else :
        with open("userdata/inventory.json") as f:
          data = json.load(f)
          data[str(interaction.user.id)].append(itemname)
        with open("userdata/inventory.json", "w") as f :
          json.dump(data, f, indent=2)
      await interaction.response.send_message(sen)
  except IndexError :
    await interaction.response.send_message("Wrong number of item. That doesn't exist in shop!")


@client.tree.command(name="inventory", description="View your inventory")
async def invento(interaction:discord.Interaction) : 
  items = ff.openinv(interaction.user.id)
  df = pd.read_csv("userdata/users.csv").query(f"id=={interaction.user.id}").reset_index()
  if df.empty :
    await interaction.response.send_message("You haven't opened your profile yet!\nUse `/profile` to open one and then run this command.")
  baits = df.loc[0, "baits"]
  em1 = discord.Embed(title=f"{interaction.user.name}'s Inventory", color=discord.Color.random())
  if len(items) == 0 :
    em1.add_field(name="There is no item in your inventory :(\n Buy something from the shop.", value="")
  else: 
    for index, itemname in enumerate(items) : 
      em1.add_field(name=f"{index+1}. {itemname}", value="", inline=False)
  em1.add_field(name="", value="", inline=False)
  em1.add_field(name="", value="", inline=False)
  em1.add_field(name=f"<:bait:1185874134417281164> baits x **{baits}**", value="", inline=False)
  await interaction.response.send_message(embed=em1)


@client.tree.command(name="use", description="Use an item from your inventory")
async def useitem(interaction:discord.Interaction, item:int) :
  item -= 1
  inven = ff.openinv(interaction.user.id)
  if len(inven) == 0 : 
    await interaction.response.send_message("You don't have any items in your inventory!")
  elif item > len(inven) : 
    await interaction.response.send_message("That item doesn't exist in your inventory!")
  else : 
    itemname = inven[item].title()
    if itemname.endswith("Wallpaper") : 
      await interaction.response.send_message("It is a wallpaper for your profile! You can use it by `/editprofile picture`.")


@client.tree.command(name="share", description="give your friends some of your money.")
async def share(interaction:discord.Interaction, member:discord.Member, amount:int) :
  if member.bot : 
    await interaction.response.send_message("Why are you giving your money to a bot?")
  if interaction.user.id == member.id :
    await interaction.response.send_message("Are you trying to send money to yourself? For real?", ephemeral=True)
  
  ff.setup(interaction.user.id, interaction.user.name)
  ff.setup(member.id, member.name)
  df = pd.read_csv("userdata/users.csv")
  placeuser = ff.userindex(interaction.user.id)
  moneyuser = df.loc[placeuser, "purrcoins"]
  if moneyuser <= 0 :
    await interaction.response.send_message("You don't have any money lol. Earn when")
  elif moneyuser < amount :
    await interaction.response.send_message("You don't have enough money to share!")
  else :
    df.loc[placeuser, "purrcoins"] -= amount
    df.loc[ff.userindex(member.id), "purrcoins"] += amount
    df.to_csv("userdata/users.csv", index=False)
    await interaction.response.send_message(f"You gave <:purrcoin:1163085791401103471>{amount} to {member.name}!")


@client.tree.command(name="gamble", description="Are you going for profit or loss?")
async def gam(interaction:discord.Interaction, amount:int) :
  if amount < 100 :
    await interaction.response.send_message("You should have at least <:purrcoin:1163085791401103471> 100 to gamble!")
  else : 
    df = pd.read_csv("userdata/users.csv")
    place = ff.userindex(interaction.user.id)
    if df.loc[place, "purrcoins"] < amount:
      await interaction.response.send_message("You don't have that much money!")
    else:
      chance = bool(random.randint(0, 1))
      if chance :
        df.loc[place, "purrcoins"] += amount
        await interaction.response.send_message(f"You **won** <:purrcoin:1163085791401103471>{amount}!")
      else : 
        df.loc[place, "purrcoins"] -= amount
        await interaction.response.send_message(f"You **lost** <:purrcoin:1163085791401103471>{amount}!")
      df.to_csv("userdata/users.csv", index=False)


@client.tree.command(name="fish", description="Go fishing and get some fish!")
async def fish(interaction:discord.Interaction) :
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  level = df.loc[place, "fishlevel"]
  baits = df.loc[place, "baits"]

  if baits < 1 : 
    await interaction.response.send_message(f"You don't have enough baits! You need at least {level+2-baits} more baits to continue fishing!")
    return
  if baits-(level+2) < 0 :
    await interaction.response.send_message(f"You don't have enough baits! You need at least {level+2-baits} more baits to continue fishing!")
    return
  fish = ["basic", "regular", "elite", "premium", "epic", "supreme"]
  fish_chance = [0.9, 0.5*(level/10), 0.2*(level/10), 0.13*(level/10), 0.02*(level/10), 0.008*(level/10)]
  caught = {fish[0]:0, fish[1]:0, fish[2]:0, fish[3]:0, fish[4]:0, fish[5]:0}
  caughtlist = random.choices(fish, weights=fish_chance, k=level+2)
  df.loc[place, "baits"] -= level+2
  for f in caughtlist :
    df.loc[place, f] += 1
    df.loc[place, "totalfishes"] += 1
    caught[f] += 1
  df.to_csv("userdata/users.csv", index=False)
  await interaction.response.send_message(f"You caught:\n<:basic:1185599289368526898> **{caught['basic']}** basic fish\n<:regular:1185599334310490123> **{caught['regular']}** regular fish\n<:elite:1185599299451617372> **{caught['elite']}** elite fish\n<:premium:1185599320276340806> **{caught['premium']}** premium fish\n<:epic:1185599310356820048> **{caught['epic']}** epic fish\n<:supreme:1185599340622925974> **{caught['supreme']}** supreme fish")


@client.tree.command(name="bucket", description="Shows you the total number of fishes that you have caught.")
async def bucket(interaction:discord.Interaction) :
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  basic = df.loc[place, "basic"]
  regular = df.loc[place, "regular"]
  elite = df.loc[place, "elite"]
  premium = df.loc[place, "premium"]
  epic = df.loc[place, "epic"]
  supreme = df.loc[place, "supreme"]
  em = discord.Embed(title=f"{interaction.user.name}'s Bucket")
  em.add_field(name="Basic <:basic:1185599289368526898>", value=basic)
  em.add_field(name="Regular <:regular:1185599334310490123>", value=regular, inline=False)
  em.add_field(name="Elite <:elite:1185599299451617372>", value=elite, inline=False)
  em.add_field(name="Premium <:premium:1185599320276340806>", value=premium, inline=False)
  em.add_field(name="Epic <:epic:1185599310356820048>", value=epic, inline=True)
  em.add_field(name="Supreme <:supreme:1185599340622925974>", value=supreme, inline=False)
  await interaction.response.send_message(embed=em)


@client.tree.command(name="sellfish", description="sell caught fishes and earn money!")
@discord.app_commands.describe(tier="The tier of fish you want to sell.")
@app_commands.choices(tier=[
  app_commands.Choice(name="basic", value=1),
  app_commands.Choice(name="regular", value=2),
  app_commands.Choice(name="elite", value=3),
  app_commands.Choice(name="premium", value=4),
  app_commands.Choice(name="epic", value=5),
  app_commands.Choice(name="supreme", value=6),
  app_commands.Choice(name="all", value=7)
])
async def sellf(interaction: discord.Interaction, tier:discord.app_commands.Choice[int]) : 
  global fish_price
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  if tier.name != "all" : 
    if df.loc[place, tier.name] == 0 : 
      await interaction.response.send_message(f"You don't have any {tier.name} fish to sell!")
      return

    if tier.name == "basic" :
      amount = df.loc[place, "basic"]
      cost = fish_price["basic"]
    elif tier.name == "regular" :
      amount = df.loc[place, "regular"]
      cost = fish_price["regular"]
    elif tier.name == "elite" :
      amount = df.loc[place, "elite"]
      cost = fish_price["elite"]
    elif tier.name == "premium" :
      amount = df.loc[place, "premium"]
      cost = fish_price["premium"]
    elif tier.name == "epic" :
      amount = df.loc[place, "epic"]
      cost = fish_price["epic"]
    elif tier.name == "supreme" :
      amount = df.loc[place, "supreme"]
      cost = fish_price["supreme"]

    money = amount * cost
    df.loc[place, "purrcoins"] += money
    df.loc[place, tier.name] = 0
    df.to_csv("userdata/users.csv", index=False)
    await interaction.response.send_message(f"You sold {tier.name} tier fish and received {money} purrcoins!")
  else :
    basic = df.loc[place, "basic"] 
    regular = df.loc[place, "regular"] 
    elite = df.loc[place, "elite"] 
    premium = df.loc[place, "premium"] 
    epic = df.loc[place, "epic"] 
    supreme = df.loc[place, "supreme"]
    total = basic*fish_price["basic"] + regular*fish_price["regular"] + elite*fish_price["elite"] + premium*fish_price["premium"] + epic*fish_price["epic"] + supreme*fish_price["supreme"]
    df.loc[place, "purrcoins"] += total
    df.loc[place, "basic"] = 0
    df.loc[place, "regular"] = 0
    df.loc[place, "elite"] = 0
    df.loc[place, "premium"] = 0
    df.loc[place, "epic"] = 0
    df.loc[place, "supreme"] = 0
    df.to_csv("userdata/users.csv", index=False)
    if total == 0 : 
      await interaction.response.send_message("You don't have any fishes in your bucket right now :(\nCatch them using `/fish` command")
    else : 
      await interaction.response.send_message(f"You sold all your fishes and received {total} purrcoins!")


@client.tree.command(name="fishinfo" , description="Shows information about fishes tier.")
@app_commands.choices(tier=[
  app_commands.Choice(name="basic", value=1),
  app_commands.Choice(name="regular", value=2),
  app_commands.Choice(name="elite", value=3),
  app_commands.Choice(name="premium", value=4),
  app_commands.Choice(name="epic", value=5),
  app_commands.Choice(name="supreme", value=6)
])
async def finfo(interaction:discord.Interaction, tier:app_commands.Choice[int]) :
  df = pd.read_csv("userdata/users.csv")
  place = ff.userindex(interaction.user.id)
  quan = df.loc[place, tier.name]
  if tier.name == "basic" : 
    t = "Basic Fish <:basic:1185599289368526898>"
    d = "They are the most common found. They can be sold for <:purrcoin:1163085791401103471>**10**."
  elif tier.name == "regular" :
    t = "Regular Fish <:regular:1185599334310490123>"
    d = "They are the second most common found after the basic fishes. They can be sold for <:purrcoin:1163085791401103471>**50**."
  elif tier.name == "elite" :
    t = "Elite Fish <:elite:1185599299451617372>"
    d = "Not that common, but are worthy and comes in Tier 3 of fishes. Can be sold for <:purrcoin:1163085791401103471>**100**."
  elif tier.name == "premium" :
    t = "Premium Fish <:premium:1185599320276340806>"
    d = "They are worth a lot of purrcoins, coming in Tier 4. They are rarely found and can be sold in <:purrcoin:1163085791401103471>**250**."
  elif tier.name == "epic" :
    t = "Epic Fish <:epic:1185599310356820048>"
    d = "Epic like there names, these fishes are Tier 5, coming after Premium Fishes. They are extremely rare and can be sold in <:purrcoin:1163085791401103471>**800**."
  elif tier.name == "supreme <:supreme:1185599340622925974>" :
    t = "Supreme Fish"
    d = "Hardly found, these fishes are Tier 6 fishes and their chances of getting found is increased by researching on fishlevel. Worth <:purrcoin:1163085791401103471>**2500**, even 3 of them are enough to become rich."

  em = discord.Embed(title=t, description=d, color=discord.Color.random())
  em.add_field(name="", value=f"You have `{quan}` in your bucket.")
  await interaction.response.send_message(embed=em)


@client.tree.command(name="item", description="gives you information about an item")
@discord.app_commands.describe(item="The item you want to know about")
@app_commands.choices(item=[
  app_commands.Choice(name="Christmas Wallpaper", value=1),
  app_commands.Choice(name="Purrbot Wallpaper", value=2),
  app_commands.Choice(name="Anime Wallpaper", value=3),
  app_commands.Choice(name="Batman Wallpaper", value=4),
  app_commands.Choice(name="Superman Wallpaper", value=5),
  app_commands.Choice(name="Spiderman Wallpaper", value=6),
  app_commands.Choice(name="Ironman Wallpaper", value=7),
  app_commands.Choice(name="Landscape Wallpaper", value=8),
  app_commands.Choice(name="Valentines Wallpaper1", value=9),
  app_commands.Choice(name="Valentines Wallpaper2", value=10),
  app_commands.Choice(name="Bait", value=9),
])
async def iteminfo(interaction:discord.Interaction, item:discord.app_commands.Choice[int]) :
  with open("data/shop.json") as f:
    items = json.load(f)
  for i in range(items):
    if items[i]["itemname"] == item.name: 
      break
  em = discord.Embed(title=item.name, description=items[i]["description"], color=discord.Color.random())
  if "Wallpaper" in item.name : 
    em.set_image(url=wallpapers[item.name])
    em.set_footer(text=f"Price: {items[i]["price"]} purrcoins")
  await interaction.response.send_message(embed = em)

#______________________________________FUN________________________________________

@client.tree.command(name="fact", description="Wanna know a fact?")
async def fact(interaction: discord.Interaction):
  api_url = 'https://api.api-ninjas.command/v1/facts?limit=1'
  response = requests.get(
    api_url, headers={'X-Api-Key': 'FEnW6LZPfHjmtNGdRtihvA==VRaEObBqXKoHkwIB'})
  if response.status_code == requests.codes.ok:
    resultt = (response.json()[0]["fact"])
  else:
    resultt = ("Error from the server!")
  await interaction.response.send_message(resultt, ephemeral=False)


@client.tree.command(name="echo", description="Makes the bot repeat a message that you entered")
@discord.app_commands.describe(msg="word or sentence, that the bot should repeat")
async def echo(interaction: discord.Interaction, msg: str):
  await interaction.channel.send(msg)
  asyncio.sleep(1)
  await interaction.response.send_message("Done :>", ephemeral=True)


@client.tree.command(name="pet", description="Do you like cute animals? :>")
@discord.app_commands.describe(pets="Select your pet from the above options")
@app_commands.choices(pets=[
  app_commands.Choice(name="Rabbit", value=1),
  app_commands.Choice(name="Cat", value=2),
  app_commands.Choice(name="Panda", value=3),
  app_commands.Choice(name="Hamster", value=4),
  app_commands.Choice(name="Dog", value=5)
])
async def pet(interaction: discord.Interaction, pets:discord.app_commands.Choice[int]):
  with open("data/animals.json") as f:
    pet_json = json.load(f)
  if pets.name == "Cat":
    em = discord.Embed(title=f"{interaction.user.name} orders for a cat 🐱", color=0xe67e22)
  elif pets.name == "Dog":
    em = discord.Embed(title=f"{interaction.user.name} gets a dog!", color=0xe74c3c)
  elif pets.name == "Panda":
    em = discord.Embed(title=f"{interaction.user.name} is having a panda! So cute >.<", color=interaction.user.color)
  elif pets.name == "Hamster" : 
    em = discord.Embed(title=f"{interaction.user.name}, here is your cute hamster. Doesn't it look really cute (≧∀≦)ゞ", color=0x9b59b6)
  elif pets.name == "Rabbit" : 
    em = discord.Embed(title=f"Here's a cute bunny for ya, {interaction.user.name}!", color=0x2ecc71)
    
  petName = pets.name.lower()
  print(random.choice(pet_json[petName]))
  em.set_image(url=random.choice(pet_json[petName]))
  em.set_footer(text="Hope you are happy now :D")
  await interaction.response.send_message(embed=em, ephemeral=False)


@client.tree.command(name="pick1", description="Randomly chooses an object from the given options")
@discord.app_commands.describe(option1="type your first option", option2="type your second option")
async def pick(interaction: discord.Interaction, option1: str, option2: str):
  await interaction.response.send_message(f"I choose **{random.choice([option1, option2])}** 🙋‍♂️", ephemeral=False)


@client.tree.command(name="8ball", description="Ask a question and get an answer from the bot!")
@discord.app_commands.describe(question="Enter your question")
async def ball(interaction: discord.Interaction, question: str):
  if question.endswith("?") == False:
    question = f"{question}?"
  aww = random.choice(answer_me)
  em = discord.Embed(title="Your question :", description=f"{question}?", color=interaction.user.color)
  em.add_field(name="My Response :", value=aww)
  em.set_footer(text=f"Asked by {interaction.user.name}")
  await interaction.response.send_message(embed=em, ephemeral=False)


@client.tree.command(name="diceroll", description="Rolls out a dice for you")
async def rolldice(interaction: discord.Interaction):
  await interaction.response.send_message(
    "Rolling....... <a:roll_dice:1028655608016142409>")
  await interaction.edit_original_response(content=f"You rolled a {random.randint(1,6)}!")


@client.tree.command(name="toss", description="Why not toss a coin and let it decide?")
@discord.app_commands.describe(side="Will it be Heads or will it be Tails?")
@app_commands.describe(side="Choose a coin side")
@app_commands.choices(side=[
  app_commands.Choice(name="Heads", value=1),
  app_commands.Choice(name="Tails", value=2)
])
async def toss(interaction: discord.Interaction, side: discord.app_commands.Choice[int]):
  result = random.choice(["Heads", "Tails"])
  if side.name == result:
    await interaction.response.send_message(
      f"**{result}**! Damn, you won! ( •̀ ω •́ )✧", ephemeral=False)
  elif side.name != result:
    await interaction.response.send_message(
      f"**{result}**! Oops, looks like you lost 💔", ephemeral=False)

@client.tree.command(name="rate", description="rate anyone on the basis of anything you want")
@discord.app_commands.describe(member="Mention the member you wanna rate",arg="Type the quality on which you want the member to be rated (Eg - Coolness, Sweet, etc)")
async def rate(interaction: discord.Interaction, member: discord.Member, arg: str):
  per = random.randint(0, 100)
  urr = f"http://www.yarntomato.command/percentbarmaker/button.php?barPosition={per}&leftFill=%2366FFFF"
  em = discord.Embed(title=(f"{member}'s {arg} percentage is : "), color=interaction.user.color)
  em.set_image(url=urr)
  await interaction.response.send_message(embed=em)


@client.tree.command(name="randomnum", description="Generates random numbers from the given range by you")
@discord.app_commands.describe(startnum="From? (included in the generator)", endnum="To? (Included in the generator)")
async def rng(interaction: discord.Interaction, startnum: int, endnum: int):
  em = discord.Embed(title="RANDOM NUMBER GENERATOR", description=f"{random.randint(startnum, endnum)}", color=interaction.user.color)
  em.set_footer(text=f"~requested by {interaction.user.name}")
  await interaction.response.send_message(embed=em, ephemeral=False)


@client.tree.command(name="riddle", description="use this command to get a twisty riddle!")
async def rid(interaction:discord.Interaction) : 
  rid_url = 'https://api.api-ninjas.command/v1/riddles'
  r = requests.get(rid_url, headers={'X-Api-Key': 'FEnW6LZPfHjmtNGdRtihvA==VRaEObBqXKoHkwIB'})
  rdq = r.json()[0]["question"]
  rda = r.json()[0]["answer"]
  await interaction.response.send_message(rdq, view=RiddAns(str(rda)))


@client.tree.command(name="hiddendm", description="send a message to member dm")
@discord.app_commands.describe(member="Mention the person you want to send a dm.", message="the text you want to send to that person.")
async def dm(interaction:discord.Interaction, member:discord.Member, message:str) :
  await interaction.response.send_message(f"Your message has been sent to {member.name}!", ephemeral=True)
  await member.send(f"{interaction.user} has a message for you : ||{message}||")
  


@maths.command(name="add", description="sums up given numbers")
async def adding(interaction:discord.Interaction, nums:str
):
  nums = nums.split()
  result=0
  reslis = " + ".join(nums)
  try : 
    for i in nums :   
      result += float(i)
    await interaction.response.send_message(f"The result of `{reslis}` is **{result}**")
  except Exception as e :
    await interaction.response.send_message("There might be some error. You sure you wrote only numbers?")
    print(e)


@maths.command(name="multiply", description="Multiplies the numbers provided by the user")
async def multing(interaction:discord.Interaction, nums:str
):
  nums = nums.split()
  result=1
  reslis = " * ".join(nums)
  try : 
    for i in nums :   
      result *= float(i)
    await interaction.response.send_message(f"The result of `{reslis}` is **{result}**")
  except Exception as e :
    await interaction.response.send_message("There might be some error. You sure you wrote only numbers?")
    print(e)


@maths.command(name="subtract", description="Subtracts given numbers")
async def subtracting(interaction:discord.Interaction, nums:str
):
  nums = nums.split()
  result=float(nums[0])
  reslis = " - ".join(nums)
  nums.pop(0)
  try : 
    for i in nums : 
      result -= float(i)
    await interaction.response.send_message(f"The result of `{reslis}` is **{result}**")
  except Exception as e :
    await interaction.response.send_message("There might be some error. You sure you wrote only numbers?")
    print(e)


@maths.command(name="exponent", description="Calculates the number of some power")
@discord.app_commands.describe(num="type the exponent", power="power, the exponent should be raised to")
async def sq(interaction: discord.Interaction, num: int, power: int):
  z1 = num**power
  await interaction.response.send_message(f"{num} with the Power {power} = {z1}", ephemeral=False)


@maths.command(name="divide", description="divides a number by another number")
@discord.app_commands.describe(numerator="Known as dividend", denominator="Known as divisor")
async def divi(interaction: discord.Interaction, numerator: int, denominator: int):
  quot = numerator / denominator
  await interaction.response.send_message(f"{numerator} divided by {denominator} is {quot}", ephemeral=False)


@maths.command(name="factorial", description="returns the factorial series of a given number")
@discord.app_commands.describe(num="Factorial of which number?")
async def facto(interaction: discord.Interaction, num: int):
  ab = 1
  if num > 0:
    for jk in range(1, num + 1):
      ab = ab * jk
    await interaction.response.send_message(f"The factorial of {num} number is **{ab}**.", ephemeral=False)
  else:
    await interaction.response.send_message("The given number should be greater than 0", ephemeral=True)


@maths.command(name="shapes", description="to calculate area and volume of many shapes")
@discord.app_commands.describe(shape="Choose a shape", value="numbers for calculation, with space between 2 or more values")
@app_commands.choices(shape=[
  app_commands.Choice(name="Circle", value=1),
  app_commands.Choice(name="Square", value=2),
  app_commands.Choice(name="Rectangle", value=3),
  app_commands.Choice(name="Right Triangle", value=4),
  app_commands.Choice(name="Rhombus", value=5),
  app_commands.Choice(name="Trapezium", value=6),
  app_commands.Choice(name="Parallelogram", value=7),
  app_commands.Choice(name="Ellipse", value=8),
  app_commands.Choice(name="Cuboid", value=9),
  app_commands.Choice(name="Cube", value=10),
  app_commands.Choice(name="Sphere", value=11),
  app_commands.Choice(name="Cylinder", value=12),
  app_commands.Choice(name="Cone", value=13),
  ])
async def ar2(interaction:discord.Interaction, shape:discord.app_commands.Choice[int], value:str) : 
  val = value.split()
  em = discord.Embed(title="__AREA__", colour=0x00fbb4)
  if shape.name == "Circle" : 
    if len(val) == 1 : 
      r = float(val[0])
      area1 = 3.14 * r * r
      area2 = Fraction(f'{area1}')
      area3 = r*r
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Radius* = `{r}` unit", value="", inline=False)
      em.add_field(name="*Formula* = 𝝅r²", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value=f"Area (Decimal) = `{area1}` sq. units", inline=False)
      em.add_field(name="", value=f"Area (Fraction) = `{area2}` sq. units", inline=False)
      em.add_field(name="", value=f"Area (Pi) = `{area3}`𝝅 sq. units", inline=False)
      await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("Guess you entered more than 1 value. Enter values like this : `5.4` (radius)", ephemeral=True)

  if shape.name == "Square" : 
    if len(val) == 1 : 
      side = float(val[0])
      area = side * side
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Side* = `{r}` unit", value="", inline=False)
      em.add_field(name="*Formula* = Side x Side", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value=f"Area = `{area}` sq. units", inline=False)
      await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("If you know, the square has all equal sides so only 1 value is enough. Enter values like this : `9` (side)", ephemeral=True)

  if shape.name == "Rectangle" or shape.name == "Parallelogram" : 
    if len(val) == 2 : 
      length = float(val[0])
      breadth = float(val[1])
      area = length*breadth
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Length* = `{length}` unit", value="", inline=False)
      em.add_field(name=f"*Breadth* = `{breadth}` unit", value="", inline=False)
      em.add_field(name="*Formula* = length x breadth", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value=f"Area = `{area}` sq. units", inline=False)
      await interaction.response.send_message(embed=em)   
    else : 
      await interaction.response.send_message("Either you forgot that 2 values are required or maybe you entered more than 2 values. Enter values like this : `14 8`(base height)", ephemeral=True)

  if shape.name == "Right Triangle" : 
    if len(val) == 2 : 
      base = float(val[0])
      height = float(val[1])
      area = (base*height)/2
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Base* = `{base}` unit", value="", inline=False)
      em.add_field(name=f"*Height* = `{height}` unit", value="", inline=False)
      em.add_field(name="*Formula* = 1/2 x base x height", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value=f"Area = `{area}` sq. units", inline=False)
      await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("I think you are forgetting that only 2 values are required. Enter values like this `3 4` (base height)", ephemeral=True)

  if shape.name == "Rhombus" : 
    if len(val) == 2 : 
      d1 = float(val[0])
      d2 = float(val[1])
      area = (d1*d2)/2
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Diagonal 1* = `{d1}` unit", value="", inline=False)
      em.add_field(name=f"*Diagonal 2* = `{d2}` unit", value="", inline=False)
      em.add_field(name="*Formula* = 1/2 x (diagonal 1 x diagonal 2)", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value=f"Area = `{area}` sq. units", inline=False)
      await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("You have forgotten that there are only 2 values required for the rhombus! Enter values in this format : `2 3`(diagonal1 diagonal2)", ephemeral=True)

  if shape.name == "Trapezium" : 
    if len(val) == 3 : 
      b1 = float(val[0])
      b2 = float(val[1])
      h = float(val[2])
      area = 1/2*h*(b1+b2)
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Base 1* = `{b1}` unit", value="", inline=False)
      em.add_field(name=f"*Base 2* = `{b2}` unit", value="", inline=False)
      em.add_field(name="*Formula* = 1/2 x (base 1 + base 2) x height", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value=f"Area = `{area}` sq. units", inline=False)
      await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("Try the command again with sufficient values. Enter values in this format : `3 4 12`(base1 base2 height)", ephemeral=True)

  if shape.name == "Ellipse" : 
    if len(val) == 2 : 
      m1 = float(val[0])
      m2 = float(val[1])
      area1 = 3.14 * m1 * m2
      area2 = Fraction(f"{area1}")
      area3 = m1 * m2
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Major Radius* = `{m1}` unit", value="", inline=False)
      em.add_field(name=f"*Minor Radius* = `{m2}` unit", value="", inline=False)
      em.add_field(name="*Formula* = 𝝅 x major axis x minor axis", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="Area =", value=f"`{area1}` sq. units (in decimal)\n`{area2}` sq. units (in fraction)\n`{area3}`𝝅 sq. units (in pi)", inline=False)
      await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("Try the command again with sufficient values. Enter values in this format : `3 4 12`(base1 base2 height)", ephemeral=True)

  if shape.name == "Cuboid" : 
    if len(val) == 3 : 
      l = float(val[0])
      b = float(val[1])
      h = float(val[2])
      area_total = (2 * l * b) + (2 * l * h) + (2 * b * h)
      area_lateral = (l + b) * 2 * h
      volume = l * b * h
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Length* = `{l}` unit", value="", inline=False)
      em.add_field(name=f"*Breadth* = `{l}` unit", value="", inline=False)
      em.add_field(name=f"*Height* = `{h}` unit", value="", inline=False)
      em.add_field(name="*Formula (TSA)* = (2 x length x breadth) + (2 x length x height) + (2 x breadth x height)", value="", inline=False)
      em.add_field(name="*Formula (LSA)* = 2 x (length + breadth) x height", value="", inline=False)
      em.add_field(name="*Formula (volume)* = length x breadth x height", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value=f"Area (TSA) = `{area_total}` sq. units", inline=False)
      em.add_field(name="", value=f"Area (CSA) = `{area_lateral}` sq. units", inline=False)
      em.add_field(name="", value=f"Volume = `{volume}` sq. units", inline=False)
      await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("Only 3 values are needed. Enter values like this : `7 8 91` (length breadth height)", ephemeral=True)

  if shape.name == "Cube" : 
    if len(val) == 1 : 
        a = float(val[0])
        area_total = 6 * a * a
        area_lateral = 4 * a * a
        volume = a * a * a
        em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
        em.add_field(name=f"*Side* = `{a}` unit", value="", inline=False)
        em.add_field(name="*Formula (TSA)* = 6 x side x side", value="", inline=False)
        em.add_field(name="*Formula (LSA)* = 4 x side x side", value="", inline=False)
        em.add_field(name="*Formula (volume) = side * side * side")
        em.add_field(name="", value="", inline=False)
        em.add_field(name="", value="", inline=False)
        em.add_field(name="", value=f"Area (TSA) = `{area_total}` sq. units", inline=False)
        em.add_field(name="", value=f"Area (CSA) = `{area_lateral}` sq. units", inline=False)
        em.add_field(name="", value=f"Volume = `{volume}` sq. units", inline=False)
        await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("You need to enter only 1 value. Because cube has length, breadth and height of same size! Enter values like this : `4` (side)", ephemeral=True)

  if shape.name == "Sphere" :
    if len(val) == 1 : 
      r = float(val[0])
      area_total1 = 4 * 3.14 * r * r    
      area_total2 = Fraction(f'{area_total1}')
      area_total3 = 4 * r * r
      volume1 = (4/3) * 3.14 * r * r * r
      volume2 = Fraction(volume1)
      volume3 = (4/3) * r * r * r
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Radius* = `{r} unit`", value="", inline=False)
      em.add_field(name="*Formula (TSA)* = 4 x 𝝅 x radius x radius ", value="", inline=False)
      em.add_field(name="*Formula (volume)* = 4/3 x 𝝅 x radius x radius x radius", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="*Area (TSA) =", value=f"`{area_total1}` sq. units (in decimal)\n`{area_total2}` sq. units (in fraction)\n`{area_total3}`𝝅 sq. units (in pi)", inline=False)
      em.add_field(name="Volume =", value=f"`{volume1}` sq. units (in decimal)\n`{volume2}` sq. units (in fraction)\n`{volume3}`𝝅 sq. units (in pi)", inline=False)
      em.set_footer(text="*curved surface area is same as total surface area in sphere.")
      await interaction.response.send_message(embed=em)
    else : 
      await interaction.response.send_message("You need to enter only 1 value. Enter values like this : `6` (radius)", ephemeral=True)

  if shape.name == "Cylinder" : 
    if len(val) == 2 : 
      r = float(val[0])
      h = float(val[1])
      area_total1 = 2 * 3.14 * r * (r + h)
      area_total2 = Fraction(f'{area_total1}')
      area_total3 = 2 * r * (r + h)
      area_lateral1 = 2 * 3.14 * r * h
      area_lateral2 = Fraction(f'{area_lateral1}')
      area_lateral3 = 2 * r * h
      volume1 = 3.14 * r * r * h
      volume2 = Fraction(f'{volume1}')
      volume3 = r * r * h
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Radius* = `{r}` unit", value="", inline=False)
      em.add_field(name=f"*Height* = `{h}` unit", value="", inline=False)
      em.add_field(name="*Formula (TSA)* = 2 x 𝝅 x radius x (radius + height)", value="", inline=False)
      em.add_field(name="*Formula (CSA)* = 2 x 𝝅 x radius x height", value="", inline=False)
      em.add_field(name="*Formula (volume)* = 𝝅 x radius x radius x height", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="Area (TSA) =", value=f"`{area_total1}` sq. units (in decimals)\n`{area_total2}` sq.unit (in fraction)\n`{area_total3}`𝝅  sq. units (in pi)", inline=False)
      em.add_field(name="Area (CSA) =", value=f"`{area_lateral1}` sq. units (in decimals)\n`{area_lateral2}` sq.unit (in fraction)\n`{area_lateral3}`𝝅  sq. units (in pi)", inline=False)
      em.add_field(name="Volume =", value=f"`{volume1}` sq. units (in decimals)\n`{volume2}` sq.unit (in fraction)\n`{volume3}`𝝅  sq. units (in pi)", inline=False)
      await interaction.response.send_message(embed=em, ephemeral=False)
    else : 
        await interaction.response.send_message("Ayo, you need to provide 2 values which will be taken as radius and height.", ephemeral=True)

  if shape.name == "Cone" : 
    if len(val) == 2 : 
      r = float(val[0])
      l = float(val[1])
      area_total1 = 3.14 * r * (r + l)
      area_total2 = Fraction(f'{area_total1}')
      area_total3 = r * (r + l)
      area_lateral1 = 3.14 * r * l
      area_lateral2 = Fraction(f'{area_lateral1}')
      area_lateral3 = r * l
      volume1 = (1/3) * 3.14 * r * r * l
      volume2 = Fraction(f'{volume1}')
      volume3 = (1/3) * r * r * l
      em.add_field(name=f"*Shape* = `{shape.name}`", value="", inline=False)
      em.add_field(name=f"*Radius* = `{r}` unit", value="", inline=False)
      em.add_field(name=f"*Slant Height* = `{l}` unit", value="", inline=False)
      em.add_field(name="*Formula (TSA)* = 𝝅 x radius x (radius + slant height)", value="", inline=False)
      em.add_field(name="*Formula (CSA)* = 𝝅 x radius x slant height", value="", inline=False)
      em.add_field(name="*Formula (volume)* = 1/3 x 𝝅 x radius x radius x slant height", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="", value="", inline=False)
      em.add_field(name="Area (TSA) =", value=f"`{area_total1}` sq. units (in decimals)\n{area_total2} sq.unit (in fraction)\n`{area_total3}`𝝅  sq. units (in pi)", inline=False)
      em.add_field(name="Area (CSA) =", value=f"`{area_lateral1}` sq. units (in decimals)\n`{area_lateral2}` sq.unit (in fraction)\n`{area_lateral3}`𝝅  sq. units (in pi)", inline=False)
      em.add_field(name="Volume =", value=f"`{volume1}` sq. units (in decimals)\n`{volume2}` sq.unit (in fraction)\n`{volume3}`𝝅  sq. units (in pi)", inline=False)
      await interaction.response.send_message(embed=em, ephemeral=False)
    else : 
        await interaction.response.send_message("Ayo, you need to provide 2 values which will be taken as radius and height.", ephemeral=True)
        

@maths.command(name="sqroot", description="returns the square root of a number")
@discord.app_commands.describe(num="Any number from 0 to infinite (except fractions)")
async def aqqq(interaction:discord.Interaction, num:float) : 
  if num >= 0 : 
    rooot = math.sqrt(num)
    await interaction.response.send_message(f"The square root of number `{num}` is `{rooot}`")
  else : 
    await interaction.response.send_message("That's an invalid number!", ephemeral=True)


@maths.command(name="log10", description="returns the log of a number with base as 10")
@discord.app_commands.describe(num="Any number from 0 to infinity (except fractions)")
async def logari(interaction:discord.Interaction, num:float) : 
  if num >= 0 : 
    logarithm = math.log10(num)
    await interaction.response.send_message(f"log₁₀ of {num} is `{logarithm}`")
  else : 
    await interaction.response.send_message("That's an invalid number!")
    
#_______________________________ROLEPLAY_______________________________________

@client.tree.command(name="hug", description="Why not hug others to show affection?")
@discord.app_commands.describe(member="Mention the member you wanna hug")
async def slap(interaction: discord.Interaction, member: discord.Member):
  user_id = int(interaction.user.id)
  person_id = int(member.id)
  result = ff.increase_action_count("userdata/hug_count.json", user_id, person_id)
  hug_gif = requests.get("https://api.otakugifs.xyz/gif?reaction=hug")
  hug_gif = hug_gif.json()["url"]
  em = discord.Embed(title=f"__{interaction.user.name}__ hugs __{member.name}__", color=interaction.user.color)
  em.set_image(url=hug_gif)
  em.set_footer(text=f"You hugged {member.name} {result} time(s)!")
  await interaction.response.send_message(embed=em)


@client.tree.command(name="slap", description="Don't hold your anger, just slap and calm yourself down~")
@discord.app_commands.describe(member="Mention the member you wanna slap")
async def slap(interaction: discord.Interaction, member: discord.Member):
  user_id = int(interaction.user.id)
  person_id = int(member.id)
  result = ff.increase_action_count("userdata/slap_count.json", user_id, person_id)
  slap_gif = requests.get("https://api.otakugifs.xyz/gif?reaction=slap")
  slap_gif = slap_gif.json()["url"]
  em = discord.Embed(title=f"__{interaction.user.name}__ slaps __{member.name}__", color=interaction.user.color)
  em.set_image(url=slap_gif)
  em.set_footer(text=f"You slapped {member.name} {result} time(s)!")
  await interaction.response.send_message(embed=em)
  

@client.tree.command(name="pat", description="Everyone loves to be patted!")
@discord.app_commands.describe(member="Mention the member you want to pat")
async def pat(interaction: discord.Interaction, member: discord.Member):
  pat_gif = requests.get("https://api.otakugifs.xyz/gif?reaction=pat")
  pat_gif = pat_gif.json()["url"]
  em = discord.Embed(title=f"__{interaction.user.name}__ pats __{member.name}__", color=interaction.user.color)
  em.set_image(url=pat_gif)
  await interaction.response.send_message(embed=em)
  

@client.tree.command(name="wish", description="Would you like wish for someone close to you?")
@discord.app_commands.describe(member="Mention the member you wanna wish for", reason="The reason for what you are wishing for. (Ex - health, success, etc)")
async def wis(interaction:discord.Interaction, member:discord.Member, reason:typing.Optional[str]) : 
  user = interaction.user.name
  if reason : 
    await interaction.response.send_message(f"{user} prays for {member.name}'s {reason} <:prayerAngel:1118161249197371473>")
  else : 
    await interaction.response.send_message(f"{user} prays for {member.name} <:prayerAngel:1118161249197371473>")



#______________________________ADMIN____________________________________________

@client.tree.command(name="purge", description="Clears the number of messages and 5 is default!")
@app_commands.checks.has_permissions(manage_messages=True, manage_channels=True)
async def purg(interaction: discord.Interaction, number:typing.Optional[int]):
  if number != None : 
    if number > 50 : 
      await interaction.response.send_message("Hola dude. That's too many. Deletion of maximum 50 messages are allowed!", ephemeral=True)
    elif number <= 50 :
      await interaction.response.defer(ephemeral=True)
      await interaction.channel.purge(limit=number)
      await interaction.followup.send("Done!")
  else :
    number = 5
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=number)
    await interaction.followup.send("Done!")


@client.tree.command(name="kaboom", description="deletes a channel from the server")
@app_commands.checks.has_permissions(administrator=True)
async def boom(interaction:discord.Interaction, channel: discord.TextChannel):
    await interaction.response.send_message(f"The channel {channel} has been destroyed completely!")
    await channel.delete()


@client.tree.command(name="kick", description="Want to make someone leave the server?")
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction:discord.Interaction, member: discord.Member, reason:typing.Optional[str]):
  if reason == None : 
    reason = "(No reason given)"
    await interaction.response.send_message(f"{member} has been kicked.")
  else : 
    await interaction.response.send_message(f"{member} has been kicked due to {reason}.")
  await member.kick(reason=reason)


@client.tree.command(name="poll", description="A beautified way of creating a poll.")
@app_commands.checks.has_permissions(administrator=True)
@discord.app_commands.describe(emojis="Emojis need to add for reaction (with spaces)", header="Heading of the embedded Poll", content="Main question of the poll", footer="Footer of the embedded poll message")
async def pollio(interaction:discord.Interaction,content:str, emojis:str, header:typing.Optional[str], footer:typing.Optional[str]) :
  if header == None : 
    header = "**POLL**"
  emojis = emojis.split()
  em = discord.Embed(title=header, description=content, color=interaction.user.color)
  if footer != None : 
    em.set_footer(text=footer)
  msg = await interaction.channel.send(embed=em) 
  for i in emojis : 
    await msg.add_reaction(i)
  await interaction.response.send_message("The poll is ready!", ephemeral=True)
  
#_____________________________________________________________________________________

@purg.error
async def purgeerror(interaction, error) : 
  if isinstance(error, app_commands.MissingPermissions) : 
    await interaction.response.send_message("You don't have permissions of manage channels and manage messages!", ephemeral=True)
  elif isinstance(error, app_commands.BotMissingPermissions) : 
    await interaction.response.send_message("Well, looks like, you didn't give me enough permissions to do so.")
  else : 
    raise error

@boom.error
async def boomerror(interaction, error) : 
  if isinstance(error, app_commands.MissingPermissions) : 
    await interaction.response.send_message("You sure you are an adminstrator?", ephemeral=True)
  elif isinstance(error, app_commands.BotMissingPermissions) : 
    await interaction.response.send_message("Well, looks like, you didn't give me enough permissions to do so.")
  else : 
    raise error


@kick.error
async def kickerror(interaction, error) : 
  if isinstance(error, app_commands.MissingPermissions) : 
    await interaction.response.send_message("You don't have permissions, my friend. You need to be an adminstrator", ephemeral=True)
  elif isinstance(error, app_commands.BotMissingPermissions) : 
    await interaction.response.send_message("Well, looks like, you didn't give me enough permissions to do so.")
  else : 
    raise error


@pollio.error
async def polioerror(interaction, error) : 
  if isinstance(error, app_commands.MissingPermissions) : 
    await interaction.response.send_message("You don't have permissions for adminstrator, my friend.", ephemeral=True)
  elif isinstance(error, app_commands.BotMissingPermissions) : 
    await interaction.response.send_message("Well, looks like, you didn't give me enough permissions to do so.")
  else : 
    raise error

@research.error
async def research_error(interaction:discord.Interaction, error):
  if isinstance(error, app_commands.errors.CommandOnCooldown):
    tim = int((float(f"{error.retry_after:.2f}"))/60)
    await interaction.response.send_message(f"You can use this command after {tim} minute(s)")

@steal.error
async def steal_error(interaction:discord.Interaction, error):
  if isinstance(error, app_commands.errors.CommandOnCooldown):
    seconds = float(f"{error.retry_after:.2f}")
    await interaction.response.send_message(f"You can use this command after {seconds:.2f} second(s)")

@search.error
async def search_error(interaction:discord.Interaction, error):
  if isinstance(error, app_commands.errors.CommandOnCooldown):
    seconds = float(f"{error.retry_after:.2f}")
    await interaction.response.send_message(f"You can use `search` every 30s. Next time, you can use it after {seconds:.2f} second(s)")

@dailylogin.error
async def dailylogin_error(interaction:discord.Interaction, error):
  if isinstance(error, app_commands.errors.CommandOnCooldown):
    seconds = float(f"{error.retry_after:.2f}")
    hours = (seconds/60)/60
    await interaction.response.send_message(f"Your next login reward will be available in {hours:.2f} hour(s)")


# FIX SPAMSTOP COMMAND BECAUSE IT STOPS THE SPAMS IN OTHER SERVERS TOO 



client.run("ODYzNDkwMTE5OTc2ODc4MDkw.YOnp1w.0edvYFhnfhDXVF4jyBAHUGu46rM")
