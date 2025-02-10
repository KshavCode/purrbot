#IMPORTING
import discord
from discord import app_commands
from discord.ext import commands, tasks
import random, pandas as pd, requests, asyncio, typing, math, json, os
from itertools import cycle
from fractions import Fraction

pd.options.mode.chained_assignment = None


# FUNCTIONS 
def setup(userid:int, author) : 
  if not os.path.exists("userdata/users.csv") : 
    df = pd.DataFrame({"id":[], "purrcoins":[], "purrgems":[], "dailylevel":[], "username":[], "nickname":[], "favpet":[], "age":[], "gender":[],"bio":[], "wallpaper":[],"embcolor":[], "basic" : [], "regular" : [], "elite" : [], "premium" : [], "epic" : [], "supreme" : [], "fishlevel":[], "baits":[], "totalfishes":[]})
    df.to_csv("userdata/users.csv", index=False)
  if not os.path.exists("userdata/inventory.json") : 
    with open("userdata/inventory.json", "w") as f : 
      f.write("[]")
  df = pd.read_csv("userdata/users.csv")
  with open("userdata/inventory.json") as f : 
    datafile = json.load(f)
  if userid not in df["id"].values :
    newdf = pd.DataFrame({"id":[userid], "purrcoins":[1000], "purrgems":[0], "dailylevel":[1], "username":[author], "nickname":["Not set"], "favpet":["Not set"], "age":["Not set"], "gender":["Not set"],"bio":["Not set"], "wallpaper":["Not Set"], "embcolor":[0], "basic":[0], "regular":[0], "elite":[0], "premium":[0], "epic":[0], "supreme":[0], "fishlevel":[1], "baits":[0], "totalfishes":[0]})
    df = pd.concat([df, newdf], ignore_index=True)
    df.to_csv("userdata/users.csv", index=False)
  user = False
  for i in datafile : 
    if str(userid) in i :
      user = True
      break
  if not user :
    datafile.append({str(userid):[]})
    with open("userdata/inventory.json", "w") as f :
      json.dump(datafile, f, indent=2)
    print("Registered new user")


def countershow(filename, userid) : 
  with open(filename) as f :
    read = json.load(f)
  for i in read : 
    if userid in i :
      break
  lisofppl = i[userid]
  sorted_lis = sorted(lisofppl, key=lambda d: list(d.values())[0], reverse=True)
  return sorted_lis

def dataman(filename, userid, personid) :
  user = False
  with open(filename) as f : 
    file_data = json.load(f)
  for i in file_data : 
    if str(userid) in i : 
      user = True  
      break

  if user == False : 
    file_data.append({userid : []})
    with open(filename, "w") as w :
      json.dump(file_data, w, indent=2)
      user = True

  if user == True : 
    person = False
    with open(filename) as reading : 
      data = json.load(reading)
    for x in data :
      for y in x.keys() : 
        if int(y) == userid : 
          break
    for y in x.values() : 
      for z in y :  
        for z1 in z.keys() : 
          if int(z1) == personid :   
            person = True 
            break      

    if person == False : 
      y.append({personid:0})
      with open(filename, "w") as writing : 
        json.dump(data, writing, indent=2)
        person = True

    if person == True : 
      with open(filename) as readingf : 
        dataf = json.load(readingf)
      flag1 = False
      for x1 in dataf :
        for x2 in x1.keys() : 
          if int(x2) == userid :
            flag1 = True
            break 
        if flag1 == True : 
          break

      flag2 = False
      for a1 in x1[x2] : 
        for a3 in a1.keys() : 
          if int(a3) == personid :
            a1[a3] = a1[a3] + 1
            flag2 = True
            with open(filename, "w") as new_data : 
              json.dump(dataf, new_data, indent=2)
            break
        if flag2 == True :
          break
      return a1[a3]

def openinv(userid:str) :
  with open("userdata/inventory.json") as f : 
    datafile = json.load(f)
  for i in datafile : 
    if str(userid) in i :
      return i[str(userid)]
  return []

def userindex(userid:int) :
  df = pd.read_csv("userdata/users.csv")
  return df.index[df["id"] == userid][0]

  

@tasks.loop(seconds=120)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

r = requests.head(url="https://discord.command/api/v1")
try:
  print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
  print("No rate limit")

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=['purr ', 'Purr ', 'PURR '],
                      intents=intents,
                      case_insensitive=True)
client.remove_command('help')


@client.event
async def on_ready():
  change_status.start()
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
      await g.channels[i].send("Thanks for inviting me here. Check my available commands by using `/help`! More commands are yet to come.")
    except (discord.Forbidden, AttributeError):
      i += 1
    except IndexError:
      pass
    else:
      success = True

def registered(userid, filename) : 
  user = False
  with open(filename) as f :
    read = json.load(f)

  for i in read :
    if userid in i :
      user = True
      break
    else : 
      user = False
  return user





#-------------------------------HELP DICTIONARY----------------------------------


help_args = {
  "toss": "side --> To tell whether you want heads or tails.",
  "rate":
  "member --> Mention the member to perform action on\narg --> the quality on which you want to rate the member.",
  "invite": "No arguments to fulfill.",
  "slap" : "member --> Mention the member to perform action on", 
  "pat" : "member --> Mention the member to perform action on",
  "pfp" : "`optional` member --> Mention the member to perform action on",
  "factorial" : "num --> Number on which the command should be performed",
  "echo" : "msg --> Any sentence of word",
  "spamstart" : "message --> Any sentence or word\n`optional`amount --> Integer, for repition. 50, if not entered.",
  "info" : "No arguments to fulfill.",
  "randomnum" : "startnum --> Any positive number to start range with\nendnum --> Any positive number to end the range",
  "diceroll" : "No arguments to fulfill.",
  "pick1" : "option1 --> Choice 1 to choose from\noption2 --> Choice 2 to choose from.",
  "8ball" : "question --> Type the question you want to get answer for.",
  "logs" : "No arguments to fulfill.",
  "exponent" : "num --> Number on which the command should be performed\npower --> integer, at which the number will be raised.",
  "fact" : "No arguments to fulfill.",
  "add" : "num1 --> Number 1 to perform action\nnum2 --> Number 2 to perform action\n`optional` num3 --> Number 3 to perform action\n`optional` num4 --> Number 4 to perform action\n`optional` num5 --> Number 5 to perform action\n`optional` num6 --> Number 6 to perform action\n`optional` num7 --> Number 7 to perform action\n`optional` num8 --> Number 8 to perform action\n",
  "multiply" : "num1 --> Number 1 to perform action\nnum2 --> Number 2 to perform action\n`optional` num3 --> Number 3 to perform action\n`optional` num4 --> Number 4 to perform action\n`optional` num5 --> Number 5 to perform action\n`optional` num6 --> Number 6 to perform action\n`optional` num7 --> Number 7 to perform action\n`optional` num8 --> Number 8 to perform action",
  "subtract" : "num1 --> Number 1 to perform action\nnum2 --> Number 2 to perform action\n`optional` num3 --> Number 3 to perform action\n`optional` num4 --> Number 4 to perform action\n`optional` num5 --> Number 5 to perform action\n`optional` num6 --> Number 6 to perform action\n`optional` num7 --> Number 7 to perform action\n`optional` num8 --> Number 8 to perform action",
  "divide" : "numerator --> Number which will act as dividend\ndenominator --> Number which will act as divisor",
  "pet" : "pets --> Animal to be chosen from the given options.",
  "riddle" : "No arguments to fulfill.",
  "encode" : "text --> Any sentence/word",
  "decode" : "code --> symbols that are used to encode",
  "feedback" : "No arguments to fulfill.",
  "purge" : "`optional` number --> Any natural number. 5 is default",
  "kick" : "member --> Mention the member to perform action on\n`optional`reason --> the main reason due to which the action has been taken",
  "kaboom" : "channel --> Mention the channel on which the action has to be performed",
  "hiddendm" : "member --> Mention the member to perform action on\nmessage --> Any sentence or word",
  "shape" : "shape --> Select the 2D/3D shape from the options to perform action\nvalue --> Enter the numbers to use for the action or with spaces if entering more values",
  "sqroot" : "num --> Number on which the command should be performed on",
  "log10" : "num --> Number on which the command should be performed on",
  "userinfo" : "`optional`member --> Mention the member to perform action on",
  "serverinfo" : "No arguments to fulfill.",
  "wish" : "member --> Mention the member to perform action on\n`optional`reason --> the main reason due to which the action has been taken",
  "remindme" : "message --> Any sentence or word\ntime --> Time in minutes (m) or seconds (s) placed at the end. For example : 4s, 23m, 2m, 90s, etc.",
  "poll" : "content --> Any sentence defining the purpose of something\nemojis --> Enter emojis that you want Purrbot to add as reaction\n`optional` header --> Heading\n`footer` --> Footer (text at the bottom)",
  "profile" : "member --> Mention the member to perform action on",
  "edit" : "val --> Add a new value to the existing value",
  "leaderboard" : "basis --> Enter the basis to get the leaderboard",
  "search" : "No arguments to fulfill.",
  "steal" : "No arguments to fulfill.",
  "research" : "leveltype --> Enter to whether upgrade fish or daily level",
  "shop" : "No arguments to fulfill.",
  "buy" : "itemid --> ID of the item\n`optional` quantity --> Quantity of the item to buy",
  "inventory" : "No arguments to fulfill.",
  "share" : "member --> Mention the member to perform action on\namount --> Amount of purrcoins to be shared",
  "gamble" : "amount --> Amount of purrcoins to gamble",
  "fish" : "No arguments to fulfill.",
  "bucket" : "No arguments to fulfill.",
  "sellfish" : "tier --> Enter the tier of fish to sell or to sell all",
  "fishinfo" : "tier --> Enter the tier of fish to sell or to sell all",
  "item" : "item --> ID of the item",
  "balance" : "No arguments to fulfill.",
  "counter" : "val --> Enter the roleplay command to be counted"
}

#________________________________________________________________________________

#_______________________________LIST/DICTIONARY__________________________________

hug_kdrama = ["https://0.soompi.io/wp-content/uploads/2021/01/31075443/park-bo-young-park-hyung-sik-strong-woman-do-bong-soon2.gif", "https://media.tenor.command/7M4nIDsCmHIAAAAC/kdrama-hug.gif", "https://i.pinimg.command/originals/39/cf/35/39cf35d4a2fd347baf9a353908f32ea1.gif", "https://media.tenor.command/4sxxFiTMItgAAAAd/hug-cuddle.gif", "https://0.soompi.io/wp-content/uploads/2021/01/31084225/han-hyo-joo-lee-jong-suk-w3.gif", "https://64.media.tumblr.command/40ef99dfd56f6893bb7aa18c130b546d/tumblr_ou792yP2OB1tmjt2ko10_400.gif", "https://media.tenor.command/Hyax0hXopTYAAAAd/run-on-run-on-kdrama.gif", "https://img.buzzfeed.command/buzzfeed-static/static/2021-12/28/18/asset/115826acea96/anigif_sub-buzz-8300-1640715731-7.gif", "https://media.tenor.command/CVfsx3oi5C8AAAAC/ji-chang-wook-jcw.gif", "https://24.media.tumblr.command/c4ea73f3ebff800107f1c8614c12850e/tumblr_myf8hurUjO1sgbtl8o1_500.gif", "https://pa1.narvii.command/7520/b326fbb4b3c152e3e8382113088efdb6cc0077b1r1-480-270_hq.gif", "https://i.pinimg.command/originals/a8/74/2a/a8742afb38b6c62a46d0a56f2c872bc0.gif", "https://thumbs.gfycat.command/EducatedCleanDoe-size_restricted.gif", "https://unbotheredunnies.files.wordpress.command/2021/02/d01facd548ad875202c66840ce8257cf99a7d840.gif","https://68.media.tumblr.command/ec7432d878e42465b27b50374fc5b19d/tumblr_oji29c3seU1rzk6m3o1_r2_500.gif", "https://img.buzzfeed.command/buzzfeed-static/static/2020-11/4/1/asset/7614a2480210/anigif_sub-buzz-2252-1604452794-16.gif", "https://unbotheredunnies.files.wordpress.command/2021/05/original.gif", "https://i.imgur.command/Oj92IL3.gif", "https://gifdb.command/images/file/romantic-hug-lee-min-ho-kim-go-eun-king-eternal-monarch-7fuwx7muzjoz9182.gif", "https://64.media.tumblr.command/a9c3e5cc2d95296e4d1e8f85af1dbeed/tumblr_ojtt894ukl1w1vx4ko4_r1_250.gif", "https://media.tenor.command/tIkCctOxj6YAAAAM/nam-joo-hyuk-joohyuk.gif", "https://i.pinimg.command/originals/b9/0e/55/b90e55ed98a56dfe782a9d5fe84ca18b.gif", "https://favim.command/pd/s14/orig/170130/couple-cute-gif-kdrama-Favim.command-5028624.gif", "https://i.pinimg.command/originals/41/ae/6a/41ae6a2c3459ab609630719d61e52afa.gif", "https://64.media.tumblr.command/607769b5580bbf572ae7d2ba2612fc72/tumblr_p6odlhgCaX1wsuo8ro3_500.gif", "https://78.media.tumblr.command/5176f1f2952e4068a47802cd43d93e95/tumblr_pb3zkr0qsn1t8gzeto5_400.gif", "https://media.tenor.command/70Ep-IFhbUgAAAAC/goblin-kdrama.gif", "https://image.kpopmap.command/2020/08/its-okay-to-not-be-okay-kim-soohyun-seo-yeji-final-cover.gif","https://images6.fanpop.command/image/photos/43800000/iKON-ikon-43842638-277-400.gif", "https://i.gifer.command/GrR9.gif", "https://media.tenor.command/GbQFj4bbTwYAAAAC/yoona-kdrama.gif", "https://64.media.tumblr.command/1875bbe406584eef8c8f5e74a4ced4de/e81942059f27fee3-0f/s540x810/1cee6c92b4750889eba018565ba726e5522db8ae.gif", "https://pa1.narvii.command/6194/632ff7f1a6906ac3825ff39da6526e311757c9e7_hq.gif", "https://media.giphy.command/media/xUOwFSnqUijKCWkWbK/giphy.gif", "https://media.tenor.command/bSaBvnDj_uQAAAAC/jung-hae-in-kdrama.gif", "https://pa1.narvii.command/6346/36369bd42454387cdccacc4cc646548f99a61d10_hq.gif", "https://64.media.tumblr.command/e68c7600ad0a3029df9bdcf27b79195c/tumblr_ou792yP2OB1tmjt2ko6_400.gif"]


kiss_kdrama = ["https://media.tenor.command/KRG0qaxHm64AAAAC/kdrama-kiss.gif", "https://i.pinimg.command/originals/13/f8/3a/13f83a3ba6e2c06987e929dac3585647.gif", "https://media.tenor.command/QgO2f9tV-JUAAAAC/ji-changwook-nam-jihyun.gif", "https://media.tenor.command/GWqjWnt7hr0AAAAC/kdrama-kiss.gif", "https://media.tenor.command/J6eCRjI3HXMAAAAC/nam-joo-hyuk-joohyuk.gif", "https://media.tenor.command/tFAgy_JmttMAAAAM/kdrama-extraordinary-attorney-woo.gif", "https://media.tenor.command/H1kgKmJKwwQAAAAC/kiss-love.gif", "https://media.tenor.command/rG0C_6IJAE0AAAAC/kimsohyun-kiss.gif", "https://i.pinimg.command/originals/5c/0f/3f/5c0f3f72a40ecab28d92bb6042a1440d.gif", "https://media.tenor.command/UaqiTT4wxkAAAAAd/startup-korean-drama.gif", "https://media.tenor.command/QepV72O79uoAAAAd/startup-korean-drama.gif", "https://media.tenor.command/oK8QVSPfPdUAAAAd/startup-korean-drama.gif", "https://gifdb.command/images/high/kdrama-2521-taeri-joohyuk-kiss-tf2z9s8m6lu3o7tb.gif", "https://media.tenor.command/u3k8NpFEYIsAAAAC/kdrama-korean.gif", "https://media.tenor.command/pmVk3X3ujLwAAAAC/kiss-kdrama.gif", "https://media.tenor.command/4wEWCsuIKeEAAAAM/nam-joo-hyuk-joohyuk.gif", "https://media.tenor.command/MgWoNYLPiAYAAAAC/kiss-kdrama.gif", "https://4.bp.blogspot.command/-bMkikfVzFwg/VuMEFu3TM2I/AAAAAAACy4c/TW6q9L4IkKwb_WOHgNy-cTJk4G4u3e1hw/s1600/16.3.gif", "https://media.tenor.command/4tXrUXD0KOsAAAAC/sweet-kiss.gif", "https://media.tenor.command/sLjSAmG5o70AAAAd/kiss-sweet.gif", "https://media.tenor.command/TLJL7DTgTWcAAAAd/pinocchio-park-shin-hye.gif", "https://gifdb.command/images/high/sweet-love-couple-kiss-vietnamese-drama-cv7hnpbadxs0ueo9.gif", "https://0.soompi.io/wp-content/uploads/2021/10/13183141/strong-woman-do-bong-soon.gif", "https://media.tenor.command/NbhC3v1KUA4AAAAC/joy-kiss-cheek-kiss.gif", "https://68.media.tumblr.command/b31985a20634726e7cd066670d619dee/tumblr_obp6nq64wa1rqg3fvo4_500.gif", "https://media.tenor.command/nC_LTE0D1_4AAAAM/extraordinary-attorney-woo-kang-tae-oh.gif", "https://media.giphy.command/media/kfcOmuaDqHYCiaeREV/giphy.gif", "https://subtitledreams.files.wordpress.command/2017/02/queeninhyunsman_kiss1.gif", "https://i.pinimg.command/originals/4b/fc/75/4bfc752039005c1beb1b5881126577d8.gif", "https://i.makeagif.command/media/12-11-2018/S3XJDE.gif", "https://thumbs.gfycat.command/DazzlingKaleidoscopicBoutu-max-1mb.gif", "https://i.makeagif.command/media/11-01-2015/zur9pZ.gif", "https://3.bp.blogspot.command/-qA3-ne_ja8A/UcykX5MCFwI/AAAAAAAAMGs/mPXfvmuNI6w/s624/2013-06-27+22_03_03.gif", "https://0.soompi.io/wp-content/uploads/2021/10/13182005/secretary-kim.gif", "https://favim.command/pd/p/orig/2018/11/13/korean-drama-kdrama-gif-Favim.command-6557747.gif", "https://gifdb.command/images/high/fight-for-my-way-couple-hot-kiss-hufa2402kiktvnve.gif", "https://0.soompi.io/wp-content/uploads/2021/10/14143550/something-in-the-rain1.gif",            "https://i.pinimg.command/originals/c3/81/67/c38167daab7310dbba33b5019c535b3f.gif", "https://i.pinimg.command/originals/e4/c3/bc/e4c3bc07c1f2bec0b274d7c77483160e.gif", "https://media.tenor.command/3yoEGJlxbscAAAAM/kiss-couple.gif", "https://4.bp.blogspot.command/-13hznpo1MF0/U4dos6KY5LI/AAAAAAAACZE/t-csSKbOhWg/s1600/My+Love+From+Another+Star+Kiss.gif", "https://media.tenor.command/LJfmQeId0QUAAAAC/love-kdrama.gif", "https://0.soompi.io/wp-content/uploads/2021/10/14065626/i-am-not-a-robot.gif", "https://subtitledreams.files.wordpress.command/2017/02/queeninhyunsman_kiss1.gif", "https://i.makeagif.command/media/11-01-2015/zur9pZ.gif", "https://66.media.tumblr.command/a84432f8535eba1bddc5f2df5dcc047b/tumblr_inline_o83ttqa95y1u511vp_400.gif", "https://4.bp.blogspot.command/-MVamcqusHvo/Ut2gxFuQTXI/AAAAAAAAV5U/KD063tpBZQM/s1600/2014-01-20+23_13_17.gif"]

dogs = [
  "https://www.rd.command/wp-content/uploads/2019/01/shutterstock_673465372.jpg?fit=700,467",
  "https://i.pinimg.command/736x/ef/59/0d/ef590d3e2990e6827d96ad8ce55a755b.jpg",
  "https://cf.ltkcdn.net/dogs/images/std/236742-800x515r1-cutest-puppy-videos.jpg",
  "https://i.pinimg.command/originals/be/82/15/be821544fc5f328567cb538f96edb49a.jpg",
"https://images.hindustantimes.command/rf/image_size_960x540/HT/p2/2018/05/16/Pictures/_1571873a-58de-11e8-b431-73159b4b09e2.jpg",
  "https://a-z-animals.command/media/2021/12/Prettiest-_-Cutest-Dogs-header.jpg",
  "https://www.hiptoro.command/wp-content/uploads/2020/09/1-102.jpg",
  "https://bestwishes.vip/wp-content/uploads/2020/12/3.jpeg",
  "https://i.pinimg.command/originals/ef/59/0d/ef590d3e2990e6827d96ad8ce55a755b.png",
  "https://hips.hearstapps.command/ghk.h-cdn.co/assets/17/40/pom.jpg",
"https://www.thesprucepets.command/thmb/et0R6AiQHOqP9s4WGHcfKBDPjVo=/2667x2000/smart/filters:no_upscale()/cute-teacup-dog-breeds-4587847-hero-4e1112e93c68438eb0e22f505f739b74.jpg",
"https://ichef.bbci.co.uk/news/976/cpsprodpb/EB24/production/_112669106_66030514-b1c2-4533-9230-272b8368e25f.jpg",
  "https://www.sheknows.command/wp-content/uploads/2018/08/fajkx3pdvvt9ax6btssg.jpeg?w=1255", "https://rukminim1.flixcart.command/image/416/416/jri3jww0/poster/r/g/m/large-cute-dogs-group-puppy7-original-imafd8ywygjbejza.jpeg?q=70",
  "https://www.petsworld.in/blog/wp-content/uploads/2015/10/b05967dfb43f08adfdb30f2f6a4c665d.jpg",
  "https://wallpaperaccess.command/full/1076378.jpg",
  "https://www.hiptoro.command/wp-content/uploads/2020/09/1-102.jpg",
  "https://i.pinimg.command/736x/ef/1d/c3/ef1dc3b0c5c1cbd7d7d0a27cdcb06e3b.jpg",
  "https://imagesvc.meredithcorp.io/v3/mm/image?q=60&c=sc&rect=456%2C155%2C1558%2C1258&poi=face&w=2000&h=2000&url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F47%2F2020%2F06%2F26%2Fwhite-maletese-puppy-walking-641791436-2000.jpg",
"https://thumbor.bigedition.command/pomeranian/La3jJyKkEx14rv44zDZoytW12eI=/800x0/filters:quality(80)/granite-web-prod/d2/4d/d24d6d51ac7a489b8515f076fa47750a.jpeg",
"https://www.scotsman.command/webimg/b25lY21zOjRkMzljMWVkLThkMjAtNDFkZi1hN2Q2LTY3NjM2NzEwNjMxMDpjOWEyMDU0NC05NjA1LTQwMDctYjNjNi04YmY4Y2IyMGY3MDc=.jpg?width=640&quality=65&smart&enable=upscale",
  "https://i.pinimg.command/originals/98/e8/94/98e894e43d26e3393f17f030505da425.jpg",
  "https://i.pinimg.command/originals/80/d3/64/80d364e09d31fcba8af274926d4332ff.jpg",
  "https://s9.favim.command/orig/140101/boo-cute-doggies-dogs-Favim.command-1212748.jpg",
  "https://i.pinimg.command/originals/50/35/fc/5035fc30e323ff0b1a29b290b05f9af6.jpg",
  "https://i.pinimg.command/236x/e2/42/1e/e2421ea92c654c3e88aa220b69cbd9e3--so-cute-puppy-love.jpg",
  "https://i.ytimg.command/vi/glrQiz923nc/hqdefault.jpg",
  "https://dogexpress.in/wp-content/uploads/2017/05/Tiny.jpg",
  "https://www.boredpanda.command/blog/wp-content/uploads/2022/04/puppy-photos-omica-photography-coverimage.jpg",
"https://pbs.twimg.command/profile_images/378800000636206082/9394577cf435fa7b8a3de789b4035226_400x400.jpeg",
  "https://wallpaperaccess.command/full/390975.jpg",
  "https://assets.iflscience.command/assets/articleNo/32549/aImg/8946/1464370531-4239-why-adorable-puppies-can-make-you-feel-violent-l.jpg",
  "https://i.pinimg.command/736x/fc/91/1a/fc911a8d2740ae1714d9d2e978b6f5f4.jpg",
  "https://www.eventstodayz.command/wp-content/uploads/2016/12/cute-dog-wallpaper.jpg",
  "https://i.imgur.command/QiuzY7W.jpg",
  "https://i.pinimg.command/originals/55/68/60/55686080f066e8898ab848389bfd6ad0.jpg",
  "https://i.pinimg.command/originals/8e/8c/1f/8e8c1f365007539d47de6e58142be41f.jpg",
  "https://i.pinimg.command/originals/cf/a9/82/cfa982e7487e2cab46845ef208438148.jpg",
  "https://i.pinimg.command/originals/46/04/35/4604356e5b27d38ba5ad9e1cb6b2345c.jpg",
  "https://i.pinimg.command/736x/56/03/4f/56034f1837b57f66fe6fd4004cba3c99.jpg",
  "https://www.thesprucepets.command/thmb/oncdQ_5UJh-JhEiWiDge9AdiT94=/1080x1350/filters:no_upscale():max_bytes(150000):strip_icc()/51985952_1279464795537148_4833125964911932806_n-5c73f09b46e0fb000107631b.jpg",
  "https://i.pinimg.command/474x/74/53/25/7453256386ad622a42e33571885505d8--cute-teacup-puppies-teacup-maltese-puppies.jpg",
  "https://i.pinimg.command/474x/c4/13/90/c413907510cc710e2abee348a403a51e--teacup-maltese-puppies-maltese-dogs.jpg",
  "https://i.pinimg.command/originals/ca/4a/4c/ca4a4c40cb430fc585fb0895f4f7caed.jpg",
  "https://live.staticflickr.command/8481/8187694388_fe4a41e397_c.jpg",
  "https://i.pinimg.command/736x/6c/6d/45/6c6d45b433f5961e48b7dd0a0f1e3f4f--teacup-maltese-teacup-puppies.jpg",
  "https://barkingroyalty.command/wp-content/uploads/2015/12/pomeraninan-puppy.jpg",
  "https://i.ytimg.command/vi/akyDq4dA3Hg/hqdefault.jpg",
  "https://static.inspiremore.command/wp-content/uploads/2016/10/19121005/VS7.jpg",
  "https://i.pinimg.command/originals/d9/ac/03/d9ac0315119ee05471d4a87eb496dc34.jpg"
]
cats = [
  "https://d1hjkbq40fs2x4.cloudfront.net/2016-07-16/files/cat-sample_1313.jpg",
  "https://hips.hearstapps.command/hmg-prod.s3.amazonaws.command/images/cute-photos-of-cats-cuddling-1593203046.jpg",
  "https://iheartcats.command/wp-content/uploads/2020/07/cat-mom-kitten-cute.jpg",
  "https://cdn.wallpapersafari.command/17/26/HXv6nC.jpg",
  "https://iheartcats.command/wp-content/uploads/2020/08/madfluffs_103546217_688328451965891_7808474257930839654_n-e1596310221302.jpg",
  "https://www.teahub.io/photos/full/216-2168687_cat-photo-cat-pictures-high-quality.jpg",
  "https://i.pinimg.command/236x/7e/0a/50/7e0a507de8cf8b46e0f2665f1058ef37.jpg",
  "https://wallpaper.dog/large/10802305.jpg",
  "https://cdn.quotesgram.command/img/88/59/86321725-very-cute-cat-hd-wallpapers-beautiful-house-usa-wallpapersvery-stuff-puppy-quotes-puppies-kittens-things.jpg",
  "https://www.pngitem.command/pimgs/m/343-3433369_cute-cat-animation-png-transparent-png.png",
  "https://www.pngitem.command/pimgs/m/220-2204702_gatito-kawaii-png-cute-cat-cartoon-funny-transparent.png",
  "https://c.tenor.command/9y5iGiCiGRQAAAAC/pusheen-tea.gif",
  "http://pm1.narvii.command/6525/28af3dc98268edd47d8e4608c5caa721a94a6b04_00.jpg",
  "https://wallpapers-clan.command/wp-content/uploads/2022/06/cute-pusheen-pfp-21.jpg",
  "https://i.pinimg.command/originals/48/b9/38/48b938baf7e9dc96eee009efecfff21e.jpg",
  "https://pm1.narvii.command/7606/a603c6dc6e700197bd622d92f0d1a269d2984c93r1-640-640v2_00.jpg",
  "https://media1.giphy.command/media/OmK8lulOMQ9XO/giphy.gif",
  "https://cdn.shopify.command/s/files/1/1369/6411/files/cutest-cat-gifs-kitten-meow_large.gif?v=1504275637",
  "https://c.tenor.command/8rRT6XN0ztEAAAAd/kitty-cat.gif",
  "https://media3.giphy.command/media/DjYqNVITTewEM/giphy.gif",
  "https://bestanimations.command/media/cats/1352541851funny-cat-gif-2.gif",
  "https://data.whicdn.command/images/291013693/original.gif",
  "https://www.pbh2.command/wordpress/wp-content/uploads/2013/05/cutest-cat-gifs-bowl-kitten.gif",
  "https://64.media.tumblr.command/b0b41b61022ee24f9fad6dae79045190/4100834cd496877d-30/s500x750/c9d268f91280b17941b03a8c5dee0d3e6d2b3958.gifv",
  "https://www.icegif.command/wp-content/uploads/pusheen-icegif-1.gif",
  "https://i.ibb.co/7vGLS2G/Cute-Cat-GIF-Adorable-white-Scottish-fold-kitty-trying-to-catch-his-toy-but-he-can-t-cat-gifs-command.gif",
  "https://www.pbh2.command/wordpress/wp-content/uploads/2013/05/cutest-cat-gifs-scratch.gif",
  "https://i.ibb.co/BBgMtY9/Cute-Kitten-GIF-Super-cute-kitty-meowing-in-her-comfy-box-She-needs-her-mom-or-she-s-hungry-cat-gifs.gif",
  "https://encrypted-tbn0.gstatic.command/images?q=tbn:ANd9GcQYXtz_AUZwrN3j366MYpz4-bnh_sl_sgykoQ&usqp=CAU",
  "https://i.pinimg.command/originals/bc/f4/d1/bcf4d183aefc4cb5a559dafc0c3c7435.gif",
  "https://c.tenor.command/mvfRtjepEVEAAAAC/nyancat-pootisman.gif",
  "https://i.gifer.command/4Jc.gif",
  "https://w7.pngwing.command/pngs/329/490/png-transparent-nyan-cat-youtube-sticker-pixel-animals-text-rectangle.png",
  "https://media4.giphy.command/media/gx54W1mSpeYMg/giphy_s.gif"
]
pandas = [
"https://media1.giphy.command/media/ewzF6uunnPn6L5amuW/200w.gif?cid=6c09b9521k9td7njdvuymcnzrwwm08qsedj400g6tkwp46uo&rid=200w.gif&ct=g",
"https://media.tenor.command/CoQL2lJ_3SwAAAAM/panda.gif",
"https://bestanimations.command/media/panda/1328820576baby-panda-funny-cute-gif.gif",
"https://i.pinimg.command/originals/ce/d4/d9/ced4d9f94106ac92584305410bc72427.gif",
"https://i.pinimg.command/originals/00/34/0e/00340e4ed1007334d4db5f61453b3586.gif",
"https://i.gifer.command/3X6v.gif",
"https://24.media.tumblr.command/dc33a2dfc97782cac4edb0eceb3c0843/tumblr_mt1ykeSeSu1shzgrdo1_400.gif",
"https://64.media.tumblr.command/854da9326e03fcc1edff8873b6f562c6/1b26d6c59a6aa576-40/s400x600/66c62895d2cf7b48be805aa177a42440089c2d62.gif",
"https://i.pinimg.command/originals/d7/83/22/d78322dee7ad770df4773f150510c9b1.gif",
"https://media.tenor.command/I2x449Tko0cAAAAM/panda-door.gif",
"http://31.media.tumblr.command/58e5484cb235b02310d28d8deb2f8335/tumblr_mssamnJkld1riml7wo1_400.gif",
"https://giffiles.alphacoders.command/879/87909.gif",
"https://i.gifer.command/Kxbe.gif",
"https://media.tenor.command/H1mTFQ6-a1wAAAAC/panda.gif",
"https://64.media.tumblr.command/f654b8e20f1e48a89ba67d5991bced36/7b0d9b291522ebb2-08/s500x750/b634d79abd16f82316b333b3a5d82b5418358f96.gif",
"https://media.tenor.command/3OMzo-QSVqEAAAAM/baby-hug.gif",
"https://media.tenor.command/ti_Qr2TVWLAAAAAC/panda-cute.gif",
"https://media.tenor.command/hPHY8AbjC_0AAAAM/funny-animals-dogs.gif",
"http://25.media.tumblr.command/55af4f662ba70454e748797aed040784/tumblr_mkdoyyeYeC1s7itpyo1_500.gif",
"https://media.tenor.command/_Eci4l5V2M0AAAAM/%E6%8A%B1%E6%8A%B1-%E5%91%B5%E6%8A%A4.gif",
"https://media.tenor.command/QcRz7lyD99gAAAAC/panda-cute.gif",
"https://media.tenor.command/ezdIp0GQkDAAAAAM/baby-pandas-panda.gif",
"https://i.gifer.command/WyZw.gif",
"https://media.tenor.command/lynvyeM4fOIAAAAM/h%C3%B3ng-cute.gif",
"https://thumbs.gfycat.command/CrazyFatAzurewingedmagpie-size_restricted.gif",
"https://media2.giphy.command/media/xT8qB1QeVVwk2NmF0Y/giphy.gif",
"http://24.media.tumblr.command/f591706368af324d2d77137d77e2cb08/tumblr_n3b2gbOXJf1s9ab4to1_400.gif"
]
hamster = ["https://image.winudf.command/v2/image/Y29tLmFuZHJvbW8uZGV2NTUzMjk5LmFwcDU0NjY1OV9zY3JlZW5zaG90c18xX2Y2ZWMyYWJj/screen-0.jpg?fakeurl=1&type=.jpg", "https://t4.ftcdn.net/jpg/05/61/40/53/360_F_561405378_tFqUXOUhDc13eBYtHpV5qChCWu0EN6eR.jpg", "https://i.ytimg.command/vi/MQqcSymu8HA/maxresdefault.jpg", "https://w0.peakpx.command/wallpaper/330/13/HD-wallpaper-cute-hamster-in-meadow-with-daisies-field-young-wild-grass.jpg", "https://images.saymedia-content.command/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cq_auto:eco%2Cw_1200/MTk2OTU0OTI4Mzk5MjYzNDkz/reasons-not-to-have-a-pet-hamster.png", "https://cf.ltkcdn.net/small-mammals/small-mammal-names/images/orig/323197-1600x912-hamster-flowers.jpg", "https://images.hindustantimes.command/img/2022/03/09/1600x900/Cute_hamster_first_time_eating_spaghetti_might_make_you_crave_for_some_Watch_1646830772153_1646830807999.png", "https://d1muy2ct2wkbaz.cloudfront.net/video/465000/464811/580x325/0.jpg", "https://www.eastcoastdaily.in/wp-content/uploads/2020/09/everyone-likes-chips.jpg", "https://i.pinimg.command/474x/2c/1d/de/2c1dde6528b9c8631b677d61505ffbb7.jpg", "https://i.pinimg.command/236x/56/22/7b/56227b85727d7305a7bcebb4379c801b.jpg", "https://i.pinimg.command/236x/25/7c/8b/257c8b61dd7c709b2abeae0a70676cd5--cute-kawaii-drawings-cute-cartoon-drawings.jpg", "https://68.media.tumblr.command/c15d0ea21e9de79e24b239f892002c20/tumblr_oo5i9hDHP01rluhlpo1_400.gif", "https://images.squarespace-cdn.command/content/v1/5883ba0ee4fcb5d74e068902/1638552840118-WSMAG6RD8E9EHK55HVYE/Jude-Halloween-2021-013-small.jpg", "https://www.thesprucepets.command/thmb/zXziTJx98ZGKMgmwX4ijBNOCQlY=/1732x0/filters:no_upscale():strip_icc()/GettyImages-497336201-853468639f5c4a43ab54222f15d92b77.jpg", "https://wallpapers.command/images/hd/cute-drawing-pictures-qh0hdd7593g4sycj.jpg", "https://ih1.redbubble.net/image.4736607326.4847/mwo,x1000,ipad_2_skin-pad,1000x1000,f8f8f8.u2.jpg", "https://static.vecteezy.command/system/resources/previews/017/048/296/original/cute-hamster-illustration-hamster-kawaii-chibi-drawing-style-hamster-cartoon-vector.jpg", "https://www.inspiremore.command/wp-content/uploads/2022/05/hamster-cheese.jpeg", "https://images1.fanpop.command/images/photos/2600000/Cute-Baby-hamsters-2628881-460-345.jpg", "https://thumbs.dreamstime.command/b/cute-hamster-springtime-cartoon-character-funny-animal-265969510.jpg", "https://supremepetfoods.command/wp-content/uploads/2015/08/iStock-1072781282-1200px-510x305.jpg", "https://w0.peakpx.command/wallpaper/449/861/HD-wallpaper-hamster-animal-cute-hamster-hello-themes.jpg", "https://cdn.pixabay.command/photo/2023/03/11/22/08/ai-generated-7845365_960_720.jpg", "https://www.pngkit.command/png/detail/65-656483_image-black-and-white-hamster-animals-cute-kawaii.png", "https://t4.ftcdn.net/jpg/05/78/23/67/360_F_578236729_1Y0KL1rIgFulbmvapsBUiyAukc9Bod6M.jpg", "https://wallpapers.command/images/hd/cute-hamster-pictures-qoklyec3lhkocsoo.jpg", "https://images-cdn.ubuy.co.in/63f8336fab3ea80d5604fa67-hamster-cute-hamster-white-wall.jpg"]

rabbit = ["https://t3.ftcdn.net/jpg/05/70/60/74/360_F_570607483_xwyvxx2liLMmjwTDKULTh7LTsOmv6Umt.jpg", "https://m.media-amazon.command/images/I/41fO4oChXSL._AC_UF894,1000_QL80_.jpg", "https://c4.wallpaperflare.command/wallpaper/204/370/353/bunny-wallpaper-preview.jpg", "https://www.animallama.command/wp-content/uploads/2023/03/how-smart-are-rabbits-768x512.jpg", "https://cdn.wallpapersafari.command/16/76/eUij9X.jpg", "https://t4.ftcdn.net/jpg/05/60/46/57/360_F_560465710_VpBpJLv0yCT2GmDH8AFlJwoddYWtTeDG.jpg", "https://t3.ftcdn.net/jpg/05/61/31/20/360_F_561312086_cvzegHUnmNN0ZLPZBVDb3BDuFKHJ1iXN.jpg", "https://i2-prod.leicestermercury.co.uk/news/leicester-news/article7306132.ece/ALTERNATES/s1200b/0_gettyimages-1214873071-170667a.jpg", "https://i.ytimg.command/vi/8BYa0U1h5Fs/hqdefault.jpg", "https://t4.ftcdn.net/jpg/05/58/60/47/360_F_558604762_6Q02BIpSwrpBIGgwCYdssBzVtCsXL3vV.jpg", "https://www.peta.org/wp-content/uploads/2021/04/rabbit-blue-background.jpg", "https://media.tenor.command/q_jj1u340XAAAAAM/snowball-bunny-carrot.gif", "https://i.ytimg.command/vi/FC4Kun_BimM/maxresdefault.jpg", "https://e1.pxfuel.command/desktop-wallpaper/204/576/desktop-wallpaper-beautiful-baby-bunny-rabbits-cute-white-baby-rabbit.jpg", "https://cdn.wallpapersafari.command/3/20/2CwjPD.jpg", "https://cdn4.sharechat.command/img_595318_1a1fd232_1671213592534_sc.jpg", "https://i.pinimg.command/originals/05/49/5a/05495abb66573cfc4d697be122b54531.jpg", "https://www.boredpanda.command/blog/wp-content/uploads/2021/11/cute-rabbits-307-618b7d91f120c__700.jpg", "https://i.ytimg.command/vi/65hXnBFRTnQ/maxresdefault.jpg", "https://w0.peakpx.command/wallpaper/1020/863/HD-wallpaper-adorable-fluffy-bunny-cute-rabbit-fluffy-adorable-bunny-cute-baby.jpg", "https://cdn.wallpapersafari.command/59/70/4HrRwe.jpg", "https://wallpaperaccess.command/full/83858.jpg", "https://www.ntu.ac.uk/__data/assets/image/0019/641305/rabbit.jpg", "https://cdn.pixabay.command/photo/2020/02/02/14/30/rabbit-4813172__340.jpg", "https://w0.peakpx.command/wallpaper/818/348/HD-wallpaper-cute-rabbit-cute-rabbit-lovely-green-color-beautiful.jpg", "https://wallpapers.command/images/featured/0g8mij2ea0et2gs4.jpg", "https://i.ytimg.command/vi/hDJkFLnmFHU/mqdefault.jpg", "https://t3.ftcdn.net/jpg/05/60/19/82/360_F_560198269_NaE7QBRQFRy2t4X7CnDe9GigXAe5HTad.jpg", "https://img5.goodfon.command/wallpaper/nbig/8/6c/iaitsa-colorful-krolik-paskha-spring-easter-eggs-bunny-cut-4.jpg", "https://i.redd.it/125ebgihdbu41.jpg", "https://i.pinimg.command/originals/86/f6/dc/86f6dc70f9c0492eb16e00fb0877848c.jpg", "https://i.ytimg.command/vi/c_cg-2f9RUw/hqdefault.jpg", "https://i.pinimg.command/originals/08/cc/b3/08ccb35a48d4d6b7712da31c4a059857.jpg", "https://m.media-amazon.command/images/I/41fO4oChXSL._AC_UF894,1000_QL80_.jpg", "https://i.pinimg.command/originals/08/cc/b3/08ccb35a48d4d6b7712da31c4a059857.jpg", "https://cdn.pixabay.command/photo/2014/06/21/08/43/rabbit-373691__340.jpg", "https://i.ytimg.command/vi/00MDZZP0CKE/maxresdefault.jpg", "https://livesweetblog.command/wp-content/uploads/2020/08/IMG_2937-1024x768(pp_w768_h576).jpg", "https://t3.ftcdn.net/jpg/05/58/30/26/360_F_558302664_usO2Ikpq0UZNmAps1dvIf29x2yS6ars5.jpg", "https://t4.ftcdn.net/jpg/05/58/59/75/360_F_558597598_XMJzQG0G7MTdz1lXC41Nwzy8mJsgvOfj.jpg", "https://i.pinimg.command/236x/f4/3e/09/f43e0997de88ff4100bc7e9d3da5d5ea.jpg", "https://i.pinimg.command/474x/2c/da/16/2cda162873cfcfab78bad0db344af5fa.jpg"]

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

spam = False

b = {'a': '𓂅', 'b': '✦', 'c': '𝖄', 'd': '⊹', 'e': '⋆', 'f': '⌕', 'g': 'ꗃ', 'h': '𝕯', 'i': 'ഒ', 'j': '୨', 'k': '୧', 'l': '⌯', 'm': '﹅', 'n': '﹆', 'o': 'ଘ', 'p': 'ꕤ', 'q': 'ꔛ', 'r': '𓏲', 's': 'ָ', 't': 'ǂ', 'u': '𓍼', 'v': '⋈', 'w': 'ꮺ', 'x': '⌗', 'y': 'ꉂ', 'z': 'ᨒ', '1': '๑', '2': '∇', '3': 'θ', '4': 'Λ', '5': 'Γ', '6': 'Ξ', '7': 'ω', '8': 'ξ', '9': 'δ', '0': 'ε', 'A': 'ζ', 'B': 'η', 'C': '𝕬', 'D': '⊷', 'E': '⋭', 'F': '≟', 'G': '≲', 'H': '⍤', 'I': '⨒', 'J': '⊿', 'K': '𝟃', 'L': '⋴', 'M': '⊎', 'N': '⊅', 'O': '⋓', 'P': 'ӫ', 'Q': '옻', 'R': 'ഋ', 'S': '∵', 'T': '⋠', 'U': '≢', 'V': '≭', 'W': '⩲', 'X': '∔', 'Y': '⊖', 'Z': '₪', ' ': '✧', '.': '↢', ',': '↡', "'": '↺', '/': '↻', '?': '↼', '!': '↾', '@': '↳', '#': '↲', '$': '↸', '%': '↹', '^': '⇏', '&': '⇪', '*': '⇫', '(': '⇬', ')': '⇭', '_': '⇮', '+': '⇯', '=': '⇻', '-': '⇺', '~': '⇹', '`': '⇸', '|': '⇷', '<': '⇾', '>': '⇽', ';': '⇲', ':': '⇱', '{': '⇰', '}': 'ↇ', '[': 'Ⅰ', ']': '円'}

lis_decode = {'𓂅': 'a', '✦': 'b', '𝖄': 'c', '⊹': 'd', '⋆': 'e', '⌕': 'f', 'ꗃ': 'g', '𝕯': 'h', 'ഒ': 'i', '୨': 'j', '୧': 'k', '⌯': 'l', '﹅': 'm', '﹆': 'n', 'ଘ': 'o', 'ꕤ': 'p', 'ꔛ': 'q', '𓏲': 'r', 'ָ': 's', 'ǂ': 't', '𓍼': 'u', '⋈': 'v', 'ꮺ': 'w', '⌗': 'x', 'ꉂ': 'y', 'ᨒ': 'z', '๑': '1', '∇': '2', 'θ': '3', 'Λ': '4', 'Γ': '5', 'Ξ': '6', 'ω': '7', 'ξ': '8', 'δ': '9', 'ε': '0', 'ζ': 'A', 'η': 'B', '𝕬': 'C', '⊷': 'D', '⋭': 'E', '≟': 'F', '≲': 'G', '⍤': 'H', '⨒': 'I', '⊿': 'J', '𝟃': 'K', '⋴': 'L', '⊎': 'M', '⊅': 'N', '⋓': 'O', 'ӫ': 'P', '옻': 'Q', 'ഋ': 'R', '∵': 'S', '⋠': 'T', '≢': 'U', '≭': 'V', '⩲': 'W', '∔': 'X', '⊖': 'Y', '₪': 'Z', '✧': ' ', '↢': '.', '↡': ',', '↺': "'", '↻': '/', '↼': '?', '↾': '!', '↳': '@', '↲': '#', '↸': '$', '↹': '%', '⇏': '^', '⇪': '&', '⇫': '*', '⇬': '(', '⇭': ')', '⇮': '_', '⇯': '+', '⇻': '=', '⇺': '-', '⇹': '~', '⇸': '`', '⇷': '|', '⇾': '<', '⇽': '>', '⇲': ';', '⇱': ':', '⇰': '{', 'ↇ': '}', 'Ⅰ': '[', '円': ']'}

tex = ""
tex2 = ""

prof_emoji = {"Cat" : "<a:catjam:1153311918535225404>", "Rabbit" : "<:innocent_rabbit:1153312818037280808>", "Hamster" : "<:hamsterr:1153313216940740719>", "Panda" : "<a:panda:1153313424256794634>", "Dog" : "<a:dogopdance:1153314038562951250>", "Not set" : ""}

itemdesc = {"Bait": "Basic is a common item. It can be used to catch fishes."}

items = {
  "name":["Bait","Christmas Wallpaper","Purrbot Wallpaper","Anime Wallpaper","Batman Wallpaper","Superman Wallpaper","Spiderman Wallpaper","Ironman Wallpaper","Landscape Wallpaper","Valentines Wallpaper1","Valentines Wallpaper2"],
  "cost": [10,500,1000,300,500,500,700,600,300,800,800]}

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
class maths(app_commands.Group):
  ...
maths = maths(name="math", description="Performs various calculations")

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
    if (user.name, user.discriminator) == (member.name, member.discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"{user.name}#{user.discriminator} has been unbanned!")


#----------------------------------HELP--------------------------------------

@client.tree.command(name="help", description="lists out all the available commands of the Purrbot")
@discord.app_commands.describe(command="enter the command name, which you want help with")
async def help(interaction: discord.Interaction, command:typing.Optional[str]):
  em = discord.Embed(title="HELP", color=interaction.user.color)
  if command == None:

    em.add_field(name="<:commands:1103517903166382091>Normal Commands",
                 value="`logs`  `pfp`  `info`  `encode`  `decode`  `feedback`  `invite`  `userinfo`  `serverinfo`  `remindme`\n", inline=False)

    em.add_field(name="<:commands:1103517903166382091>Game Commands", value="`profile`  `edit`  `dailylogin`  `research`  `balance`  `search`  `steal`  `shop`  `buy`  `inventory`  `use`  `share`  `gamble`  `fish`  `bucket`  `sellfish`  `fishinfo`  `leaderboard`\n", inline=False)
    
    em.add_field(name="<:commands:1103517903166382091>Fun Commands",
      value="`fact`  `riddle`  `echo`  `spam`  `spamstop`  `rate`  `toss`  `diceroll`  `8ball`  `pet`  `pick1`  `randomnum`  `hiddendm`",
      inline=True)
    em.add_field(name="<:commands:1103517903166382091>Roleplay Commands",
                 value="`pat`  `slap` `wish`",
                 inline=False)
    em.add_field(name="<:commands:1103517903166382091>Mathematical Commands",
      value="`factorial`  `add`  `subtract`  `multiply`  `divide`  `exponent`  `log10`  `shapes`  `sqroot`",
      inline=False)
    
    em.add_field(name="<:commands:1103517903166382091>Moderation Commands",
      value="`kick`  `purge`  `kaboom`  `poll`",
      inline=False)

  elif command :
    with open("data/help.json") as f:
      help_dict = json.load(f)
    command = command.lower()
    em.add_field(name=f"<a:symbol:1103534543895531610> {command}", value=help_dict[command], inline=False)
    em.add_field(name="Arguments Required :", value=help_args[command], inline=False)

  elif command.lower() not in help_dict: 
    em.add_field(name="INVALID COMMAND", value="Either the command is unavailable in Purrbot or you must have made a spelling error.")

  await interaction.response.send_message(embed=em, ephemeral=False)


#____________________________________NORMAL_______________________________________

@client.tree.command(name="logs", description="Tells you about the recent updates and fixes")
async def log(interaction: discord.Interaction):
  em = discord.Embed(title="PurrBot Logs, 7 April 2024", description="*Purrbot's major update and we are happy to announce that officialy, Purrbot has become an economy bot! I have put all of my knowledge in the bot and I hope there are no bugs. If some bug occurs, kindly provide me the information about it using the feedback command. Thank you for your support! More updates will be coming slowly as I have to plan things beforehand. You can also provide suggestions using the feedback!*", color = 0x3498db)
  #<a:star_2:1085488210064461955> for updates
  em.add_field(name="Updates <a:blu_glitter:1161309978099986492>", value="<a:star_2:1085488210064461955> __New Category__ -> `Game Commands`", inline=False)
  #<:wren:1105395863955714059> for fixes
  em.add_field(name="Fixes", value="Everything is fixed currently!")
  em.set_footer(text="You can send feedbacks using /feedback.", icon_url=client.user.avatar)
  await interaction.response.send_message(embed=em, ephemeral=False)


@client.tree.command(name="info", description="Gives information regarding the Bot Status")
async def info(interaction: discord.Interaction):
  try:
    user = await client.fetch_user("781419439160688660")
  except:
    user = 'purrfectkun'
  servers123 = str(len(client.guilds))
  with open("data/help.json") as f:
    help_dict = json.load(f)
  em = discord.Embed(title=client.user, description="ID = 863490119976878090", color=0xffb6e4)
  em.add_field(name="<:person:1085489445584785508> Owner :", value = user.mention, inline=False)
  em.add_field(name="<a:coding:1085489342551695371> Version :", value="PurrBot v2", inline=False)
  em.add_field(name="<a:Discord:1085489545258217542> Library : ", value="discord.py 2.0")
  em.add_field(name="<:server:1085489879401639976> No. of Servers : ", value=servers123, inline=False)
  em.add_field(name="<:Cool:912744704460857375> No. of Commands : ", value=len(help_dict), inline=False)
  em.add_field(name="<:people:1085588661980102671> Bot Users :", value=str(len({m.id for m in client.get_all_members()})), inline=False)
  em.add_field(name="<a:Errorr:1085489721926496346> Errors :", value="0 Errors", inline=False)
  em.add_field(name="<:thinking_cat_face:937049263509225502> Since :", value="Sunday, 11 July 2021", inline=False)
  em.set_thumbnail(url="https://i.pinimg.command/564x/39/69/7f/39697f5042715e373aa7144caf3f4795.jpg")
  await interaction.response.send_message(embed=em, ephemeral=False)


@client.tree.command(name="pfp", description="shows avatar of the member you mentioned or yours if not mentioned")
@discord.app_commands.describe(member="leave it blank if you want your pfp to be displayed")
async def pfp(interaction: discord.Interaction, member: discord.Member = None):
  if member == None:
    member = interaction.user
  em = discord.Embed(title=f"__Avatar of {member}__",
                     color=interaction.user.color)
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
  try : 
    global b, tex
    for y in text : 
      cc = b[y]
      tex = text.replace(y, cc)
      text = tex
    await interaction.response.send_message(text, ephemeral=False)
  except : 
    await interaction.response.send_message("Oops, looks like you passed invalid character. I can't encode like that! Just give some A-Z, integers and spaces. Special characters not allowed.")


@client.tree.command(name="decode", description="turns the code back to the original text")
@discord.app_commands.describe(code="type the code here")
async def dec(interaction:discord.Interaction, code:str) : 
  try : 
    global lis_decode, tex2 
    for i1 in code : 
      gg1 = lis_decode[i1]
      tex2 = code.replace(i1, gg1)
      code = tex2
    await interaction.response.send_message(code, ephemeral=False)
  except : 
    await interaction.response.send_message("Looks like some error occured in the bot or maybe you have given invalid code to decode.")


@client.tree.command(name="feedback", description="tell the bot owner about your experience with the Purrbot.")
async def fedback(interaction:discord.Interaction) : 
  feedback_modal = Feedback()
  feedback_modal.user = interaction.user
  await interaction.response.send_modal(feedback_modal)


@client.tree.command(name="userinfo", description="shows the information regarding a member")
@discord.app_commands.describe(member="mention a member. Will show your info if none")
async def userinfo(interaction:discord.Interaction, member:discord.Member=None) : 
  user = member or interaction.user
  roles = []
  for r in user.roles : 
    roles.append(str(r.mention))
  colorcode = user.color 
  uid = user.id
  nickn = user.nick or "No nickname set"
  created = user.created_at.strftime("%A, %B %d %Y, %I:%M:%S %p")
  joined = user.joined_at.strftime("%A, %B %d %Y, %I:%M:%S %p")
  avatar_url = user.display_avatar
  role = len(user.roles)
  if len(str(" | ").join([x.mention for x in user.roles])) > 1024:
    rol = "Too many to display"
  else : 
    rol = " | ".join(roles)
    
  memorbot = user.bot 
  botpfp = client.user.avatar
  if not memorbot : 
    memorbot = "not a bot"
  else : 
    memorbot = "a bot"

  em = discord.Embed(title="User Information", description=f"ID = {uid}", color=colorcode)
  em.set_thumbnail(url=avatar_url)
  em.add_field(name="", value="")
  em.add_field(name="Member name : ", value=f"{user}", inline=False)
  em.add_field(name="Nickname : ", value=f"{nickn}", inline=False)
  em.add_field(name="Created on :", value=f"{created}", inline=False)
  em.add_field(name="Joined on :", value=f"{joined}", inline=False)
  em.add_field(name=f"Roles ({role}) :", value=f"{rol}", inline=False)
  em.set_footer(text=f"{user} is {memorbot}", icon_url=botpfp)
  await interaction.response.send_message(embed=em)


@client.tree.command(name="serverinfo", description="shows the information about the current server.")
async def svinfo(interaction:discord.Interaction) : 
  sv = interaction.guild
  svid = sv.id
  svname = sv.name 
  svcr = sv.created_at.strftime("%A, %B %d %Y, %I:%M:%S %p")
  svown = sv.owner
  svmem = sv.member_count
  svtchan = len(sv.text_channels)
  svvchan = len(sv.voice_channels)
  svthumb = sv.icon
  svem = len(sv.emojis)

  em = discord.Embed(title=svname, description=f"Server ID : {svid}", color=interaction.user.color)
  em.add_field(name=f"__Owner__ : *{svown}*", value="", inline=False)
  em.add_field(name=f"__Total Members__ : *{svmem}*", value="", inline=False)
  em.add_field(name=f"__Created At__ : *{svcr}*", value="", inline=False)
  em.add_field(name=f"__Text Channels__ : *{svtchan}*", value="", inline=False)
  em.add_field(name=f"__Voice Channels__ : *{svvchan}*", value="", inline=False)
  em.add_field(name=f"__Emojis__ : *{svem}*", value="", inline=False)
  em.set_thumbnail(url=svthumb)
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
  url = f"https://leetcode-stats-api.herokuapp.command/{username}"
  try:
    r = requests.get(url).json()
    if r["status"] != "success":
      await interaction.response.send_message("Kindly check if you provided the correct username, otherwise, this might just be an issue from the other side (It'll be fixed soon, else use `/feedback` to notify the creator).")
    else : 
      em = discord.Embed(title=f"LeetCode stats ({username})", color=interaction.user.color)
      em.add_field(name="Total Solved", value=r["totalQuestions"], inline=False)
      em.add_field(name="Easy Solved:", value=r["easySolved"], inline=False)
      em.add_field(name="Medium Solved:", value=r["mediumSolved"], inline=False)
      em.add_field(name="Hard Solved:", value=r["hardSolved"], inline=False)
      em.add_field(name="Acceptance Rate:", value=r["acceptanceRate"], inline=False)
      em.add_field(name="Rank:", value=r["ranking"], inline=False)
      em.set_footer(text=f"Requested by {interaction.user.display_name}",icon_url=interaction.user.avatar)
      await interaction.response.send_message(embed=em)
  except: 
    await interaction.response.send_message("There might be some small issue from the server side. Kindly try again for a few times.")
    


#________________________________________________________________________________

# GAME COMMANDS
@app_commands.checks.cooldown(1, 3600*24, key=lambda i: (i.user.id))
@client.tree.command(name="dailylogin", description="Gives you currency every day")
async def dailylogin(interaction:discord.Interaction):
  df = pd.read_csv("userdata/users.csv")
  place = userindex(interaction.user.id)
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
  setup(member.id, member.name)
  global wallpapers
  df = pd.read_csv("userdata/users.csv")
  place = userindex(member.id)
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
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)
  if val.name == "Default" : 
    df.loc[place, "wallpaper"] = "Not Set"
  else : 
    inv = openinv(interaction.user.id)
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
  place = userindex(interaction.user.id)
  df.loc[place, "embcolor"] = val.value
  df.to_csv("userdata/users.csv", index=False)
  await interaction.response.send_message("Overwriting of data successful!", ephemeral=True)


@client.tree.command(name="balance", description="Shows your balance")
async def balance(interaction:discord.Interaction):
  df = pd.read_csv("userdata/users.csv")
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)

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


@app_commands.checks.cooldown(1, 900, key=lambda i: (i.user.id))
@client.tree.command(name="research", description="Research on new techniques to get more purrcoins in daily login or get more fishes.")
@app_commands.choices(leveltype=[
  app_commands.Choice(name="dailylevel", value=1),
  app_commands.Choice(name="fishlevel", value=2)
])
async def research(interaction:discord.Interaction, leveltype:discord.app_commands.Choice[int]):
  df = pd.read_csv("userdata/users.csv")
  place = userindex(interaction.user.id)
  money = df.loc[place, "purrcoins"]
  level = df.loc[place, leveltype.name]
  if leveltype.name == "dailylevel" : 
    chance = random.choice([True, True, False])
    cost = int(1000*0.5*level)
    if money < cost :
      await interaction.response.send_message(f"You don't have enough purrcoins to research! Earn {cost} then you can research to level up your daily.")
    elif money > cost : 
      df.loc[place, "purrcoins"] -= cost
      df.to_csv("userdata/users.csv", index=False)
      if chance == False : 
        await interaction.response.send_message("You researched but found nothing sadly.......")
      elif chance == True : 
        df = pd.read_csv("userdata/users.csv")
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
  global items
  col = discord.Color.random()
  em1 = discord.Embed(title="Shop", color=col)
  if len(items["name"]) > 25 :
    for i in range(0, 25) : 
      itemname = items["name"][i]
      itemcost = items["cost"][i]
      em1.add_field(name=f"{i}{itemname}", value=f"<:purrcoin:1163085791401103471> **{itemcost}**", inline=False)
    await interaction.response.send_message(embed=em1)

    em2 = discord.Embed(color=col)
    for i in range(25, len(items["name"])) : 
      itemname = items["name"][i]
      itemcost = items["cost"][i]
      em2.add_field(name=f"{i}{itemname}", value=f"<:purrcoin:1163085791401103471> **{itemcost}**", inline=False)
    await interaction.channel.send(embed=em2)
  elif len(items["name"]) <= 25 :
    for i in range(0, len(items["name"])) : 
      itemname = items["name"][i]
      itemcost = items["cost"][i]
      em1.add_field(name=f"{i}. {itemname}", value=f"<:purrcoin:1163085791401103471> **{itemcost}**", inline=False)
    await interaction.response.send_message(embed=em1)


@client.tree.command(name="buy", description="Buy an item from the shop")
async def buyitem(interaction:discord.Interaction, itemid:int, quantity:typing.Optional[int]=1) : 
  if quantity <=0:
    await interaction.response.send_message("Quantity must be greater than 0.")
    return
  elif quantity > 1000 : 
    await interaction.response.send_message("Quantity should be lower than 1000 -.-")
  try : 
    global items
    df = pd.read_csv("userdata/users.csv")
    itemlist = openinv(interaction.user.id)
    place = userindex(interaction.user.id)
    money = df.loc[place, "purrcoins"]
    itemname = items["name"][itemid]
    itemname = itemname.title()
    if "Wallpaper" in itemname and quantity != 1 : 
      quantity = 1
      itemcost = items["cost"][itemid]
      sen = f"Wallpapers are bought only once. Hence, you only bought 1 {itemname} for <:purrcoin:1163085791401103471> **{itemcost}**!" 

    itemcost = (items["cost"][itemid])*quantity
    with open("userdata/inventory.json") as f : 
      data = json.load(f)
    if itemname in itemlist : 
      await interaction.response.send_message(f"You already have {itemname} in your inventory!")

    elif money < itemcost :
      await interaction.response.send_message(f"You need {itemcost-money} purrcoins to buy {quantity} {itemname}!")
      return

    elif money >= itemcost :
      sen = f"You bought {quantity} {itemname} for <:purrcoin:1163085791401103471> **{itemcost}**!"
      df.loc[place, "purrcoins"] -= itemcost
      if itemid == 0 : 
        df.loc[place, "baits"] += quantity
      else :
        for i in data : 
          if str(interaction.user.id) in i :
            i[str(interaction.user.id)].append(itemname)
            break
        with open("userdata/inventory.json", "w") as f :
          json.dump(data, f, indent=2)
      await interaction.response.send_message(sen)
      df.to_csv("userdata/users.csv", index=False)

  except IndexError :
    await interaction.response.send_message("Wrong number of item. That doesn't exist in shop!")


@client.tree.command(name="inventory", description="View your inventory")
async def invento(interaction:discord.Interaction) : 
  itemn = 1
  items = openinv(interaction.user.id)
  df = pd.read_csv("userdata/users.csv")
  place = userindex(interaction.user.id)
  baits = df.loc[place, "baits"]
  em1 = discord.Embed(title=f"{interaction.user.name}'s Inventory", color=discord.Color.random())
  if len(items) != 0 : 
    for x in range(len(items)) : 
      em1.add_field(name=f"{itemn}. {items[x]}", value="", inline=False)
      itemn += 1
  else : 
    em1.add_field(name="There is no item in your inventory :(\n Buy something from the shop.", value="")
  em1.add_field(name="", value="", inline=False)
  em1.add_field(name="", value="", inline=False)
  em1.add_field(name=f"<:bait:1185874134417281164> baits x **{baits}**", value="", inline=False)
  await interaction.response.send_message(embed=em1)


@client.tree.command(name="use", description="Use an item from your inventory")
async def useitem(interaction:discord.Interaction, item:int) :
  item -= 1
  inven = openinv(interaction.user.id)

  if len(inven) == 0 : 
    await interaction.response.send_message("You don't have any items in your inventory!")

  elif item > len(inven) : 
    await interaction.response.send_message("That item doesn't exist in your inventory!")

  elif item <= len(inven) : 
    itemname = inven[item].title()
    if itemname.endswith("Wallpaper") : 
      await interaction.response.send_message("It is a wallpaper for your profile! You can use it by `/editprofile picture`.")


@client.tree.command(name="share", description="give your friends some of your money.")
async def share(interaction:discord.Interaction, member:discord.Member, amount:int) :
  if member.bot : 
    await interaction.response.send_message("Why are you giving your money to a bot?")
  elif interaction.user.id == member.id :
    await interaction.response.send_message("Are you trying to send money to yourself? For real?", ephemeral=True)
  else : 
    setup(member.id, member.name)
    df = pd.read_csv("userdata/users.csv")
    placeuser = userindex(interaction.user.id)
    placemember = userindex(member.id)
    moneyuser = df.loc[placeuser, "purrcoins"]

    if moneyuser <= 0 :
      await interaction.response.send_message("You don't have any money lol. Earn when")
    elif moneyuser < amount :
      await interaction.response.send_message("You don't have enough money to share!")
    else :
      df.loc[placeuser, "purrcoins"] -= amount
      df.loc[placemember, "purrcoins"] += amount
      df.to_csv("userdata/users.csv", index=False)
      await interaction.response.send_message(f"You gave <:purrcoin:1163085791401103471>{amount} to {member.name}!")


@client.tree.command(name="gamble", description="Are you going for profit or loss?")
async def gam(interaction:discord.Interaction, amount:int) :

  if amount < 100 :
    await interaction.response.send_message("You should have at least <:purrcoin:1163085791401103471> 100 to gamble!")
  else : 
    chance = [True, False]
    df = pd.read_csv("userdata/users.csv")
    place = userindex(interaction.user.id)
    if random.choice(chance) :
      df.loc[place, "purrcoins"] += amount
      await interaction.response.send_message(f"You **won** <:purrcoin:1163085791401103471>{amount}!")
    else : 
      df.loc[place, "purrcoins"] -= amount
      await interaction.response.send_message(f"You **lost** <:purrcoin:1163085791401103471>{amount}!")
    df.to_csv("userdata/users.csv", index=False)


@client.tree.command(name="fish", description="Go fishing and get some fish!")
async def fish(interaction:discord.Interaction) :
  df = pd.read_csv("userdata/users.csv")
  place = userindex(interaction.user.id)
  level = df.loc[place, "fishlevel"]
  baits = df.loc[place, "baits"]

  if baits <= 0 : 
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
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)
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
  place = userindex(interaction.user.id)
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
  global wallpapers, items, itemdesc
  if item.name == "Christmas Wallpaper" :
    des = "A special wallpaper for Christmas."
  elif item.name == "Purrbot Wallpaper" :
    des = "A wallpaper of Purrbot, expensive one!"
  elif item.name == "Anime Wallpaper" :
    des = "Name suggests, a beautiful anime wallpaper."
  elif item.name == "Batman Wallpaper" :
    des = "Wallpaper of The Dark Knight. Popular superhero these days."
  elif item.name == "Superman Wallpaper" :
    des = "Superman wallpaper, be invincible with this one!"
  elif item.name == "Spiderman Wallpaper" :
    des = "Peter Parker by day, Spiderman by night. Our favorite teenage superhero!"
  elif item.name == "Ironman Wallpaper" :
    des = "Tony stark is cool isn't it? If you like him, then here you go!"
  elif item.name == "Landscape Wallpaper" :
    des = "Who doesn't love a beautiful landscape? Make your profile look outstanding."
  elif item.name == "Valentines Wallpaper1" :
    des = "This one's exclusive! Pretty for those who are taken tho."
  elif item.name == "Valentines Wallpaper2" :
    des = "Second exclusive which is again really beautiful only for those who are taken hehe."
  elif item.name == "Bait":
    des = itemdesc(item.name)

  em = discord.Embed(title=item.name, description=des, color=discord.Color.random())
  pr = items["cost"][item.value]
  if "Wallpaper" in item.name : 
    em.set_image(url=wallpapers[item.name])
    em.set_footer(text=f"Price: {pr} purrcoins")
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
  
  if pets.name == "Cat":
    em = discord.Embed(title=f"{interaction.user.name} orders for a cat 🐱", color=0xe67e22)
    em.set_image(url=random.choice(cats))
    
  elif pets.name == "Dog":
    em = discord.Embed(title=f"{interaction.user.name} gets a dog!", color=0xe74c3c)
    em.set_image(url=random.choice(dogs))
    
  elif pets.name == "Panda":
    em = discord.Embed(
      title=f"{interaction.user.name} is having a panda! So cute >.<",
      color=interaction.user.color)
    em.set_image(url=random.choice(pandas))
    
  elif pets.name == "Hamster" : 
    em = discord.Embed(title=f"{interaction.user.name}, here is your cute hamster. Doesn't it look really cute (≧∀≦)ゞ", color=0x9b59b6)
    em.set_image(url=random.choice(hamster))

  elif pets.name == "Rabbit" : 
    em = discord.Embed(title=f"Here's a cute bunny for ya, {interaction.user.name}!", color=0x2ecc71)
    em.set_image(url=random.choice(rabbit))

  em.set_footer(text="Hope you are happy now :D")
  await interaction.response.send_message(embed=em, ephemeral=False)


@client.tree.command(name="pick1", description="Randomly chooses an object from the given options")
@discord.app_commands.describe(option1="type your first option", option2="type your second option")
async def pick(interaction: discord.Interaction, option1: str, option2: str):
  ty6 = random.randint(1, 2)
  if ty6 == 1:
    chose = option1
  elif ty6 == 2:
    chose = option2
  await interaction.response.send_message(f"I choose **{chose}** 🙋‍♂️", ephemeral=False)


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
  await interaction.edit_original_response(
    content=f"You rolled a {random.randint(1,6)}!")


@client.tree.command(name="toss", description="Why not toss a coin and let it decide?")
@discord.app_commands.describe(side="Will it be Heads or will it be Tails?")
@app_commands.describe(side="Choose a coin side")
@app_commands.choices(side=[
  app_commands.Choice(name="Heads", value=1),
  app_commands.Choice(name="Tails", value=2)
])
async def toss(interaction: discord.Interaction,
               side: discord.app_commands.Choice[int]):
  toss1 = random.randint(1, 2)
  if toss1 == 1:
    toss3 = "Heads"
  elif toss1 == 2:
    toss3 = "Tails"

  if side.name == toss3:
    await interaction.response.send_message(
      f"**{toss3}**! Damn, you won! ( •̀ ω •́ )✧", ephemeral=False)
  elif side.name != toss3:
    await interaction.response.send_message(
      f"**{toss3}**! Oops, looks like you lost 💔", ephemeral=False)


@client.tree.command(name="spamstart", description="start a spam for a given amount.")
@discord.app_commands.describe(
  message="type the sentence/word you want",
  amount=
  "The number of times, the sentence/word should be spammed. Must be less than 100 and 50 is default"
)
async def spam(interaction: discord.Interaction,
               message: str,
               amount: typing.Optional[int] = 50):
  global spam
  await interaction.response.send_message("Starting spam.", ephemeral=True)
  spam = True

  if amount <= 100:
    for i in range(amount):
      await interaction.channel.send(message)
      if spam == False:
        await interaction.response.send_message("Stopping the spam....")
        await interaction.channel.send("The spam has been stopped.")
        break
    spam = False
  else:
    await interaction.response.send_message(
      "Please enter the amount less than 100.", ephemeral=True)


@client.tree.command(name="spamstop", description="stops the spam")
@commands.has_permissions(manage_messages=True)
async def stopspam(interaction: discord.Interaction):
  global spam
  if spam == True:
    spam = False
    await interaction.response.send_message("Spam has been stopped!",
                                            ephemeral=True)
  else:
    await interaction.response.send_message(
      "I can't see any spam going on .-?", ephemeral=True)


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
  r = requests.get(rid_url, headers={'X-Api-Key': 'BTspUmBIPI31D1TVhqwQrQ==gEeG6rS7mi0Fenkl'})
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




@client.tree.command(name="slap", description="Don't hold your anger, just slap and calm yourself down~")
@discord.app_commands.describe(member="Mention the member you wanna slap")
async def slap(interaction: discord.Interaction, member: discord.Member):
  user_id = int(interaction.user.id)
  person_id = int(member.id)
  result = dataman("userdata/slap_count.json", user_id, person_id)
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
