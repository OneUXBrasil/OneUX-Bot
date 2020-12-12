import discord
from .data import add_bot
from discord.utils import get
from discord.ext.commands import *

class Bots(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color = 0x646ecb

	@cooldown(2, 86400, BucketType.user)
	@guild_only()
	@command(aliases=["adicionar", "add", "botadd"])
	async def addbot(self, ctx):
		await ctx.send(embed=discord.Embed(color=self.color, description="Enviei uma mensagem no seu DM! Caso não tenha recebido, habilite as mensagens de membros do servidor!"))
		await ctx.author.send(embed=discord.Embed(color=self.color, description="Olá %s. Por favor, informe o **ID** do seu Bot." % ctx.author.mention))
		_id = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)
		await ctx.author.send(embed=discord.Embed(color=self.color, description="Okay! Agora me informe o prefixo!"))
		prefixo = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)
		
		if int(_id.content) in [x.id for x in ctx.guild.members]:
			return await ctx.author.send(embed=discord.Embed(color=self.color, description="Esse bot já **está** no servidor!\n ``Pedido finalizado``."))
		else:
			await ctx.author.send(embed=discord.Embed(color=self.color, description="Certo! Informações enviadas com sucesso!"))			
			convite = "https://discord.com/oauth2/authorize?client_id=%s&scope=bot&permissions=3492929" % _id.content
			aceitar = "dl.acbot %s %s" % (ctx.author.mention, _id.content)
			rejeitar = "dl.rjbot %s %s [MOTIVO_OPCIONAL]" % (ctx.author.mention, _id.content)

			emb = discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="Pedido solicitado por: %s\n" % (ctx.author.mention))
			emb.add_field(name="ID:", value="%s" % _id.content, inline=True)
			emb.add_field(name="Prefixo:", value="%s" % prefixo.content, inline=True)
			emb.add_field(name="Convite:", value="%s" % convite, inline=False)
			emb.add_field(name="Aceitar:", value="%s" % aceitar, inline=True)
			emb.add_field(name="Rejeitar:", value="%s" % rejeitar, inline=True)

			bot_user = await self.bot.fetch_user(int(_id.content))

			await self.bot.get_channel(749431819295916083).send(content=ctx.author.mention,
				embed=discord.Embed(color=self.color, description=f"<:status_idle:749750856253046907> **O bot ``{bot_user}`` pedido por {ctx.author.mention} entrou para a verificação, aguarde...**"))

			return await self.bot.get_channel(730556662993387580).send(embed=emb, content="<@&742813032362803291>")
			
	@guild_only()
	@has_role("Verificadores")
	@command(aliases=["aceitar", "botadc", "aceitarbot", "botaceitar"])
	async def acbot(self, ctx, member: discord.Member=None, *, bot_id:int=None):
		if member == None:
			return await ctx.send(embed=discord.Embed(color=self.color, description="%s, mencione o DONO do **bot** nos argumentos!" % ctx.author.mention))
		elif bot_id == None:
			return await ctx.send(embed=discord.Embed(color=self.color, description="%s, coloque o ID do **bot** nos argumentos!" % ctx.author.mention))			
		await ctx.send(embed=discord.Embed(color=self.color, description="Certo! O Bot foi aceito em nossa comunidade, obrigado."))
		emb = discord.Embed(color=self.color, title="Olá, %s!" % member.name, description="O seu bot foi aceito no servidor! Em breve adicionaremos ele.\n Por favor, leia as regras que se encontra no canal <#732709606119178391> para evitar problemas com seu bot!\n\nAtenciosamente, DevLabs.")
		emb.set_thumbnail(url=str(member.avatar_url))
		emb.set_footer(text="©️ DevLabs")
		try:
			add_bot(owner_id=member.id, bot_id=bot_id)
		except Exception as error:
			await ctx.send(embed=discord.Embed(color=self.color, description="Opss... Ocorreu um erro.\n*%s*" % error))
		else:
			bot_user = await self.bot.fetch_user(bot_id)
			await member.add_roles(get(ctx.guild.roles, name="💻DevBots"))
			return await self.bot.get_channel(749431819295916083).send(content=member.mention,
				embed=discord.Embed(color=self.color, description=f"<:status_online:749750856467087451> **O bot ``{bot_user}`` pedido por {member.mention} foi aceito pelo verificador {ctx.author.mention}...**"))
			#return await member.send(embed=emb)

	@guild_only()
	@has_role("Verificadores")
	@command(aliases=["rejeitar", "botrjt", "rejeitarbot", "botrejeitar"])
	async def rjbot(self, ctx, member: discord.Member=None, bot_id:int=None, *, reason=None):
		if member == None:
			return await ctx.send(embed=discord.Embed(color=self.color, description="%s, mencione o dono do **bot** nos argumentos!" % ctx.author.mention))
		elif reason == None:
			reason = "Não citado pelo administrador."
		await ctx.send(embed=discord.Embed(color=self.color, description="Certo! O Bot não foi aceito, obrigado."))
		emb = discord.Embed(color=self.color, title="Olá, %s!" % member.name, description="Infelizmente o seu bot não foi aprovado para ser adicionado em nosso servidor.\n**Motivo**: %s\n\nAtenciosamente, DevLabs." % reason)
		emb.set_thumbnail(url=str(member.avatar_url))
		emb.set_footer(text="©️ DevLabs")
		bot_user = await self.bot.fetch_user(bot_id)
		return await self.bot.get_channel(749431819295916083).send(content=member.mention,
			embed=discord.Embed(color=self.color, description=f"<:status_dnd:749750856601174086> **O bot ``{bot_user}`` pedido por {member.mention} foi rejeitado pelo verificador {ctx.author.mention}...**\n**Motivo:** {reason}"))
		#return await member.send(embed=emb)

def setup(bot):
	bot.add_cog(Bots(bot))