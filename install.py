import argparse, venv, os

parser = argparse.ArgumentParser(description='Install Selenne 6.0')

parser.add_argument('--no-venv', action='store_true', help='Install without virtual environment')

def gen_cfg():
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'w') as f:
            f.write("""prefix: s.
TOKEN: 

warn_on_ready: False

color: 0xfe2a9b
colours:
  red: blue""")

def install(env:bool = True): 
    if env:
        print('Installing stable version...')
        venv.create('venv', with_pip=True, clear=True, upgrade_deps=True)
        print('Installing requirements...')
        os.system('venv\\Scripts\\activate & pip install -r requirements.txt')
        print('Generating default config')
        gen_cfg()
        print('Done!')
    else:
        print('Installing system version...')
        os.system('pip install -r requirements.txt')
        print('Generating default config')
        gen_cfg()
        print('Done!')



if __name__ == '__main__':
    args = parser.parse_args()
    
    
    install(not args.no_venv)