import os
import discord
from discord.ext import commands
import requests
import sys
import setuptools
from itertools import cycle
import threading
from core import Astroz, Cog
import datetime
import logging
import time
import asyncio
import aiohttp
import tasksio
from discord.ext import tasks
import random
from utils.Tools import *

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

proxies = open('proxies.txt').read().split('\n')
proxs = cycle(proxies)
proxies={"http": 'http://' + next(proxs)}

class antichannel(Cog):
    def __init__(self, client: Astroz):
        self.client = client      
        self.headers = {"Authorization": f"Bot OTA2MDg1NTc4OTA5NTQ4NTU0.GY8nds.JJ-k2ckUpGokqxdvbwlgJwmklthFvzqLR0qcwI"}




        
    async def delete(channel: discord.abc.GuildChannel):
      try:
        await channel.delete()
      except:
        pass


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel) -> None:
        try:
          start = time.perf_counter()
          data = getConfig(channel.guild.id)
          anti = getanti(channel.guild.id)
          event= getHacker(channel.guild.id)
          antievent = event["antinuke"]["antichannel-create"]
          punishment = data["punishment"]
          wlrole = data['wlrole']
          wled = data["whitelisted"]
          guild = channel.guild
          reason = "Channel Created | Not Whitelisted"
        
          async for entry in guild.audit_logs(
                limit=1):
            user = entry.user.id
          api = random.randint(8,9)
          if entry.user.id == self.client.user.id or entry.user.id == guild.owner_id or str(entry.user.id) in wled or anti == "off" or antievent == False:
            return
     
          else:
           if entry.action == discord.AuditLogAction.channel_create:
            async with aiohttp.ClientSession(headers=self.headers) as session:
              if punishment == "ban":
                  async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                    end = time.perf_counter()
                    fck = end-start
                 #   r = requests.delete(
			       #       f"https://discord.com/api/v8/channels/{channel.id}",
			        #      headers=self.headers)
                #    if 'retry_after' in r.text:
                #      time.sleep(r.json()['retry_after'])
                #    else:
                #      if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                 #       logging.info(f"Successfully Deleted Channel {channel.name}")
                 #     else:
                  #      pass
                    #await channel.delete()
                    if r.status in (200, 201, 204):
                      logging.info("Successfully banned %s in %s ms"% (user, fck*1000))
                    
              elif punishment == "kick":
                         async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r2:
                             r = requests.delete(
			                      f"https://discord.com/api/v8/channels/{channel.id}",
			                        headers=self.headers)
                             if 'retry_after' in r.text:
                               time.sleep(r.json()['retry_after'])
                             else:
                               if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                                 logging.info(f"Successfully Deleted Channel {channel.name}")
                               else:
                                 pass
                             if r2.status in (200, 201, 204):
                             

                               logging.info("Successfully kicked %s" % (user))
              elif punishment == "none":
                mem = guild.get_member(entry.user.id)
                await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
                r = requests.delete(
			              f"https://discord.com/api/v8/channels/{channel.id}",
			              headers=self.headers)
                if 'retry_after' in r.text:
                  time.sleep(r.json()['retry_after'])
                  if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    logging.info(f"Successfully Deleted Channel {channel.name}")
                else:
                  pass
              else:
                       return
        except Exception as error:
            if isinstance(error, discord.Forbidden):
              return





    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel) -> None:
        try:
          data = getConfig(channel.guild.id)
          anti = getanti(channel.guild.id)
          event= getHacker(channel.guild.id)
          antievent = event["antinuke"]["antichannel-delete"]
          wlrole = data['wlrole']  
          punishment = data["punishment"]
          wled = data["whitelisted"]
          guild = channel.guild
          reason = "Channel Deleted | Not Whitelisted"
          
          async for entry in guild.audit_logs(
                limit=1):
            user = entry.user.id
          api = random.randint(8,9)
          if str(entry.user.id) in wled or anti == "off" or antievent == False or entry.user.id == self.client.user.id or entry.user == guild.owner:
            pass
          else:
           if entry.action == discord.AuditLogAction.channel_delete:
            async with aiohttp.ClientSession(headers=self.headers) as session:
              if punishment == "ban":
                  async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                    chan = await channel.clone(reason=reason)
                    await chan.edit(category=channel.category, position=channel.position)
                    if r.status in (200, 201, 204):
                      
                      logging.info("Successfully banned %s" % (user))
              elif punishment == "kick":
                         async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r2:
                             await channel.clone(reason=reason)
                             if r2.status in (200, 201, 204):
                               
                               logging.info("Successfully kicked %s" % (user))
              elif punishment == "none":
                mem = guild.get_member(entry.user.id)
                await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
                await channel.clone(reason=reason)
              else:
                       return
        except Exception as error:
            if isinstance(error, discord.Forbidden):
              return
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after) -> None:
      try:
        data = getConfig(before.guild.id)
        anti = getanti(before.guild.id)
        event= getHacker(before.guild.id)
        antievent = event["antinuke"]["antichannel-update"]
        wlrole = data['wlrole']  
        punishment = data["punishment"]
        wled = data["whitelisted"]
        guild = after.guild
        reason = "Channel Updated | Not Whitelisted"
        
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.utcnow() - datetime.timedelta(seconds=30)):
            user = entry.user.id
        api = random.randint(8,9)
        if str(entry.user.id) in wled or anti == "off" or antievent == False or entry.user.id == self.client.user.id or entry.user == guild.owner:
            pass
                 
        else:
         if entry.action == discord.AuditLogAction.channel_update or entry.action == discord.AuditLogAction.overwrite_update:
          async with aiohttp.ClientSession(headers=self.headers) as session:
            if punishment == "ban":
                  async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                    await after.edit(name=f"{before.name}", topic=before.topic, nsfw=before.nsfw, category=before.category, slowmode_delay=before.slowmode_delay, type=before.type, overwrites=before.overwrites, reason=reason)
                    if r.status in (200, 201, 204):
                      
                      logging.info("Successfully banned %s" % (user))
            elif punishment == "kick":
                         async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r2:
                             await after.edit(name=f"{before.name}", topic=before.topic, nsfw=before.nsfw, category=before.category, slowmode_delay=before.slowmode_delay, type=before.type, overwrites=before.overwrites, reason=reason)
                             if r2.status in (200, 201, 204):
                               
                               logging.info("Successfully kicked %s" % (user))
            elif punishment == "none":
              mem = guild.get_member(entry.user.id)
              await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
              await after.edit(name=f"{before.name}", topic=before.topic, nsfw=before.nsfw, category=before.category, slowmode_delay=before.slowmode_delay, type=before.type, overwrites=before.overwrites, reason=reason)
            else:
                       return
      except Exception as error:
            if isinstance(error, discord.Forbidden):
              return