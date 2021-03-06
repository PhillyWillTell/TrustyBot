from random import choice as randchoice
from datetime import datetime as dt
from discord.ext import commands
import discord
from .utils.dataIO import dataIO
from .utils import checks
import random
import os
import asyncio

try:
    from phue import Bridge
    phue_install = True
except ImportError:
    phue_install = False


class Oilers:

    def __init__(self, bot):
        self.bot = bot
        self.bridge = Bridge("192.168.0.35")
        self.lights = self.bridge.lights 
        self.bridge2 = Bridge("192.168.0.115")
        self.lights2 = self.bridge2.lights 

    # @commands.command(pass_context=True)
    async def oilersgoal2(self):
        old_lights = {}
        old_lights2 = {}
        for light in self.lights:
            old_lights[light.name] = [light.on, light.colortemp]
        for light in self.lights2:
            old_lights2[light.name] = [light.on, light.colortemp]
        for i in range(5):
            await self.oilers_hex_set(1.0, 1.0)
            await asyncio.sleep(0.5)
            await self.oilers_hex_set(0, 0)
            await asyncio.sleep(0.5)
        for light in self.lights:
            old_temp = old_lights[light.name][1]
            if old_temp < 154:
                old_temp = 154
            if old_temp > 500:
                old_temp = 499
            light.colortemp = old_temp
            light.on = old_lights[light.name][0]
        for light in self.lights2:
            old_temp = old_lights2[light.name][1]
            if old_temp < 154:
                old_temp = 154
            if old_temp > 500:
                old_temp = 499
            light.colortemp = old_temp
            light.on = old_lights2[light.name][0]
            

    @commands.command(hidden=True, name="oilers_connect")
    async def hue_connect(self):
        """Setup command if bridge cannot connect"""
        self.bridge.connect()
        self.bridge2.connect()
        print("done")

    async def oilers_hex_set(self, x:float, y:float, *, name=None):
        """Sets the colour for Oilers Goals"""
        if x > 1.0 or x < 0.0:
            x = 1.0
        if y > 1.0 or y < 0.0:
            y = 1.0
        for light in self.lights:
            if not light.on:
                light.on = True
            light.xy = [x, y]
        for light in self.lights2:
            if not light.on:
                light.on = True
            light.xy = [x, y]

def setup(bot):
    bot.add_cog(Oilers(bot))