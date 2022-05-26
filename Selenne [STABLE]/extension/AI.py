import discord
from discord.ext import commands

from dcs.functions import f_lib

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
tensorflow.compat.v1.disable_resource_variables()

import random
import json
import pickle

from deep_translator import GoogleTranslator

import logging
logging.basicConfig(filename='db/ai/log.log', filemode='a', encoding = 'utf8', format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)

path = 'db/AI/models/Selenne/'
AI_version = 'CHS:0.1'

async def setup(b):
    global bot
    bot = b

    global extension_help
    
    extension_help = {
        'general_display': 'cmd',
        'specific_display': {
            'cmd': 'use'
            }
        }

    bot.add_listener(on_message)

    bot.add_command(ai)

    #load_model()
    global translator_input, translator_output
    lan = 'es'
    translator_input = GoogleTranslator(source=lan, target='en')
    translator_output = GoogleTranslator(source='en', target=lan)

    bot.log.info(f'selenne.AI loaded: Extension Version: {version}')

def teardown(bot):
    bot.log.info(f'selenne.AI unloaded')

version = 'AI Implementation: ALFA'
ename = 'AI'

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
    global data, words, labels, training, output, net, model
    with open(f'{path}intents.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    with open(f'{path}data.pickle', 'rb') as f:
        words, labels, training, output = pickle.load(f)

    net = tflearn.input_data(shape=[None, len(training[0])])
    #Layers: Same as the trainer
    net = tflearn.fully_connected(net, 16) 
    net = tflearn.fully_connected(net, 16) 
    net = tflearn.fully_connected(net, 16)
    #OTP
    net = tflearn.fully_connected(net, len(output[0]), activation='softmax') #Last Layer
    net = tflearn.regression(net)

    #LOAD MODEL
    model = tflearn.DNN(net)
    model.load(f'{path}model.tflearn')

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
async def ai(ctx, *, args = None):
    if ctx.author.id == bot.owner:
        
        if args == 'reload':
            await ctx.send('Actually AI models cant be reloaded, in orther to do that **REBOOT THE WHOLE BOT**')
            #Cant be reloaded
            '''msg = await ctx.send('Reloading AI model...')
            try:
                await bot.reload_extension('extension.Selenne')
                await msg.edit('AI model reloaded')
            except:
                await msg.edit('Error While Reloading AI model')'''
        elif args in ['version', 'v']:
            await ctx.send(f'Current AI model: **Selenne:{AI_version}**')
        else:
            await ctx.send('Wrong Syntax')
    else: 
        await ctx.send('You dont have permissions to use this command')

#Global Var
bot_name = ['selenne', 'selene', 'sele']

@commands.Cog.listener()
async def on_message(message):
    
    #Exceptions in the call
    if 's.' in message.content: return
    
    msg = str(message.content.lower())

    if msg.startswith('selenne') or msg.startswith('selene') or msg.startswith('sele'):
        #Translator
        msg = msg.removeprefix('selenne')
        msg = msg.removeprefix('selene')
        msg = msg.removeprefix('sele')
        inp = translator_input.translate(msg)
        logging.info(f'Translation: {inp}')

        #Gets the most probable answere    
        results = model.predict([bag_of_words(inp, words)])
        result_index = numpy.argmax(results)
        tag = labels[result_index]

        logging.info(f'prob: {results[0][result_index]}')
        #if True:
        if results[0][result_index] > 0.70:
            #Finds the answere
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
                    
                    p_tg = tg['tag']
                    logging.info(f'tag: {p_tg}')

            #Sends the answere
            print(translator_output.translate(random.choice(responses)))
        
        #AI dont get the right answere
        else:
            print(translator_output.translate('Sorry, I didn\'t get that'))
            p_tg = tg['tag']
            logging.error(f'AI CANT GENERATE ANSWERE: Input:{msg} ({inp}), Prob: {results[0][result_index]}, Suggested Model: {p_tg}')
