import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import json
import re

#SOUP
# 1. Configuration et Chargement
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
ID_CHANNEL = 1461789288201982168

def load_ferias_items(file_path):
    items_dict = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Extraction de l'ID et du Nom
        matches = re.findall(r'"([a-zA-Z0-9]+)":\["([^"]+)"', content)
        for item_id, item_name in matches:
            items_dict[item_name] = item_id
    except FileNotFoundError:
        print(f"Attention : {file_path} non trouvé.")
    return items_dict

FERIAS_DATA = load_ferias_items('itemlist.js')

def load_skills_data():
    try:
        with open('skills.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Attention : skills.json non trouvé.")
        return {"baseskills": {}}

SKILLS_DATA = load_skills_data()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def load_all_data():
    with open('recipes.json', 'r', encoding='utf-8') as f1:
        recipes = json.load(f1)
    with open('ingredient_list.json', 'r', encoding='utf-8') as f2:
        ingredients = json.load(f2)
    return recipes, ingredients

recipes_data, ingre_data = load_all_data()

# 2. Classes pour l'interface

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
        
        results = (f"Great Success : {recipe['great_success']}\nSuccess : {recipe['success']}\n"
                   f"Failure : {recipe['failure']}\nGreat Failure : {recipe['great_failure']}")
        embed.add_field(name="Résultats", value=results, inline=False)

        legende = (f"🔴 : Guild Adventure Cat (Grand Voyage Destinations)\n🔵 : Guild Adventure Cat\n🟢 : Guild Shop ou Guild Adventure Cat\n🟣 : Gutsy Meat : Road Shop | Taiko Olive : Weekly Market")
        embed.add_field(name="Légende",value=legende,inline=False)

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


# FERIAS

# Fonction qui gère les suggestions pendant que l'utilisateur écrit
async def item_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    # On cherche les items qui contiennent la chaîne tapée (insensible à la casse)
    choices = [
        app_commands.Choice(name=name, value=name)
        for name in FERIAS_DATA.keys()
        if current.lower() in name.lower()
    ]
    # Discord limite à 25 suggestions maximum
    return choices[:25]

@bot.tree.command(name="ferias", description="Chercher un objet sur Ferias")
@app_commands.autocomplete(item=item_autocomplete)
@app_commands.describe(item="Le nom de l'objet")
async def ferias(interaction: discord.Interaction, item: str):
    item_id = FERIAS_DATA.get(item)
    
    if item_id:
        # Construction de l'URL
        url = f"https://xl3lackout.github.io/MHFZ-Ferias-English-Project/sozai/sozai.htm?{item_id}"
        
        # On utilise la classe FeriasLinkView que tu as déjà définie
        # On passe 'item' pour que le label du bouton soit le nom de l'objet
        view = FeriasLinkView(url=url, label=item)
        
        await interaction.response.send_message(view=view)
    else:
        await interaction.response.send_message(f"❌ L'objet '{item}' n'existe pas dans la base Ferias.", ephemeral=True)
    
class FeriasLinkView(discord.ui.View):
    def __init__(self, url: str, label: str):
        super().__init__()
        # On ajoute un bouton de type "Lien" (style gris par défaut sur Discord)
        self.add_item(discord.ui.Button(label=label, url=url, style=discord.ButtonStyle.link))
        
# SKILLS
class SkillCallView(discord.ui.View):
    def __init__(self, calls, baseskills):
        super().__init__(timeout=None)
        for call_name in calls:
            # On crée un bouton pour chaque talent dans 'calls'
            self.add_item(SkillCallButton(call_name, baseskills))

class SkillCallButton(discord.ui.Button):
    def __init__(self, skill_name, baseskills):
        super().__init__(label=skill_name, style=discord.ButtonStyle.grey)
        self.skill_name = skill_name
        self.baseskills = baseskills

    async def callback(self, interaction: discord.Interaction):
        # On récupère les infos du talent appelé
        skill_info = self.baseskills.get(self.skill_name)
        if not skill_info:
            await interaction.response.send_message(f"❌ Données pour {self.skill_name} introuvables.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f":link: **{self.skill_name}**",
            color=discord.Color.green()
        )
        
        img_url = skill_info.get("img")
        if img_url:
            embed.set_image(url=img_url)

        lines = []
        skill_keys = [k for k in skill_info.keys() if "skill" in k]
        for key in sorted(skill_keys, key=lambda x: int(re.search(r'\d+', x).group())):
            lines.append(f"・{skill_info[key]}")

        embed.description = "\n\n".join(lines)
        
        # On envoie la réponse en éphémère pour ne pas encombrer le chat
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def skill_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    choices = []
    baseskills = SKILLS_DATA.get("baseskills", {})
    search_text = current.lower()
    
    for skill_name, data in baseskills.items():
        show_val = data.get("show", "").replace("*", "") # On nettoie les étoiles
        
        # On vérifie si la recherche match le NOM du talent OU le champ SHOW
        if search_text in skill_name.lower() or search_text in show_val.lower():
            
            # Label affiché dans la liste : "Herbal Science (Medical Sage)"
            display_name = f"{skill_name} ({show_val})" if show_val else skill_name
            
            # La VALUE reste toujours skill_name pour que la commande /skill le trouve dans le JSON
            choices.append(app_commands.Choice(name=display_name[:100], value=skill_name))
            
    return choices[:25]

@bot.tree.command(name="skill", description="Afficher les paliers d'un talent")
@app_commands.autocomplete(name=skill_autocomplete)
@app_commands.describe(name="Nom du talent")
async def skill(interaction: discord.Interaction, name: str):
    baseskills = SKILLS_DATA.get("baseskills", {})
    
    if name in baseskills:
        skill_info = baseskills[name]
        
        embed = discord.Embed(
            title=f":book: **{name}**",
            color=discord.Color.blue()
        )
        
        img_url = skill_info.get("img")
        if img_url:
            embed.set_image(url=img_url)
        
        description_lines = []
        skill_keys = [k for k in skill_info.keys() if "skill" in k]
        for key in sorted(skill_keys, key=lambda x: int(re.search(r'\d+', x).group())):
            description_lines.append(f"・{skill_info[key]}")
        
        embed.description = "\n\n".join(description_lines)

        # --- Gestion des Calls ---
        call_keys = [k for k in skill_info.keys() if k.startswith("call")]
        calls_found = [skill_info[ck] for ck in call_keys if skill_info[ck] in baseskills]

        if calls_found:
            # On ajoute les boutons si des calls existent
            view = SkillCallView(calls_found, baseskills)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            # Sinon, on envoie juste l'embed simple
            await interaction.response.send_message(embed=embed)
                
    else:
        await interaction.response.send_message(f"❌ Le talent '{name}' est introuvable.", ephemeral=True)

# 3. Commandes
@bot.event
async def on_ready():
    # On synchronise les commandes slash
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    print(f"{bot.user} is live !")

@bot.command()
async def soup(ctx):
    if ctx.channel.id != ID_CHANNEL: return 
    try: await ctx.message.delete()
    except: pass

    embed = discord.Embed(title="🍲 Quelle Soupe souhaites-tu ?", color=discord.Color.blue())
    gif_url = "https://media.discordapp.net/attachments/1271081376283889735/1463413371230617783/terminalmontage-monster-hunter.gif?ex=6971bd68&is=69706be8&hm=05f69bbd21cb0ffdeadf2746f8513da987dff804f58e02c3c65aa50ea6187cee"
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
