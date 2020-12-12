import discord
from requests import get
from discord.ext.commands import *
from random import randint, choice 

def possibles_answers():
	return str(choice(
		["Sim", "Não", "Claro!", "Óbviamente.", "Provavelmente.", "Nem o Google sabe responder..."]))

class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color = 0x7A4EF9

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["8ball", "8bal"], usage="++8ball [question]")
	async def ball(self, ctx, *, question:str=None):
		if question == None:
			return await ctx.send(embed=discord.Embed(color=self.color, description="<:not_check:676916774196871170> Faça alguma pergunta!\n**Uso correto:** %s" % ctx.command.usage))
		else:
			return await ctx.send(embed=discord.Embed(color=self.color, description="**Pergunta:** %s\n**Resposta:** %s" %(question, str(possibles_answers()))))

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["piada", "joke", "chr"])
	async def charada(self, ctx):
		r = get("https://us-central1-kivson.cloudfunctions.net/charada-aleatoria", headers={"Accept": "Accept: application/json"}).json()
		return await ctx.send(embed=discord.Embed(color=self.color, description="**%s**\n\n%s" %(r["pergunta"], r["resposta"])))

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["caraoucoroa"])
	async def roll(self, ctx):
		result = choice(["Cara", "Coroa"])

		if result == "Cara":
			return await ctx.message.add_reaction("😄")
		else:
			return await ctx.message.add_reaction("👑")

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["dd"])
	async def dado(self, ctx):
		return await ctx.send(embed=discord.Embed(color=self.color, description="🎲| ** Joguei o dado e caiu em: %s **" %(randint(1, 6))))

	# @cooldown(2, 10, BucketType.user)
	# @guild_only()
	# @command()
	# async def say(self, ctx, *, msg):
	# 	await ctx.message.delete()
	# 	return await ctx.send(msg)

	@Cog.listener()
	async def on_message(self, message):
		if message.channel.id == 732004223159631893:
			await message.add_reaction("🔼")
			await message.add_reaction("🔽")
			await message.add_reaction("❤")

def setup(bot):
	bot.add_cog(Fun(bot))