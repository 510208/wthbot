import socket
import discord
from discord.ext import commands
import json
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
    TOKEN = config["token"]
from embed import Embeds
import logging
import whois as wh
import random
# 初始化日誌
logging.basicConfig(level=logging.DEBUG, format="[%(name)18s] [%(asctime)24s] [%(levelname)4s]: %(message)s", datefmt="%Y/%m/%d %H:%M")
# 設定日誌等級
logging.getLogger().setLevel(logging.INFO)
# 設定日誌格式
logging.getLogger().handlers[0].setFormatter(logging.Formatter("[%(name)18s] [%(asctime)24s] [%(levelname)4s]: %(message)s"))
# 覆蓋日誌等級名稱
logging.addLevelName(logging.DEBUG, "DEBG")
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.ERROR, "ERRO")
import re
from ipinfo import ip2carrier
# 匯入Minecraft測試模組
from mcstatus import JavaServer, BedrockServer

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    text = f"""
   ___   ___
  |   ) |       Started...
  |     |___)   Builded by SamHacker

  Bot Name: {bot.user.name}
  Bot ID:   {bot.user.id}
    """
    # await bot.sync_commands(force=True)
    # 將text分割成多行，以Array的形式儲存
    text = text.split("\n")
    # 逐行輸出
    for line in text:
        logging.info(line)

server_cmd = bot.create_group(name="server", description="伺服器管理指令")
java_cmd = server_cmd.create_subgroup(name="java", description="Java版伺服器管理指令")
bedrock_cmd = server_cmd.create_subgroup(name="bedrock", description="Bedrock版伺服器管理指令")

def chk_mcip(s):
    pattern = r"^([\da-z\.-]+)(:\d{1,5})?$"
    return re.match(pattern, s) is not None

@java_cmd.command(name="status", description="查詢Java版Minecraft伺服器狀態")
async def java_status(ctx, ip: str, port: int=25565):
    logging.info(f"JE - 正在查詢 {ip}:{port} 的伺服器狀態...")
    try:
        if chk_mcip(ip) == False:
            embed = Embeds(
                title=f"{ip}:{port} 伺服器狀態",
                description=r"發生錯誤：IP地址格式錯誤\n\n請確認IP地址格式是否正確，它必須合乎以下正規表示式： `^([\da-z\.-]+)(:\d{1,5})?$`",
                color=0xFF0000,
                footer="機器人由 SamHacker 開發",
                footer_icon="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64"
            )
            embed = embed.error_embed()
            embed.set_thumbnail(url="https://www.minecraft.net/content/dam/minecraftnet/franchise/logos/Homepage_Download-Launcher_Creeper-Logo_500x500.png")
            await ctx.respond(embed=embed)
            return
        
        server = JavaServer(ip, port)
        stat = server.status()

        simple_motd = stat.motd.to_plain()
        # 確保 MOTD 不超過 1024 個字符
        motd = simple_motd[:1021] + '...' if len(simple_motd) > 1024 else simple_motd

        embed = discord.Embed(
            title=f"{ip}:{port} 伺服器狀態",
            description=f"結果",
            color=0x00FF00
        )
        embed.add_field(name="伺服器MOTD", value=motd, inline=False)
        l = round(stat.latency, 2)
        embed.add_field(name="伺服器延遲", value=f"{l}ms")
        embed.add_field(name="伺服器人數", value=f"{stat.players.online}/{stat.players.max}")
        embed.add_field(name="伺服器版本", value=stat.version.name, inline=False)
        embed.add_field(name="伺服器協議", value=stat.version.protocol)
        # embed.add_field(name="預設遊戲模式", value=stat.gamemode, inline=False)
        embed.set_thumbnail(url="https://www.minecraft.net/content/dam/minecraftnet/franchise/logos/Homepage_Download-Launcher_Creeper-Logo_500x500.png")
        # embed.add_field(name="伺服器軟體", value=stat.software)
        embed.set_footer(text="機器人由 SamHacker 開發", icon_url="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64")
        await ctx.respond(embed=embed)
    except Exception as e:
        logging.error(f"發生錯誤：{e}")
        embed = Embeds(
            title=f"{ip}:{port} 伺服器狀態",
            description=f"發生錯誤：{e}\n\n請確認伺服器是否開啟，並且伺服器版本是否支援伺服器狀態查詢。",
            color=0xFF0000,
            footer="機器人由 SamHacker 開發",
            footer_icon="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64"
        )
        await ctx.respond(embed=embed.error_embed())

@bedrock_cmd.command(name="status", description="查詢Bedrock版Minecraft伺服器狀態")
async def bedrock_status(ctx, ip: str, port: int=19132):
    logging.info(f"BE - 正在查詢 {ip}:{port} 的伺服器狀態...")
    try:
        if chk_mcip(ip) == False:
            embed = Embeds(
                title=f"{ip}:{port} 伺服器狀態",
                description=r"發生錯誤：IP地址格式錯誤\n\n請確認IP地址格式是否正確，它必須合乎以下正規表示式： `^([\da-z\.-]+)(:\d{1,5})?$`",
                color=0xFF0000,
                footer="機器人由 SamHacker 開發",
                footer_icon="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64"
            )
            # 將嵌入訊息右側圖示設為https://www.minecraft.net/content/dam/minecraftnet/franchise/logos/Homepage_Download-Launcher_Creeper-Logo_500x500.png
            embed = embed.error_embed()
            embed.set_thumbnail(url="https://www.minecraft.net/content/dam/minecraftnet/franchise/logos/Homepage_Download-Launcher_Creeper-Logo_500x500.png")
            await ctx.respond(embed=embed)
            return
        
        server = BedrockServer(ip, port)
        stat = server.status()

        simple_motd = stat.motd.to_plain()
        # 確保 MOTD 不超過 1024 個字符
        motd = simple_motd[:1021] + '...' if len(simple_motd) > 1024 else simple_motd

        embed = discord.Embed(
            title=f"{ip}:{port} 伺服器狀態",
            description=f"結果",
            color=0x00FF00
        )
        embed.add_field(name="伺服器MOTD", value=motd, inline=False)
        l = round(stat.latency, 2)
        embed.add_field(name="伺服器延遲", value=f"{l}ms")
        embed.add_field(name="伺服器人數", value=f"{stat.players.online}/{stat.players.max}")
        embed.add_field(name="伺服器版本", value=stat.version.name, inline=False)
        embed.add_field(name="伺服器協議", value=stat.version.protocol)
        embed.add_field(name="預設遊戲模式", value=stat.gamemode, inline=False)
        embed.set_thumbnail(url="https://www.minecraft.net/content/dam/minecraftnet/franchise/logos/Homepage_Download-Launcher_Creeper-Logo_500x500.png")
        # embed.add_field(name="伺服器軟體", value=stat.software)
        embed.set_footer(text="機器人由 SamHacker 開發", icon_url="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64")
        await ctx.respond(embed=embed)
    except Exception as e:
        logging.error(f"發生錯誤：{e}")
        # embed = Embeds(
        #     title=f"{ip}:{port} 伺服器狀態",
        #     description=f"發生錯誤：{e}\n\n請確認伺服器是否開啟，並且伺服器版本是否支援伺服器狀態查詢。",
        #     color=0xFF0000,
        #     footer="機器人由 SamHacker 開發",
        #     footer_icon="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64"
        # )
        # await ctx.respond(embed=embed.error_embed())
        await ctx.respond(f"發生錯誤：{e}")

network = bot.create_group(name="network", description="網路有關指令")
@network.command(name="whois", description="查詢網域WHOIS資訊")
async def whois(ctx, domain: str):
    logging.info(f"正在查詢 {domain} 的WHOIS資訊...")
    await ctx.respond("<:emoji_15:1186087763972460544>  已受理查詢，請稍後，已送出申請...")
    w = wh.whois(domain)
    logging.info(f"查詢 {domain} 的WHOIS資訊完成！")
    # msg.edit(content="<a:done:1185774834962141304>  查詢完成！正在格式化")
    embed = discord.Embed(
        title=f"{domain} WHOIS 查詢",
        description="結果",
        color=0x00FF00
    )
    # 檢查網域是否有效
    if w.domain_name == None:
        embed = discord.Embed(
            title=f"{domain} WHOIS 查詢",
            description="結果",
            color=0xFF0000,
            image="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64"
        )
        embed.add_field(name="錯誤", value="無法查詢到網域資訊，請確認網域是否有效。")
        embed.set_footer(text="機器人由 SamHacker 開發", icon_url="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64")
        await ctx.send(embed=embed)
        # msg.edit(content="<a:error:1185774838057533500>  查詢失敗，請確認網域是否有效")
        return
    embed.add_field(name="域名", value=w.domain_name, inline=False)
    embed.add_field(name="註冊商", value=w.registrar)
    embed.add_field(name="註冊日期", value=w.creation_date)
    embed.add_field(name="到期日期", value=w.expiration_date, inline=False)
    embed.add_field(name="更新日期", value=w.updated_date)
    embed.add_field(name="WHOIS伺服器", value=w.whois_server)
    embed.add_field(name="狀態", value=w.status, inline=False)
    embed.add_field(name="名稱伺服器", value=w.name_servers)
    embed.add_field(name="郵件伺服器", value=w.emails)
    embed.add_field(name="網域ID", value=w.id)
    embed.add_field(name="網域狀態", value=w.state)
    embed.add_field(name="網域DNSSEC", value=w.dnssec)
    embed.set_thumbnail(url="https://www.whois.com/images/twimg.png")
    embed.set_footer(text="機器人由 SamHacker 開發", icon_url="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64")
    # msg.edit(content="<:agree:1218485450134655008>  查詢完成！正在發送結果...")
    await ctx.send(embed=embed)

@network.command(name="ipinfo", description="查詢IP地址資訊")
async def ipinfo(ctx, ip: str):
    logging.info(f"正在查詢 {ip} 的IP地址資訊...")
    await ctx.respond("<:emoji_15:1186087763972460544>  已受理查詢，請稍後，已送出申請...")
    carrier, country = ip2carrier(ip)
    logging.info(f"查詢 {ip} 的IP地址資訊完成！")
    # msg.edit(content="<a:done:1185774834962141304>  查詢完成！正在格式化")
    embed = discord.Embed(
        title=f"{ip} IP地址查詢",
        description="結果",
        color=0x00FF00
    )
    embed.add_field(name="IP地址", value=ip, inline=False)
    embed.add_field(name="國家", value=country)
    embed.add_field(name="運營商", value=carrier)
    embed.set_thumbnail(url="https://www.whois.com/images/twimg.png")
    embed.set_footer(text="機器人由 SamHacker 開發", icon_url="https://cdn.discordapp.com/avatars/959977374471028779/597bb4483e073564aabadb47b554ea9f.png?size=64")
    # msg.edit(content="<:agree:1218485450134655008>  查詢完成！正在發送結果...")
    await ctx.send(embed=embed)

sync_bot = bot.create_group(name="sync", description="同步有關指令(開發用，僅限 SamHacker 可使用)")
@sync_bot.command(name="sync", description="同步指令")
async def sync(ctx, force: bool=False):
    if ctx.author.id == 959977374471028779:
        await ctx.send("開始同步...")
        await bot.sync_commands(force=force)
        await ctx.send("同步完成！")
        await ctx.respond("同步完成！")
    else:
        await ctx.respond("你沒有權限使用這個指令！")

wth = bot.create_group(name="whatthe", description="各種各樣出現也不奇怪的指令們")

@wth.command(name="ping", description="測試機器人延遲")
async def ping(ctx):
    await ctx.respond("正在測試延遲...")
    await ctx.send(f"延遲：{round(bot.latency * 1000)}ms")

@wth.command(name="8ball", description="隨機回答問題")
async def eightball(ctx, *, question: str = ""):
    answers = [
        "不要懷疑自己，做就對了",
        "你有沒有聽過自己在說甚麼？",
        "我不想回答，沒空",
        "你想太多了",
        "我相信你辦的到的！",
        "我不知道，你自己決定吧",
        "你問我，我也不知道",
        "我只是台電腦，你想問我甚麼？萬物之靈？",
        "去啊，你覺得可以就做吧",
        "相信自己，終有屬於自己的未來",
        "先關掉 Discord，再打開，這樣一來就會得到結果了",
        f"Did you mean: {random.randint(0, 100)}?",
        "我不知道，你自己問問看",
        "問你朋友，他們會給你適合的答案",
        f"我覺得這件事的機率大概有... {random.randint(0, 10000)/100}%",
        "東邊日出西邊雨，道是無晴卻有晴",
        "白雲生處有人家，過雨江南萬木斜",
        "青山綠水間，白雲悠悠處",
        "江流曲似鎖，山色傍空林",
        "斜陽已在西，獨立翠微間",
        "樓觀兩相極，一夜看清秋",
        "白雲生處有人家，過雨江南萬木斜",
        "水聲連沙落月明，花氣沉來鳥不驚",
        "青門古道音容在，古戍寒煙故嶺間",
        "古木古亭聲角急，古簾古籠夢翩翩",
    ]
    ans_maybe = random.choice(answers)
    embed = Embeds(
        title="神奇八號球",
        description=f"虔誠的信徒啊，我收到你的請求了\n\n我想說，對於{question}，我的答案是：{ans_maybe}",
        color=0x00FF00
    )
    await ctx.send(embed=embed.success_embed())

# @wth.command(name="selectone", description="隨機抽一個人")
# async def selectone(ctx, members: , pick: int=1):
#     if len(members) == 0:
#         # 取得當前頻道所有除了機器人以外的成員
#         members = ctx.channel.members
#         members = list(filter(lambda m: m.bot == False, members))
#         random.shuffle(members)
#         pick_per = []
#         for i in range(pick):
#             pick_per.append(members[i-1])
#         if pick == 1:
#             await ctx.send(f"我選擇了 {random.choice(members).mention}！")
#         else:
#             await ctx.send(f"我選擇了 {', '.join([m.mention for m in pick_per])}！")
#     else:
#         await ctx.send(f"我選擇了 {random.choice(members).mention}！")

bot.run(TOKEN)