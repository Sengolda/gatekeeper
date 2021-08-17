import sqlite3
import discord
from discord.ext.commands import Cog, command, group, has_guild_permissions as has_perms
from asyncio import sleep
import random
from discord.ext import tasks

ROLE_ID = 'YOUR_MEMBER_ID_ROLE_HERE'

class gatekeep(Cog, name="GateKeep"):
	def __init__(self, bot):
		self.bot = bot
		self.verified = []
		self.fill_verified.start()
	
    
	@tasks.loop(seconds=15)
	async def fill_verified(self):
		self.verified.clear()
		db = sqlite3.connect('sqlite.db')
		c = db.cursor()
		c.execute('SELECT user_id FROM gatekeep')
		users = c.fetchall()
		z = []
		for i in users:
			for e in i:
				z.append(e)

		self.verified.extend(z)
		print(self.verified)

	@group(invoke_without_command=True)
	async def gatekeep(self, ctx):
		await ctx.send_help(ctx.command)


	@gatekeep.command(help="add a user that can bypass the gatekeep.")
	@has_perms(manage_guild=True)
	async def add(self, ctx, user: discord.User):
		db = sqlite3.connect('sqlite.db')
		c = db.cursor()
		try:
			c.execute('INSERT INTO gatekeep VALUES (?)', (user.id,))
		except:
			await ctx.send(f"This user is already whitelisted\n to remove them do `{ctx.prefix}gatekeep remove`.")

		else:
			db.commit()
			await ctx.send(f'{user} is now added to the whitelist.')
	
	@gatekeep.command(help="remove a user that can bypass the gatekeep.")
	@has_perms(manage_guild=True)
	async def remove(self, ctx, user: discord.User):
		db = sqlite3.connect('sqlite.db')
		c = db.cursor()
		try:
			c.execute('DELETE FROM gatekeep WHERE user_id = ?', (user.id,))
		except Exception:
			await ctx.send(f'This user never was added.')
		
		else:
			db.commit()
			await ctx.send(f'Removed {user} from the whitelist\nThey can no-longer bypass gatekeep.')
	
	@Cog.listener()
	async def on_member_join(self, member: discord.Member):
		if member.id not in self.verified:
			print('')
			ch = await member.guild.create_text_channel(f'gatekeep-{member.id}')
			await ch.set_permissions(member, read_messages=True)
			await ch.send("Please wait 20 seconds.")
			await sleep(20)
			await ch.set_permissions(member, overwrite=None)
			rand_word = random.choice(['Tyeoe,sz','sjindihe','OWOOWDDN','6rxdds','78gxdd'])
			await ch.send(f'{member.mention} Yo welcome to bot\'s gatekeep please type the following\n{str(rand_word)}\n\nAlso this is case-sensitive.')
			def check(m):
				return m.channel == ch and m.author == member
			
			user_msg = await self.bot.wait_for('message', check=check, timeout=60.0)
			if str(user_msg.content) == str(rand_word):
				await member.add_roles(discord.Object(id=int(ROLE_ID)))
				await ch.send("Congo, you passed!")
				await sleep(0.10)
				await ch.delete()
		
		else:
			await member.add_roles(discord.Object(id=int(ROLE_ID)))
		



def setup(bot):
	bot.add_cog(gatekeep(bot))