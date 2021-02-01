from discord.ext import commands
import discord
import requests
import json
import os
client = commands.Bot(command_prefix="cov ")
client.remove_command("help")
@client.event
async def on_ready():
    await client.change_presence(
    activity=discord.Activity(            type=discord.ActivityType.watching, name="For `cov help`"))
    print(client.user, "is ready")

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send("The prefix is `cov`")
    message.content = message.content.lower()
    await client.process_commands(message)
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		em = discord.Embed(title="Invalid Command", description=f"{str(error)}. Try `cov help` for a list of commands.", color=0x275ef4)
		await ctx.send(embed=em)
@client.group(invoke_without_command=True)
async def total(ctx):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/total').text)['data']
  em=discord.Embed(title='Total COVID-19 Data',description='')
  em.add_field(name='Total Confirmed Cases',value=str(data['confirmed']),inline=False)
  em.add_field(name='Total Deaths',value=str(data['deaths']),inline=False)
  em.add_field(name='Total Recovered',value=str(data['recovered']),inline=False)
  em.add_field(name='Total Active Cases',value=str(data['active']),inline=False)
  await ctx.send(embed=em)
@total.command(name='confirmed')
async def total_confirmed(ctx):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/total').text)['data']['confirmed']
  em=discord.Embed(title='Total COVID-19 Confirmed Cases',description=str(data))
  await ctx.send(embed=em)
@total.command(name='deaths')
async def total_deaths(ctx):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/total').text)['data']['deaths']
  em=discord.Embed(title='Total COVID-19 Deaths',description=str(data))
  await ctx.send(embed=em)
@total.command(name='recovered')
async def total_recovered(ctx):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/total').text)['data']['recovered']
  em=discord.Embed(title='Total COVID-19 Recovered',description=str(data))
  await ctx.send(embed=em)
@total.command(name='active')
async def total_active(ctx):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/total').text)['data']['active']
  em=discord.Embed(title='Total COVID-19 Active Cases',description=str(data))
  await ctx.send(embed=em)
@client.group()
async def country(ctx,country_name):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/country/'+str(country_name)).text)['data']
  em=discord.Embed(title='Country COVID-19 Data',description='')
  em.add_field(name='Country Name',value=str(data['location']))
  em.add_field(name='Country Confirmed Cases',value=str(data['confirmed']),inline=False)
  em.add_field(name='Country Deaths',value=str(data['deaths']),inline=False)
  em.add_field(name='Country Recovered',value=str(data['recovered']),inline=False)
  em.add_field(name='Country Active Cases',value=str(data['active']),inline=False)
  await ctx.send(embed=em)
@country.error
async def country_error(ctx,error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Specify a country, like this: `cov country <country name>`")
#country subcommands do not work
'''@country.command(name='confirmed')
async def country_confirmed(ctx,country_name):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/country'+str(country_name)).text)['data']['confirmed']
  em=discord.Embed(title='Country COVID-19 Confirmed Cases',description=str(data))
  await ctx.send(embed=em)
@country.command(name='deaths')
async def country_deaths(ctx,country_name):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/country/'+str(country_name)).text)['data']['deaths']
  em=discord.Embed(title='Country COVID-19 Deaths',description=str(data))
  await ctx.send(embed=em)
@country.command(name='recovered')
async def country_recovered(ctx,country_name):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/country/'+str(country_name)).text)['data']['recovered']
  em=discord.Embed(title='Country COVID-19 Recovered',description=str(data))
  await ctx.send(embed=em)
@country.command(name='active')
async def country_active(ctx,country_name):
  data=json.loads(requests.get('https://covid2019-api.herokuapp.com/v2/country/'+str(country_name)).text)['data']['active']
  em=discord.Embed(title='Country COVID-19 Active Cases',description=str(data))
  await ctx.send(embed=em)'''
@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(
        title="Help",
        description=
        "COVID-19 - Help Command.\nRemember to use `cov` before each command! You can use `cov help <command>` for information on a certain command.",
        color=0x275ef4)
    em.add_field(
        name="Commands",
        value=
        "`total`,`country`",inline=False
    )
    await ctx.send(embed=em)
class HelpCommand:
    def __init__(self, title, desc, usage, aliases):
        self.title = "Help on`"+title+'`'
        self.desc = desc
        self.color = 0x275ef4
        self.desc = desc
        self.aliases = aliases
        self.usage = '`'+usage+'`'
        self.em = discord.Embed(
            title=self.title, description=self.title, color=self.color)
        self.em.add_field(name="Description", value=desc,inline=False)
        self.em.add_field(name="Usage", value=usage,inline=False)
        self.em.add_field(name='Aliases', value=aliases,inline=False)
@help.command(name='total')
async def help_total(ctx):
  em=HelpCommand('total','Gives total COVID-19 data on confirmed cases, deaths, recoveries, and active cases. For just the total confirmed cases data, run `cov total confirmed`. For just the total deaths, run `cov total deaths`. For just the recoveries, run `cov total recovered`. For just the total active cases, run `cov total active`.','cov total','None')
  await ctx.send(embed=em.em)
@help.command(name='help')
async def help_help(ctx):
  em=HelpCommand('help','Gives a list of the bot commands.','cov help','None')
  await ctx.send(embed=em.em)
@help.command(name='country')
async def help_country(ctx):
  #For just the country confirmed cases data, run `cov country confirmed <country name>`. For just the country deaths, run `cov country deaths`. For just the recoveries, run `cov country recovered <country name>`. For just the country active cases, run `cov country active <country name>`. 
  em=HelpCommand('country','Gives country COVID-19 data on confirmed cases, deaths, recoveries, and active cases. The country name can also be replaced with the ISO code of the country.','cov country <country name>','None')
  await ctx.send(embed=em.em)
client.run(os.getenv("DISCORD_BOT_SECRET"))