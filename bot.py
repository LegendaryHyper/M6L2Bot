from config import *
import discord
from discord.ext import commands
from config import TOKEN
from gen import gen_and_save

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot başlatıldı!")  

async def send_image(user, image_path):
    with open(image_path, 'rb') as img:
        file = discord.File(img)
        await user.send(file=file)

@bot.command()
async def start(ctx: commands.Context):
    await ctx.send(f"Merhaba, {ctx.author.name}.")

@bot.command()
async def generate(ctx, prompt):
    gen_imgs = gen_and_save(prompt)
    with open(gen_imgs[0], 'rb') as img:
        file = discord.File(img)
        await ctx.send(file=file)

if __name__ == "__main__":
    bot.run(TOKEN)
