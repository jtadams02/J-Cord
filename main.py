import discord
from discord.ext import commands
import os
# Signal will allow us to update our swearlist on CTRL+C
import signal
# Below will handle getting the discord bot's token to log in
from dotenv import load_dotenv
load_dotenv()
# For testing with bungie stuff
import aiobungie
# Random number generator
import random
# Bungie API Key a7a359696ab84fcebf7a31bb9b2ebddf
# Probably shouldn't leave that public but whatevs
bclient = aiobungie.Client('a7a359696ab84fcebf7a31bb9b2ebddf')
# Date and Time
import datetime,time
# UserList

# We need our list of no-no words, lets get it
bad_words = []
f = open('swearlist.txt','r+')
for line in f:
    if not line.strip().lower().isspace():
        bad_words.append(line.strip().lower())
# And here will be the responses to the bad words
bad_responses = ["Erm, Language!","That's not gonna fly here buddy","Watch it buster!","I'm warning you kiddo","We don't talk like that around here"]
# And here will be the responses to the people who are excluded
in_the_clear = ["I didn't see anything","I'll let it slide this time","She gets a pass","I'm misandrist so I'll just ignore this"]
# Responses to truppa
joe_words = [
    "Not funny",
    "Try again tman",
    "No one cares",
    "Did anyone ask?"
]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
# Time that the discord client starts????
startTime = time.time()
# I don't know what code below does
# Bot variable?

bot = commands.Bot(command_prefix='$',intents=intents)

@bot.command()
async def whois(ctx):
        await ctx.send("I am a discord bot made in Python by the legendary man JT!")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(789609064967307274)
    startTime = time.time()
    await channel.send("Raspberry PyBot Online!")




@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # This is just the prefix command. I know I'm not doing commands right but I'm learning okay
    if message.content == '$':
        await message.channel.send("`$ is my prefix. If you\'d like to see more commands enter \"$help\"\nI am a bot coded in Python by JT`")
        return

    # Simple help command
    if message.content == '$help':
        await message.channel.send("`There aren't a lot of commands right now, but here's what we got:\n$swear : Report a swear word you would like to add to the no-no list\n$delete : Delete a swear word from the swear list\n$list : List all of the swears in the swearlist!\n$shutdown : Turn off the discord bot (Only JT can run this)`")
        return

    # I'm gonna make the shutdown command run first due to priority reasons
    if message.content == '$shutdown':
        if message.author.id == 173748750068482048:
            await client.close()
            return # Is this needed?
        else:
            message.reply('Sorry, but only King JT can run this command! Better luck next time')
            return
    
    # List the swear list
    if message.content == '$list':
        # Loop time to print
        response1 = '`'
        for word in bad_words:
            response1+=(word+'\n')
        response1+='`'
        await message.channel.send(response1)
        return
            
    # Ideally this will add the given swear to the swear list. Jt should maintain the swear list to make sure it is right
    if message.content.startswith("$swear"):
        msg = message.content
        if len(msg.split()) < 2:
            await message.reply("We're sorry, but we cannot add an empty space to the list",delete_after=5.0)
            return
        swear = msg.split(' ')[1]
        if swear.isspace():
            await message.reply("We're sorry, but we cannot add an empty space to the list",delete_after=5.0)
            return
        temp = f # Temp variable I do not think is needed!
        if swear.lower() in bad_words:
            await message.reply("We're sorry, but that swear is already on the list!",delete_after=5.0)
            return
        else:
            #temp.write('\n'+swear.lower())
            bad_words.append(swear.lower())
            toSend = (swear+' has been added to the swearlist. Thank you for making our server a safer place!')
            await message.channel.send(toSend)
            return
        
    # This code will remove swears from the bad_words array and ideally the file    
    if message.content.startswith("$delete"):
        msg = message.content 
        if len(msg.split()) < 2:
            await message.reply("Sorry, but swears are only 1 word long!",delete_after=5.0)
            return
        swear = msg.split(' ')[1]
        if swear.isspace():
            await message.reply("Cannot delete empty string",delete_after=5.0)
            return
        if swear.lower() in bad_words:
            # Now we remove the swear
            while(swear.lower() in bad_words):
                bad_words.remove(swear)
            response = swear +" has been deleted!"
            await message.reply(response)
            return
            #IDK how to remove it from file yet?!
        else: 
            await message.reply("We're sorry, but that swear is not in the swear list!")
            return

            

    if message.content == '$uptime':
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        msg = 'JT Bot has been active for: ' + str(uptime)
        await message.channel.send(msg)
        return

    if message.content.startswith('$hi'):
        await message.channel.send('Hello there! I am a robot!')

    if message.content.startswith('$time'):
        today = datetime.today()
        await message.channel.send(today)
        return

    # Below code checks whether or not a word in the message matches a word in bad_words
    # delete_after causes the message to delete after 5 seconds!
    if any(word in message.content.lower() for word in bad_words):
            if message.author.id == 743721232326852628:
                await message.reply(random.choice(in_the_clear),delete_after=5.0)
                return
            else:
                await message.reply(random.choice(bad_responses),delete_after=5.0)
                return
    # tman, just respondes to tman lol
    if message.author.id == 1106741623943086090:
        random_number = random.randint(1,2)
        if random_number == 1:
            await message.reply(random.choice(joe_words),delete_after=5.0)
        return

# Below 2 functions will run on a disconnect from wifi, not when CTRL+C is pressed
@client.event
async def on_disconnect():
    # This should run when the discord bot disconnects from the server. At this time I will have it update the swearlist file!
    print('Regular disconnect')
    # We need to update swear list!
    f.close()
    rewriteFile = open('swearlist.txt','w')
    for i in bad_words:
        rewriteFile.write(i.lower()+'\n')
        print(i.lower())
    # Should be perfect

@client.event
async def on_shard_disconnect():
    # This should run when the discord bot disconnects from the server. At this time I will have it update the swearlist file!
    print("Shard Disconnect")
    f.close()
    rewriteFile = open('swearlist.txt','w')
    for i in bad_words:
        rewriteFile.write('\n'+i.lower())
        print ("Writing: " + i.lower + " to file!")
    return

# Handler for CTRL+C, thanks stack overflow
def signal_handler(sig,frame):
    print("CTRL+C Detected")
    f.close()
    rewriteFile = open('swearlist.txt','w')
    for i in bad_words:
        rewriteFile.write('\n'+i.lower())
        print ("Writing: " + i.lower + " to file!")
    # This code kills program
    sys.exit(0)

client.run(os.getenv('BOT_TOKEN'))
signal.signal(signal.SIGINT, signal_handler)
#signal.pause() THIS CODE DOESNT WORK ON WINDOWS!

