from mcstatus import JavaServer

server = JavaServer("pgserver.ddns.net", 25565)
stat = server.status()

print(stat.players)

# print(stat.motd)
# print(stat.motd.parsed)
print(stat.motd.to_plain())
