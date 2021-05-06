import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
import os
import io

intent = discord.Intents(members = True, guilds=True)
client=commands.Bot(command_prefix=".", intents=intent)
while True:
    print("Input token:")
    token_input = input()
    if token_input != '':
        token = token_input
        break
        

################################################################
def get_friend_list(save):
    dick = {}
    if save == 1:
        dirname = client.user.name.replace(' ', '')
        fname = f'{dirname}\\{client.user.name}_friends.txt'
        if os.path.exists(fname):
            os.remove(fname)
        with io.open(fname, 'a', encoding='utf-8') as f:
            for friend in client.user.friends:
                f.write(f'{friend} - {friend.avatar_url}\n')
        print("File successfully saved!\n")
    elif save == 2:
        for i, friend in enumerate(client.user.friends):
            dick[i+1] = friend
            print(f'{i+1}) {friend} - {friend.avatar_url}')
        print("------------------------")
        return dick
##################################################################
def server_export(save):
    if save == 1:
        dirname = client.user.name.replace(' ', '')
        fname = f'{dirname}\\{client.user.name}_servers.txt'
        if os.path.exists(fname):
            os.remove(fname)
        with io.open(fname, 'a', encoding='utf-8') as f:
            for channel in client.guilds:
                f.write(f'{channel}\n')
        print("File successfully saved!\n")
    elif save == 2:
        dick = {}
        for i, channel in enumerate(client.guilds):
            dick[i+1] = channel
            print(f'{i+1}) {channel}')
        print("------------------------")
        return dick
##################################################################
async def chat_export(save, user, chat_num):
    channel = user.dm_channel
    date_format = '%d/%m/%Y %H:%M'
    messages = await channel.history(oldest_first= True, limit=chat_num).flatten()
    print(f'Exporting {len(messages)} messages...') 
    if save == 1:
        dirname = client.user.name.replace(' ', '') +'\\user_'+user.name.replace(' ', '')
        fname = f'{dirname}\\{client.user.name}_{user.name}_messages.txt'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if os.path.exists(fname):
            os.remove(fname)
        with io.open(fname, 'a', encoding='utf-8') as f:
            for message in messages:
                if message.attachments:
                    for attachment in message.attachments:
                        #name =message.author.name + '_' + str(message.created_at.date()) + '_' + attachment.filename
                        await attachment.save(dirname + '\\'+ str(message.created_at.date())+ '_' + attachment.filename)
                        f.write(f'{message.author} - {message.created_at.strftime(date_format)} : {attachment.filename} == {attachment.url}\n')
                else:
                    f.write(f'{message.author} - {message.created_at.strftime(date_format)} : {message.content} \n')
        print("File successfully saved!\n")
    elif save == 2:
        for message in messages:
                if message.attachments:
                    for attachment in message.attachments:
                        #name =message.author.name + '_' + str(message.created_at.date()) + '_' + attachment.filename
                        #await attachment.save(dirname + '\\'+ str(message.created_at.date())+ '_' + attachment.filename)
                        print(f'{message.author} - {message.created_at.strftime(date_format)} : {attachment.filename} == {attachment.url}\n')
                else:
                    print(f'{message.author} - {message.created_at.strftime(date_format)} : {message.content}\n')
        print("------------------------")
##################################################################
async def channel_msg_export(save, channel, server, chat_num):
    date_format = '%d/%m/%Y %H:%M'
    messages = await channel.history(oldest_first= True, limit=chat_num).flatten()
    print(f'Exporting {len(messages)} messages...') 
    if save == 1:
        dirname = client.user.name.replace(' ', '') +'\\server_'+server.name.replace(' ', '') +'\\'+ channel.name.replace(' ', '')
        fname = f'{dirname}\\{server.name}_{channel.name}_messages.txt'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if os.path.exists(fname):
            os.remove(fname)
        with io.open(fname, 'a', encoding='utf-8') as f:
            for message in messages:
                if message.attachments:
                    for attachment in message.attachments:
                        #name =message.author.name + '_' + str(message.created_at.date()) + '_' + attachment.filename
                        await attachment.save(dirname + '\\'+ str(message.created_at.date())+ '_' + attachment.filename)
                        f.write(f'{message.author} - {message.created_at.strftime(date_format)} : {attachment.filename} == {attachment.url}\n')
                else:
                    f.write(f'{message.author} - {message.created_at.strftime(date_format)} : {message.content} \n')
        print("File successfully saved!\n")
    elif save == 2:
        for message in messages:
                if message.attachments:
                    for attachment in message.attachments:
                        #name =message.author.name + '_' + str(message.created_at.date()) + '_' + attachment.filename
                        #await attachment.save(dirname + '\\'+ str(message.created_at.date())+ '_' + attachment.filename)
                        print(f'{message.author} - {message.created_at.strftime(date_format)} : {attachment.filename} == {attachment.url}\n')
                else:
                    print(f'{message.author} - {message.created_at.strftime(date_format)} : {message.content}\n')
        print("------------------------")
##################################################################
def get_server_channels(server):
    dick = {}
    count = 1
    for channel in server.channels:
        if channel.category != None and channel.category.name == "Text Channels":
            dick[count] = channel
            print(f'{count}) {channel.name}')
            count +=1
    return dick




@client.event
async def on_ready():
    dirname = client.user.name.replace(' ', '')
    if not os.path.exists(dirname):
            os.makedirs(dirname)
    print("Do you want results to be exported to file?\n1) Yes\n2) No")
    save = int(input()) # 1 == true, 2 == false
    while(True):
        print("""What do you want to do? \n1) Get friend list \n2) Get server list \n3) Get chat logs with user\n4) Get chat logs from server channel""")
        choice = int(input())
        if choice == 1:
            get_friend_list(save)
        elif choice == 2:
            server_export(save)
        elif choice == 3:
            dick = get_friend_list(2)
            print("Messages with which friend do you want to export?")
            friends_num = int(input())
            print("How many messages do you want to export?")
            chat_num = int(input())
            await chat_export(save, dick[friends_num], chat_num)
        elif choice == 4:
            dick = server_export(2)
            print("Messages from which server do you want to export?")
            server_num = int(input())
            channels = get_server_channels(dick[server_num])
            print("Messages from which channel do you want to export?")
            channel_num = int(input())
            print("How many messages do you want to export?")
            chat_num = int(input())
            await channel_msg_export(save ,channels[channel_num], dick[server_num], chat_num)
        await asyncio.sleep(1)

client.run(token, bot=False)

