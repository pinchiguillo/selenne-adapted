import json

class Extension():
    def __init__(self, bot):
        self.bot = bot
        #! Scheme

        self.name = None
        self.version = None
        self.bot_version = None
        
        class Help():
            enabled = False
            def __init__(self):
                self.general_display = str()
                self.specific_display = dict()
                self.specific_display_help = "{'cmd': 'use'}"

            def add(self):
                return {'general_display': self.general_display,'specific_display': self.specific_display}

        self.help = Help()

        self.commands = list()
        self.listeners = list()
        self.cogs = list()
        self.views = list()

        _version = self.name.replace(' ', '')
        self._version = f'{_version.lower()}: {self.version}'    

    async def check_compatibility(self):
        if 'alfa' in self.version or 'beta' in self.version:
            self.bot.log.warning(f'{self.name} is being loaded in a development state')
        
        if list(self.bot_version)[8:11] != list(self.bot.version)[8:11]:  self.bot.log.warning(f'{self.name} OUTDATED. {self.name} built for {self.bot_version}, current: {self.bot.version}')

    async def load_cogs(self):
        for cog in self.cogs:
                await self.bot.add_command(cog)
                self.bot.log.info(f'{cog} command added')

    async def load_views(self):
        for view in self.views:
                await self.bot.add_view(view)
                self.bot.log.info(f'{view} view reloaded')

    async def add_help(self):
        if not self.help.enabled: return
        with open('db/system/help.json', 'r') as f:
            help_list = json.load(f)
        help_list[self.name] = self.help.add()
        with open('db/system/help.json', 'w', encoding='utf-8') as f:
            json.dump(help_list, f, indent=5)
    async def remove_help(self):
        with open('db/system/help.json', 'r') as f:
            help_list = json.load(f)
        del help_list[self.name]
        with open('db/system/help.json', 'w', encoding='utf-8') as f:
            json.dump(help_list, f, indent=5, ensure_ascii= False)

    async def loaded(self): self.bot.log.info(f'extension.{self._version.lower()} loaded')
    async def unloaded(self): self.bot.log.info(f'extension.{self._version.lower()} unloaded')
