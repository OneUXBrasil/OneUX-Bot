import discord
from discord.ext.commands import *
from random import randint
from requests import get
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class SearchJob(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color = 0x646ecb

	@cooldown(1, 60, BucketType.user)
	@guild_only()
	@command(aliases=["job", "sjob"])
	async def searchjob(self, ctx, *, job:str=None):
		if job == None: 
			return await ctx.send(embed=discord.Embed(color=randint(0, 0xFFFFFF), description="Por favor, não deixe em branco o campo ``job``."))
		url = "https://www.manager.com.br/empregos-%s" % job.strip().lower()
		soup = BeautifulSoup(get(url, headers={"User-Agent": UserAgent().chrome}).text, "html.parser")
		embed = discord.Embed(color=self.color, timestamp=ctx.message.created_at, url=url, title="Mais informações clique aqui.")
		embed.set_footer(text="Empregos de %s" % job.strip().title())

		for a in soup.findAll("div", attrs={"class": "lista-resultado-busca"}):
			embed.description = str(a.find("article", attrs={"class": "vaga hlisting"}).text)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(SearchJob(bot))