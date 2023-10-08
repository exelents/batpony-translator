import os
import re

from dotenv import load_dotenv, find_dotenv

# find the .env file and load it 
load_dotenv(find_dotenv())

from tokeneeezer import Tokeeenizer
my_tokenizer = Tokeeenizer()
import interactions
from interactions import MISSING

the_id_of_your_guild = int(os.getenv('DISCORD_GUILD_ID'))
print(f"the_id_of_your_guild = {the_id_of_your_guild}")
print(f"TOKEN = {os.getenv('DISCORD_BOT_TOKEN')}")
bot = interactions.Client(token=os.getenv('DISCORD_BOT_TOKEN'))

@bot.command(
    name="encode",
    description="Encode a message",
    scope=the_id_of_your_guild,
    options = [
        interactions.Option(
            name="text",
            description="What you want to encode",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def encode(ctx: interactions.CommandContext, text: str):
    try:
        encoded_text = my_tokenizer.encode_text(text)
        await ctx.send(f"Original text:\n{text}\n\nEncoded text:\n", ephemeral=True)
        await ctx.send(encoded_text, ephemeral=True)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}", ephemeral=True)


@bot.command(
    name="decode",
    description="Decode a message",
    scope=the_id_of_your_guild,
    options = [
        interactions.Option(
            name="text",
            description="What you want to decode",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def decode(ctx: interactions.CommandContext, text: str):
    try:
        decoded_text = my_tokenizer.decode_text(text)
        await ctx.send(f"Decoded text:\n\n{decoded_text}", ephemeral=True)  
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}", ephemeral=True)


@bot.command(
    name="translate",
    description="Translate from\\to batpony language",
    scope=the_id_of_your_guild,
    options = [
        interactions.Option(
            name="text",
            description="What you want to translate",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def translate(ctx: interactions.CommandContext, text: str):
    try:
        # Проверка, следует ли декодировать текст
        if re.match(f"^[{my_tokenizer.e_char}\- \n]*$", text):
            decoded_text = my_tokenizer.decode_text(text)
            await ctx.send(f"Decoded text:\n\n{decoded_text}", ephemeral=True)
        else:
            encoded_text = my_tokenizer.encode_text(text)
            await ctx.send(f"Original text:\n{text}\n\nEncoded text:\n", ephemeral=True)
            await ctx.send(encoded_text, ephemeral=True)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}", ephemeral=True)

bot.start()

