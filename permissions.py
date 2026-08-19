import discord

async def apply_permissions(guild):
    # =================================
    # Base Role Setup
    # =================================
    everyone = guild.default_role
    founder = discord.utils.get(guild.roles, name="👑 Founder")
    owner = discord.utils.get(guild.roles, name="⚜️ Owner")
    admin = discord.utils.get(guild.roles, name="🛡️ Admin")
    moderator = discord.utils.get(guild.roles, name="🔨 Moderator")

    staff_roles = [founder, owner, admin, moderator]

    member = discord.utils.get(guild.roles, name="🌸 Member")
    level_1 = discord.utils.get(guild.roles, name="✨ Level I")
    level_2 = discord.utils.get(guild.roles, name="🌙 Level II")
    level_3 = discord.utils.get(guild.roles, name="🌌 Level III")

    # =================================
    # 📋 logs
    # =================================
    logs_channel = discord.utils.get(guild.channels, name="📜・logs")

    if logs_channel:
        await logs_channel.set_permissions(everyone, view_channel=False)

        for role in staff_roles:
            if role:
                await logs_channel.set_permissions(role, view_channel=True)

        if founder:
            await logs_channel.set_permissions(founder, send_messages=True)

        for role in [owner, admin, moderator]:
            if role:
                await logs_channel.set_permissions(role, send_messages=False)

    # =================================
    # 🎫 tickets
    # =================================
    ticket_channel = discord.utils.get(guild.channels, name="🎫・open-ticket")

    if ticket_channel:
        # Everyone CAN see the channel to raise a ticket, but cannot type or react
        await ticket_channel.set_permissions(
            everyone, 
            view_channel=True, 
            send_messages=False, 
            add_reactions=False
        )

        for role in staff_roles:
            if role:
                await ticket_channel.set_permissions(
                    role, 
                    view_channel=True, 
                    send_messages=True, 
                    manage_messages=True, 
                    manage_channels=True
                )

    # =================================
    # 📌 information
    # =================================
    welcome_channel = discord.utils.get(guild.channels, name="👋・welcome")
    rules_channel = discord.utils.get(guild.channels, name="📖・rules")
    announcements_channel = discord.utils.get(guild.channels, name="📢・announcements")
    goodbye_channel = discord.utils.get(guild.channels, name="👋・goodbye")
    invite_tracker_channel = discord.utils.get(guild.channels, name="📈・invite-tracker")

    # 👋 welcome
    if welcome_channel:
        await welcome_channel.set_permissions(everyone, send_messages=False)
        if founder:
            await welcome_channel.set_permissions(founder, send_messages=True)
        if owner:
            await welcome_channel.set_permissions(owner, send_messages=True)

    # 📖 rules
    if rules_channel:
        await rules_channel.set_permissions(everyone, send_messages=False, add_reactions=True)
        for role in staff_roles:
            if role:
                await rules_channel.set_permissions(role, send_messages=True, manage_messages=True)

    # 📢 announcements
    if announcements_channel:
        await announcements_channel.set_permissions(everyone, send_messages=False)
        if founder:
            await announcements_channel.set_permissions(founder, send_messages=True)
        if owner:
            await announcements_channel.set_permissions(owner, send_messages=True)

    # 👋 goodbye
    if goodbye_channel:
        await goodbye_channel.set_permissions(everyone, send_messages=False)
        if founder:
            await goodbye_channel.set_permissions(founder, send_messages=True)

    # 📈 invite-tracker
    if invite_tracker_channel:
        await invite_tracker_channel.set_permissions(everyone, send_messages=False)
        if founder:
            await invite_tracker_channel.set_permissions(founder, send_messages=True)
        if owner:
            await invite_tracker_channel.set_permissions(owner, send_messages=True)

    # =================================
    # 💬 community
    # =================================
    general_channel = discord.utils.get(guild.channels, name="💬・general-chat")
    intro_channel = discord.utils.get(guild.channels, name="🌸・introductions")
    media_channel = discord.utils.get(guild.channels, name="🖼️・media")
    memes_channel = discord.utils.get(guild.channels, name="😂・memes")
    bot_channel = discord.utils.get(guild.channels, name="🤖・bot-commands")

    # 💬 general-chat (Standard messaging. Links handled below by Level rules)
    if general_channel:
        await general_channel.set_permissions(
            everyone, 
            send_messages=True, 
            attach_files=False, 
            embed_links=False,
            create_public_threads=False,
            create_private_threads=False
        )

    # 🌸 introductions (Locked down for members; strictly for bots/onboarding tools)
    if intro_channel:
        await intro_channel.set_permissions(everyone, send_messages=False)

    # 🖼️ media (Images allowed, text links blocked. Filter out GIFs via Discord AutoMod)
    if media_channel:
        await media_channel.set_permissions(everyone, send_messages=True, attach_files=True, embed_links=False)

    # 😂 memes (Requires embed_links for the native Discord GIF picker to function)
    if memes_channel:
        await memes_channel.set_permissions(everyone, send_messages=True, attach_files=True, embed_links=True)

    # 🤖 bot-commands (Slash commands only, absolute zero file/link leakage)
    if bot_channel:
        await bot_channel.set_permissions(
            everyone, 
            send_messages=True, 
            use_application_commands=True, 
            attach_files=False, 
            embed_links=False
        )

    # =================================
    # 🎮 gaming & 🌸 anime
    # =================================
    gaming_chat = discord.utils.get(guild.channels, name="🎮・gaming-chat")
    gaming_vc = discord.utils.get(guild.channels, name="🎮・gaming-vc")
    
    anime_chat = discord.utils.get(guild.channels, name="🌸・anime-chat")
    anime_vc = discord.utils.get(guild.channels, name="🌸・anime-vc")

    # Content streams: Social media & game links allowed natively. Threads locked for default members.
    for chat_channel in [gaming_chat, anime_chat]:
        if chat_channel:
            await chat_channel.set_permissions(
                everyone,
                send_messages=True,
                attach_files=True,
                embed_links=True,
                create_public_threads=False, # Disabled for everyone
                create_private_threads=False # Disabled for everyone
            )
            for role in staff_roles:
                if role:
                    await chat_channel.set_permissions(role, manage_messages=True, manage_threads=True)

    for vc_channel in [gaming_vc, anime_vc]:
        if vc_channel:
            await vc_channel.set_permissions(everyone, connect=True, speak=True, stream=True, use_voice_activation=True)
            for role in staff_roles:
                if role:
                    await vc_channel.set_permissions(role, mute_members=True, deafen_members=True, move_members=True)

    # =================================
    # 🎵 music
    # =================================
    music_chat = discord.utils.get(guild.channels, name="🎵・music-chat")
    music_lounge = discord.utils.get(guild.channels, name="🎧・music-lounge")
    karaoke_room = discord.utils.get(guild.channels, name="🎤・karaoke-room")

    # Music text lounge: Commands, reactions, and embeds enabled. Files disabled. Filter GIFs via AutoMod.
    if music_chat:
        await music_chat.set_permissions(
            everyone,
            send_messages=True,
            attach_files=False,
            embed_links=True,
            add_reactions=True,
            use_application_commands=True,
            create_public_threads=False, # Disabled for everyone
            create_private_threads=False # Disabled for everyone
        )
        for role in staff_roles:
            if role:
                await music_chat.set_permissions(role, manage_messages=True, manage_threads=True)

    # Audio Lounges: Audio-only. Video stream sharing completely blocked.
    for audio_vc in [music_lounge, karaoke_room]:
        if audio_vc:
            await audio_vc.set_permissions(
                everyone, 
                connect=True, 
                speak=True, 
                stream=False,  
                use_voice_activation=True,
                use_application_commands=True
            )
            for role in staff_roles:
                if role:
                    await audio_vc.set_permissions(role, mute_members=True, deafen_members=True, move_members=True)

    # =================================
    # 🎙 voice lounges
    # =================================
    chill_lounge = discord.utils.get(guild.channels, name="☕・chill-lounge")
    squad_room = discord.utils.get(guild.channels, name="🔊・squad-room")
    duo_room = discord.utils.get(guild.channels, name="👥・duo-room")
    trio_room = discord.utils.get(guild.channels, name="👥・trio-room")
    late_night = discord.utils.get(guild.channels, name="🌙・late-night-talks")

    voice_lounges = [chill_lounge, squad_room, duo_room, trio_room, late_night]

    for channel in voice_lounges:
        if channel:
            await channel.set_permissions(everyone, connect=True, speak=True, stream=True, use_voice_activation=True)
            for role in staff_roles:
                if role:
                    await channel.set_permissions(
                        role,
                        mute_members=True,
                        deafen_members=True,
                        move_members=True,
                        priority_speaker=True
                    )

    # =================================
    # ⭐ Level perks
    # =================================
    # 🌙 Level II permissions override for general server texts
    if level_2:
        for channel in guild.text_channels:
            if channel.name in ["💬・general-chat"]:
                await channel.set_permissions(level_2, attach_files=True, use_external_emojis=True)

    # 🌌 Level III permissions override (Allows links & threads in general chat, and threads in other hubs)
    if level_3:
        for channel in guild.text_channels:
            # Full Level III perks for General Chat
            if channel.name == "💬・general-chat":
                await channel.set_permissions(
                    level_3,
                    attach_files=True,
                    embed_links=True,
                    create_public_threads=True,
                    create_private_threads=True,
                    use_external_emojis=True
                )
            # Thread creation access for other interactive community channels
            elif channel.name in ["🎮・gaming-chat", "🌸・anime-chat", "🎵・music-chat", "🖼️・media", "😂・memes"]:
                await channel.set_permissions(
                    level_3,
                    create_public_threads=True,
                    create_private_threads=True
                )

    # =================================
    # Core System Disclaimer
    # =================================
    # Discord API cannot natively track target-specific contexts such as:
    # - "Allow only Game links" / "Allow only Spotify/YouTube links"
    # - "Block raw file GIFs but allow PNGs"
    # Execute these rule specifications inside Discord's Native AutoMod Dashboard.