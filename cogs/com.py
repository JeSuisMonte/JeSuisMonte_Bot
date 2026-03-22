import discord
from discord.ext import commands
from discord import app_commands
import os
import re

class com(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Guides Principaux : `!guide` `!leaps` `!controller` `!ravi` `!diva` `!transcend` `!ass` \n\nUtilitaire : `!help` `/ferias` `/skill` `/monster-info` `!roadshop` `!poogie` `!hp` `!elements` `!mymissions` `!caravan` `!towersim` `!ravigem` `!ms` `!invite`\n\nFun : `!jsmt` `!bann` `!korinyi` `!hb2025`")

    @commands.command()
    async def guide(self, ctx):
        embed = discord.Embed(
            title=f"Guides",
            description=f"### [Guide de Leaps](<https://docs.google.com/document/d/1RQVOQ972N0vQrda9iZ-arEygWzxjAyWC6rBgbzYcBCM/edit?usp=sharing>)\nMust à lire lorsque vous débutez Monster Hunter Frontier !\n"
                        f"### [Guide d'Introduction au HR5](<https://docs.google.com/document/d/17oYptlMWyc54jsivwzAHaxz1o5SnG34LtRyGEeb5fU8/edit?usp=sharing>)\nContient des informations utiles lorsque vous arrivez au HR5.\n"
                        f"### [Guide Contrôles de Manettes](<https://docs.google.com/document/d/11MHCoxtoiIaDi6JuXivnIieHRnjEqxmv8XuPbzDfRoQ/edit?usp=sharing>)\nGuide complet sur la configuration des manettes XBOX 360, XBOX One, PS4, PS5 et Switch Pro.\n"
                        f"### [Guide Raid Ravi](<https://docs.google.com/document/d/1xncvMF3V4uhl0EO7m2rQsXcXlBNgLpLnZlGgvoMMngA/edit?usp=sharing>)\nGuide complet sur les Raid Ravi organisés sur Rain.\nImpératif à lire avant de participer à votre premier Raid Ravi !\n"
                        f"### [Guide Transcendance](<https://docs.google.com/document/d/1X50OzRDhaS4Xvuvbwlkph_ruxhV_AvLBYUM3R2XHc6E/edit?usp=sharing>)\nGuide complet englobant tout ce qu'il y a à savoir sur la Transcendance.\n"
                        f"### [Guide Quêtes de la Diva](<https://docs.google.com/spreadsheets/d/1vu_qmEdAGHOcD4MduFq5q6RsTAkUfBDZMk_5nZjxLt4/edit?usp=sharing>)\nGuide complet expliquant chaque étape de la série de quête de la Diva.\n"
                        f"### [Guide pour utiliser l'Armor Set Searcher](<https://docs.google.com/document/d/1rGFjKraGMhIltTDz4IUK_pJUieQ7_JYeCtgqFYBYOQQ/edit?usp=sharing>)\nGuide expliquant l'utilisation de l'outil Armor Set Searcher.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def leaps(self, ctx):
        await ctx.send("Guide de Leaps : https://docs.google.com/document/d/1RQVOQ972N0vQrda9iZ-arEygWzxjAyWC6rBgbzYcBCM/edit?usp=sharing")

    @commands.command()
    async def diva(self, ctx):
        await ctx.send("Guide des quêtes de la Diva : https://docs.google.com/spreadsheets/d/1vu_qmEdAGHOcD4MduFq5q6RsTAkUfBDZMk_5nZjxLt4/edit?usp=sharing")

    @commands.command()
    async def controller(self, ctx):
        await ctx.send("Guide pour configurer votre manette sur Frontier : https://docs.google.com/document/d/11MHCoxtoiIaDi6JuXivnIieHRnjEqxmv8XuPbzDfRoQ/edit?usp=sharing")

    @commands.command()
    async def ravi(self, ctx):
        await ctx.send("Guide complet concernant les Raids Raviente de Rain : https://docs.google.com/document/d/1xncvMF3V4uhl0EO7m2rQsXcXlBNgLpLnZlGgvoMMngA/edit?usp=sharing")

    @commands.command()
    async def ass(self, ctx):
        await ctx.send("Guide sur l'Armor Set Searcher : https://docs.google.com/document/d/1rGFjKraGMhIltTDz4IUK_pJUieQ7_JYeCtgqFYBYOQQ/edit?usp=sharing")

    @commands.command()
    async def ravigem(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/1271081376283889735/1271592997066117130/Untitled-2_copy.png?ex=69b88143&is=69b72fc3&hm=ea58d3e94837b06763563079127e6180c37330fcbd68c11db46aabbd87a78f23&=&format=webp&quality=lossless')

    @commands.command()
    async def transcend(self, ctx):
        await ctx.send("Guide sur la Transcendance : https://docs.google.com/document/d/1X50OzRDhaS4Xvuvbwlkph_ruxhV_AvLBYUM3R2XHc6E/edit?usp=sharing")

    @commands.command()
    async def roadshop(self, ctx):
        with open ("img/com/dpg.webp", "rb") as f:
            picture = discord.File(f)
            await ctx.send("## Prérequis du Roadshop\nVoici les prérequis afin de débloquer la majorité des objets du Roadshop.\n(*À noter que certains objets ont leurs propres prérequis.*)\n> Étage de Road = 20   |   Fatalis = 10 (Festi Gem, Festi Tkt)\n> Étage de Road = 45   |   Fatalis = 5 (Wht Fatalis Decos)\n> Étage de Road = 45   |   Fatalis = 5 (Tech/Hiden Cuffs and Decos)\n> Étage de Road = 45   |   Fatalis = 20 (Entrusted Secret Text)\n> Étage de Road = 50   |   Fatalis = 30 (Matériaux Musou)\n> Étage de Road = 50   |   Fatalis = 30 (10th Armor Voucher)\n> Étage de Road = 60   |   Fatalis = 10 (Superior Tkt)\n> Étage de Road = 62   |   Fatalis = 5 (PZ Cuffs)\n> Étage de Road  = 80  |   Fatalis = 30 (Premium ZP Armor tkt)\n> Étage de Road = 80   |   Fatalis = 30 (Ravi Deco)\n*Les matériaux Musou ne sont pas tous disponible en même temps, ils sont répartit sur deux listes alternant chaque semaine.\nLa rotation actuelle est indiquée ici : https://discord.com/channels/937230168223789066/1036849967895150602/1397759724681695334", file=picture)

    @commands.command()
    async def bann(self, ctx):
        with open("img/com/bann.webp", "rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    @commands.command()
    async def hb2025(self, ctx):
        with open("img/com/hb2025.png", "rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
            
    @commands.command()
    async def ms(self, ctx):
        with open("img/com/ms.webp", "rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    @commands.command()
    async def jsmt(self, ctx):
        with open("img/com/jsmt.gif", "rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    @commands.command()
    async def poogie(self, ctx):
        with open ("img/com/poogie.webp", "rb") as f:
            picture = discord.File(f)
            await ctx.send("## Poogies de Guilde\n\nLes différents poogies présent dans le clan hall donnent différent buffs en fonction de leurs costumes.\nPour cela, il vous faudra les nourrir de poogie cracker, achetables dans le clan shop.\nCes buff durent jusqu'à ce que vous vous déconnectez (*idem si votre jeu crash*).\nVoici les costumes les plus importants ainsi que leurs effets.\n\nVous pouvez consulter les autres costumes ainsi que les matériaux requis sur le [Site de la Wycademy.](<https://wycademy.vercel.app/hunter-notes/locations/guild-hall?embed=guild-poogie-skills#guild-poogie-skills>)", file=picture)

    @commands.command()
    async def hp(self, ctx):
        with open("img/com/hp.webp", "rb") as f:
            picture = discord.File(f)
            await ctx.send("https://docs.google.com/spreadsheets/d/1U0A5oTth1aNYIu_5tlawzLBAC4447KGthpl5uMmyQm0/edit#gid=0", file=picture)

    @commands.command()
    async def korinyi(self, ctx):
        with open("img/com/korinyi.webp", "rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    @commands.command()
    async def gem(self, ctx):
        with open("img/caravan/gem.png", "rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    @commands.command()
    async def towersim(self, ctx):
        await ctx.send("[Simulateur d'arme Tower](https://wycademy.vercel.app/tools/simulator/tower-weapon)")

    @commands.command()
    async def elements(self, ctx):
        with open("img/com/elements.webp", "rb") as f:
            picture = discord.File(f)
            await ctx.send("[Plus d'informations sur les éléments hybride](<https://wycademy.vercel.app/hunter-notes/getting-started/elements>)", file=picture)

    @commands.command()
    async def mymissions(self, ctx):
        with open("img/com/mymissions.webp", "rb") as f:
            picture = discord.File(f)
            await ctx.send("## MY MISSIONS\nAfin d'augmenter rapidement le niveau de vos My Missions, vous pouvez utiliser des `My Mission Tkt`,"
            "achetable dans la road ou en effectuant la Bounty https://discord.com/channels/937230168223789066/1470332587741282358.\n"
            "Il vous faut un total de 1395 My Mission Tkts pour atteindre le niveau max, il vous faudra donc faire la Free BBQ09 **9 fois**.\n"
            "Si vous décidez tout de même de les augmenter à la main, les quêtes se trouvent dans la catégorie `My Missions Quest`.\n"
            "[Voir ici pour plus d'informations sur les SR Stats.](<https://wycademy.vercel.app/hunter-notes/getting-started/style-rank?embed=style-rank-stats#style-rank-stats)>", file=picture)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("https://discord.gg/kk6PKPtKA9")

async def setup(bot):
    await bot.add_cog(com(bot))