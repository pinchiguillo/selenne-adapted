@bot.command()
async def uwu(ctx: commands.Context) -> None:
  r = await ctx.invoke(bot.get_command("command_name"), command_parameters_if_any)