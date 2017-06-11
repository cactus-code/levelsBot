import itertools
import discord
from discord.ext.commands import Bot

level_bot = Bot(command_prefix="?")
player_stars = {}

with open("stars.txt","r") as file:
    content = file.readlines()
content = [x.strip('\n') for x in content]

d = dict(itertools.zip_longest(*[iter(content)] * 2, fillvalue=""))
player_stars.update(d)

token = "MzEzNzczNjQ1Mjk2MzA0MTI4.C_wkBg.ee0Btf1Hdbu6mjhxlUv6HJ8X8_A"
game = "Shooting Stars"

@level_bot.event
async def on_ready():
    #This runs when the bot boots up
    print("Client logged in")
    print('Name:{}'.format(level_bot.user.name))
    print('ID:{}'.format(level_bot.user.id))
    print(discord.__version__)
    print('Playing:{}'.format(game))
    await level_bot.change_presence(game=discord.Game(name=game))

@level_bot.command(pass_context=True)
async def give_stars(ctx,*args):
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

@level_bot.command(pass_context=True)
async def list_stars(ctx,*args):
    if len(player_stars) is not 0:
        for key in player_stars:
            if key == args[0]:
                await level_bot.send_message(ctx.message.channel, 'User "{}" has {} :stars:.'.format(key,player_stars[key]))
                break
            else:
                message = ctx.message.content
                user = message.replace('?list_stars ','')
                await level_bot.send_message(ctx.message.channel, 'User "{}" is not registered for the :stars: list.'.format(user))
                break
    elif len(player_stars) is 0:
        message = ctx.message.content
        user = message.replace('?list_stars ','')
        await level_bot.send_message(ctx.message.channel, 'User "{}" is not registered for the :stars: list.'.format(user))
        
@level_bot.command(pass_context=True)
async def clear_stars(ctx,*args):
    global player_stars
    if args[0].lower() == "all":
        del player_stars
        player_stars = {}
        await level_bot.send_message(ctx.message.channel, 'Deleted stars for all users.')
    else:
        del player_stars[args[0]]
        await level_bot.send_message(ctx.message.channel, 'Deleted stars for user "{}".'.format(args[0]))
#await level_bot.send_message(ctx.message.channel, 'User "{}" was not found.'.format(args[0]))

@level_bot.command(pass_context=True)
async def shutdown(ctx):
    with open("stars.txt","w") as file:
        for key in player_stars:
            new_line = "\n"
            file.write(str(key))
            file.write(new_line)
            file.write(str(player_stars[key]))
            file.write(new_line)
    await level_bot.send_message(ctx.message.channel, 'Closed bot and backed up all stars to "stars.txt".')
    await level_bot.close()

@level_bot.event
async def on_message(message):
    await level_bot.process_commands(message)

level_bot.run(token)
        
