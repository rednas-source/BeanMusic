async def check_if_in_vc(interaction):
    if interaction.user.voice is None:
        return False
    else:
        return True
    
    
async def loop_on(interaction):
    # Turning on the loop
    if interaction.guild.voice_client.is_playing() == False and interaction.guild.voice_client.is_paused() == False:
        await interaction.response.send_message("The music is not playing", ephemeral=True)
        return False
    else:
        await interaction.response.send_message("Loop is on", ephemeral=True)
        return True

async def loop_off(interaction):
    # Turning off the loop
    if interaction.guild.voice_client.is_playing() == False and interaction.guild.voice_client.is_paused() == False:
        await interaction.response.send_message("The music is not playing", ephemeral=True)
        return False
    else:
        await interaction.response.send_message("Loop is off", ephemeral=True)
        return True

async def pause(interaction):
    # Pausing the music
    if interaction.guild.voice_client.is_playing() == False and interaction.guild.voice_client.is_paused() == False:
        await interaction.response.send_message("The music is already paused", ephemeral=True)
        return False
    else:
        interaction.guild.voice_client.pause()
        await interaction.response.send_message("Paused", ephemeral=True)
        return True

async def resume(interaction): 
    # Resuming the music
    if interaction.guild.voice_client.is_playing() == False and interaction.guild.voice_client.is_paused() == False:
        await interaction.response.send_message("The music is not paused", ephemeral=True)
        return False
    else:
        interaction.guild.voice_client.resume()
        await interaction.response.send_message("Resumed", ephemeral=True)
        return True

async def stop(interaction):
    # Stopping the music
    if interaction.guild.voice_client.is_playing() == False and interaction.guild.voice_client.is_paused() == False:
        await interaction.response.send_message("The music is not playing", ephemeral=True)
        return False
    else:
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Stopped", ephemeral=True)
        return True

async def clear_queue(interaction):
    # Clearing the queue
    pass

async def skip(interaction):
    # Skipping the music
    pass

async def shuffle(interaction):
    # Shuffling the queue
    pass




async def check_if_bot_in_vc(interaction):
    print( interaction.guild.voice_client)
    if interaction.guild.voice_client == None:
        return False
    else:
        return True


async def join_voice(interaction):
    # Joining the voice channel
    await interaction.user.voice.channel.connect()
    print("Joined the voice channel")
    

 
async def isFree(interaction):
    # Checking if the voice channel is free
    if interaction.guild.voice_client is None:
        return True  
    else: 
        return False

async def isPlaying(interaction):
    # Checking if the bot is playing music
    if interaction.guild.voice_client.is_playing():
        return True
    else:
        return False
    
    
async def isPaused(interaction):
    # Checking if the bot is paused
    if interaction.guild.voice_client.is_paused():
        return True
    else:
        return False
    
async def isStopped(interaction):
    # Checking if the bot is stopped
    if interaction.guild.voice_client.is_playing() == False and interaction.guild.voice_client.is_paused() == False:
        return True
    else:
        return False
    
async def isSameChannel(interaction):
    # Checking if the bot is in the same channel
    if interaction.guild.voice_client.channel == interaction.user.voice.channel:
        return True
    else:
        return False
    
    
async def isNotSameChannel(interaction):
    # Checking if the bot is not in the same channel
    if interaction.guild.voice_client.channel != interaction.user.voice.channel:
        return True
    else:
        return False
    