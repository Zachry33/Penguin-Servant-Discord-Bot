# penguinsServent.py
import os
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands
import sqlite3
import datetime

# Note: Discord Guilds == Discord Servers
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Add intents for the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
bot = commands.Bot( command_prefix='!',intents = intents)

# Connect bot to database and initilize table with users
connection = sqlite3.connect('PenguinsServant.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS ' + GUILD.replace(' ', '') + ' (Username TEXT PRIMARY KEY, Nick TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS ' + GUILD.replace(' ', '') + '_List' + ' (Content TEXT, Due INTEGER, Username TEXT, FOREIGN KEY(Username) REFERENCES ' + GUILD.replace(' ', '') + '(Username))')

user = bot.user

# Join Arr with spaces for usernames 
def arrToStr (arr) :
    out = ' '.join(arr)
    return out
    
# Attempts to find member by display name
def getDisplayName(DN) :
    guild = getGuild(GUILD)
    for member in guild.members:
        if member.display_name == DN:
            return member
    return None

# Attemps to find member by nick
def getNick(nick) :
    guild = getGuild(GUILD)
    for member in guild.members:
        if member.nick == nick:
            return member
    return None

# Attempts to find user by discord name
def getMemb(name) :
    guild = getGuild(GUILD)
    for member in guild.members:
        if member.name == name:
            return member
    return None

# Attemps to find the users name by checking display name, nick and discord name
# Returns None if cannot be found
def getMember(name) :
    target = getMemb(name)
    if target != None :
        return target
    target = getNick(name)
    if target != None:
        return target
    target = getDisplayName(name)
    return target

# Returns a Role object given a string of the role name
def getRole(roleName) :
    guild = getGuild(GUILD)
    for role in guild.roles:
        if role.name == roleName:
            return role
    return None

# Returns the guild object given the name of the guild
def getGuild(GUILD) :
    for guild in bot.guilds:
        if guild.name == GUILD:
            return guild

# Accepts a datetime delta object and returns a strng with the format of ? days ? hours
def getDueDate(dtDelta) :
    # Total seconds in the duration
    total_seconds = int(dtDelta.total_seconds())
    
    # Calculate days, then the remaining seconds
    days, remaining_seconds = divmod(total_seconds, 86400) # 60*60*24 seconds in a day
    
    # Calculate hours from the remaining seconds
    hours, _ = divmod(remaining_seconds, 3600) # 60*60 seconds in an hour
    
    # Use 'day' or 'days' for correct grammar
    day_str = "day" if days == 1 else "days"
    hour_str = "hour" if hours == 1 else "hours"
    
    return f'{days} {day_str}, {hours} {hour_str}'

# On Connection to discord
@bot.event
async def on_ready():

    # Locates guild and prints information for the guild
    guild = getGuild(GUILD)
    print(f'{user} has connected to discord in the server ' f'{guild.name} (id: {guild.id})')
   
    # Add required roles if they do not exist already
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

    # Insert new data into database
    for member in guild.members:
        cursor.execute(f'INSERT OR IGNORE INTO {GUILD.replace(' ', '')} (Username, Nick) VALUES (?, ?)', (member.name, member.nick))

# Sends a message to any user who joins the server and adds them to the db
@bot.event
async def on_member_join(member):
    cursor.execute(f'INSERT OR IGNORE INTO {GUILD.replace(' ','')} (Username, Nick) VALUES (?, ?)', (member.name, member.nick))
    await member.create_dm()
    await member.dm_channel.send("How did you get here")

# If a user joins a VC and they have the bad boy role then they will be server muted or vise vera if the opposite
@bot.event
async def on_voice_state_update(member, before, after):
    if before.mute == False and getRole('Bad Boy') in member.roles and after.channel != None:
        try :
            await member.edit(mute = True)
        except :
            print ('User not in Voice')
    elif before.mute == True and getRole('Bad Boy') not in member.roles and after.channel != None:
        try :
            await member.edit(mute = False)
        except :
            print ('User not in Voice')

# If someone with the bad boy role trys to talk in a text channel their message will be deleted
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
      return
    else :
        if type (message.author) is discord.member.Member :
            if getRole('Bad Boy') in message.author.roles and type(message.channel) is not discord.channel.DMChannel: 
                await message.channel.send(f'{message.author} tried to speak')
                await message.delete()


# Rolls a random number between 0 and 100
@bot.command(name = 'roll', help = ': Rolls a number between 0 and 100')
async def roll(context):
    if context.author == bot.user:
        return
    else :
        response = random.randint(0,100)
        await context.send(response)

# This command will take in a name and do the following:
# - Give the "Bad Boy" role
# - Server mute them if they are in a call
# - update current nickname into db
# - Change their nick to "Bad Boy"
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
        elif target.top_role >= getRole('Penguin Owner'):
            await context.send(f'{badBoy} has too much aura to be silenced')
        else :
            await target.add_roles(getRole('Bad Boy'))
            try:
                await target.edit(mute = True)
            except:
                print('User not in voice')
            cursor.execute(f'UPDATE {GUILD.replace(' ','')} SET Nick = ? WHERE Username = ?', (target.nick, target.name))
            await target.edit(nick = 'Bad Boy')
            await context.send(f'{badBoy} has been silenced')

# This command will take in a name and do the following:
# - Remove the "Bad Boy" role
# - Server unmute them if they are in a call
# - Remove their nick
@bot.command (name = 'unsilence', help = ': This user has been forgiven and can now talk (removes bad boy role)')
@commands.has_role('Penguin Owner')
async def unsilence(context, *nameArr) :
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
            cursor.execute(f'SELECT Nick FROM {GUILD.replace(' ', '')} WHERE Username = ?', (target.name,))
            oldNick = cursor.fetchone()
            await target.edit (nick = oldNick[0])
            await context.send(f'{goodBoy} has been forgiven')

# This command will display the users current to do list with given due dates
@bot.command (name = 'list', help = ': this users current to do list will be displayed')
async def list (context) :
    if context.author == bot.user:
        return
    else :
        cursor.execute(f'SELECT Content, Due FROM {GUILD.replace(' ', '')}_List WHERE Username = ? ORDER BY Due ASC', (getMember(context.author),))
        listData = cursor.fetchall()
        output = ""
        for row in listData:
            output += row[0] + ' Due in: ' + getDueDate(datetime.datetime.fromtimestamp(row[1])-datetime.datetime.now) + '\n'
        output = output.strip()
        if (output == '') :
            await context.send('List is empty')
        else :
            await context.send(output)
        

# This command will add the specified item to the users current to do list
@bot.command (name = 'add', help = ': this will add the item specified to the users list. Format: ("content" + " " + "MM/DD/HH)"')
async def add (context, *textArr) :
    if context.author == bot.user:
        return
    elif len(textArr) == 0:
        await context.send('Improper Format')
    else :
        # parse the given date into unix timestamp
        date = datetime.strptime(datetime.datetime.now().year + textArr[-1], '%Y/%m/%d/%H')
        timestamp = date.timestamp()
        if datetime.datetime.now > date :
            await context.send('Improper Time Format')
            return
        # add the rest of the content into a string and add it to the list
        content = ' '.join(textArr[:-1]).strip()
        cursor.execute(f'INSERT INTO {GUILD.replace(' ','')}_List (Content, Due, Username) VALUES (?, ? ,?)', (content, timestamp, context.author))
        await context.send(f'{content} added to list')

# This command will remove the specified item from the users current to do list 
@bot.command (name = 'complete', help = ': this will remove the specified item from the users list. (must specify exact name)')
async def remove(context, *textArr) :
    if context.author == bot.user:
        return
    elif len(textArr) == 0:
        await context.send('Improper Format')
    else :
        content = ' '.join(textArr).strip()
        cursor.execute(f'SELECT Content FROM {GUILD.replace(' ', '')}_List WHERE Username = ? AND Content = ?', (context.author, content))
        listData = cursor.fetchone()
        if (len(listData)== 0) :
            await context.send(f'{content} was not found in your list')
        elif (listData[0].strip() == content) :
            cursor.execute(f'DELETE FROM {GUILD.replace(' ','')}_List WHERE Content = ? AND Username = ?', (content, context.author))
            await context.send(f'{content} has been removed from your list')
        else :
            await context.send(f'{content} was not found in your list')



# This Command will allow you to interact with a virtual penguin with battling and leveling
                
# On appropriate errors the bot will send back the appropriate message
@bot.event
async def on_command_error(context,error) :
    print (error)
    if isinstance (error,commands.errors.MissingRole): 
        await context.send(f'You do not have the role Penguin Owner so you can not command me')
    elif isinstance (error,commands.errors.CommandInvokeError):
        raise (error)
    else :
        raise


bot.run(TOKEN)