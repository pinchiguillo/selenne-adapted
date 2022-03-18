class f_lib:
    def appear(this : str, arg : str):
        arg_split = arg.split(' ')
        mention = False
        i = 0
        while i in range(len(arg_split)) and not mention:
            if arg_split[i] in this: 
                mention = True
            i += 1

        return mention
    def adecuate(msg, accent = True, special_char = True, special_char_unicode = False, spaces = True, lower_upper = 0):
        if accent == False:
            msg = msg.replace('á', 'a')
            msg = msg.replace('é', 'e')
            msg = msg.replace('í', 'i')
            msg = msg.replace('ó', 'o')
            msg = msg.replace('ú', 'u')
        if special_char == False:
            if special_char_unicode == True:
                msg = msg.replace('!', '/u001')
                msg = msg.replace('?', '/u002')
                msg = msg.replace('"', '/u003')
                msg = msg.replace('.', '/u004')
            elif special_char_unicode == False:
                msg = msg.replace('!', '')
                msg = msg.replace('?', '')
                msg = msg.replace('"', '')
                msg = msg.replace('.', '')
        if spaces == False:
            msg = msg.replace(' ', '')
        elif spaces != True:
            msg = msg.replace(' ', spaces)
        if lower_upper == 'lower':
            msg = msg.lower()
        elif lower_upper == 'upper':
            msg = msg.upper()
        return msg
    def pop_str(msg : str, pop : list):
        msg = msg.split(' ')
        
        #Localizar pop in msg
        i = 0
        check = False
        while i in range(len(pop)) and not check:
            try:
                index = msg.index(pop[i])
                check = True
            except:
                pass
            i += 1
        
        msg.pop(index)
        #Unir nuevamente
        try:
            msg_ = ''
            for i in range(len(msg)):
                msg_ = msg_ + str(msg[i]) + ' '
        except:
            pass
        msg = msg_.removesuffix(' ')

        return msg
    def char_list(find : str, _in : list, pos = False):
        located = False
        i = 0

        while i in range(len(_in)) and not located:
            _str = str(_in[i])
            lst = []
            for j in _str:
                lst.append(j)
            if find in lst:
                located = True
            else:
                i += 1

        if located == True:
            if pos == True:
                return i
            else:
                return True
        else:
            return False