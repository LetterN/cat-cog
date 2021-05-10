import discord
import time
from .util import Topic, getSeconds, safeget
from discord.ext import commands

class SS13(commands.Cog, name='SS13 Module'):
  def __init__(self):
    super().__init__()

  @commands.command(name="station_status")
  async def ss13_status(self, ctx: commands.Context, ip_port:str):
    ipp = ip_port.split(":")
    dat = self.__standardnizeData(Topic(ipp[0], ipp[1], "status"))

    ourembed: discord.Embed = discord.Embed()
    # We do this first!
    in_the_field = [
      {"name": "Map Name", "value": dat["map_name"]},
      {"name": "Gamemode", "value": dat["mode"]},
      {"name": "Round ID", "value": dat["round_id"]},
      {"name": "Players", "value": dat["players"], "inline": True},
      {"name": "Player Cap", "value": dat["popcap"], "inline": True},
      # DO NOT BLAME ME, SOMEONE STOLE PYTHON'S SWITCH OP
      {"name": "Game State", "value": {0:"Initializing game",1:"Waiting on Lobby",2:"Starting",3:"Started",4:"Round ended"}.get(dat["gamestate"],"Started?")},
      {"name": "Round Duration", "value": dat["round_duration"]+" second(s)"},
      {"name": "Revision", "value": dat["revision"]}
    ]
    ourembed.from_dict({
      "title": "Server Status of "+ip_port,
      "type": "rich",
      "description": "GenericDesc",
      "url": "byond://"+ip_port,
      "fields": in_the_field
    })
    ctx.send(None, embed=ourembed)
    return

  def __standardnizeData(self, data:dict):
    """
    Cleans up the JSON data and returns a backup value if it's nonexistent.
    INTERNAL, CANNOTFAIL
    """
    return_json = {}
    ## begin arry
    return_json["map_name"] = safeget(data, "map_name") or safeget(data, "map") or "Unknown"
    return_json["mode"] = safeget(data, "mode") or "Secret"
    return_json["round_id"] = safeget(data, "round_id") or 0  ## can be a string
    if int(safeget(data, "players")) < 1:
      return_json["players"] = 1
    else:
      return_json["players"] = str(safeget(data, "players"))
    return_json["popcap"] = str(safeget(data, "popcap") or 90)   ##genneraly best guess popcap, will be overriten by maxpop cfg!
    return_json["gamestate"] = str(safeget(data, "gamestate") or 3)    ##|0:SS Startup|1:Lobby|2:Game Starting|3:Game Started|4:Game Ended|
    #works with magic(TM)
    arry_time = 1
    if safeget(data,"stationtime") or safeget(data,"roundduration") or safeget(data,"roundtime"):
      arry_time = (safeget(data,"stationtime") or safeget(data,"roundduration") or safeget(data,"roundtime")).split(":")
      
    return_json["round_duration"] = str(safeget(data, "round_duration") or safeget(data, "elapsed") or getSeconds(*arry_time) or int(time.time()))
    return_json["revision"] = safeget(data, "revision") or ""
    return return_json
