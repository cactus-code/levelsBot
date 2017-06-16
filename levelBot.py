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

token = "add bot token here"
game = "Shooting Stars"

def check_for_role(ctx):
    user_role = discord.utils.get(ctx.message.server.roles, name="Starlord")
    author_roles = (ctx.message.author).roles
    return any(role == user_role for role in author_roles)

level_bot.event
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
    if run:
        with open("stars.txt","w") as file:
            for key in player_stars:
                new_line = "\n"
                file.write(str(key))
                file.write(new_line)
                file.write(str(player_stars[key]))
                file.write(new_line)
        await level_bot.send_message(ctx.message.channel, 'Backed up all user stars to "stars.txt".')
        print('Backed up all user stars for server {} to "stars.txt".'.format(ctx.message.server))
    else:
        await level_bot.send_message(ctx.message.author, 'You do not have permission to backup stars for this server "{}".'.format(ctx.message.server))
        
@level_bot.command(pass_context=True)
async def give_stars(ctx,*args):
    await level_bot.delete_message(ctx.message)
    run = check_for_role(ctx)
    if run:
        try:
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
                    print("Gave {}{} stars to user with ID: {}".format(operator,args[1],args[0]))
            if num == 0:
                user = str(args[0])
                stars = 0 + int(args[1])
                player_stars[user] = stars
                await level_bot.send_message(ctx.message.channel, 'User "{}" was added to the list with {} :stars: (+{}).'.format(args[0],args[1],args[1]))
                print('Added user with ID: {} to star list with {} stars.'.format(args[0],args[1]))
        except:
            await level_bot.send_message(ctx.message.channel, 'Invalid number. Please enter a valid user and a number of stars.')
    else:
        await level_bot.send_message(ctx.message.author, 'You do not have permission to interact with user stars in server "{}".'.format(ctx.message.server))

@level_bot.command(pass_context=True)
async def list_stars(ctx,*args):
    await level_bot.delete_message(ctx.message)
    try:
        if player_stars:
            if args[0].lower() == "all":
                await level_bot.send_message(ctx.message.author,'Stars for server {}:'.format(ctx.message.server))
                for key in player_stars:
                    await level_bot.send_message(ctx.message.author,key + ' : ' + player_stars[key])
                    print('Sent list of all user stars for server: {} to user: {}.'.format(ctx.message.server,ctx.message.author))
            else:
                for key in player_stars:
                    if key == args[0]:
                        await level_bot.send_message(ctx.message.channel, 'User "{}" has {} :stars:.'.format(key,player_stars[key]))
                        print('Sent number of stars for user with ID: {} to server: {}.'.format(args[0],ctx.message.server))
                        return None
                user = args[0]
                await level_bot.send_message(ctx.message.channel, 'User "{}" is not registered for the :stars: list.'.format(user))
        else:
            if args[0].lower() == "all":
                await level_bot.send_message(ctx.message.author, 'There are no users on the star list for server {}.'.format(ctx.message.server))
            else:
                message = ctx.message.content
                user = message.replace('?list_stars ','')
                await level_bot.send_message(ctx.message.channel, 'User "{}" is not registered for the :stars: list.'.format(user))
    except:
        await level_bot.send_message(ctx.message.channel, 'User was not given. Please specify the user after the "?list_stars" command. Alternatively you can type "?list_stars all" to see the full star list for that server.')
        
@level_bot.command(pass_context=True)
async def clear_stars(ctx,*args):
    await level_bot.delete_message(ctx.message)
    run = check_for_role(ctx)
    if run:
        global player_stars
        if args[0].lower() == "all":
            del player_stars
            player_stars = {}
            await level_bot.send_message(ctx.message.channel, 'Deleted :stars: for all users.')
            print('Deleted stars for all users on server: {}.'.format(ctx.message.server))
        else:
            try:
                del player_stars[args[0]]
                await level_bot.send_message(ctx.message.channel, 'Deleted :stars: for user "{}".'.format(args[0]))
                print('Deleted stars for user with ID: {} on server: {}.'.format(args[0],ctx.message.server))
            except:
                await level_bot.send_message(ctx.message.channel, 'User "{}" was not found.'.format(args[0]))
    else:
        await level_bot.send_message(ctx.message.author, 'You do not have permission to interact with user stars in server "{}".'.format(ctx.message.server))

@level_bot.command(pass_context=True)
async def shutdown(ctx):
    await level_bot.delete_message(ctx.message)
    run = check_for_role(ctx)
    if run:
        with open("stars.txt","w") as file:
            for key in player_stars:
                new_line = "\n"
                file.write(str(key))
                file.write(new_line)
                file.write(str(player_stars[key]))
                file.write(new_line)
        await level_bot.send_message(ctx.message.channel, 'Closed bot and backed up all stars to "stars.txt".')
        print('Closed bot and backed all stars up to "stars.txt".')
        await level_bot.close()
    else:
        await level_bot.send_message(ctx.message.author, 'You do not have permission to shutdown this bot in server "{}".'.format(ctx.message.server))

@level_bot.event
async def on_message(message):
    await level_bot.process_commands(message)

level_bot.run(token)
