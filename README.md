O Hack da UnB - Jogo Educativo de Cibersegurança

Bem-vindo ao O Hack da UnB, um jogo desenvolvido em Python com Pygame que simula um cenário de investigação forense digital. O objetivo é ensinar conceitos básicos de Linux, SSH, Logs e Redes através de uma narrativa interativa.

📋 Pré-requisitos

Python 3.10 ou superior instalado.

Pip (gerenciador de pacotes do Python).

⚙️ Como Configurar o Ambiente (Instalação)

Recomendamos o uso de um Ambiente Virtual (venv) para não misturar as bibliotecas deste projeto com outras do seu sistema.

Siga os passos abaixo de acordo com o seu sistema operacional:

1. Criar o Ambiente Virtual

Abra o terminal (ou CMD/PowerShell) na pasta raiz deste projeto e digite:

No Windows:

python -m venv venv


No Linux / Mac:

python3 -m venv venv


2. Ativar o Ambiente Virtual

Você saberá que funcionou quando aparecer (venv) no começo da linha do seu terminal.

No Windows:

venv\Scripts\activate


No Linux / Mac:

source venv/bin/activate


3. Instalar as Dependências

Com a venv ativa, instale o Pygame usando o arquivo requirements.txt:

pip install -r requirements.txt


🚀 Como Rodar o Jogo

Após a instalação, e com a venv ainda ativa, execute o arquivo principal:

python main.py


(Se estiver no Linux/Mac e o comando acima não funcionar, tente python3 main.py)

🎮 Como Jogar

Mouse: Utilize para clicar e avançar os diálogos do professor (clique na caixa de diálogo quando quiser avançar o texto).

Teclado: Utilize para digitar comandos no terminal e responder às perguntas.

Dica: Leia atentamente o que o professor pede. Bem como olhe a seção de objetivos na esquerda da tela.

Dica: Você pode segurar Backspace para apagar texto rapidamente.

Objetivo: Encontre o aluno responsável por alterar as notas no sistema SIGAA antes que suas chances (Integridade do Sistema) acabem.

🛠️ Estrutura do Projeto

main.py: Ponto de entrada do jogo. Gerencia a janela e os estados.

settings.py: Configurações globais (resolução, cores, constantes).

story.py: Contém todo o roteiro, diálogos e lógica da narrativa.

states/: Gerencia as cenas (Gameplay e Cutscenes).

ui/: Componentes da interface (Terminal, Caixa de Texto, Balão de Fala).

assets/: Imagens e sons do jogo.

Desenvolvido por: Arthur Luiz, Bruno Henrique e Luis Felipe
Disciplina: Informática e Sociedade - UnB