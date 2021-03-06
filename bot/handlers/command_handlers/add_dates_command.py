from re import findall
from discord import Embed, Emoji, utils
from itertools import zip_longest
from math import ceil
import logging
from datetime import datetime

from ...environment import bot_environment, emotes
from ..helpers import get_role_mention

# Sends message with rich embed with dates given in command message
# assigning emote to each and reactions for voting under sent message.
async def add_dates_command(context, dates):

    # Extract dates from command parameter.
    dates = findall(r'(\d{1,2}\.\d{1,2};{1})', dates + ';')

    # Check if there are any dates and if their amount isn't to big.
    if len(dates) == 0:
        logging.error('add_dates_command: No dates found')
        return
    elif len(dates) > len(emotes):
        logging.error('add_dates_command: Too many dates found')
        return

    # Create Rich Embed with given dates.
    embed = Embed(
        title='Terminy na kolejny tydzień. Oznaczcie które dni wam pasują:',
        type='rich',
        description= '\n\n'.join(['{}{}{}'.format(emotes[it], u'\u00A0'*4, str(datetime.strptime(date, '%d.%m;').replace(year=datetime.now().year).strftime('%d.%m, %A'))) for (it, date) in enumerate(dates)]),
    )

    # Check if config file have role mention for current server.
    try:
        role_mention_id = get_role_mention(context)
    except:
        return

    # Send message with proper mention and rich embed.
    dates_msg = await context.send(f'<@&{role_mention_id}>', embed=embed)

    # Add reactions for voting.
    for i in range(0, len(dates)):
        await dates_msg.add_reaction(emotes[i])

    # Add `X` reaction for signaling no date chosen.
    await dates_msg.add_reaction('❌')