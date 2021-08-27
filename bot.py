from discord import channel
import requests
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import time
import os
from bs4 import BeautifulSoup
import string
import pandas as pd
from datetime import date

from requests.models import requote_uri


_url = 'https://brave.com/transparency/'
_url2 = "https://bravebat.info/brave_initiated_bat_purchase"

def MAU_DAU(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.content,"html.parser")
    
    # select MAU <p>
    mau = str(soup.select("div p")[1])
    
    # filter MAU data
    mau = mau.replace("<p>","")
    mau = mau.replace("</p>","")
    mau = mau.replace("Million","M")
    
    # select DAU <p>
    dau = str(soup.select("div p")[2])
    
    # filter MAU data
    dau = dau.replace("<p>","")
    dau = dau.replace("</p>","")
    dau = dau.replace("Million","M")

    # return data on dict 
    return {"mau":mau,"dau":dau}

def check_month():
    today = date.today()
    current_month = today.strftime("%Y-%m")
    return current_month

def filter_Transaction_monthly (df,current_month):
    for row in df:
        return row[row['Date'].str.contains(current_month, case=False)]


def monthly_ads(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")

    table_transaction = soup.findAll('table')[0]
    df = pd.read_html(str(table_transaction))
    current_month = check_month()

    trans_tb = filter_Transaction_monthly(df,current_month)
    
    trans_tb['Dollar Amount'] = trans_tb['Dollar Amount*'].str.replace(r'\D', '')

    monthly_transaction = 0
    for row in trans_tb['Dollar Amount']:
        monthly_transaction += int(row)
 
    return ('${:,}'.format(monthly_transaction))



bot = commands.Bot(command_prefix="?")

@bot.command()
@has_permissions(manage_channels=True)
async def h(ctx, arg):
    await ctx.send("?config channels: to create the trackers\n?start trackers: to track data every 12h")

@bot.command()
@has_permissions(manage_channels=True)
async def config(ctx, arg):
    cat = discord.utils.get(ctx.guild.categories, name="🐯🎯 Brave DATA 🎯🐯")
    if(cat):
        await ctx.send("Category already exists! Type ?start trackers")
    else:
        await ctx.guild.create_category("🐯🎯 Brave DATA 🎯🐯")
        cat = discord.utils.get(ctx.guild.categories, name="🐯🎯 Brave DATA 🎯🐯")
        await ctx.send("Category create!")
        guild = ctx.message.guild
        channel_name_updated = "MAU: "
        await guild.create_voice_channel(name=channel_name_updated, category=cat)
        channel_name_updated = "DAU: "
        await guild.create_voice_channel(name=channel_name_updated, category=cat)
        channel_name_updated = "Monthly ads: "
        await guild.create_voice_channel(name=channel_name_updated, category=cat)
        await ctx.send("Channels ready to track. Type ?start trackers")


@bot.command()
@has_permissions(manage_channels=True)

async def start(ctx, arg):
    cat = discord.utils.get(ctx.guild.categories, name="🐯🎯 Brave DATA 🎯🐯")
    list_voice_ch = cat.channels
    starttime = time.time()
    while True:
        mau_dau_dict = MAU_DAU(_url)
        month_ads = monthly_ads(_url2)
        print("MAU: " + mau_dau_dict['mau'] + "  " + "DAU: " + mau_dau_dict['dau'] + "  " + "Monthly ads: " + month_ads)
        ### Update MAU
        channel_name_updated = "MAU: " + mau_dau_dict['mau']
        # await ctx.send(channel_name_updated)
        # print(channel_name_updated)
        ch = discord.utils.get(ctx.guild.channels, id=list_voice_ch[0].id)
        await ch.edit(name = channel_name_updated)

        ### Update DAU
        channel_name_updated = "DAU: " + mau_dau_dict['dau']
        # await ctx.send(channel_name_updated)
        # print(channel_name_updated)
        ch = discord.utils.get(ctx.guild.channels, id=list_voice_ch[1].id)
        await ch.edit(name = channel_name_updated)

        ### Update Monthly ads
        channel_name_updated = "Monthly ads: " + month_ads
        # await ctx.send(channel_name_updated)
        # print(channel_name_updated)
        ch = discord.utils.get(ctx.guild.channels, id=list_voice_ch[2].id)
        await ch.edit(name = channel_name_updated)
        time.sleep(43200.0 - ((time.time() - starttime) % 43200.0))


if __name__ == '__main__':
    print("Running")
    bot.run(os.environ.get('TOKEN_BRAVE_DATA_BOT'))
    