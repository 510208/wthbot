from discord import *

class Embeds():
    def __init__(self,
                    title: str,
                    description: str,
                    color: int,
                    footer: str = "此機器人由 SamHacker 開發",
                    footer_icon: str = "https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64",
                    thumbnail: str = None,
                    image: str = None,
                    author: str = "SamHacker",
                    author_icon: str = "SamHacker",
                    author_url: str = "https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64",
                    fields: list = None
                ):
        self.title = title
        self.description = description
        self.color = color
        self.footer = footer
        self.footer_icon = footer_icon
        self.thumbnail = thumbnail
        self.image = image
        self.author = author
        self.author_icon = author_icon
        self.author_url = author_url
        self.fields = fields

    def embed(self):
        embed = Embed(
            title=self.title,
            description=self.description,
            color=self.color
        )
        embed.set_footer(text=self.footer, icon_url=self.footer_icon)
        return embed
    
    def error_embed(self):
        embed = Embed(
            title=self.title,
            description=self.description,
            color=Color.red()
        )
        embed.set_footer(text=self.footer, icon_url=self.footer_icon)
        return embed
    
    def success_embed(self):
        embed = Embed(
            title=self.title,
            description=self.description,
            color=Color.green()
        )
        embed.set_footer(text=self.footer, icon_url=self.footer_icon)
        return embed
    
    def warn_embed(self):
        embed = Embed(
            title=self.title,
            description=self.description,
            color=Color.orange()
        )
        embed.set_footer(text=self.footer, icon_url=self.footer_icon)
        return embed
    
    def info_embed(self):
        embed = Embed(
            title=self.title,
            description=self.description,
            color=Color.blue()
        )
        embed.set_footer(text=self.footer, icon_url=self.footer_icon)
        return embed
    
    def bot_info_embed():
        embed = Embed(
            title="關於我",
            description="我是一個 Discord 機器人，由 [SamHacker](https://github.com/510208) 製作。如果對機器人有問題，可以聯繫他喔！",
            color=Color.blue()
        )
        embed.set_footer(text="SamHacker 開發！", icon_url="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64")