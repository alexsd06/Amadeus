#https://discord.com/oauth2/authorize?client_id=1123282242844770416&permissions=8&integration_type=0&scope=bot+applications.commands
import os
from characterai import aiocai, sendCode, authUser
import asyncio
import discord
from characterai import aiocai
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot_token=os.getenv("BOT_TOKEN")
email=os.getenv("EMAIL")
chai_token=os.getenv("CHAI_TOKEN")
amadeus_id=os.getenv("AMADEUS_ID")

client = aiocai.Client(chai_token)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
@bot.command()
async def token(ctx):
	sendCode(email)
	await ctx.send("*System: An authentication token was just sent to your email! Run !code link_here to get your token!*")
@bot.command()
async def code(ctx, *args):
	link=args[0]
	token=authUser(link, email)
	await ctx.send(f"*System: Your token is: {token}*")

@bot.command()
async def test(ctx):
	await ctx.send("*System status: online!*")

@bot.command()
async def amadeus(ctx, *args):
	async with ctx.typing():
		string=" ".join(args)
		print (f"User: {string}")
		async with await client.connect() as chat:
			chat_data=await client.get_chat(amadeus_id)
			message = await chat.send_message(
				amadeus_id, chat_data.chat_id, string
			)
			print(f"Amadeus: {message.text}")  # message.name
			await ctx.send(message.text)

@bot.command()
async def reset(ctx):
	print ("Resetting Amadeus!")
	me = await client.get_me()
	async with await client.connect() as chat:
		await chat.new_chat(amadeus_id, me.id)
		print ("Chat history reset!")
		await ctx.send("*System: Amadeus forgot everything!*")
@bot.event
async def on_ready():
	print (f"Amadeus is now online!")

bot.run(bot_token)