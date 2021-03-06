import discord
import requests

from checks import *
from discord.ext import commands
from datetime import datetime
from functions import *
from unicode import *
from telnetlib import Telnet

class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @is_liaison()
    async def eventhost(self, ctx, user: discord.Member):
        'Add or remove event host role - liaison only'
        eventhostrole = ctx.guild.get_role(event_host)
        if eventhostrole in user.roles:
            await user.remove_roles(eventhostrole)
            await ctx.send(f'```Succesfully took {eventhostrole.name} from {user.name}```')
        else:
            await user.add_roles(eventhostrole)
            await ctx.send(f'```Succesfully added {eventhostrole.name} to {user.name}```')
    
    @commands.command()
    @is_creative_designer()
    async def masterbuilder(self, ctx, user: discord.Member):
        'Add or remove master builder role - ECD only'
        master_builder_role = ctx.guild.get_role(master_builder)
        if master_builder_role in user.roles:
            await user.remove_roles(master_builder_role)
            await ctx.send(f'```Succesfully took {master_builder_role.name} from {user.name}```')
        else:
            await user.add_roles(master_builder_role)
            await ctx.send(f'```Succesfully added {master_builder_role.name} to {user.name}```')
    
    @commands.command()
    @is_staff()
    async def serverban(self, ctx, user: discord.Member):
        'Add or remove server banned role'
        serverbannedrole = ctx.guild.get_role(server_banned)
        if serverbannedrole in user.roles:
            await user.remove_roles(serverbannedrole)
            await ctx.send(f'Took Server Banned role from {user.name}')
        else:
            await user.add_roles(serverbannedrole)
            await ctx.send(f'Added Server Banned role to {user.name}')
    
    @commands.command()
    @is_staff()
    async def start(self, ctx):
        'Not currently working'
        startEmbed = discord.Embed(description='start working out fatass')
        await ctx.send(embed=startEmbed)
        
    @commands.command()
    @is_staff()
    async def stop(self, ctx):
        'Stops the server'
        em = discord.Embed()
        try:
            self.bot.telnet_object.session.write(bytes('stop', 'ascii') + b"\r\n")
        except:
            em.title='Command error'
            em.colour = 0xFF0000
            em.description='Something went wrong'
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = 'Server stopped.'
            await ctx.send(embed=em)
    
    @commands.command(aliases=['adminconsole', 'ac'])
    @is_staff()
    async def telnet(self, ctx, *args):
        'mv, gtfo, kick, mute or warn from discord'
        em = discord.Embed()
        command = ''
        for x in range(len(args)):
            command += f'{args[x]} '
        try:
            if args[0] in ['mute', 'stfu', 'gtfo', 'ban', 'unban', 'unmute', 'smite', 'noob', 'tban', 'tempban', 'warn', 'mv', 'kick', 'cc','say']:
                self.bot.telnet_object.session.write(bytes(command, 'ascii') + b"\r\n")
            elif args[0] == 'slconfig':
                if args[1] not in ['add', 'remove']:
                    raise no_permission(['IS_SENIOR_ADMIN'])
                else:
                    self.bot.telnet_object.session.write(bytes(command, 'ascii') + b"\r\n")
            else:
                raise no_permission(['IS_SENIOR_ADMIN'])
        except Exception as e:
            em.title='Command error'
            em.colour = 0xFF0000
            em.description = f'{e}'
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = 'Command sent.'
            await ctx.send(embed=em)
    
    @commands.command()
    @is_senior()
    async def kill(self, ctx):
        'Kills the server'
        em = discord.Embed()
        try:
            self.bot.telnet_object.session.write(bytes('telnet.stop', 'ascii') + b"\r\n")
        except:
            em.title='Command error'
            em.colour = 0xFF0000
            em.description='Something went wrong'
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = 'Killed the server.'
            await ctx.send(embed=em)
        
    
    @commands.command()
    @is_staff()
    async def restart(self, ctx):
        'Restarts the server'
        em = discord.Embed()
        try:
            self.bot.telnet_object.session.write(bytes('restart', 'ascii') + b"\r\n")
        except:
            em.title='Command error'
            em.colour = 0xFF0000
            em.description='Something went wrong'
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = 'Server restarting.'
            await ctx.send(embed=em)
    
    @commands.command()
    @is_senior()
    async def console(self, ctx,*, command):
        'Send a command as console'
        '''await ctx.send(f'```:[{str(datetime.utcnow().replace(microsecond=0))[11:]} INFO]: {ctx.author.name} issued server command: /{command}```')'''
        em = discord.Embed()
        try:
            self.bot.telnet_object.session.write(bytes(command, 'ascii') + b"\r\n")
        except Exception as e:
            em.title='Command error'
            em.colour = 0xFF0000
            em.description = f'{e}'
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = 'Command sent.'
            await ctx.send(embed=em)
    
    @commands.command(aliases=['status'])
    async def state(self, ctx):
        'Gets the current status of the Server'
        em = discord.Embed()
        try: 
            json = requests.get("http://play.totalfreedom.me:28966/list?json=true").json()
        except:
            em.description = 'Server is offline'
            em.colour = 0xFF0000
        else:
            em.description = 'Server is online'
            em.colour = 0x00FF00
        await ctx.send(embed=em)
        
    @commands.command()
    async def list(self, ctx):
        'Gives a list of online players.'
        em = discord.Embed()
        em.title = "Player List"
        try: 
            json = requests.get("http://play.totalfreedom.me:28966/list?json=true").json()
        except ConnectionError:
            em.description = 'Server is offline'
        else:
            if json["online"] == 0:
                em.description = "There are no online players"
            else:
                em.description = "There are {} / {} online players".format(json["online"], json["max"])
                owners = json["owners"]
                if len(owners) != 0:
                    em = format_list_entry(em, owners, "Server Owners")
                executives = json["executives"]
                if len(executives) != 0:
                    em = format_list_entry(em, executives, "Executives")
                developers = json["developers"]
                if len(developers) != 0:
                    em = format_list_entry(em, developers, "Developers")
                senior_admins = json["senioradmins"]
                if len(senior_admins) != 0:
                    em = format_list_entry(em, senior_admins, "Senior Admins")
                admins = json["admins"]
                if len(admins) != 0:
                    em = format_list_entry(em, admins, "Admins")
                #trialadmins = json["trialadmins"]
                #if len(trialadmins) != 0:
                    #em = format_list_entry(em, trialmods, "Trial Mods")
                masterbuilders = json["masterbuilders"]
                if len(masterbuilders) != 0:
                    em = format_list_entry(em, masterbuilders, "Master Builders")
                operators = json["operators"]
                if len(operators) != 0:
                    em = format_list_entry(em, operators, "Operators")
                imposters = json["imposters"]
                if len(imposters) != 0:
                    em = format_list_entry(em, imposters, "Imposters")
        await ctx.send(embed=em)
    @commands.command()
    async def ip(self, ctx):
        'Returns the server IP'
        await ctx.send('play.totalfreedom.me')
        #pass #discordSRV responds already.    
   
    @commands.command()
    @is_staff()
    async def archivereports(self, ctx):
        """Archive all in-game reports older than 24 hours"""
        count = 0
        reports_channel = self.bot.get_channel(reports_channel_id)
        archived_reports_channel = self.bot.get_channel(archived_reports_channel_id)
        await ctx.channel.trigger_typing()
        async for report in reports_channel.history(limit=100):
            try:
                embed = report.embeds[0]
            except:
                await report.delete()
            time = embed.timestamp
            difference = datetime.now() - time
            if difference.days >= 0:
                await report.delete()
                await archived_reports_channel.send("Message archived because it is older than 24 hours", embed=embed)
                count += 1
        await ctx.send("Archived **{}** reports that are older than 24 hours".format(count))
    
    @commands.command()
    @is_mod_or_has_perms()
    async def fixreports(self, ctx):
        await ctx.channel.trigger_typing()
        reports_channel = self.bot.get_channel(reports_channel_id)
        messages = await reports_channel.history(limit=500).flatten()
        fixed = 0
        for message in messages:
            if len(message.reactions) == 0 and message.author == message.guild.me:
                await message.add_reaction(clipboard)
                fixed += 1
        await ctx.send(f'Fixed **{fixed}** reports')

def setup(bot):
    bot.add_cog(ServerCommands(bot))
