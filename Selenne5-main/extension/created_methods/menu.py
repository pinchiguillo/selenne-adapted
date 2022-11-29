import discord

async def menu(self, ctx):
        embed = discord.Embed(title='Selenne Life', description = '**Cargando...**', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        #? Lista de menus
        menus = {
            'Pagina Principal': '🔤',
            'Ranking': '🔤',
            'Banco': '🔤',
            'Transferencia': '🔤',
            'Registro': '🔤'
        }
        main_menu = 'Pagina Principal'

        #.? View Object
        class MenusSelectorView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.timeout = 120

                #? Selector Class
                class MenusSelector(discord.ui.Select):
                    def __init__(self):
                        options = []
                        for menu in menus.keys():
                            if menu == active_menu: options.append(discord.SelectOption(label = menu, emoji=menus[menu], default=True))
                            else: options.append(discord.SelectOption(label = menu, emoji=menus[menu]))
                            

                        super().__init__(placeholder='Selecciona un menu', min_values=1, max_values=1, options=options)

                    async def callback(self, interaction: discord.Interaction):
                        global view_otp
                        view_otp = self.values[0]
                        embed.description = '**Cargando...**'
                        await interaction.response.edit_message(embed=embed, view=None)
                        self.view.stop()
                self.add_item(MenusSelector())
                class ExitBtn(discord.ui.Button):
                    def __init__(self):
                        super().__init__(style=discord.ButtonStyle.danger, label='Exit')
                    
                    async def callback(self, interaction: discord.Interaction):
                        global view_otp
                        view_otp = None
                        embed.description = '**Cargando...**'
                        await interaction.response.edit_message(embed=embed, view=None)
                        self.view.stop()
                if active_menu == 'Pagina Principal': self.add_item(ExitBtn())

        #? Bucle de interaccion
        active_menu = main_menu
        view = MenusSelectorView()
        while True:
            #? Different Menus Code
            match active_menu:
                case 'Pagina Principal' : embed.description = 'Pagina Principal'
                case 'Ranking' : embed.description = 'Ranking'
                case 'Banco' : embed.description = 'Banco'
                case 'Transferencia' : embed.description = 'Transferencia'
                case 'Registro' : embed.description = 'Registro'

            #? Output Code DO NOT TOUCH
            active_menu = None 
            await msg.edit(embed=embed, view=view)
            await view.wait()
            active_menu = view_otp
            view = MenusSelectorView()
            if not active_menu: break
            
        #? END
        embed.description = 'Se ha cerrado el menu'
        await msg.edit(embed=embed, view=None, delete_after=5)
        await ctx.message.delete()
        