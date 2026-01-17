import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json

# 1. Configuration et Chargement
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
ID_CHANNEL = 1461789288201982168

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def load_all_data():
    with open('recipes.json', 'r', encoding='utf-8') as f1:
        recipes = json.load(f1)
    with open('ingre.json', 'r', encoding='utf-8') as f2:
        ingredients = json.load(f2)
    return recipes, ingredients

recipes_data, ingre_data = load_all_data()

# 2. Classes pour l'interface

class TalentView(discord.ui.View):
    def __init__(self, talents):
        super().__init__(timeout=180)
        self.talents = talents
        self.current_page = 0
        self.per_page = 5 
        self.total_pages = (len(self.talents) - 1) // self.per_page + 1

    def create_embed(self):
        start = self.current_page * self.per_page
        end = start + self.per_page
        chunk = self.talents[start:end]

        embed = discord.Embed(
            title=f"📖 Guide des Talents ({self.current_page + 1}/{self.total_pages})",
            color=discord.Color.gold()
        )
        for name, value in chunk:
            embed.add_field(name=name, value=value, inline=False)
        return embed

    @discord.ui.button(label="⬅️ Précédent", style=discord.ButtonStyle.grey)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Si on recule alors qu'on est à la page 0 (index 0), on va à la dernière page
        if self.current_page == 0:
            self.current_page = self.total_pages - 1
        else:
            self.current_page -= 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Suivant ➡️", style=discord.ButtonStyle.grey)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Si on avance alors qu'on est sur la dernière page, on revient à 0
        if self.current_page >= self.total_pages - 1:
            self.current_page = 0
        else:
            self.current_page += 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

class TalentInfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="ℹ️ Info Talents", style=discord.ButtonStyle.secondary, row=4)

    async def callback(self, interaction: discord.Interaction):
        # Fusion des deux listes pour le système de pages
        all_talents = [
            ("Buchigiri", "Donne True Guts et Adrenaline+2."),
            ("Unaffected+3", "Donne les effets de High-Grade Earplugs, Dragon Wind Breaker et Quake Res+1."),
            ("Dragon Wind Breaker", "Garantie une protection contre le Vent Draconique (Dragon Wind)."),
            ("Super HG Earplugs", "Garantie une protection contre les cris de Tier 3."),
            ("Stun Negated", "Immunisé contre les stuns."),
            ("Great Luck", "Augmente les récompenses standardes de quête de 29/32."),
            ("Caring+3", "Les attaques des joueurs et PNJ ne vous affectent pas. \nVos attaques ne les affectent pas non plus."),
            ("Adrenaline+2", "Multiplie votre attaque de 1.5 (1.3 Bowgun) quand vos HP sont inférieur à 40.\nL'augmentation de votre défense est fixée à 90."),
            ("Peerless", "La consommation de stamina est divisée par deux (15 > 8 unités).\nLa consommation de stamina durant une esquive ou une garde est réduite de 50%."),
            ("Goddess' Embrace", "Garanti une chance sur quatre de ne recevoir aucun dégât d'une attaque."),
            ("Hunger Negated", "La longueur de votre jauge de stamina ne diminue plus."),
            ("Wide-Area+3", "En plus des items concernés par Wide-Area+2, les items suivant affectent vos alliés présent dans la même zone que vous : Mega Potions, Blight Cure Fruits, Zenith Espinas Antitoxin, Crimson Raviente Blood."),
            ("Wide-Area+2", "Les items suivant affectent vos alliés présent dans la même zone que vous :\n*Herbs, Potions, Antidotes, Cool Drinks, Hot Drinks, Armor Seed, Power Seed.*"),
            ("Hasard Res (Large)", "Réduit la diminution de vie infligée par la lave, ainsi qu'1/3 de la vitesse de la réduction de vie causée par la chaleur."),
            ("Divine Whim", "Immunisé contre les stuns."),
            ("Paralysis Negated", "Immunisé face à la paralysie."),
            ("Sleep Negated", "Immunisé face au sommeil."),
            ("Poison Negated", "Immunisé face au poison."),
            ("All Res+20", "+20 de chaque résistance élémentaire."),
            ("Fire Res+30", "+30 de résistance au Feu."),
            ("Water Res+30", "+30 de résistance à l'Eau."),
            ("Ice Res+30", "+30 de résistance à la Glace. "),
            ("Thunder Res+30", "+30 de résistance à la Foudre."),
            ("Dragon Res+30", "+30 de résistance à l'élément Dragon."),
            ("Medical Sage", "Les objets de soin soignent instantanément les points de vie rouge.\nEffet Supplémentaire en fonction du nombre de joueur possédant ce talent :\n - 2 : Les objets de soin affectent tous le monde.\n- 3 : +20 points de vie supplémentaire.\n- 4 : +50 points de vie supplémentaire.\nLe talent Recovery s'additionne à Medical Sage (**concerne uniquement les objets de soin**, *ex : Max Potion = Oui, Ancient Potion = Non*) "),
            ("Encourage+2", "Donne l'effet de Horn Maestro, ainsi qu'Evasion+2 et Stun Halved pour toute l'équipe.\n(Horn Maestro : -50% de chance que les cornes se brisent. La durée des effets des cornes est multipliée par 1,5, concerne aussi les HH)."),
            ("Assistance", "Le bras du joueur brille en rouge, +20 d'attaque et +50 de défense en plus de donner les effets de Damage Recovery Speed+2, Status Immunity et Peerless aux joueurs proches.\nLa zone effective est de 3 roulades (ou 2 avec Evade Distance Up).\nLes bras des joueurs affectés brilleront en jaune.\nLe joueur possédant le talent gagne +20 d'attaque et +50 de défense mais ne bénéficie pas de Peerless, Status Immunity ou Damage Recovery Speed.\nLes talents d'Assistance écraseront leurs versions inférieures si d'autres joueurs affectées les possèdent.\n(Status Halved -> Remplacé par Status Immunity. Immunity Myriad -> Conservé car supérieur à Status Immunity)."),
            ("Red Soul", "+15 d'attaque.\nAttaquer un autre joueur lui donne +30 d'attaque.\nAttaquer un joueur possédant Blue Soul lui donne +100 de défense ainsi que l'effet du talent Goddess' Embrace pendant 2 minutes. +30 d'attaque si attaqué par un joueur possédant Blue Soul,\nvous pourrez aussi stun un monstre avec n'importe quelle arme en frappant la tête, **dure 2 minutes**.\nL'attaque supplémentaire est une stat additionnelle **ignorant** les multiplicateurs des autres talents des joueurs concernés."),
            ("Blue Soul", "+50 de défense.\nAttaquer un autre joueur donne +100 de défense.\nAttaquer un joueur possdéant Blue Soul alors qu'il est touché par une affliction ou un effet de status les annuleront.\nÊtre attaqué par un joueur possédant Red Soul donne +100 de défense et active l'effet du talent Goddess' Embrace, **dure 2 minutes**."),
            ("Incitement", "Attaquer un monstre forcera son attention sur vous en plus de donner +40 d'attaque, les dégâts reçu par ce monstre seront réduit durant cette période.\nL'icone de yeux jaunes indique que vous êtes reprérés, les yeux rouge signifient que l'effet du talent est actif.\nSe tenir trop longtemps éloigné de la portée du monstre annule prématurément l'effet du talent.\nIncitement se recharge au bout de **30 secondes**.")
        ]
        
        view = TalentView(all_talents)
        await interaction.response.send_message(embed=view.create_embed(), view=view, ephemeral=True)

class RecipeButton(discord.ui.Button):
    def __init__(self, recipe_key, label, style):
        super().__init__(label=label, style=style)
        self.recipe_key = recipe_key

    async def callback(self, interaction: discord.Interaction):
        current_recipes, current_ingre = load_all_data()
        recipe = current_recipes["recipes"][self.recipe_key]
        colors = current_ingre["ingredients_colors"]

        def format_line(text):
            if not text: return "> Aucun"
            items = [i.strip() for i in text.split(",")]
            formatted_items = []
            for it in items:
                ingre_info = colors.get(it)
                emoji = ingre_info.get("color", ":white_circle:") if ingre_info else ":white_circle:"
                url = ingre_info.get("url", "") if ingre_info else ""
                link = f"[{it}]({url})" if url else it
                formatted_items.append(f"> {emoji} {link}")
            return "\n".join(formatted_items)
        
        embed = discord.Embed(
            title=f"📜 {recipe['name']}",
            description=f"**Type:** {self.recipe_key}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Base", value=format_line(recipe['base_ingre']), inline=False)
        embed.add_field(name="Ingrédients 2", value=format_line(recipe['ingre2']), inline=False)
        embed.add_field(name="Ingrédients 3", value=format_line(recipe['ingre3']), inline=False)
        embed.add_field(name="Ingrédients 4", value=format_line(recipe['ingre4']), inline=False)
        
        results = (f"Great Success : {recipe['great_success']}\nSucces : {recipe['success']}\n"
                   f"Failure : {recipe['failure']}\nGreat Failure : {recipe['great_failure']}")
        embed.add_field(name="Résultats", value=results, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

class RecipePanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.display_mode = "talent" 
        self.current_page = 0
        self.items_per_page = 20 
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        
        recipe_keys = list(recipes_data["recipes"].keys())
        total_pages = (len(recipe_keys) - 1) // self.items_per_page + 1
        
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        current_keys = recipe_keys[start:end]

        color_map = {
            "red": discord.ButtonStyle.danger,
            "green": discord.ButtonStyle.success,
            "blue": discord.ButtonStyle.primary,
            "grey": discord.ButtonStyle.secondary
        }

        for key in current_keys:
            recipe = recipes_data["recipes"][key]
            if self.display_mode == "talent":
                gs = recipe.get("great_success") or "Inconnu"
                s = recipe.get("success") or ""
                show_mode = str(recipe.get("showtalents", "1"))
                label = f"{gs} | {s}" if (show_mode == "2" and s.strip()) else gs
            else:
                label = recipe.get("name") or "Nom inconnu"
            
            label = (label[:77] + "...") if len(label) > 80 else label
            style = color_map.get(recipe.get("color", "blue"), discord.ButtonStyle.primary)
            self.add_item(RecipeButton(key, label, style))

        # Navigation & Contrôles sur la ligne 4
        if total_pages > 1:
            prev_btn = discord.ui.Button(label="⬅️", style=discord.ButtonStyle.grey, disabled=(self.current_page == 0), row=4)
            prev_btn.callback = self.prev_page
            self.add_item(prev_btn)

            page_display = discord.ui.Button(label=f"P. {self.current_page + 1}/{total_pages}", style=discord.ButtonStyle.grey, disabled=True, row=4)
            self.add_item(page_display)

            next_btn = discord.ui.Button(label="➡️", style=discord.ButtonStyle.grey, disabled=(self.current_page == total_pages - 1), row=4)
            next_btn.callback = self.next_page
            self.add_item(next_btn)

        btn_text = "🔄 REPAS" if self.display_mode == "talent" else "🔄 TALENTS"
        btn_style = discord.ButtonStyle.success if self.display_mode == "talent" else discord.ButtonStyle.danger
        
        switch_btn = discord.ui.Button(label=btn_text, style=btn_style, row=4)
        switch_btn.callback = self.switch_callback
        self.add_item(switch_btn)

        # Ajout du bouton Info Talents tout à droite
        self.add_item(TalentInfoButton())

    async def prev_page(self, interaction: discord.Interaction):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(view=self)

    async def next_page(self, interaction: discord.Interaction):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(view=self)

    async def switch_callback(self, interaction: discord.Interaction):
        self.display_mode = "name" if self.display_mode == "talent" else "talent"
        self.update_buttons()
        await interaction.response.edit_message(view=self)

# 3. Commandes
@bot.event
async def on_ready():
    print(f"{bot.user} is live !")

@bot.command()
async def soup(ctx):
    if ctx.channel.id != ID_CHANNEL: return 
    try: await ctx.message.delete()
    except: pass

    embed = discord.Embed(title="🍲 Quelle Soupe souhaites-tu ?", color=discord.Color.blue())
    gif_url = "https://media.discordapp.net/attachments/1271081376283889735/1461807631604912283/ezgif-63a0d38c5b45b78c.gif"
    embed.set_image(url=gif_url)

    footer_text = (
            "🔴 : Guild Adventure Cat (Grand Voyage Destinations)\n"
            "🔵 : Guild Adventure Cat\n"
            "🟢 : Guild Shop ou Guild Adventure Cat\n"
            "🟣 : Gutsy Meat : Road Shop | Taiko Olive : Weekly Market"
            )
    embed.set_footer(text=footer_text)

    await ctx.send(embed=embed, view=RecipePanel())

if token: bot.run(token)
else:
    print("Error : No token found.")