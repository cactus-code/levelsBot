import itertools
import sys
import discord
from discord.ext.commands import Bot

level_bot = Bot(command_prefix="?")
player_stars = {}

with open("stars.txt","r") as file:
    content = file.readlines()
content = [x.strip('\n') for x in content]

d = dict(itertools.zip_longest(*[iter(content)] * 2, fillvalue=""))
player_stars.update(d)

token = "MzIzNjg0MTUwMjIzNTY4OTA3.DCD-KQ.aafOb2aoFhlUSKb_oix2_Nb6G4Y"
game = "Shooting Stars"

def check_for_role(ctx):
    user_role = discord.utils.get(ctx.message.server.roles, name="Starlord")
    author_roles = (ctx.message.author).roles
    run = False
    for role in author_roles:
        if role == user_role:
            run = True
            break
    return run

@level_bot.event
async def on_ready():
    #This runs when the bot boots up
    print("Client logged in")
    print('Name:{}'.format(level_bot.user.name))
    print('ID:{}'.format(level_bot.user.id))
    print(discord.__version__)
    print('Playing:{}'.format(game))
    await level_bot.change_presence(game=discord.Game(name=game))

@level_bot.event
async def on_server_join(server):
    await level_bot.send_message(server.default_channel,"Greatings, I am a bot. My purpose as a bot is to track user's 'stars' or levels. Stars can only be allocated by people with the 'Starlord' role. A full list of commands can be obtained through the '?help' command. Have fun!")
    await level_bot.create_role(server,name="Starlord",colour=discord.Colour.gold(),hoist=False,mentionable=True)

@level_bot.command(pass_context=True)
async def backup(ctx):
    await level_bot.delete_message(ctx.message)
    run = check_for_role(ctx)
    if run == True:
        with open("stars.txt","w") as file:
            for key in player_stars:
                new_line = "\n"
                file.write(str(key))
                file.write(new_line)
                file.write(str(player_stars[key]))
                file.write(new_line)
        await level_bot.send_message(ctx.message.channel, 'Backed up all user stars to "stars.txt".')
    else:
        await level_bot.send_message(ctx.message.author, 'You do not have permission to backup stars for this server "{}".'.format(ctx.message.server))
        
    
@level_bot.command(pass_context=True)
async def give_stars(ctx,*args):
    await level_bot.delete_message(ctx.message)
    run = check_for_role(ctx)
    if run == True:
        global player_stars
        num = 0
        if int(args[1]) >= 0:
            operator = "+"
        elif int(args[1]) < 0:
            operator = ""
        for key in player_stars:
            if key == args[0]:
                num = num + 1
                player_stars[key] = int(player_stars[key]) + int(args[1])
                await level_bot.send_message(ctx.message.channel, 'User "{}" now has {} :stars: ({}{}).'.format(key,player_stars[key],operator,args[1]))
        if num == 0:
            user = str(args[0])
            stars = 0 + int(args[1])
            player_stars[user] = stars
            await level_bot.send_message(ctx.message.channel, 'User "{}" was added to the list with {} :stars: (+{}).'.format(args[0],args[1],args[1]))
    else:
        await level_bot.send_message(ctx.message.author, 'You do not have permission to interact with user stars in server "{}".'.format(ctx.message.server))

@level_bot.command(pass_context=True)
async def list_stars(ctx,*args):
    await level_bot.delete_message(ctx.message)
    try:
        if len(player_stars) is not 0:
            for key in player_stars:
                if key == args[0]:
                    await level_bot.send_message(ctx.message.channel, 'User "{}" has {} :stars:.'.format(key,player_stars[key]))
                    return None
            user = args[0]
            await level_bot.send_message(ctx.message.channel, 'User "{}" is not registered for the :stars: list.'.format(user))
        elif len(player_stars) is 0:
            message = ctx.message.content
            user = message.replace('?list_stars ','')
            await level_bot.send_message(ctx.message.channel, 'User "{}" is not registered for the :stars: list.'.format(user))
    except:
        await level_bot.send_message(ctx.message.channel, 'User was not given. Please give the user after the "?list_stars" command.')
        
@level_bot.command(pass_context=True)
async def clear_stars(ctx,*args):
    await level_bot.delete_message(ctx.message)
    run = check_for_role(ctx)
    if run == True:
        global player_stars
        if args[0].lower() == "all":
            del player_stars
            player_stars = {}
            await level_bot.send_message(ctx.message.channel, 'Deleted :stars: for all users.')
        else:
            try:
                del player_stars[args[0]]
                await level_bot.send_message(ctx.message.channel, 'Deleted :stars: for user "{}".'.format(args[0]))
            except:
                await level_bot.send_message(ctx.message.channel, 'User "{}" was not found.'.format(args[0]))
    else:
        await level_bot.send_message(ctx.message.author, 'You do not have permission to interact with user stars in server "{}".'.format(ctx.message.server))

@level_bot.command(pass_context=True)
async def shutdown(ctx):
    await level_bot.delete_message(ctx.message)
    run = check_for_role(ctx)
    if run == True:
        with open("stars.txt","w") as file:
            for key in player_stars:
                new_line = "\n"
                file.write(str(key))
                file.write(new_line)
                file.write(str(player_stars[key]))
                file.write(new_line)
        await level_bot.send_message(ctx.message.channel, 'Closed bot and backed up all stars to "stars.txt".')
        await level_bot.close()
    else:
        await level_bot.send_message(ctx.message.author, 'You do not have permission to shutdown this bot in server "{}".'.format(ctx.message.server))

@level_bot.event
async def on_message(message):
    await level_bot.process_commands(message)

level_bot.run(token)
        
