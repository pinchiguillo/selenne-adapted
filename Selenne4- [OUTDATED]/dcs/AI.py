class reg:
    def create(dir:str, usr_id:int, nickname:str = "", relationship:int = "", ignored:bool = False, diary_dir:str = "", auth:bool = False):
        import json
        #Abrir datos antiguos
        with open(dir) as file:
            data = json.load(file)
        
        #Comprobar si existe en el registro
        if str(usr_id) in data:
            print('User Alrready registered')
            return False
        else:
            data[usr_id] = []
            data[usr_id].append({
                'nickname': nickname,
                'relationship': relationship,
                'ignored': ignored,
                'diary': diary_dir,
                'auth': auth
                })
            
            #Save
            with open(dir, 'w') as file:
                json.dump(data, file, indent=4)
            
            #Return
            return True

    def find(dir:str, id = None):
        import json
        with open(dir) as file:
            data = json.load(file)
        print(id in data)
    
    def read(dir:str, usr_id:str = None, info = 'all'):
        import json
        #Abrir datos antiguos
        with open(dir) as file:
            data = json.load(file)
        
        #Comprobar si existe en el registro
        if usr_id == None:
            return data
        else:
            if str(usr_id) in data:
                if info == 'all':
                    dat = data[str(usr_id)]
                    dat = dat[0]
                    return dict(dat)
                else:
                    for dat in data[usr_id]:
                        return dat[info]
                    
            else:
                return False

    def modify(dir:str, usr_id:str, var:str, value):
        import json
        #Abrir datos antiguos
        with open(dir) as file:
            data = json.load(file)
        
        #Comprobar si existe en el registro
        if str(usr_id) in data:
            for dat in data[usr_id]:
                dat[var] = value
        
        with open(dir, 'w') as file:
                json.dump(data, file, indent=4)
            
        #Return
        return True
    
    def regen(dir:str, check = False):
        if check:
            FILE = open(dir, 'w')
            tmp = {}
            FILE.write(str(tmp))
            FILE.close
            print(f'{dir} ha sido regenrado con exito')
        else:
            print('Para ejecutar este comando debes habilitar el check')

    def get_user_with(reg:dict, var, value):
        import json
        #var = auth
        #value = True
        otp =[]
        key = [*reg]
        for i in range(len(key)):
            reg_tmp = reg[str(key[i])]
            tmp = dict(reg_tmp[0])
            if tmp["auth"]:
                otp.append(key[i])
        
        return otp