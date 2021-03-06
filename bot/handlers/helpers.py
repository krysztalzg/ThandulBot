import logging

from ..environment import bot_environment

# Removes message with command if have permissions.
async def remove_command_message(message):
    try:
        await message.delete()
    except:
        logging.error('Failed to delete message.')
        return

# Checks if command can be called by given user in given channel.
def should_perform_command(context):
    if not check_author_permission(context.command.name, context.author.id):
        logging.error(f'should_perform_command: user without permissions to use command. {context.author.name} {context.message.content}')
        return False

    if not check_channel_id(context.command.name, context.channel.id):
        logging.error(f'should_perform_command: command called in wrong channel. {context.channel.name} {context.message.content}')
        return False

    return True

# Checks if user that issued admin command is in permissions list.
def check_author_permission(command, author_id):
    if command in bot_environment.admin_commands:
        return str(author_id) == str(bot_environment.admin_id)
    else:
        return True

# Checks if user issued command in correct channel from config file.
def check_channel_id(command, channel_id):
    if command in bot_environment.command_channels.keys():
        return channel_id in bot_environment.command_channels[command]
    else:
        return True

# Get role mention that is present on server that command was issued at.
def get_role_mention(context):
    try:
        mentionable_role = bot_environment.mention_role_ids[context.guild.id][context.channel.id]
        if mentionable_role in [role.id for role in context.guild.roles]:
            return mentionable_role
    except:
        logging.error('No role to mention.')
        raise Exception()
