
# connect4

_By Kevin Shannon and Tanner Krewson_

The original vertical four in a line game.

### Try it out: https://kevinshannon.dev/connect4/

## Development

(If you open `index.html` directly, singleplayer will not work because it will be unable to load its web worker. [More info](https://stackoverflow.com/questions/21408510/chrome-cant-load-web-worker))

1. Install [Node.js](https://nodejs.org/).
2. Clone Connect4 to your computer.
3. Run `npm install`.
4. To start the development server, run `npm run dev`.

## Para Rodar o Back-End
1. Crie um ambiente virtual no diretório Connect-4 com o comando `python3 -m venv .venv`
2. Ative o ambiente virtual com 
 - No Windows, execute: `.\.venv\Scripts\activate`
 - No Unix ou no MacOS, execute: `source .\.venv\bin\activate` (linux)
3. Instale as dependências do projeto com ` pip install -r .\requirements\all_requirements.txt`
4. Suba a aplicação com `python.exe .\back_app\run.py`

- A aplicação deve subir uma base de dados sqlite com as tabelas ao inicializar.
