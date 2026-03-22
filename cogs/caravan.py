import discord
from discord.ext import commands
from discord import app_commands
import time
import os
import json
import re

class caravan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class CaravanView(discord.ui.View):
        def __init__(self):
            # Durée avant expiration (en secondes)
            self.timeout_duration = 1800 
            super().__init__(timeout=self.timeout_duration)
            
            self.current_page = 1
            self.total_pages = 7
            
            # Calcul du moment de l'expiration pour le compte à rebours
            self.expire_at = int(time.time() + self.timeout_duration)
            self.message = None

        def get_file_and_embed(self):
            """Génère l'objet File et l'Embed mis à jour pour la page actuelle."""
            file_path = f"img/caravan/caravan{self.current_page}.png"
            filename = f"caravan{self.current_page}.png"
            
            file = discord.File(file_path, filename=filename)
            
            # Texte de description (inchangé)
            desc = (
                "Les talents Caravane (*Caravan Skills*) sont des talents additionnels obtenables en améliorant votre Gemme Caravane.\n"
                "Ces talents sont similaires à ceux des repas dans la franchise principale.\n\n"
                "Il existe deux types de talent de Caravane : **Passif et Actif**\n\n"
                "**Talent Passif** : Ces talents sont toujours actifs.\n"
                "Par exemple, le talent Negotiation offre 1 chance sur 8 d'obtenir une réduction de 25% sur tout ce qui a un prix en Zenny ou en GZenny.\n\n"
                "**Talent Actif** : Ces talents sont sélectionnables et ont chacun un prix.\n"
                "Vous possédez un total de 10 points dépensables en talents de Caravane.\n\n"
                "**Conseils**\n"
                "- Bonus Art est avantageux contre le Raviente ou le Duremudira.\n"
                "- KO Technique et Weapon Art Large sont bien pour le marteau et les tonfas.\n"
                "- Shooting Rampage : Applique un buff basé sur les dégâts brut de votre arme. Le multiplicateur de dégât de ce talent compte les talents comme Adrenaline ou Combat Supremacy.\n"
                "- Goddess of Luck (Sm) : À chaque coup encaissé, donne une chance sur dix de ne pas subir de dégâts. S'additionne à Divine Protection, le chant de la Diva ainsi qu'aux Maiden's Wish."
            )

            embed = discord.Embed(
                title="Talents Caravane", 
                color=discord.Color.blue(),
                description=desc
            )
            embed.set_image(url=f"attachment://{filename}")
            
            # Footer avec Page + Compte à rebours dynamique
            embed.set_footer(text=f"Page {self.current_page} / {self.total_pages}")
            embed.description += f"\n\n⌛ **Ce menu expire <t:{self.expire_at}:R>**"
            
            return file, embed

        async def update_view(self, interaction: discord.Interaction):
            """Met à jour le message avec la nouvelle image et l'embed."""
            file, embed = self.get_file_and_embed()
            await interaction.response.edit_message(attachments=[file], embed=embed, view=self)

        @discord.ui.button(label="◀️", style=discord.ButtonStyle.gray)
        async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.current_page = self.total_pages if self.current_page == 1 else self.current_page - 1
            await self.update_view(interaction)

        @discord.ui.button(label="▶️", style=discord.ButtonStyle.gray)
        async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.current_page = 1 if self.current_page == self.total_pages else self.current_page + 1
            await self.update_view(interaction)

        async def on_timeout(self):
            """Désactive les boutons et modifie l'embed quand le temps est écoulé."""
            for item in self.children:
                item.disabled = True
            
            try:
                if self.message:
                    # On récupère le premier embed de la liste
                    edit_embed = self.message.embeds
                    edit_embed.description = edit_embed.description.replace("⌛ **Ce menu expire", "❌ **Menu expiré")
                    await self.message.edit(view=self, embed=edit_embed)
            except Exception:
                pass

    @commands.command()
    async def caravan(self, ctx):
        # Suppression du message de commande de l'utilisateur
        try: 
            await ctx.message.delete()
        except: 
            pass

        # Comme CaravanView est nichée, on l'appelle via self
        view = self.CaravanView()
        file, embed = view.get_file_and_embed()
        view.message = await ctx.send(file=file, embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(caravan(bot))