import discord
import re

from datetime import datetime
from discord.ext.commands import *
from random import randint
from time import sleep
from discord.utils import get

class Logs(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color = 0x646ecb

	@Cog.listener()
	async def on_message_delete(self, message):
		if not message.author.bot:		
			emb = discord.Embed(color=self.color, timestamp=message.created_at, title="Mensagem Apagada!", description="Uma mensagem foi apagada por %s. Veja abaixo mais detalhes:" % message.author.mention)
			emb.add_field(name="Canal:", value="%s" % message.channel.name)
			emb.add_field(name="Horário:", value="%s" % message.created_at.strftime("%H:%M:%S"), inline=False)
			emb.add_field(name="Mensagem:", value="%s" % message.content, inline=True)
			emb.add_field(name="Link:", value="%s" % message.jump_url, inline=False)

			return await self.bot.get_channel(743687007406129223).send(embed=emb)

	@Cog.listener()
	async def on_message_edit(self, before, after):
		if not before.author.bot:
			emb = discord.Embed(color=self.color, timestamp=before.created_at, title="Mensagem Editada!", description="Uma mensagem foi editada por %s. Veja abaixo mais detalhes:" % before.author.mention)
			emb.add_field(name="Canal:", value="%s" % before.channel.name)
			emb.add_field(name="Horário:", value="%s" % before.created_at.strftime("%H:%M:%S"), inline=False)
			emb.add_field(name="Mensagem(Antes):", value="%s" % before.content, inline=True)
			emb.add_field(name="Mensagem(Depois):", value="%s" % after.content, inline=True)
			emb.add_field(name="Link:", value="%s" % before.jump_url, inline=False)
			try:
				return await self.bot.get_channel(729163031430561793).send(embed=emb)
			except:
				return

def setup(bot):
	bot.add_cog(Logs(bot))