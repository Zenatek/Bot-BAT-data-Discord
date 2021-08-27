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
    mau = mau.replace("Million","mln")
    
    # select DAU <p>
    dau = str(soup.select("div p")[2])
    
    # filter MAU data
    dau = dau.replace("<p>","")
    dau = dau.replace("</p>","")
    dau = dau.replace("Million","mln")

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


# ch_id_list = list()

# bot = commands.Bot(command_prefix='&')

# @bot.command(ch_id_list = ch_id_list)
# @has_permissions(manage_channels=True)
# async def config(ctx, arg):

#     await ctx.guild.create_category("📈 Brave DATA Tracker 📈")
#     cat = discord.utils.get(ctx.guild.categories, name="📈 Brave DATA Tracker 📈")
#     guild = ctx.message.guild
#     channel_name_updated = "USD | Gwei"
#     await guild.create_voice_channel(name=channel_name_updated, category=cat)
#     ch_id_list.append(discord.utils.get(ctx.guild.channels, name=channel_name_updated))
#     # print(ch_id_list)
#     helper = "Go to voice channel settings and set connect to False.\n\n" "Type: $start track"
#     await ctx.send(helper)


# @bot.command(price_url=price_url, gas_url=gas_url, ch_id_list = ch_id_list)
# @has_permissions(manage_channels=True)

# async def start(ctx, arg):
#     starttime = time.time()
#     while True:
#         bat_price = bat_current_price(price_url)
#         gas_value = gas_current_value(gas_url)
#         channel_name_updated = str(bat_price) + " USD " + " | " + str(gas_value) + " Gwei"
#         # await ctx.send(channel_name_updated)
#         print(channel_name_updated)
#         ch = discord.utils.get(ctx.guild.channels, id=ch_id_list[0].id)
#         await ch.edit(name = channel_name_updated)
#         time.sleep(300.0 - ((time.time() - starttime) % 300.0))


if __name__ == '__main__':
    print("Running")
    #bot.run(os.environ.get('TOKEN'))
    # bot.run("")
    print(MAU_DAU(_url))
    print(monthly_ads(_url2))