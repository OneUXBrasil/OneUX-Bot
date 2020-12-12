import discord

from discord.ext.commands import *
from discord.utils import get

class Bots(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color = 0x646ecb
		self.prefixes = ["a?", "j!", "++", "-", "--", "dl.", "dl!", "s.", "sc.", "so.", ">", "@", "s!", "i/", "a.", "e!", "$"]

	@cooldown(2, 86400, BucketType.user)
	@guild_only()
	@command(aliases=["adicionar", "add", "botadd"])
	async def addbot(self, ctx):

		await ctx.send(embed=discord.Embed(color=self.color, description="Enviei uma mensagem no seu DM! Caso não tenha recebido, habilite as mensagens de membros do servidor!", timestamp=ctx.message.created_at))
		await ctx.author.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="Olá %s. Por favor, informe o **ID** do seu Bot." % ctx.author.mention))
		_id = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)
		await ctx.author.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="Okay! Agora me informe o prefixo!"))
		prefixo = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)

		if prefixo.content in self.prefixes:
			return await ctx.author.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="Opss... Aparentemente já existe um **bot** com esse mesmo prefixo! Certifique-se de que seu bot possui um **setprefix** e escolha um prefixo não usado.\n``Prefixos:`` %s" % ', '.join(self.prefixes)))
		else:
			await ctx.author.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="Certo! Seu pedido foi realizado, em breve daremos uma resposta.\nAtenciosamente, DevLabs!"))
			convite = "https://discord.com/oauth2/authorize?client_id=%s&scope=bot&permissions=3492929" % _id.content
			emb = discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="Pedido solicitado por: %s\n" % (ctx.author.mention))
			emb.add_field(name="ID:", value="%s" % _id.content)
			emb.add_field(name="Prefixo:", value="%s" % prefixo.content, inline=True)
			emb.add_field(name="Convite:", value="%s" % convite, inline=False)
			return await self.bot.get_channel(730556662993387580).send(embed=emb)

	@guild_only()
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=["aceitar", "botadc", "aceitarbot", "botaceitar"])
	async def acbot(self, ctx, member: discord.Member=None):
		if member == None:
			return await ctx.send(embed=discord.Embed(color=self.color, description="%s, mencione o dono do **bot** nos argumentos!" % ctx.author.mention))
		await ctx.send(embed=discord.Embed(color=self.color, description="Certo! A mensagem foi enviada para o usuário."))
		emb = discord.Embed(color=self.color, title="Olá, %s!" % member.name, description="O seu bot foi adicionado no servidor com sucesso! Por favor, leia as regras que se encontra no canal <#732709606119178391> para evitar problemas com seu bot!\n\nAtenciosamente, DevLabs.")
		emb.set_thumbnail(url=str(member.avatar_url))
		emb.set_footer(text="©️ DevLabs")
		return await member.send(embed=emb)

	@guild_only()
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=["rejeitar", "botrjt", "rejeitarbot", "botrejeitar"])
	async def rjbot(self, ctx, member: discord.Member=None, *, reason=None):
		if member == None:
			return await ctx.send(embed=discord.Embed(color=self.color, description="%s, mencione o dono do **bot** nos argumentos!" % ctx.author.mention))
		elif reason == None:
			reason = "Não citado pelo administrador."
		await ctx.send(embed=discord.Embed(color=self.color, description="Certo! A mensagem foi enviada para o usuário."))
		emb = discord.Embed(color=self.color, title="Olá, %s!" % member.name, description="Infelizmente o seu bot não foi aprovado para ser adicionado em nosso servidor.\n**Motivo**: %s\n\nAtenciosamente, DevLabs." % reason)
		emb.set_thumbnail(url=str(member.avatar_url))
		emb.set_footer(text="©️ DevLabs")
		return await member.send(embed=emb)

def setup(bot):
	bot.add_cog(Bots(bot))