from os import getenv
from os.path import dirname, isfile, join
from dotenv import load_dotenv
import eventlet.wsgi
try:
    from back_app.factory import check_and_upgrade_all_tables
except ModuleNotFoundError:
    from factory import check_and_upgrade_all_tables

try:
    from back_app.factory import create_app
except ModuleNotFoundError:
    from factory import create_app

# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

# instancia nossa função factory criada anteriormente
app, ws = create_app(getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    check_and_upgrade_all_tables(app)

    ip = '0.0.0.0'
    # import ipdb;ipdb.set_trace()
    port = app.config['PORT']
    debug = app.config['DEBUG']
    if debug:
        ip = 'localhost'
    eventlet.wsgi.server(eventlet.listen((ip, port)), app)
    # executa o servidor web do flask
    #app.run(
    #    host=ip, debug=debug, port=port, use_reloader=debug
    #)
