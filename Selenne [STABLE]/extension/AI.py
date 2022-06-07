import discord
from discord.ext import commands
import json

import sys

if 'tflearn' in sys.modules:
    del sys.modules["tflearn"]
if 'tensorflow' in sys.modules:
    del sys.modules["tensorflow"]



import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import random
import pickle
from deep_translator import GoogleTranslator

async def setup(b):
    global bot
    bot = b

    global extension_help
    
    extension_help = {
        'general_display': 's.ai',
        'specific_display': {
            's.ai version': 'Displays the AI version',
            's.ai reload': 'Reloads the AI',
            }
        }

    #add_help()

    #ADD CMD
    bot.add_listener(on_message)

    bot.add_command(AI)

    load_model()
    global translator_input, translator_output
    translator_input = GoogleTranslator(source='es', target='en')
    translator_output = GoogleTranslator(source='en', target='es')

    #END
    if bot_version != bot.version: bot.log.warning(f'extension.{version.lower()} outdated')
    bot.log.info(f'extension.{version.lower()} loaded')

def teardown(bot):
    bot.log.info(f'extension.{version.lower()} unloaded')
    remove_help()
    bot.remove_command('ai')

bot_version = 'Selenne 4.8.5'
version = 'AI_Manager: BETA'
ename = 'AI Manager'

#ModelName_Version_BiggerLayer.Number_Of_Layers
ai_version = 'CH_0.1_128.4'

path = f'db/AI/models/{ai_version}/'

#HELP
def add_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    help_list[ename] = extension_help
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)
def remove_help():
    with open('db/system/help.json', 'r') as f:
        help_list = json.load(f)
    del help_list[ename]
    with open('db/system/help.json', 'w', encoding='utf-8') as f:
        json.dump(help_list, f, indent=5)

def load_model():
    global data, words, labels, training, output
    with open(f'{path}intents.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    with open(f'{path}data.pickle', 'rb') as f:
        words, labels, training, output = pickle.load(f)

    net = tflearn.input_data(shape=[None, len(training[0])])
    #   MODEL DISPLAY (SAME AS TRAINER) V
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 128)
    net = tflearn.fully_connected(net, 128)
    net = tflearn.fully_connected(net, 32)
    #   MODEL DISPLAY (SAME AS TRAINER) A
    net = tflearn.fully_connected(net, len(output[0]), activation='softmax') #Last Layer
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.load(f'{path}model.tflearn')

    bot.ai = model

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

@commands.command()
async def AI(ctx, args = None):
    if not ctx.author.id in bot.developers:return

    match args:
        case 'reload':
            try:
                load_model()
                await ctx.send('Model Reloaded')
            except Exception as error:
                bot.log.error(error)
                await ctx.send('Model reload Failed')
        case 'version':
            await ctx.send(f'AI Version: {ai_version}')


@commands.Cog.listener()
async def on_message(message):
    #DEV SERVER
    try:
        if not message.guild.id == 913949547514974249: return
    except AttributeError: return
    #DEV SERVER
    if message.author.bot: return

    if 'selenne' in message.content.lower() or 'selene' in message.content.lower() or 'sele' in message.content.lower():
        #Remove Selenne from name
        msg = message.content.lower().replace('selenne', '')
        msg = msg.replace('selene', '')
        msg = msg.replace('sele', '')

        #AI Conexion
        inp = translator_input.translate(msg)
        results = bot.ai.predict([bag_of_words(inp, words)])
        result_index = numpy.argmax(results)
        tag = labels[result_index]
        
        if results[0][result_index] > 0.85:
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
                    
                    p_tg = tg['tag']
                    print(f'tag: {p_tg}')
        
            await message.channel.send(translator_output.translate(random.choice(responses)))
            bot.log.info(f'AI:{ai_version}: Inp: \'{inp}\', Tag: \'{p_tg}\', Match: {results[0][result_index]}')
        else:
            await message.channel.send(translator_output.translate('Sorry, I didn\'t get that'))
            bot.log.warning(f'AI:{ai_version}: Inp: \'{inp}\'')
