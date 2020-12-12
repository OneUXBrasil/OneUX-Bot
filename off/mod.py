import discord
import re

from datetime import datetime
from discord.ext.commands import *
from random import randint
from time import sleep
from discord.utils import get
	
async def user_none_message(ctx, user=None):
	return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0x646ecb, description="%s, mencione o usuário que deseja punir." %(ctx.author.mention)))

async def blacklist_user(ctx, bot, user=None, type_=None, reason=None):
	channel = bot.get_channel(728371478256418917)
	if reason == None:
		reason = "não citado pelo administrador."
	emb = discord.Embed(color=0xf70010, description="Usuário %s Punido." % user.mention, timestamp=ctx.message.created_at)
	emb.add_field(name="ID:", value=user.id)
	emb.add_field(name="Punição:", value=type_, inline=False)
	emb.add_field(name="Motivo:", value=reason, inline=True)
	emb.set_thumbnail(url=str(user.avatar_url))
	await channel.send(embed=emb)

class Moderation(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color = 0x646ecb

	@Cog.listener()
	async def on_message(self, message):

		invites = ["DISCORD.GG/", "DISCORD.ME/", "DISCORD.CHAT/", "TOP.GG/SERVERS/"]

		for item in invites:
			if item.lower() in message.content.lower():

				if message.author.id == 296428519947370499: 
					pass
				elif message.author.id == 617916467588890625: 
					pass
				else:
					await message.delete()			
					await message.channel.send(embed=discord.Embed(color=self.color, description=
					"%s, você não pode enviar convites de outros servidores!\n"% (message.author.mention)))

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@has_permissions(kick_members=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=["kickar", "kicks", "k"])
	async def kick(self, ctx, member: discord.Member=None, *, reason=None):
		if member == None:
			return await user_none_message(ctx, user=member)
		else:
			await member.kick()
			await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=self.color, description=f"**O(a) Usuário(a) {member.mention} foi kickado(a) com sucesso!**"))
			await blacklist_user(ctx, self.bot, user=user, type_="expulso", reason=reason)

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@has_permissions(ban_members=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=["banir", "banirs", "b"])
	async def ban(self, ctx, member: discord.Member=None, *, reason:str=None):

		if member == None:
			return await user_none_message(ctx, user=member)
		elif reason == None:
			reason = "Sem motivos citado."
		else:
			await member.ban(reason=reason)
			await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,color=self.color,description="Usuário banido com sucesso!"))
			await blacklist_user(ctx, self.bot, user=user, type_="banido", reason=reason)

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@has_permissions(ban_members=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=["desbanir"])
	async def unban(self, ctx, *, member: discord.Member=None):
		if member == None:
			return await user_none_message(ctx, user=member)
		await ctx.guild.unban(await self.bot.fetch_user(member.id))
		return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=self.color, description="Usuário desbanido com sucesso."))

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@has_permissions(manage_messages=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=["purge", "clear", "clean", "a", "limpar"])
	async def apagar(self, ctx, *, limit:int=None):
		if limit == None:
			return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at), color=self.color, description="%s, mencione quantas mensagens serão apagadas." % ctx.author.mention)
		await ctx.message.delete()
		apg = await ctx.channel.purge(limit=limit)
		await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,color=self.color,description=f"{len(apg)} mensagem(ns) foram apagadas em: {ctx.channel.mention}!"))

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@has_permissions(ban_members=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=["s"])
	async def softban(self, ctx, member: discord.Member=None, *, reason=None):
		if member == None:
			return await user_none_message(ctx, user=member)
		user = await self.bot.fetch_user(member.id)
		await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,color=self.color,description="O usuário sofreu um softban com sucesso!"))
		await member.ban(delete_message_days=7)
		await ctx.guild.unban(user)
		await blacklist_user(ctx, self.bot, user=user, type_="softban", reason=reason)

	@cooldown(2, 10, BucketType.user)
	@guild_only() 
	@has_permissions(manage_roles=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=['mutar'])
	async def mute(self, ctx, user: discord.Member=None, *, msg=None):
		if user == None:
			return await user_none_message(ctx, user=user)
		await ctx.message.delete()
		await user.add_roles(ctx.guild.get_role(717845138411618405))
		await blacklist_user(ctx, self.bot, user=user, type_="mutado", reason=msg)
		await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=self.color, description=f"O usuário {user.mention} foi mutado."), delete_after=10)

	@cooldown(2, 10, BucketType.user)
	@guild_only() 
	@has_permissions(manage_roles=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(name='unmute', aliases=['desmutar', 'unmutar', 'unmuta'])
	async def unmute(self, ctx, *, user: discord.Member=None, msg=None):
		if user == None:
			return await user_none_message(ctx, user=user)
		await ctx.message.delete()		
		await user.remove_roles(ctx.guild.get_role(717845138411618405))
		await ctx.send(embed=discord.Embed(color=user.color,description=f"O usuário {user.mention} foi desmutado."), delete_after=10)

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@has_permissions(manage_guild=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=['tempomutar', 'mutartempo'])
	async def tempmute(self, ctx, user: discord.Member=None, temp:int=None, *, msg=None):
		if user == None:
			return await user_none_message(ctx, user=user)
		await ctx.message.delete()
		await ctx.send(embed=discord.Embed(color=ctx.author.colour,timestamp=ctx.message.created_at,description=f"O usuário {user.mention} foi mutado por ``{temp}``s."), delete_after=11)
		await blacklist_user(ctx, self.bot, user=user, type_="mutado por %ss"%(temp), reason=msg)
		await user.add_roles(ctx.guild.get_role(717845138411618405))
		sleep(temp)
		await user.remove_roles(ctx.guild.get_role(717845138411618405))

	async def warn_command_sender(self, ctx, member, reason, for_="member"):
		timestamp = datetime.now()
		emb = discord.Embed(color=self.color, timestamp=ctx.message.created_at, title=
			"Olá, %s.\n" % member.name, description="Venho alertar que você recebeu um **aviso** de um administrador. Com 3 avisos recebidos você será **banido**!")
		emb.add_field(name="Motivo:", value="%s" % reason)
		emb.add_field(name="Administrador:", value="%s" % ctx.author.mention, inline=False)
		emb.add_field(name="Data:", value="%s" % timestamp.strftime("%d/%m/%Y - %H:%M:%S"), inline=False)
		emb.set_footer(text="Atenciosamente, Devlabs.", icon_url=ctx.me.avatar_url)
		emb.set_thumbnail(url=str(member.avatar_url))
		if for_ == "member":
			return await member.send(embed=emb)
		return await ctx.send(embed=emb, content="%s" % member.mention)

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@has_permissions(kick_members=True)
	@has_any_role("🧪:: DevLabs", "Administradores", "Equipe de Moderação")
	@command(aliases=['w', 'aviso', 'avisar', "avisa"])
	async def warn(self, ctx, member: discord.Member=None, *, reason=None):

		if member == None:
			return await user_none_message(ctx, user=member)
		else:
			await ctx.message.delete()
			try:
				await self.warn_command_sender(ctx, member=member, reason=reason, for_="member")
			except Exception as error:
				return await self.warn_command_sender(ctx, member=member, reason=reason, for_="ctx")

def setup(bot):
	bot.add_cog(Moderation(bot))