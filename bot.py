import discord
from discord.ext import commands


class GateKeepBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="g.", intents=discord.Intents.all())


	async def on_ready(self):
		print(f'Logged in as {self.user} (ID: {self.user.id})')
		print('-'*52)


bot = GateKeepBot()
bot.load_extension('cogs.gatekeep')
bot.run('')