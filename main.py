# BeanMusic using nextcord.py
# Buttons , Slash Commands , Help Commands

import asyncio
import nextcord, config, youtube_dl, SPOTIFY, json
from collections import deque as queue
from nextcord.ext import commands
from fun import *
import threading

if config.token == "":
    print("Please add your bot token in config.py")
    exit()

client = commands.Bot()

music_queue = queue()
global loop
loop = False

global play_thread
play_thread = None


@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_interaction(interaction):
    if interaction.type == nextcord.InteractionType.component:
        if interaction.data["custom_id"] == "play":
            await resume(interaction)
        if interaction.data["custom_id"] == "pause":
            await pause(interaction=interaction)
        if interaction.data["custom_id"] == "stop":
            await stop(interaction=interaction)
        if interaction.data["custom_id"] == "skip":
            await skip(interaction=interaction)
        if interaction.data["custom_id"] == "loop":
            await _loop(interaction=interaction)
        if interaction.data["custom_id"] == "download":
            await download(interaction=interaction)
        if interaction.data["custom_id"] == "queue":
            await QU(interaction=interaction)
        if interaction.data["custom_id"] == "djrole":
            await djrole(interaction=interaction)
        if interaction.data["custom_id"] == "removedjrole":
            await removedjrole(interaction=interaction)
        if interaction.data["custom_id"] == "clearqueue":
            await clearqueue(interaction=interaction)
        if interaction.data["custom_id"] == "shuffle":
            await shuffle(interaction=interaction)
        if interaction.data["custom_id"] == "help":
            await help(interaction=interaction)

        if interaction.data.get("custom_id") == "discon":
            await discon(interaction=interaction)

    if interaction.type == nextcord.InteractionType.application_command:
        await client.process_application_commands(interaction)


async def help(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    
    embed = nextcord.Embed(
        title="Help",
        description= config.help_text,
        color=nextcord.Color.red(),
    )
    await interaction.followup.send(embed=embed, ephemeral=True)


async def shuffle(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    
    try:
        import random
        shuffle_lst = [x for x in music_queue]
        random.shuffle(shuffle_lst)
        music_queue.clear()
        for i in shuffle_lst:
            music_queue.append(i)
        await create_embed(interaction=interaction)
    except Exception as e:
        pass


async def QU(interaction):

    global music_queue
    msg = ""
    if len(music_queue) > 0: 
        for i in music_queue:
            msg += f"⭐ `{i.get('title')}` | {i.get('duration')} min \n"
        try:
            await interaction.response.send_message(msg, ephemeral=True)
        except:
            await interaction.followup.send(msg, ephemeral=True)
    else:
        try:
            await interaction.response.send_message("None, Queue is Empty", ephemeral=True)
        except:
            await interaction.followup.send("None, Queue is Empty", ephemeral=True)
            
async def djrole(interaction):
    try:
        await interaction.response.defer()
    except: 
        pass
    
    
    # Getting DJ role
    with open("./Saves/saves.json", "r") as f:
        data = json.load(f)
    role_id = data.get(str(interaction.guild.id))
    if role_id is None:
        await interaction.followup.send("DJ role is not set, Please /setup-dj-role to Setup DJ ROLE (only For ADMINS) ", ephemeral=True)
    else:
        try:
            role = interaction.guild.get_role(role_id)
            await interaction.user.add_roles(role)
            await interaction.followup.send("DJ role added", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(
                "Bot Don't have Permisson to Set DJ Role", ephemeral=True
            )

async def removedjrole(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    
    
    
    # Removing DJ role
    with open("./Saves/saves.json", "r") as f:
        data = json.load(f)
    role_id = data.get(str(interaction.guild.id))
    if role_id is None:
        await interaction.followup.send("DJ role is not set", ephemeral=True)
    else:
        try:
            role = interaction.guild.get_role(role_id)
            await interaction.user.remove_roles(role)
            await interaction.followup.send("DJ role removed", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(
                "Bot Don't have Permisson to Remove DJ Role", ephemeral=True
            )

async def clearqueue(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    music_queue.clear()
    interaction.guild.voice_client.stop()
    await create_embed(interaction=interaction)

async def resume(interaction):
    # Pausing and Resuming music
    try:
        if interaction.guild.voice_client is None:
            await interaction.response.send_message(
                "There is no music playing", delete_after=5
            )
        if interaction.guild.voice_client is not None:
            interaction.guild.voice_client.resume()
        else:
            await interaction.response.send_message(
                "There is no music playing", delete_after=5
            )
    except Exception as e:
        print(e)

async def clear_queue(interaction):
    # Clearing queue
    try:
        music_queue.clear()
        await create_embed(interaction=interaction)
        await interaction.guild.voice_client.stop()
    except Exception as e:
        pass

async def download(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    
    # Downloading music
    if len(music_queue) > 0:
        await interaction.followup.send(
            f"[CLICK HERE]({music_queue[0].get('url')}) TO DOWNLAOD MUSIC ",
            ephemeral=True,
        )
    else:
        await interaction.followup.send(
            "There is no music in queue", ephemeral=True
        )


async def pause(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    # Pausing music
    if interaction.guild.voice_client is None:
        await interaction.followup.send(
            "There is no music playing", delete_after=5
        )
    if interaction.guild.voice_client is not None:
        interaction.guild.voice_client.pause()
    else:
        await interaction.followup.send(
            "There is no music playing", delete_after=5
        )


async def stop(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    # Stopping music
    try:
        if interaction.guild.voice_client is None:
            await interaction.followup.send(
                "There is no music playing. Already Stopped", delete_after=5
            )
        if interaction.guild.voice_client is not None:
            interaction.guild.voice_client.stop()
            music_queue.clear()
            await create_embed(interaction=interaction)
        else:
            await interaction.followup.send(
                "There is no music playing", delete_after=5
            )
    except Exception as e:
        pass    


async def discon(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    
    try:
        # Disconnecting bot from voice channel
        if interaction.guild.voice_client is None:
            await interaction.followup.send(
                "There is no music playing", delete_after=5
            )
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.disconnect()
            music_queue.clear()
            await create_embed(interaction=interaction)
    except Exception as e:
        print("Please Wait!!")
        pass


async def skip(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    
    
    try:
        # Skipping the music from the queue and playing next music
        if interaction.guild.voice_client is None:
            await interaction.followup.send(
                "There is no music playing", delete_after=5
            )

        # Else check if the queue has more than 1 song then play next one else stop the music
        elif len(music_queue) > 1:
            interaction.guild.voice_client.stop()
            await create_embed(interaction=interaction)
            await play_song(interaction=interaction)
        else:
            interaction.guild.voice_client.stop()
            music_queue.clear()
            await create_embed(interaction=interaction)
    except Exception as e:
        pass


async def _loop(interaction):
    try:
        await interaction.response.defer()
    except:
        pass
    
    
    # Looping music
    global loop

    if loop == False:
        loop = True
        await create_embed(interaction=interaction)
    else:
        loop = False
        await create_embed(interaction=interaction)


async def search_by_name(name):
    try:
        # Searching by music name
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "default_search": "auto",
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{name}", download=False)
            url = info["entries"][0]["formats"][0]["url"]
            title = info["entries"][0]["title"]
            duration = round((info["entries"][0]["duration"]) / 60, 2)
            thumbnail = info["entries"][0]["thumbnail"]

            return url, title, duration, thumbnail
    except Exception as e:
        print(e)
        return None, None, None, None


async def get_youtube_music(url):
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info["formats"][0]["url"]
            title = info["title"]
            duration = round((info["duration"]) / 60, 2)
            thumbnail = info["thumbnail"]
            return url2, title, duration, thumbnail
    except Exception as e:
        print(e)
        return None, None, None, None


async def get_youtube_playlist(url):
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": False,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": True,
            # age restrict bypass
        }
        lst = []
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            for i in info["entries"]:
                j = {
                    "url": i["formats"][0]["url"],
                    "title": i["title"],
                    "duration": round((i["duration"]) / 60, 2),
                    "thumbnail": i["thumbnail"],
                }
                lst.append(j)
            return lst

    except Exception as e:
        print(e)
        return None


async def create_embed(interaction):
    # Checking if There is any music Dashboard
    with open("embed.txt", "r") as f:
        embed_id = f.read()

    # If there is no music Dashboard Embed
    if embed_id != "":
        try:
            message = await interaction.channel.fetch_message(int(embed_id))
        except Exception as e:
            message = None
        if message:
            embed = message.embeds[0]
            # if Queue is Empty
            if len(music_queue) == 0:
                embed.description = "```Queue:\nEmpty```"
                embed.set_field_at(
                    0, name="Now Playing", value="`Nothing`", inline=False
                )
                embed.set_thumbnail(
                    url="https://images.indianexpress.com/2021/07/Nothing-logo.jpg"
                )
                embed.set_field_at(
                    1, name="Next Music", value="`Nothing`", inline=False
                )
                embed.set_field_at(3, name="Duration", value="`--`", inline=True)
                embed.set_field_at(4, name="Requested by", value="`--`", inline=True)
                embed.set_field_at(5, name="Volume", value="`--`", inline=True)
                embed.set_field_at(6, name="Loop", value="`--`", inline=True)
                embed.set_field_at(7, name="Download", value="`🙄`", inline=True)                
                await message.edit(embed=embed)
                return
            else:
                # Setting up Queue List
                des = ""
                for i in music_queue:
                    des += f"{i.get('title')}\n"
                embed.description = f"```Queue:\n{des}```"

                # Setting up Now Playing
                embed.set_field_at(
                    0,
                    name="Now Playing",
                    value=f"`{music_queue[0].get('title')}`",
                    inline=False,
                )
                embed.set_thumbnail(url=music_queue[0].get("thumbnail"))
                if len(music_queue) > 1:
                    embed.set_field_at(
                        1,
                        name="Next Music",
                        value=f"`{music_queue[1].get('title')}`",
                        inline=False,
                    )
                embed.set_field_at(
                    3,
                    name="Duration",
                    value=f"`{music_queue[0].get('duration')}`",
                    inline=True,
                )
                embed.set_field_at(
                    4,
                    name="Requested by",
                    value=f"{interaction.user.mention}",
                    inline=True,
                )
                embed.set_field_at(5, name="Volume", value=f"`100%`", inline=True)
                embed.set_field_at(6, name="Loop", value=f"`{loop}`", inline=True)
                embed.set_field_at(
                    7,
                    name="Download",
                    value=f"[Link]({music_queue[0].get('url')})",
                    inline=True,
                )
                await message.edit(embed=embed)
                return

    embed = nextcord.Embed(title="DASHBOARD", color=nextcord.Color.blue())
    # Making Queue
    lst_titles = ""
    if len(music_queue) > 1:
        for i in music_queue:
            lst_titles += f"{i.get('title')}\n"
    else:
        lst_titles = "None"
    embed.description = f"```Queue:\n{lst_titles}```"

    # Adding fields to the embed
    embed.add_field(
        name="Now Playing", value=f"`{music_queue[0].get('title')}`", inline=False
    )
    embed.set_thumbnail(url=music_queue[0].get("thumbnail"))
    if (len(music_queue)) > 1:
        embed.add_field(
            name="Next Music", value=f"`{music_queue[0].get('title')}`", inline=False
        )
    else:
        embed.add_field(name="Next Music", value="`None`", inline=False)

    with open("./Saves/saves.json", "r") as f:
        data = json.load(f)

    if str(interaction.guild.id) in data:
        embed.add_field(
            name="DJ Role",
            value=f"{interaction.guild.get_role(data[str(interaction.guild.id)]).mention}",
            inline=True,
        )
    else:
        embed.add_field(name="DJ Role", value="`None`", inline=True)

    embed.add_field(
        name="Duration", value=f"`{music_queue[0].get('duration')}`", inline=True
    )
    embed.add_field(
        name="Requested by", value=f"{interaction.user.mention}", inline=True
    )
    # Setting Volume
    try:
        embed.add_field(
            name="Volume",
            value=f"{float(nextcord.PCMVolumeTransformer.volume)* 100}%",
            inline=True,
        )
    except Exception as e:
        nextcord.AudioSource.is_opus = False
        nextcord.PCMVolumeTransformer.volume = 1
        embed.add_field(name="Volume", value=f"100%", inline=True)
        pass

    embed.add_field(name="Loop", value=f"{loop}", inline=True)
    embed.add_field(
        name="Download", value=f"[Link]({music_queue[0].get('url')})", inline=True
    )
    embed.set_footer(text="Code by: Bean")

    # Adding buttons to the embed
    button1 = nextcord.ui.Button(
        label="Play", style=nextcord.ButtonStyle.green, custom_id="play", emoji="▶️"
    )
    button2 = nextcord.ui.Button(
        label="Pause", style=nextcord.ButtonStyle.grey, custom_id="pause", emoji="⏸️"
    )
    button3 = nextcord.ui.Button(
        label="Stop", style=nextcord.ButtonStyle.red, custom_id="stop", emoji="⏹️"
    )
    button4 = nextcord.ui.Button(
        label="Skip", style=nextcord.ButtonStyle.grey, custom_id="skip", emoji="⏭️"
    )
    if loop == True:
        button5 = nextcord.ui.Button(
            label="Loop", style=nextcord.ButtonStyle.primary, custom_id="loop", emoji="🔁"
        )
    else:
        button5 = nextcord.ui.Button(
        label="Loop", style=nextcord.ButtonStyle.grey, custom_id="loop", emoji="🔁"
    )
    button7 = nextcord.ui.Button(
        label="Download",
        style=nextcord.ButtonStyle.grey,
        custom_id="download",
        emoji="📥",
    )
    button8 = nextcord.ui.Button(
        label="Queue", style=nextcord.ButtonStyle.grey, custom_id="queue", emoji="📜"
    )
    button9 = nextcord.ui.Button(
        label="Get DJ Role",
        style=nextcord.ButtonStyle.grey,
        custom_id="djrole",
        emoji="🎧",
    )
    button10 = nextcord.ui.Button(
        label="Remove DJ Role",
        style=nextcord.ButtonStyle.grey,
        custom_id="removedjrole",
        emoji="🎧",
    )
    button11 = nextcord.ui.Button(
        label="Clear Queue",
        style=nextcord.ButtonStyle.grey,
        custom_id="clearqueue",
        emoji="🗑️",
    )
    button12 = nextcord.ui.Button(
        label="Shuffle", style=nextcord.ButtonStyle.grey, custom_id="shuffle", emoji="🔀"
    )
    button13 = nextcord.ui.Button(
        label="Help", style=nextcord.ButtonStyle.primary, custom_id="help", emoji="❓"
    )

    button14 = nextcord.ui.Button(
        label="Disconnect",
        style=nextcord.ButtonStyle.red,
        custom_id="discon",
        emoji="🔌",
    )

    view = nextcord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    view.add_item(button14)
    view.add_item(button7)
    view.add_item(button8)
    view.add_item(button11)
    view.add_item(button12)
    view.add_item(button13)
    view.add_item(button9)
    view.add_item(button10)
    # Sending the embed

    embed = await interaction.channel.send(embed=embed, view=view)
    with open("embed.txt", "w") as f:
        f.write(str(embed.id))
    return


async def play_song(interaction, flag=None):
    # Checking if there is a song in the queue
    try:
        global loop
        FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }
        if flag != None:
            # Checking Loop
            if loop == False:
                music_queue.remove(music_queue[0])
                await create_embed(interaction)
                if len(music_queue) > 0:
                    print(f"Playing {music_queue[0].get('title')}")
                    interaction.guild.voice_client.play(
                        nextcord.FFmpegPCMAudio(
                            music_queue[0].get("url"), **FFMPEG_OPTIONS
                        ),
                        after=lambda e: play_song(interaction, 1),
                    )
                else:
                    print("Nothing in Queue. I am going to die... Ba Byeee")
                    await interaction.guild.voice_client.disconnect()
                    return
            else:
                music = music_queue[0]
                music_queue.remove(music_queue[0])
                music_queue.append(music)
                await create_embed(interaction)
                print(f"Playing {music_queue[0].get('title')}")

                interaction.guild.voice_client.play(
                    nextcord.FFmpegPCMAudio(
                        music_queue[0].get("url"), **FFMPEG_OPTIONS
                    ),
                    after=lambda e: play_song(interaction, 1),
                )
        elif len(music_queue) > 0:
            print(f"Playing {music_queue[0].get('title')}")
            interaction.guild.voice_client.play(
                nextcord.FFmpegPCMAudio(music_queue[0].get("url"), **FFMPEG_OPTIONS),
                after=lambda e: play_song(interaction, 1),
            )
        else:
            interaction.guild.voice_client.disconnect()
    except Exception as e:
        pass


@client.slash_command(
    name="set-volume",
    description="Set the volume of the music",
)
async def set_volume(interaction: nextcord.Interaction, volume: int):
    await interaction.response.defer()
    if volume > 100:
        await interaction.followup.send(
            "The volume must be less than 100", ephemeral=True
        )
        return
    # Audio Source
    channel = interaction.user.voice.channel
    voice = nextcord.utils.get(client.voice_clients, guild=interaction.guild)
    if voice and voice.is_connected():
        if voice.channel != channel:
            await interaction.followup.send(
                "You must be in the same voice channel as the bot", ephemeral=True
            )
            return
        if voice.source:
            voice.source.volume = volume / 100
        else:
            await interaction.followup.send(
                "The bot is not playing anything", ephemeral=True
            )
            return
    else:
        await interaction.followup.send(
            "The bot is not connected to any voice channel", ephemeral=True
        )
        return


@client.slash_command(
    name="setup-dj-role",
    description="Setup the DJ role",
)
async def setup_dj_role(interaction: nextcord.Interaction):
    await interaction.response.defer()
    # Only the owner and the admin can use this command
    if (
        interaction.user.id == client.owner_id
        or interaction.user.guild_permissions.administrator
    ):
        # Creating a new role
        role = await interaction.guild.create_role(name="DJ")

        # Saving the role id in the config file
        with open("./Saves/saves.json", "r") as f:
            data = json.load(f)

        if str(interaction.guild.id) in data:
            await interaction.followup.send(
                "You already have a DJ role", ephemeral=True
            )
            return

        data[str(interaction.guild.id)] = role.id
        with open("./Saves/saves.json", "w") as f:
            json.dump(data, f)

        await interaction.followup.send(f"Created a new role called DJ", ephemeral=True)

    else:
        await interaction.followup.send(
            "You don't have the permission to use this command", ephemeral=True
        )


@client.slash_command(
    name="get-dj-role",
    description="Get the DJ role",
)
async def get_dj_role(interaction: nextcord.Interaction):
    # Giving Role to the user
    await interaction.response.defer()

    with open("./Saves/saves.json", "r") as f:
        data = json.load(f)

    if str(interaction.guild.id) in data:
        try:
            role = interaction.guild.get_role(int(data[str(interaction.guild.id)]))
            await interaction.user.add_roles(role)
            await interaction.followup.send(
                f"Added the role {role.name} to you", ephemeral=True
            )
        except Exception as e:
            print("Dont have permission to add role")
            await interaction.followup.send(
                "I don't have the permission to add role", ephemeral=True
            )

    else:
        await interaction.followup.send("You don't have a DJ role", ephemeral=True)

async def play_spotify_through_yt(songName):
    pass



@client.slash_command(
    name="play",
    description="Play a song",
)
async def play(interaction: nextcord.Interaction, 
        type: str = nextcord.SlashOption(
        name="type",
        choices={
            "Song Name": "songname",
            "URL": "url",
        },
    ),
        value: str = nextcord.SlashOption(
        name="value",
        description="The value of the type",
        required=True,
    ),
        
        ):
    try:
        await interaction.response.defer()
        url = value
        
        if type == "songname":
            await interaction.followup.send(f"*Searching for You Song. Please Wait*", delete_after=5)
            url, title, duration, thumbnail = await search_by_name(url)
            if url == None:
                await interaction.followup.send(
                    "I can't play this music", delete_after=5
                )
                return
            music_queue.append(
                {
                    "url": url,
                    "title": title,
                    "duration": duration,
                    "thumbnail": thumbnail,
                }
            )
            await create_embed(interaction)

            if (
                interaction.guild.voice_client is not None
                and interaction.guild.voice_client.is_connected()
            ):
                if (interaction.guild.voice_client.is_playing() == False):
                    await play_song(interaction)
                print("Updated in a Queue")
            else:
                await join_voice(interaction)
                await play_song(interaction)
            return

        else: 
            if interaction.user.voice == None:
                await interaction.followup.send(
                    "You must be in a voice channel", delete_after=5
                )
                return
            if (
                url.__contains__("youtube.com") or url.__contains__("youtu.be")
            ) and url.__contains__("list"):
                try:
                    await interaction.followup.send(
                        f"Fetching PlayList Please Wait....", delete_after=5
                    )
                    # Getting the playlist from the url using threading
                    list = await get_youtube_playlist(url)
                    if list == None:
                        await interaction.followup.send(
                            "I can't play this music", delete_after=5
                        )
                        return
                    music_queue.extend(list)
                    await create_embed(interaction)
                    if (
                        interaction.guild.voice_client is not None
                        and interaction.guild.voice_client.is_connected()
                ):                
                        if (interaction.guild.voice_client.is_playing() == False):
                            await play_song(interaction)
                        print("Updated in a Queue")
                    else:
                        await join_voice(interaction)
                        await play_song(interaction)
                except Exception as e:
                    print(e)
            elif (
                url.__contains__("youtube.com") or url.__contains__("youtu.be")
            ) and not url.__contains__("list"):
                await interaction.followup.send(f"Playing....", delete_after=5)
                url, title, duration, thumbnail = await get_youtube_music(url)
                if url == None:
                    await interaction.followup.send(
                        "I can't play this music", delete_after=5
                    )
                    return
                music_queue.append(
                    {
                        "url": url,
                        "title": title,
                        "duration": duration,
                        "thumbnail": thumbnail,
                    }
                )
                await create_embed(interaction)

                if (
                    interaction.guild.voice_client is not None
                    and interaction.guild.voice_client.is_connected()
                ):
                    if (interaction.guild.voice_client.is_playing() == False):
                        await play_song(interaction)
                    print("Updated in a Queue")
                else:
                    await join_voice(interaction)
                    await play_song(interaction)

            elif url.__contains__("spotify"):
                if url.__contains__("playlist"):
                    await interaction.followup.send(
                        f"Fetching PlayList Please Wait....", delete_after=5
                    )
                    list = SPOTIFY.getTrackInfo(url)
                    if list == None:
                        await interaction.followup.send(
                            "I can't play this music", delete_after=5
                        )
                        return
                    music_queue.extend(list)
                    await create_embed(interaction)
                    if (
                        interaction.guild.voice_client is not None
                        and interaction.guild.voice_client.is_connected()
                    ):
                        if (interaction.guild.voice_client.is_playing() == False):
                            await play_song(interaction)
                            
                        print("Updated in a Queue")
                    else:
                        await join_voice(interaction)
                        await play_song(interaction)

                elif url.__contains__("track"):
                    await interaction.followup.send(f"Playing....", delete_after=5)
                    url1, title1, duration1, thumbnail1 = SPOTIFY.getTrackInfo(url)
                    url, title, duration, thumbnail = await search_by_name(title1)
                    
                    if url == None:
                        await interaction.followup.send(
                            "I can't play this music", delete_after=5
                        )
                        return
                    music_queue.append(
                        {
                            "url": url,
                            "title": title,
                            "duration": duration,
                            "thumbnail": thumbnail,
                        }
                    )
                    await create_embed(interaction)

                    if (
                        interaction.guild.voice_client is not None
                        and interaction.guild.voice_client.is_connected()
                    ):
                        if (interaction.guild.voice_client.is_playing() == False):
                            await play_song(interaction)                        
                        print("Updated in a Queue")
                    else:
                        await join_voice(interaction)
                        await play_song(interaction)
            return

    except Exception as e:
        print(e)
        await interaction.response.send_message(
            "Try Again! (Command Used before establishing Connection) ", ephemeral=True
        )




client.run(config.token)
