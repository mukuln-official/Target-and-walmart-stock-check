import requests
import discord
from webdriver import keep_alive
from bs4 import BeautifulSoup
import pandas as pd
from discord.ext import commands


bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=""))
	print(f'Logged in as {bot.user.name}')



@commands.command(name="walmart")
async def walmart(ctx, SKU, ZIP):
    url = 'https://brickseek.com/walmart-inventory-checker/'
    payload = {'search_method': 'sku', 'sku': SKU, 'zip': ZIP, 'sort': 'distance'}
    df_record = pd.DataFrame(columns=['Store','City','Availability','Quantity'])
    r = requests.post(url, data=payload).text    # Make a POST request with data
    bs = BeautifulSoup(r, 'html.parser')
    j=0
    a = bs.find_all('div', class_='table__body')
    if a == []:
        print('No results found in the searched area.')
    else:
        store=[]
        city=[]
        q=[]
        stock=[]
        for tag in bs.find_all('div', class_='table__body'): 
            for i in range(20):
                m_Store = tag.findAll('strong', class_='address-location-name')
                m=str(m_Store)
                if  i < m.count('/strong'):
                    m_s= m_Store[i].get_text().replace("\nWalmart","")
                    m_add = tag.findAll('address',class_="address")
                    m_Address = m_add[i].contents[2]      
                    m_Availability = tag.findAll('span',class_="availability-status-indicator__text")
                    m_a = m_Availability[i].get_text()
                    if m_a =='Out of Stock'or m_a == 'Limited Stock':
                        m_q = str(0)
                        j=j-1
                    else:    
                        m_Quantity = tag.findAll('span',class_="table__cell-quantity")
                        m_q = m_Quantity[j].get_text()[9:]
                    j=j+1
                    df_record = df_record.append({'Store':m_s, 'City':m_Address, 'Availability':m_a, 'Quantity':m_q }, ignore_index=True)
                    store.append(str(m_s))
                    city.append(str(m_Address))
                    q.append(str(m_a))
                    stock.append(str(m_q))
                else:
                    # df_record=str(df_record)
                    # df_record=str(df_record)
                    # df_record=str(df_record)
                    # df_record=str(df_record)
                    # df_record=str(df_record)
                    # df_record=str(df_record)
                    # df_record=str(df_record)
                    # df_record=str(df_record)
                    print(store)
                    print(city)
                    print(q)
                    print(str(df_record))
                    print()
                    break
        s='\n'
        store = s.join(store)
        city = s.join(city)
        q = s.join(q)
        stock = s.join(stock)
        embed1 = discord.Embed(title='Walmart Stock Checker', color=3447003)
        embed1.add_field(name = 'Store', value=store , inline = True)
        embed1.add_field(name = 'City', value=city , inline = True)
        embed1.add_field(name = 'Availability', value=q , inline = True)
        # embed1.add_field(name = 'Quantity', value=stock , inline = True)
        r = requests.get("https://brickseek.com/walmart-inventory-checker/?sku={}".format(SKU))
        soup = BeautifulSoup(r.content, 'html.parser')
        for tag in soup.find_all("div", "item-overview__image-wrap"):
        	link = tag.img.get("src")
        s=str(link)
        embed1.set_thumbnail(url=s)
        embed1.set_footer(text='odin#9999')
        await ctx.channel.send(embed=embed1)


@commands.command(name="target")
async def target(ctx, SKU, ZIP):
    SKU=str(SKU)
    if '-' not in SKU:
        SKU = ('{}-{}-{}'.format(SKU[0:3], SKU[3:5], SKU[5:9]))
    url = 'https://brickseek.com/target-inventory-checker/'
    payload = {'search_method': 'sku', 'sku': SKU, 'zip': ZIP, 'sort': 'distance'}
    r = requests.post(url, data=payload).text    
    bs = BeautifulSoup(r, 'html.parser')
    print(" Store                Availability      Quantity ")
    j=0
    list1=[]
    for tag in bs.find_all('div', class_='table__body'): 
        for i in range(10):
            #print(tag)
            m_Store = tag.findAll('strong', class_='address-location-name')
            m=str(m_Store)
            if i < m.count('/strong'):
                m_s= m_Store[i].get_text()
                m_add = tag.findAll('address',class_="address")
                m_Address = m_add[i].contents[0]      
                m_Availability = tag.findAll('span',class_="availability-status-indicator__text")
                m_a = m_Availability[i].get_text()
                m_q = 'Unknown'
                j=j+1
                embeder = m_s+"   "  +  m_Address   + "      " + m_a + "        " + m_q
                list1.append(embeder)
            else:break
    s='\n'
    targ = s.join(list1)
    r = requests.get("https://brickseek.com/target-inventory-checker/?sku={}".format(SKU))
    soup = BeautifulSoup(r.content, 'html.parser')
    for tag in soup.find_all("div", "item-overview__image-wrap"):
    	link = tag.img.get("src")
    link=str(link)
    embed1 = discord.Embed(title='Target Stock Checker',description=targ,color=3447003) 
    embed1.set_thumbnail(url=link)
    embed1.set_footer(text='odin#9999')
    # embed1.set_image("https://images-ext-2.discordapp.net/external/tKWiJKemxuuUUMoiRarsbbJGCABzsHXGHGFnkzBF5_g/%3Fwidth%3D608%26height%3D612/https/media.discordapp.net/attachments/765387136122880021/783219912453128202/13753__3_.png")
    await ctx.channel.send(embed=embed1)

@commands.command(name="checking")
async def checking(ctx):
	embed = discord.Embed(title='Stock Checker Instructions', description='**Requesting Channel**: <#783828598129295452>\n\n**__Walmart Stock Checker__**\n\nUsage:\n```!walmart sku ZIP```\n\nExample: ```!walmart 781200042 95928 ```\n\n**__Target Stock Checker__**\n\nUsage\n```!target DPCI Zip```\n\nExample: ```!target 057-10-0162 95928```', color=0x32a852)
	embed.set_thumbnail(url="https://media.discordapp.net/attachments/765387136122880021/783219912453128202/13753__3_.png?width=608&height=612")
	await ctx.send(embed=embed)


bot.add_command(walmart)
bot.add_command(target)
bot.add_command(checking)
keep_alive()

bot.run('token')


