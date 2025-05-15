# penguinsServent.py
import os
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands

# Note to self: Discord Guilds == Discord Servers
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot( command_prefix='!',intents = intents)

user = bot.user
def arrToStr (arr) :
    out = ' '.join(arr)
    return out
    

def getDisplayName(DN) :
    guild = getGuild(GUILD)
    for member in guild.members:
        if member.display_name == DN:
            return member
    return None

def getNick(nick) :
    guild = getGuild(GUILD)
    for member in guild.members:
        if member.nick == nick:
            return member
    return None

def getMemb(name) :
    guild = getGuild(GUILD)
    for member in guild.members:
        if member.name == name:
            return member
    return None

def getMember(name) :
    target = getMemb(name)
    if target != None :
        return target
    target = getNick(name)
    if target != None:
        return target
    target = getDisplayName(name)
    return target


def getRole(roleName) :
    guild = getGuild(GUILD)
    for role in guild.roles:
        if role.name == roleName:
            return role
    return None

def getGuild(GUILD) :
    for guild in bot.guilds:
        if guild.name == GUILD:
            return guild

@bot.event
async def on_ready():

    guild = getGuild(GUILD)
    
    print(f'{user} has connected to discord in the server ' f'{guild.name} (id: {guild.id})')
    # add required roles
    hasPenOwn = False
    HasbdBoy = False
    for currentRole in guild.roles:
        if currentRole.name == 'Penguin Owner' :
            hasPenOwn = True
        elif currentRole.name == 'Bad Boy' :
            HasbdBoy = True
    if not hasPenOwn :
        await guild.create_role(name = 'Penguin Owner', colour = discord.Colour.blurple())
        await getRole('Penguin Owner').move(below=getRole('@everyone'))
    if not HasbdBoy :
        await guild.create_role(name = 'Bad Boy', colour = discord.Colour.darker_grey())
        await getRole('Bad Boy').move(above=getRole('Penguin Owner'))


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send("How did you get here")

@bot.command(name = 'roll', help = ': Rolls a number between 0 and 100')
async def roll(context):
    if context.author == bot.user:
        return
    else :
        response = random.randint(0,100)
        await context.send(response)

#TODO check permision hierarchy
@bot.command (name = 'silence', help = ': This user has been a bad boy and they dont deserve to talk (gives bad boy role)')
@commands.has_role('Penguin Owner')
async def silence(context, *nameArr) :
    if context.author == bot.user :
        return
    else :
        badBoy = arrToStr(nameArr)
        target = getMember(badBoy)
        if target == None :
            await context.send(f'{badBoy} does not exist')
        else :
            await target.add_roles(getRole('Bad Boy'))
            try:
                await target.edit(mute = True)
            except:
                print('User not in voice')
            await target.edit(nick = 'Bad Boy')
            await context.send(f'{badBoy} has been silenced')

@bot.command (name = 'unsilence', help = ': This user has been forgiven and can now talk (removes bad boy role)')
@commands.has_role('Penguin Owner')
async def silence(context, *nameArr) :
    if context.author == bot.user :
        return
    else :
        goodBoy = arrToStr(nameArr)
        target = getMember(goodBoy)
        if target == None :
            await context.send(f'{goodBoy} does not exist')
        else :
            await target.remove_roles(getRole('Bad Boy'))
            try :
                await target.edit(mute = False)
            except:
                print('User not in voice')
            # TODO: change to previous nick after
            await target.edit (nick = None)
            await context.send(f'{goodBoy} has been forgiven')
                
     
@bot.event
async def on_command_error(context,error) :
    print (error)
    if isinstance (error,commands.errors.MissingRole): 
        await context.send(f'You do not have the role Penguin Owner so you can not command me')
    elif isinstance (error,commands.errors.CommandInvokeError):
        raise
    else :
        raise


bot.run(TOKEN)