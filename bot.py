import os
import random
import discord
from discord.ext import commands, tasks
from itertools import cycle
import json

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
status = cycle(['Dont Worry Be Happy', 'Life ma Mazza garnu parcha', 'With boobs', 'With your heart', 'in RTX 5080ti (over ya.all)'])


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_ready():
    change_status.start()
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Heyyy peeps'))
    print('Bot is ready to roll....')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')



@client.event
async def on_member_join(member):
    print(f'{member} has joined the server..')
    print(f'Hello {member} Welcome to our Server. Enjoy your stay.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command(aliases = ['8ball', 'ask'])
async def ques(ctx, *, question):
    responses = [  'It is certain',
                    'It is decided',
                    'Without a doubt',
                    'Will do definately',
                    'Yessss!!!!',
                    'You can rely on me boi.',
                    'Your wish is my command',
                    'Ask again later',
                    'Let me concentrate on my other tasks',
                    'Im a busy bot friend',
                    'I am not programmed to do so',
                    'I doubt i can do that.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter the amount of messages to clear:')

@client.event
async def on_command_error1(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter all required arguments:')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command doesnt exists!!!!!')





@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@kick.error
async def on_missing_permissions(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send('You are not authorized to use this command')


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'banned {member.mention}')

@ban.error
async def on_missing_permissions1(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send('You are not authorized to use this command')


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
         user = ban_entry.user

    if(user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned {user.mention}')
        return

@unban.error
async def on_missing_permissions2(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send('You are not authorized to use this command')

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))



client.run('Enter your bot token here')
