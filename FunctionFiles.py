import pandas as pd, json, os, requests

def setup(userid:int, author) : 
  if not os.path.exists("userdata/users.csv") : 
    df = pd.DataFrame({"id":[], "purrcoins":[], "purrgems":[], "dailylevel":[], "username":[], "nickname":[], "favpet":[], "age":[], "gender":[],"bio":[], "wallpaper":[],"embcolor":[], "basic" : [], "regular" : [], "elite" : [], "premium" : [], "epic" : [], "supreme" : [], "fishlevel":[], "baits":[], "totalfishes":[]})
    df.to_csv("userdata/users.csv", index=False)
  if not os.path.exists("userdata/inventory.json") : 
    with open("userdata/inventory.json", "w") as f : 
      f.write("[]")
  df = pd.read_csv("userdata/users.csv")
  if userid not in df["id"].values :
    newdf = pd.DataFrame({"id":[userid], "purrcoins":[1000], "purrgems":[0], "dailylevel":[1], "username":[author], "nickname":["Not set"], "favpet":["Not set"], "age":["Not set"], "gender":["Not set"],"bio":["Not set"], "wallpaper":["Not Set"], "embcolor":[0], "basic":[0], "regular":[0], "elite":[0], "premium":[0], "epic":[0], "supreme":[0], "fishlevel":[1], "baits":[0], "totalfishes":[0]})
    df = pd.concat([df, newdf], ignore_index=True)
    df.to_csv("userdata/users.csv", index=False)
  
  # Making JSON file
  with open("userdata/inventory.json") as f : 
    datafile = json.load(f)
  if str(userid) not in datafile:
    datafile.append({str(userid):[]})
    with open("userdata/inventory.json", "w") as f :
      json.dump(datafile, f, indent=2)
    print("Registered new user")

def show_action_count(filename, userid) : 
  with open(filename) as f :
    data = json.load(f)
  lisofppl = data[userid]
  sorted_lis = sorted(lisofppl, key=lambda d: list(d.values())[0], reverse=True)
  return sorted_lis

def increase_action_count(filename, userid, personid) :
  userid = str(userid)
  personid = str(personid)
  with open(filename) as f : 
    file_data = json.load(f)
  # check if user and member are in data file
  if userid not in file_data : 
    file_data[userid] = {}
  if personid not in file_data[userid]:
    file_data[userid][personid] = 0
  file_data[userid][personid] += 1
  with open(filename, "w") as w :
    json.dump(file_data, w, indent=2)
    return file_data[userid][personid]

def openinv(userid:str)->list :
  userid = str(userid)
  with open("userdata/inventory.json") as f : 
    datafile = json.load(f)
  try: 
    return datafile[userid]
  except KeyError:
    return []

def userindex(userid:int) :
  df = pd.read_csv("userdata/users.csv")
  return df.index[df["id"] == userid][0]

def retrieveLeetCodeDetails() -> tuple:
  usernames = {"AnandSaxena": "Anand", "Shinzoo05":"Jasmine", "kshavcodes" : "Keshav", "singhsomay467" : "Somay", "akashhuge7" : "Shivam"}
  problemsSolved = dict()
  errorNames = []
  for idx in usernames: 
    url = f"https://leetcode-stats-api.herokuapp.com/{idx}"
    try:
      r = requests.get(url).json()
      if r["status"] != "success":
        return "Kindly check if you provided the correct username, otherwise, this might just be an issue from the other side (It'll be fixed soon, else use `/feedback` to notify the creator)."
      else : 
        problemsSolved[r["totalSolved"]] = usernames[idx]
    except Exception as e:
      errorNames.append(usernames[idx])
      continue
  
  return ([f"{problemsSolved[i]} ({i})" for i in reversed(sorted(problemsSolved))], errorNames)