# (Passos 0 a 5 continuam idênticos à nossa última versão)

STORY_STEPS = [
    { # Passo 1: Explicação da SSH
        "professor_speech": (
            "Ok, hora de gravar a aula de amanhã.",
            "Primeiro, vamos checar a SSH.",
            "Eu tenho o log habilitado.",
            "Gosto de checar sempre que abro o PC.",
            "Você sabe o que é SSH?",
        ),
        "terminal_text": "", 
        "objective": "Cheque a sua SSH para validar possíveis invasões.", 
        "action_type": "ask_question_branching",
        "question_prompt" : "Voce sabe o que é SSH?",
        "answer_handlers":{
            "sim" : {
                "action" : "proceed_with_speech",
                "professor_speech" : ("Ah, ainda bem que não estou lidando com um leigo.", "Pode entrar, é só digitar ssh prof_larcerinho@192.158.1.1, eu vou mudar depois, nem memoriza em!"),
            },
            "nao" : {
                "action" : "proceed_with_speech",
                "professor_speech" : ("Esses alunos dos CiC estão cada vez mais desatentos",
                                      "SSH significa 'Secure Shell'. É como uma porta dos fundos segura para acessar o computador de qualquer lugar.",
                                      "Eu uso para me conectar no meu servidor aqui da universidade.",
                                      "O mais importante é que eu mantenho o 'log' de autenticação ativado.",
                                      "Esse log é um arquivo de texto que anota *toda* tentativa de conexão, seja ela bem-sucedida ou falha.",
                                      "Se alguém tentar 'bater na porta', o log me diz quem foi, quando tentou e qual 'chave' usou.",
                                      "É uma das melhores ferramentas de segurança para saber se alguém andou bisbilhotando.",
                                      "Enfim, pra entrar é só fazer ssh prof_larcerinho@192.158.1.1, eu vou mudar depois, nem memoriza em!"),
            }
        }
    },
    { # Passo 1: OK SSH
        "professor_speech": (
            "...", # Estamos atualizando esse diálogo com o branching acima (sim ou não)
        ),
        "terminal_text": "", 
        "objective": "Cheque a sua SSH para validar possíveis invasões.", 
        "action_type": "await_command",
        "command_prompt": "user@professor-pc:~$", 
        "expected_command": "ssh prof_larcerinho@192.158.1.1",
    },
    { # Passo 2: O log aparece (AUTO) - AGORA COMPLEXO
        "professor_speech": (
            "Que ataque que aconteceu aqui?!",
            "Olha esse log... tem muita sujeira, mas o ataque real está aí no meio.",
            "Preciso filtrar o que é rotina do sistema e o que é invasão."
        ),
        # O TEXTO ABAIXO FOI MODIFICADO PARA SER UM PUZZLE VISUAL
        "terminal_text": ( 
            "Last login: Fri Nov 10 09:00:01 from 192.168.0.5\n"
            "user@server:~$ cat /var/log/auth.log | tail -n 15\n"
            "Nov 10 09:17:01 server CRON[5401]: (root) CMD (run-parts /etc/cron.hourly)\n"
            "Nov 10 10:00:23 server sshd[8821]: Invalid user admin from 54.22.11.99\n"
            "Nov 10 10:00:23 server sshd[8821]: Connection closed by 54.22.11.99 port 44312 [preauth]\n"
            "Nov 10 10:15:44 server sudo: prof_larcerinho : TTY=pts/0 ; PWD=/home/prof ; USER=root ; COMMAND=/usr/bin/apt update\n"
            "Nov 10 11:42:05 server sshd[9002]: Failed password for root from 189.12.55.10 port 55210 ssh2\n"
            "Nov 10 11:42:08 server sshd[9002]: Failed password for root from 189.12.55.10 port 55210 ssh2\n"
            "Nov 10 11:42:12 server sshd[9002]: Accepted password for root from 189.12.55.10 port 55210 ssh2\n"
            "Nov 10 11:42:12 server sshd[9002]: pam_unix(sshd:session): session opened for user root by (uid=0)\n"
            "Nov 10 11:43:05 server AUDIT: type=PATH msg=audit(1700000:01): name=\"/home/senhas.txt\" mode=0100644\n"
            "Nov 10 11:45:00 server sshd[9002]: Received disconnect from 189.12.55.10 port 55210:11: Disconnected by user"
        ),
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "auto_proceed", 
        "next_step_delay": 1000 
    },
    { # Passo 3: Pergunta IP (PERGUNTA)
        "professor_speech": ("Que IP foi esse que conseguiu entrar?",), 
        "terminal_text": "...", 
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "ask_question",
        "question_prompt": "Qual IP realizou o ataque com SUCESSO?", # Pergunta mais específica
        "expected_answer": "189.12.55.10"
    },
    { # Passo 4: Pergunta Usuário (PERGUNTA)
        "professor_speech": ("Certo... e qual usuário ele violou?",),
        "terminal_text": "...",
        "objective": "Descubra o que aconteceu",
        "action_type": "ask_question",
        "question_prompt": "Qual usuário do sistema ele acessou?",
        "expected_answer": "root"
    },
    { # Passo 5: Pergunta Arquivo (PERGUNTA)
        "professor_speech": ("E qual arquivo ele acessou? O log de auditoria (AUDIT) deve dizer.",),
        "terminal_text": "...",
        "objective": "Descubra o que aconteceu",
        "action_type": "ask_question",
        "question_prompt": "Qual arquivo ele acessou?",
        "expected_answer": "senhas.txt" # Ou "/home/senhas.txt" se quiser ser rigoroso
    },
    { # Passo 5: Espera o comando 'vim' (COMANDO)
        "professor_speech": ("É, sabia que... ter esse txt ia me complicar.",
                             "Não é seguro manter todas as suas senhas em um só arquivo.",
                             "Se você realmente tem que guardar em algum lugar... use um gerenciador de senhas!",
                             "Ou só anote na vida real mesmo, em um caderninho. Muito mais seguro.",
                             "Vamos ver o que tem dentro dele"),
        "terminal_text": "...", 
        "objective": "Use 'vim senhas.txt' para ver o arquivo de senhas.",
        "action_type": "await_command",
        "command_prompt": "user@professor-pc:~$", 
        "expected_command": "vim senhas.txt"
    },
    
    # --- MUDANÇA PRINCIPAL DA RAMIFICAÇÃO ---
    
    { # Passo 6: 'vim' funciona, MOSTRA O ARQUIVO E FAZ A PERGUNTA
        "professor_speech": ("Ok, são todas as minhas senhas, vou mudar depois, mas preciso descobrir se algo foi acessado","Ok, o que vamos checar primeiro?",), # Fala antiga
        "terminal_text": (
            "--- Conteúdo de senhas.txt ---\n"
            "facebook: larcerinhoMadeira@gmail.com | euAmoBolosDeChocolate\n"
            "instagram: larceirinhoMadeira@gmail.com | euGostoDeGatinhos\n"
            "sigaa: 2345meia78@unb.br | euAmoCorrigirProva\n"
            "ifood: larcerinhoMadeira@gmail.com | Guitarra$L4r"
        ),
        "objective": "Investigue os serviços roubados",
        
        # Este novo tipo de ação sinaliza ao gameplay.py
        # que ele deve procurar por 'answer_handlers'
        "action_type": "ask_question_branching", 
        "question_prompt": "Qual servico checar primeiro?", # Como você pediu
        
        "answer_handlers": {
            # Resposta correta:
            "sigaa": {
                "action": "proceed" # Avança para o Passo 7
            },
            
            # Respostas "erradas" (eventos)
            "facebook": {
                "action": "show_event", # Não avança
                "professor_speech": ("Meu... meu Facebook! Está cheio de Minions!",),
                # O gameplay.py vai ler isso e mostrar o asset
                "terminal_event_display": "assets/images/facebook_minions.png", 
                "sound_effect": "risada_minion.wav" # Opcional
            },
            "instagram": {
                "action": "show_event", # Não avança
                "professor_speech": ("Hmm, parece que nada mudou aqui no Instagram. Normal.",),
                "terminal_event_display": None, 
                "sound_effect": None
            },
            "ifood": {
                "action": "show_event", # Não avança
                "professor_speech": ("Enviaram uma pizza pra minha casa!?! Cancela isso!",),
                "terminal_event_display": None,
                "sound_effect": "ding_dong.wav"
            }
        }
    },
    
    # --- RESTO DA HISTÓRIA (SÓ ACONTECE SE ESCOLHER 'SIGAA') ---

    { # Passo 7: O jogador ESCOLHEU 'sigaa' (AUTO)
        "professor_speech": ("As notas... Ele mudou as notas de todos!",),
        "terminal_text": (
            "Acessando sigaa.unb.br com '2345meia78@unb.br'...\n"
            "Login... sucesso!\n" 
            "!!! ALERTA: NOTAS ALTERADAS !!!"
        ),
        "objective": "Notas foram alteradas!",
        "action_type": "auto_proceed",
        "next_step_delay": 3000
    },
    {
        "professor_speech": ("Espera, algumas notas são maiores que as originais!", 
                             "Quem quer que tenha feito isso é um deles...", 
                             "Olhe esta imagem. Qual o primeiro aluno com nota maior que o normal?"),
        "terminal_text": "...", 
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "ask_question",
        "question_prompt": "Qual é o primeiro aluno com nota maior que o normal?",
        "expected_answer": "Gustavo Borges",
        
        # --- CARREGA A IMAGEM ---
        "terminal_event_display": "assets/images/notas_completas.png"
    },
    {
        "professor_speech": ("Tem mais outros...",),
        "terminal_text": "...", 
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "ask_question",
        "question_prompt": "Qual é o segundo aluno com nota maior que o normal?",
        "expected_answer": "Luigi Macedo",

        "terminal_event_display": "assets/images/notas_completas.png"  
    },
    {
        "professor_speech": ("Tem mais outros...",),
        "terminal_text": "...", 
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "ask_question",
        "question_prompt": "Qual é o terceiro aluno com nota maior que o normal?",
        "expected_answer": "Joao da Silva",
        
        "terminal_event_display": "assets/images/notas_completas.png"
    },
    { # Passo 8: Professor age (AUTO)
        "professor_speech": ("Vou corrigir isso agora... e mudar todas elas.",),
        "terminal_text": (
            "user@professor-pc:~$ (alterando senhas...)\n"
            "user@professor-pc:~$ (corrigindo notas no SIGAA...)\n"
            "Pronto."
        ),
        "objective": "Notas corrigidas!",
        "action_type": "auto_proceed",
        "next_step_delay": 2000
    },
    { # Passo 9: Espera o comando 'whois' (COMANDO)
        "professor_speech": ("Ok, vamos descobrir quem fez isso.",),
        "terminal_text": "...",
        "objective": "Pegue o Culpado (Use 'whois [IP do atacante]')",
        "action_type": "await_command",
        "command_prompt": "user@professor-pc:~$",
        "expected_command": "whois 189.12.55.10"
    },
    { # Passo 10: Resultado do 'whois' (AUTO + PERGUNTA)
        "professor_speech": ("Bingo! O endereço dele!",),
        "terminal_text": (
            "user@professor-pc:~$ whois 189.12.55.10\n\n"
            "inetnum: 189.12.55.0 - 189.12.55.255\n"
            "owner: >>Redacted<<\n"
            "address: SQN 210 Bloco Z Apto 101\n"
            "city: Brasília\n"
            "country: BR"
        ),
        "objective": "Pegue o Culpado",
        "action_type": "ask_question", # Pergunta final
        "question_prompt": "Qual a localizacao (bloco e apto) do atacante?",
        "expected_answer": "SQN 210 Bloco Z Apto 101" # Ou só "210 Bloco Z"
    },
    { # Passo 11: Fim (AUTO)
        "professor_speech": "Vou checar o endereço desse aluno no SIGAA... Ahá! Te peguei, João!",
        "terminal_text": "user@professor-pc:~$ (abrindo sigaa...)\nBuscando aluno: SQN 210 Bloco Z Apto 101...\nAluno encontrado: Joao da Silva. Matrícula: 18/0012345.\nEnviando e-mail para a coordenacao...",
        "objective": "Culpado Encontrado!",
        "action_type": "auto_proceed",
        "next_step_delay": 5000 
        # (O próximo estado seria "END_GAME_SCREEN")
    }
]