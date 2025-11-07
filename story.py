# (Passos 0 a 5 continuam idênticos à nossa última versão)

STORY_STEPS = [
    { # Passo 0: Professor checa SSH (COMANDO)
        "professor_speech": (
            "Vamos, como de costume, checar a SSH.",
            "Olha, eu tenho um serviço de log nesse computador",
            "Ele fica monitorando pra mim quem acessa essa SSH",
            "Você sabe o que é SSH né?" # Sim ou Não - If Não - Explica SSH e como conectar (ssh user@ip) - ZOA O ALUNO - Sim - AINDA BEM!
        ),
        "terminal_text": "", 
        "objective": "Cheque a sua SSH para validar possíveis invasões.", 
        "action_type": "ask_question_branching",
        "command_prompt": "user@professor-pc:~$", 
        "expected_command": "ssh prof_larcerinho@192.158.1.1",
        "answer_handlers" : {
            "sim": { 
                "action": "ok"
            },
            "nao" : {
                "action": "show_ssh_explanation"
            },
        }
    },
    { # Passo 1: O log aparece (AUTO)
        "professor_speech": (
            "Que ataque que aconteceu aqui?!",
        ),
        "terminal_text": ( 
            "PLACEHOLDER!!!! \n"
            "FAILED login for 'root' from 189.12.55.10 PORT 22\n"
            "SUCCESS login for 'root' from 189.12.55.10 PORT 22\n"
            "FILE_ACCESS: User 'root' read /home/senhas.txt\n"
            "DISCONNECTED."
        ),
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "auto_proceed", 
        "next_step_delay": 1000 
    },
    { # Passo 2: Pergunta IP (PERGUNTA)
        "professor_speech": "Que IP foi esse que me atacou?", 
        "terminal_text": "...", 
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "ask_question",
        "question_prompt": "Qual IP realizou o ataque?",
        "expected_answer": "189.12.55.10"
    },
    { # Passo 3: Pergunta Usuário (PERGUNTA)
        "professor_speech": "Certo... e qual usuário ele tentou acessar?",
        "terminal_text": "...",
        "objective": "Descubra o que aconteceu",
        "action_type": "ask_question",
        "question_prompt": "Qual usuário ele tentou acessar?",
        "expected_answer": "root"
    },
    { # Passo 4: Pergunta Arquivo (PERGUNTA)
        "professor_speech": "E qual arquivo ele acessou?",
        "terminal_text": "...",
        "objective": "Descubra o que aconteceu",
        "action_type": "ask_question",
        "question_prompt": "Qual arquivo ele acessou?",
        "expected_answer": "senhas.txt"
    },
    { # Passo 5: Espera o comando 'vim' (COMANDO)
        "professor_speech": "É, sabia que... ter esse txt ia me complicar.",
        "terminal_text": "...", 
        "objective": "Use 'vim senhas.txt' para ver o arquivo de senhas.",
        "action_type": "await_command",
        "command_prompt": "user@professor-pc:~$", 
        "expected_command": "vim senhas.txt"
    },
    
    # --- MUDANÇA PRINCIPAL DA RAMIFICAÇÃO ---
    
    { # Passo 6: 'vim' funciona, MOSTRA O ARQUIVO E FAZ A PERGUNTA
        "professor_speech": "Ok, o que vamos checar primeiro?", # Fala antiga
        "terminal_text": (
            "--- Conteúdo de senhas.txt ---\n"
            "facebook: larcerinhoMadeira@gmail.com | euAmoBolosDeChocolate\n"
            "instagram: larceirinhoMadeira@gmail.com | euGostoDeGatinhos\n"
            "sigaa: 2345meia78@unb.br | euOdeioCorrigirProvaDeAlunoBurro\n"
            "ifood: larcerinhoMadeira@gmail.com | Guitarra$L4r"
        ),
        "objective": "Investigue os serviços roubados",
        
        # Este novo tipo de ação sinaliza ao gameplay.py
        # que ele deve procurar por 'answer_handlers'
        "action_type": "ask_question_branching", 
        "question_prompt": "Qual serviço checar primeiro?", # Como você pediu
        
        "answer_handlers": {
            # Resposta correta:
            "sigaa": {
                "action": "proceed" # Avança para o Passo 7
            },
            
            # Respostas "erradas" (eventos)
            "facebook": {
                "action": "show_event", # Não avança
                "professor_speech": "Meu... meu Facebook! Está cheio de Minions!",
                # O gameplay.py vai ler isso e mostrar o asset
                "terminal_event_display": "assets/images/facebook_minions.png", 
                "sound_effect": "risada_minion.wav" # Opcional
            },
            "instagram": {
                "action": "show_event", # Não avança
                "professor_speech": "Hmm, parece que nada mudou aqui no Instagram. Normal.",
                "terminal_event_display": None, 
                "sound_effect": None
            },
            "ifood": {
                "action": "show_event", # Não avança
                "professor_speech": "Opa... não, não preciso nem checar. Cancele essa pizza.",
                "terminal_event_display": None,
                "sound_effect": "ding_dong.wav"
            }
        }
    },
    
    # --- RESTO DA HISTÓRIA (SÓ ACONTECE SE ESCOLHER 'SIGAA') ---

    { # Passo 7: O jogador ESCOLHEU 'sigaa' (AUTO)
        "professor_speech": "As notas... Ele mudou as notas de todos!",
        "terminal_text": (
            "Acessando sigaa.unb.br com '2345meia78@unb.br'...\n"
            "Login... sucesso!\n" 
            "!!! ALERTA: NOTAS ALTERADAS !!!"
        ),
        "objective": "Notas foram alteradas!",
        "action_type": "auto_proceed",
        "next_step_delay": 3000
    },
    { # Passo 8: Professor age (AUTO)
        "professor_speech": "Vou corrigir isso agora... e mudar todas elas.",
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
        "professor_speech": "Ok, vamos descobrir quem fez isso.",
        "terminal_text": "...",
        "objective": "Pegue o Culpado (Use 'whois [IP do atacante]')",
        "action_type": "await_command",
        "command_prompt": "user@professor-pc:~$",
        "expected_command": "whois 189.12.55.10"
    },
    { # Passo 10: Resultado do 'whois' (AUTO + PERGUNTA)
        "professor_speech": "Bingo! O endereço dele!",
        "terminal_text": (
            "user@professor-pc:~$ whois 189.12.55.10\n\n"
            "inetnum: 189.12.55.0 - 189.12.55.255\n"
            "owner: João 'Hackerman' da Silva\n"
            "address: SQN 210 Bloco Z Apto 101\n"
            "city: Brasília\n"
            "country: BR"
        ),
        "objective": "Pegue o Culpado",
        "action_type": "ask_question", # Pergunta final
        "question_prompt": "Qual a localização (bloco e apto) do atacante?",
        "expected_answer": "SQN 210 Bloco Z Apto 101" # Ou só "210 Bloco Z"
    },
    { # Passo 11: Fim (AUTO)
        "professor_speech": "Vou checar o endereço desse aluno no SIGAA... Ahá! Te peguei, João!",
        "terminal_text": "user@professor-pc:~$ (abrindo sigaa...)\nBuscando aluno: SQN 210 Bloco Z Apto 101...\nAluno encontrado: João da Silva. Matrícula: 18/0012345.\nEnviando e-mail para a coordenação...",
        "objective": "Culpado Encontrado!",
        "action_type": "auto_proceed",
        "next_step_delay": 5000 
        # (O próximo estado seria "END_GAME_SCREEN")
    }
]