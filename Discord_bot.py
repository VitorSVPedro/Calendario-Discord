import discord
import datetime
import calendar

TOKEN = ''

client = discord.Client()

def save():
    with open('indisponibilidades.txt', 'w') as f:
        for i in range(len(indisponibilidade)):
            for id in indisponibilidade[i]:
                f.write('{}:{}\n'.format(i, id))

def load():
    global indisponibilidade
    global data
    data = datetime.date.today()
    mes = calendar.monthrange(data.year,data.month)[1]
    indisponibilidade = [set() for i in range(mes)]

    try:
        with open('indisponibilidades.txt', 'r') as f:
            for line in f:
                dia, id = line.split(':')
                indisponibilidade[int(dia)] |= {id.strip()}
    except FileNotFoundError:
        pass

load()

def get_calendar():
    today = datetime.date(data.year, data.month, 1)
    weekday = (today.weekday() + 1) % 7
    ans = 'Dias disponiveis:\n' + '   ' * weekday

    for i in range(len(indisponibilidade)):
        today = datetime.date(data.year, data.month, i+1)
        if len(indisponibilidade[i]) == 0:
            ans += '{: 3}'.format(i+1)
        else:
            ans += '  .'
        
        if today.weekday() == 5:
            ans += '\n'

    return '`' + ans + '`'

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != '553352612158636034':
        return

    if message.content.lower().startswith('!disponibilidade'):
        await client.send_message(message.channel, get_calendar())

    elif message.content.lower().startswith('!indisponivel'):
        remove = message.content.split()
        indisponibilidade[int(remove[1])-1] |= {message.author.id}
        save()
        await client.send_message(message.channel, 'Meeeee')

    elif message.content.lower().startswith('!disponivel'):
        remove = message.content.split()
        if message.author.id in indisponibilidade[int(remove[1])-1]:
            indisponibilidade[int(remove[1])-1].remove(message.author.id)
            save()
        await client.send_message(message.channel, 'Boa jogador')

    elif message.content.lower().startswith('!sessao'):
        remove = message.content.slip()

        await client.send_message(message.channel, 'Aleluia')
   


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')

client.run(TOKEN)
#print(get_calendar())