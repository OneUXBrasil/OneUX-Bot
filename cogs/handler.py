import discord

from discord.ext.commands import (
	Cog,
	CommandOnCooldown,
	MissingPermissions,
	CommandInvokeError,
	CommandNotFound, 
	MissingAnyRole,
	BadArgument,
	NotOwner)
from math import ceil

class Handler(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color = 0x7A4EF9

	@Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, CommandOnCooldown):
			return await ctx.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="%s, por favor espere %ss para executar novamente o comando!"%(ctx.author.mention, ceil(error.retry_after))))
		if isinstance(error, (MissingPermissions, MissingAnyRole)):
			return await ctx.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="%s, você não tem permissão para executar esse comando!" %(ctx.author.mention)))
		if isinstance(error, CommandInvokeError):
			return await ctx.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="%s, comando usada de forma errada, ou ocorreu um erro inesperado." %(ctx.author.mention)))
		if isinstance(error, CommandNotFound):
			return await ctx.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="%s, não encontrei o comando ``%s``" %(ctx.author.mention, str(error).split(' ')[1])))
		#if isinstance(error, BadArgument):
		#	return await ctx.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="%s, esse usuário não existe. Verifique o nome dele e tente novamente." % ctx.author.mention))
		if isinstance(error, NotOwner):
			return await ctx.send(embed=discord.Embed(color=self.color, timestamp=ctx.message.created_at, description="%s, somente o <@296428519947370499> pode executar esse comando." % ctx.author.mention))

def setup(bot):
	bot.add_cog(Handler(bot))	