import discord, asyncio
import aiohttp
from discord import Webhook, AsyncWebhookAdapter
from time import sleep
from discord.utils import get
from discord.ext.commands import *
from datetime import *
from random import randint

class Events(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color = 0x646ecb

	@Cog.listener()
	async def on_message(self, message):
		if message.channel.id == 732004223159631893:
			await message.add_reaction("🔼")
			await message.add_reaction("🔽")
			await message.add_reaction("❤")

	"""@Cog.listener()
	async def on_member_join(self, member):
		channel = discord.utils.get(member.guild.channels, id=int(729029346987344013))
		embed = discord.Embed(color=self.color, title="Bem vindo(a) %s a nossa comunidade!" % member.name,
			description="Nós da DevLabs temos como foco ajudar as pessoas na área da programação. Aqui você pode divulgar seus projetos, pedir opiniões, **adicionar seu bot** e muito mais.\n\n"
			":small_blue_diamond: Acesse nosso Github: [Clique Aqui](https://twitter.com/devlabs/)\n"
			":small_blue_diamond: Adicione seu bot: <#745766852524900413>"
			)
			
		embed.set_thumbnail(url=str(member.avatar_url))
		embed.set_footer(text="Atenciosamente, DevLabs: A sua comunidade de programação.")

		if member.bot:
			await member.add_roles(get(member.guild.roles, name="🤖Bots"))
		else:
			await member.add_roles(get(member.guild.roles, name="Membros"))

		await channel.send(embed=embed)
	"""
	
	@Cog.listener()
	async def on_raw_reaction_add(self, payload):

		if payload.message_id == 770377487103557673:
			guild = await self.bot.fetch_guild(payload.guild_id)
			if payload.emoji.name == "python":
				await payload.member.add_roles(get(guild.roles, name="🐍Python"))

			if payload.emoji.name == "javascript":
				await payload.member.add_roles(get(guild.roles, name="⚡JavaScript"))

			if payload.emoji.name == "java":
				await payload.member.add_roles(get(guild.roles, name="☕Java"))

			if payload.emoji.name == "ccc":
				await payload.member.add_roles(get(guild.roles, name="🌀C,C++,C#"))

			if payload.emoji.name == "php":
				await payload.member.add_roles(get(guild.roles, name="🐘PHP"))

			if payload.emoji.name == "🌐":
				await payload.member.add_roles(get(guild.roles, name="🌎Web"))

			if payload.emoji.name == "📱":
				await payload.member.add_roles(get(guild.roles, name="📱Mobile"))

			if payload.emoji.name == "🖥️":
				await payload.member.add_roles(get(guild.roles, name="🖥️Desktop"))

			if payload.emoji.name == "🇸":
				await payload.member.add_roles(get(guild.roles, name="🗄️SQL"))

			if payload.emoji.name == "🇳":
				await payload.member.add_roles(get(guild.roles, name="🗄️NoSQL"))

			if payload.emoji.name == "🚹":
				await payload.member.add_roles(get(guild.roles, name="🚹 Homem"))

			if payload.emoji.name == "🚺":
				await payload.member.add_roles(get(guild.roles, name="🚺 Mulher"))

			if payload.emoji.name == "💼":
				await payload.member.add_roles(get(guild.roles, name="💼 Trabalhador(a)"))

			if payload.emoji.name == "🎓":
				await payload.member.add_roles(get(guild.roles, name="🎓 Estudante"))

			if payload.emoji.name == "🎮":
				await payload.member.add_roles(get(guild.roles, name="🎮 Gamer"))

			if payload.emoji.name == "⛔️":
				await payload.member.add_roles(get(guild.roles, name="⛔️+18"))

			if payload.emoji.name == "🔞":
				await payload.member.add_roles(get(guild.roles, name="🔞-18"))

	"""
	@cooldown(2, 10, BucketType.user)
	@command(aliases=["apresenta", "apresente-se", "meapresentar", "mep"])
	async def apresentar(self, ctx):
		if "💬Apresentado" in [x.name for x in ctx.author.roles]:
			return await ctx.send(embed=discord.Embed(color=self.color, description="Você já está apresentado!"))
		await ctx.send(embed=discord.Embed(color=self.color, description="Uma mensagem foi enviada no seu DM!"), delete_after=10)
		await ctx.author.send(embed=discord.Embed(color=self.color, description="Olá, %s. Irei realizar algumas perguntas básicas para você ser apresentando em nosso servidor.\n1. Qual seu nome real?" % ctx.author.mention))
		name = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)
		await ctx.author.send(embed=discord.Embed(color=self.color, description="2. Quantos anos você tem, %s?" % str(name.content).title()))
		idade = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)
		await ctx.author.send(embed=discord.Embed(color=self.color, description="3. Qual seu Github/GitLab/BitBucket? Caso não tenha, digite 'Nenhum'."))
		repo = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)
		await ctx.author.send(embed=discord.Embed(color=self.color, description="4. Conte-nos mais sobre você, %s" % str(name.content).title()))
		about = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=120)
		msg = await ctx.author.send(embed=discord.Embed(color=self.color, 
			description="5. Pegue os cargos de acordo com a linguagem que você programa.Clique em ✅ para finalizar.\n\n"
				"Python - <:python:693187822676344832>\nJavaScript - <:javascript:693187822697578616>\nJava: <:java:693187822646984734>\nC,C++,C# - <:cpp:693187822735327282>\nPHP - <:php:693189982755749978>\n"
				"Web - 🌐\nMobile - 📱\nDesktop - 🖥️\nSQL - 🇸\nNoSQL - 🇳\nDesenvolvedor de Bots - 🤖"))

		await msg.add_reaction(":python:693187822676344832")
		await msg.add_reaction(":javascript:693187822697578616")
		await msg.add_reaction(":java:693187822646984734")
		await msg.add_reaction(":cpp:693189982755749978")
		await msg.add_reaction(":php:693187822735327282")
		await msg.add_reaction("🌐")
		await msg.add_reaction("📱")
		await msg.add_reaction("🖥️")
		await msg.add_reaction("🇸")
		await msg.add_reaction("🇳")
		await msg.add_reaction("✅")

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji)
		try:
			while True:
				reaction, user = await self.bot.wait_for('reaction_add', timeout=120, check=check)
				if str(reaction.emoji) == "<:python:693187822676344832>":
					await ctx.author.add_roles(get(ctx.guild.roles, name="🐍Python"))
				if str(reaction.emoji) == "<:javascript:693187822697578616>":
					await ctx.author.add_roles(get(ctx.guild.roles, name="⚡JavaScript"))
				if str(reaction.emoji) == "<:java:693187822646984734>":
					await ctx.author.add_roles(get(ctx.guild.roles, name="☕Java"))
				if str(reaction.emoji) == "<:php:693187822735327282>":
					await ctx.author.add_roles(get(ctx.guild.roles, name="🐘PHP"))
				if str(reaction.emoji) == "<:cpp:693189982755749978>":
					await ctx.author.add_roles(get(ctx.guild.roles, name="🌀 C,C++,C#"))
				if str(reaction.emoji) == "🌐":
					await ctx.author.add_roles(get(ctx.guild.roles, name="🌎Web"))
				if str(reaction.emoji) == "📱":
					await ctx.author.add_roles(get(ctx.guild.roles, name="📱Mobile"))
				if str(reaction.emoji) == "🖥️":
					await ctx.author.add_roles(get(ctx.guild.roles, name="🖥️Desktop"))
				if str(reaction.emoji) == "🇸":
					await ctx.author.add_roles(get(ctx.guild.roles, name="🗄️SQL"))
				if str(reaction.emoji) == "🇳":
					await ctx.author.add_roles(get(ctx.guild.roles, name="🗄️NoSQL"))
				if str(reaction.emoji) == "✅":
					await ctx.author.add_roles(get(ctx.guild.roles, name="💬Apresentado"))
					emb = discord.Embed(color=self.color, timestamp=ctx.message.created_at)
					emb.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
					emb.add_field(name="Nome Real:", value=name.content, inline=True)
					emb.add_field(name="Idade:", value=idade.content, inline=True)
					emb.add_field(name="Git:", value=repo.content, inline=False)
					emb.add_field(name="Sobre:", value=about.content, inline=False)
					emb.set_footer(text="ID: %s" % str(ctx.author.id))		
					emb.set_thumbnail(url=str(ctx.author.avatar_url))		
					await self.bot.get_channel(741389158156730451).send(embed=emb)
					await msg.delete()
					await ctx.author.send(embed=discord.Embed(color=self.color, description="Apresentação concluída, muito obrigado."), delete_after=5)
					break
		except asyncio.TimeoutError:
			await ctx.author.send(embed=discord.Embed(color=self.color, description="Acabou o tempo de resposta. Por favor, execute o comando novamente para se apresentar."))
	"""
	"""
	@has_any_role("🧪:: DevLabs", "Administradores")
	@cooldown(2, 10, BucketType.user)
	@command(aliases=["addtutorial", "medium", "addmedium"])
	async def addtutor(self, ctx, *, text):
		if text == None:
			return await ctx.send(embed=discord.Embed(color=self.color, description="Coloque o link e um texto!"))
		else:
			async with aiohttp.ClientSession() as session:
				webhook = Webhook.from_url("https://discordapp.com/api/webhooks/721815326504910908/ngQFZtKSQq-i-lYB7KU7zHjIwSbI28GbioUl5j8CCsYtQKr9z0o0tYamyh6PAzeDJPO-", adapter=AsyncWebhookAdapter(session))
				embed = discord.Embed(color=0x2f3136, title="Nova postagem no ar!", description="%s" % text, timestamp=ctx.message.created_at)
				embed.set_footer(text="©️ 2020 DevLabs", icon_url=ctx.me.avatar_url)
				embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
				await webhook.send(embed=embed, username="Medium")
	"""

def setup(bot):
	bot.add_cog(Events(bot))

