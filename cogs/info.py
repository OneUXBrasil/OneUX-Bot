import discord
import psutil
import time
import platform
import requests
import aiohttp

from discord.ext.commands import *
from discord import AsyncWebhookAdapter
from datetime import datetime, timedelta
from discord.utils import get
from datetime import date
from random import randint
from discord.ext.commands.errors import BadArgument
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Information(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.start_time = time.time()
		self.color = 0x7A4EF9

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["hlp", "ajuda"])
	async def help(self, ctx):

		emb = discord.Embed(color=self.color, title="Prefixo: ox.", description="Comandos do Bot:", timestamp=ctx.message.created_at)
		emb.add_field(name="Informação:", value="ping, botinfo, serverinfo, userinfo, avatar, cep, emojinfo, job")
		emb.add_field(name="Diversão:", value="8ball, charada, roll, dado, clone", inline=False)
		emb.add_field(name="Em Breve:", value="Outros comandos...", inline=True)
		return await ctx.send(embed=emb)

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["picture", "pic"])
	async def avatar(self, ctx, *, member:discord.Member=None):
		if member == None:
			avatar = ctx.author.avatar_url
		else:
			avatar = member.avatar_url
		embed = discord.Embed(color=self.color, description="🖼️ [Baixar]("+ str(avatar) +")")
		embed.set_image(url=str(avatar))
		return await ctx.send(embed=embed)

	@avatar.error
	async def avatar_error(self, ctx, error):
		if isinstance(error, BadArgument):
			return await ctx.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="Não encontrei esse usuário!"))

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["useri", "ui"])
	async def userinfo(self, ctx, *, user:discord.Member=None):
		if user == None:
			user = ctx.author
		else:
			user = user

		try:
			game = user.activity.name
		except:
			game = "Nenhuma" 
		try:
			game_type = "``" + str(user.activity.type.name) + "``"
		except:
			game_type = ""

		status = str(user.status).replace("idle", "Ausente").replace("offline", "Offline").replace("dnd", "Não Pertube").replace("online", "Online")
		bots = "- Nenhuma"

		emb = discord.Embed(color=self.color, timestamp=ctx.message.created_at, description=f"**🔻 Informações de:** {user.mention}\n\n"
			"🔹 **ID:** %s\n🔹 **Tag:** %s\n🔹 **TopRole:** %s\n🔹 **Status:** %s\n🔹 **Atividade:** %s %s\n" 
			f"🔹 **Entrou no Servidor:** {(user.joined_at.strftime('%d %b %Y às %H:%M'))}, {(datetime.utcnow() - user.joined_at).days} dias atrás\n🔹 **Conta Criada:** {(user.created_at.strftime('%d %b %Y às %H:%M'))}, {(datetime.utcnow()- user.created_at).days} dias atrás" % (
				user.id, user.discriminator, user.top_role.mention, status, game_type.title(), game))
		emb.set_thumbnail(url=str(user.avatar_url_as(format="png")))
		emb.set_footer(text="OneUX © 2020", icon_url=str(user.avatar_url))
		return await ctx.send(embed=emb)

	@userinfo.error
	async def userinfo_error(self, ctx, error):
		if isinstance(error, BadArgument):
			return await ctx.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="Opsss... Não encontrei esse usuário!"))

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["guildinfo", "gi", "si"])
	async def serverinfo(self, ctx):
		emb = discord.Embed(color=self.color, timestamp=ctx.message.created_at, title="Informações do nosso Servidor!", url="https://top.gg/servers/{}".format(ctx.guild.id), 
			description="**🔻 OneUX Community:\n\n**"
			"🔹 **ID:** %s\n🔹 **Fundadores:** <@296428519947370499>, <@617916467588890625>\n🔹 **Membros:** %s\n"
			"🔹 **Cargos:** %s\n🔹 **Emojis:** %s\n🔹 **Canais:** %s\n\n" 
			"📆 Criado em: %s, %s dias atrás!"
			% (ctx.guild.id, ctx.guild.member_count, len(ctx.guild.roles),len(ctx.guild.emojis), len(ctx.guild.channels), ctx.guild.created_at.strftime('%d %b %Y às %H:%M'), (datetime.utcnow()- ctx.guild.created_at).days))
		
		emb.set_thumbnail(url=str(ctx.guild.icon_url))
		emb.set_footer(text="OneUX © 2020", icon_url=ctx.me.avatar_url)
		return await ctx.send(embed=emb)

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["ms"])
	async def ping(self, ctx):
		return await ctx.send(embed=discord.Embed(color=self.color, description=f"**A minha latência é de: **{round(self.bot.latency*1000)}ms"))

	@cooldown(2, 30, BucketType.user)
	@guild_only()
	@command(aliases=["job", "sjob"])
	async def searchjob(self, ctx, *, job:str=None):
		if job == None: 
			return await ctx.send(embed=discord.Embed(color=randint(0, 0xFFFFFF), description="Por favor, não deixe em branco o campo ``job``."))
		await ctx.send(embed=discord.Embed(color=self.color, description="Caso nenhuma **embed** apareça abaixo, significa que nenhum resultado foi encontrado."))
		url = "https://www.manager.com.br/empregos-%s" % job.strip().lower()
		soup = BeautifulSoup(requests.get(url, headers={"User-Agent": UserAgent().chrome}).text, "html.parser")
		embed = discord.Embed(color=self.color, timestamp=ctx.message.created_at, url=url, title="Mais informações clique aqui.")
		embed.set_footer(text="OneUX © 2020", icon_url=ctx.me.avatar_url)

		for a in soup.findAll("div", attrs={"class": "lista-resultado-busca"}):
			embed.description = str(a.find("article", attrs={"class": "vaga hlisting"}).text)
			await ctx.send(embed=embed)

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["ceps", "buscep", "cepinfo"])
	async def cep(self, ctx, *, cep):
			cep = requests.get(f"http://viacep.com.br/ws/{cep}/json").json()
			if str(cep["complemento"]) is "":
				comp = "Nenhum."
			else:
				comp = str(cep["complemento"])
			embed = discord.Embed(color=self.color, description=
				f'🔻 **CEP:** {str(cep["cep"])}\n\n'
				f'🔹 **Estado:** {str(cep["uf"])}\n'
				f'🔹 **Logradouro:** {str(cep["logradouro"])}\n'
				f'🔹 **Bairro:** {str(cep["bairro"])}\n'
				f'🔹 **Cidade:** {str(cep["localidade"])}\n'
				f'🔹 **Gia:** {str(cep["gia"])}\n'
				f'🔹 **IBGE:** {str(cep["ibge"])}\n'
				f'🔹 **Complemento:** {comp}\n')	
			embed.set_footer(text="OneUX © 2020", icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed)

	@cooldown(1, 15, BucketType.user)
	@guild_only()
	@command(aliases=["my", "me", "eu"])
	async def clone(self, ctx, member:discord.Member=None, *, msg=None):

		await ctx.message.delete()

		if member is None:
			member = ctx.author
		elif msg is None:
			return await ctx.send(embed=discord.Embed(color=self.color, description=f"**{member.mention}, por favor, digite algo.**"))
		else:
			async with aiohttp.ClientSession():
				webhook = await ctx.channel.create_webhook(name=member.name)
				await webhook.send(msg, username=member.name, avatar_url=member.avatar_url_as(format="png"))
				await webhook.delete()

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["emjinfo", "infoemj", "infoemoji", "emojiinfo"])
	async def emojinfo(self, ctx, *, emoji: discord.Emoji):
		if emoji is None:
			return await edit(ctx, color=self.color, description=f"**{ctx.author.mention} por favor, digite seu emoji. (++emojinfo <emoji>)**")
		else:
			embed = discord.Embed(color=self.color, description=
				f"🔻 **Nome:** {emoji.name}\n\n"
				f"🔹 **ID:** {emoji.id}\n"
				f"🔹 **Gif:** {emoji.animated}\n"
				f"🔹 **Servidor:** {emoji.guild}\n"
				f"🔹 **Criada em:** {emoji.created_at.strftime('%d/%m/%Y - %H:%M:%S')}\n"
				f"🔹 **Developer:** ``<:{emoji.name}:{emoji.id}>``\n"
				f"🔹 **Clique para [baixar]("+ str(emoji.url) +")**".replace("False", "Sim").replace("True", "Sim"))

			embed.set_thumbnail(url=str(emoji.url))
			embed.set_footer(text="OneUX © 2020", icon_url=ctx.me.avatar_url)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Information(bot))