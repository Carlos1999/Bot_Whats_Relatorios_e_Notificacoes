#Criado por Carlos Vinícius dos Santos (@Carlos1999)

# Roda programa com permissões de ADM
from ScriptsUteis.admin import *
if(not isUserAdmin()):
    runAsAdmin()
    sys.exit()

# Fecha todos os processos abertos para evitar bug que deixa vários abertos ao mesmo tempo
import psutil
lista_processos = ["firefox.exe","geckodriver.exe"]
for proc in psutil.process_iter():
    if proc.name() in  lista_processos:
        print(proc)
        proc.kill()
# sys.exit()   

# imports
print('importando dependências ------------------')
from datetime import datetime, timedelta,date
tempoinicio = datetime.now()
from classe_whats import Zapbot
from classe_comandos import Comandos
import os
from time import sleep
from pathlib import Path
import sys
import pandas as pd
import traceback

# CONFIGURAÇÕES DE PREPARAÇÃO ---------------------------------------------------------
contato_manutencao = 'Carlos Estagiário'
print(str((datetime.now() - tempoinicio)))
#classe do bot do whats com funções prontas
whats = Zapbot()
comandos = Comandos(whats,contato_manutencao)

#comandos válidos até o momento
comandos_validos = comandos.get_comandos_validos()
comandos_testes = comandos.get_comandos_exemplos()
#lista de contratos ou grupos que podem solicitar comandos ao bot
lista_permitidos = comandos.get_lista_permitidos()
print(str((datetime.now() - tempoinicio)))

# caminho abusoluto até dropbox
path_dropbox = str(Path.home())+'\\Dropbox\\'
path_bot = path_dropbox + 'Tramitação de Processos\\CONTRATOS\\BOT-Whats-e-Relatorios-Contratos\\'
# Comandos agendados 
df_comandos_agendados = pd.read_excel(r'Planilhas\Configurações BOT\Comandos - Agendados.xlsx',engine='openpyxl')
df_comandos_agendados = df_comandos_agendados.dropna()
hora_ultimo_agendamento = ''

#modo para testar todos os comandos do bot com !executar_teste_de_comandos
modo_teste = False
contador_teste = 0
#Inicia bot abrindo conversa padrão
whats.abre_conversa(contato_manutencao)
ultimo_envio_notificacoes_minutos = -1

# horário de serviço configurações
agora = datetime.now()
hora_inicio_expediente = datetime(agora.year,agora.month,agora.day,hour=7,minute=45)
hora_fim_expediente = datetime(agora.year,agora.month,agora.day,hour=18,minute=0)
dias_sem_expediente = ['Saturday' ,'Sunday']

# LOOP DE FUNCIONAMENTO GERAL ----------------------------------------------------------
while(True):
    # Verificando se está em horário de trabalho
    data_hoje = datetime.now().date().strftime('%d-%m-%Y')
    dia_da_semana = datetime.today().strftime('%A')
    agora = datetime.now()
    is_horario_de_trabalho = (hora_inicio_expediente < agora < hora_fim_expediente) and (not dia_da_semana in dias_sem_expediente )
    
    if(is_horario_de_trabalho):
        print('\r Trabalhando!',end = '')

    sleep(1)
    try:
        #abre a ultima notificação recebida
        ultima_mensagem = ''

        ultima_mensagem = whats.ultima_msg()

    except Exception as e:
        # caso não exista nenhuma notificação
        if("argument of type 'NoneType' is not iterable" in str(e) or '38M1B' in str(e)):
            print('\rNenhuma nova notificação'+str(datetime.now().strftime('DATA: %d/%m/%Y - HORA: %H:%M:%S')),end = '')
        
        else:
            
            whats.abre_conversa(contato_manutencao)
            whats.envia_msg('⚠️ Erro ao ler ultima mensagem '+str(e))
            print(e)
    try:
        # EXECUTANDO OS COMANDOS QUE ESTÃO AGENDADOS
        hora_string = str(datetime.now().strftime('%H:%M'))
        if( hora_string != hora_ultimo_agendamento) :
            for agendamento in df_comandos_agendados.itertuples():
                if(hora_string in agendamento.Hora and dia_da_semana in agendamento.Dias ):
                    whats.abre_conversa(agendamento.Contato)
                    ultima_mensagem = agendamento.Comandos
                    break
            hora_ultimo_agendamento = hora_string
        # CASO TENHA SIDO ALTERADA A PLANILHA DE COMANDOS AGENDADOS DURANTE A EXECUÇÃO DO BOT
        if('!atualizar_comandos_agendados' in ultima_mensagem):
            whats.envia_msg('Atualizando...')
            df_comandos_agendados = pd.read_excel(r'Planilhas\Configurações BOT\Comandos - Agendados.xlsx',engine='openpyxl')
            df_comandos_agendados = df_comandos_agendados.dropna()

        # Modo Teste ------------------------------------------
        if(('!parar_teste' in ultima_mensagem or len(comandos_testes) == contador_teste)) and modo_teste:
                whats.envia_msg('🤖 Modo teste parou...')
                modo_teste = False

        elif('!executar_teste_de_comandos' in ultima_mensagem):
            whats.envia_msg('🤖 Modo teste Iniciado, aguarde...')
            
            modo_teste = True
            contador_teste = 0

        if(modo_teste):
            sleep(4)
            ultima_mensagem = comandos_testes[contador_teste]
            contador_teste += 1 

        # Grupos em geral exceto pelo de Patrimonio
        if(whats.esta_na_lista(lista_permitidos) and whats.conversa_aberta() != 'Patrimonio Avisos'):
            #Comandos para Gerar e Enviar Relatórios -------------------------------
            if('!exec' in ultima_mensagem):
                comandos.comando_exec(ultima_mensagem)
            #gera relatórios de atribuição de jurídico
            elif('!gerar_juridico' in ultima_mensagem ):
                if('licitacao:True' in ultima_mensagem):
                    comandos.gerar_relatorio_setor(ultima_mensagem+',setor:JURÍDICO', data_hoje)
                else:
                    comandos.gerar_setor(ultima_mensagem+',setor:JURÍDICO', data_hoje)
            #gera relatórios de atribuição de contratos
            elif('!gerar_contratos' in ultima_mensagem ):
                if('licitacao:True' in ultima_mensagem):
                    comandos.gerar_relatorio_setor(ultima_mensagem+',setor:CONTRATOS', data_hoje)
                else:
                    comandos.gerar_setor(ultima_mensagem+',setor:CONTRATOS', data_hoje)
                # pass
            elif('!gerar_setor' in ultima_mensagem ):
                comandos.gerar_setor(ultima_mensagem,data_hoje)
            elif('!gerar_relacao' in ultima_mensagem ):
                comandos.gerar_relacao(ultima_mensagem,data_hoje)

            #Relatórios de Readequação e prestação de contas
            elif('!gerar_semanais' in ultima_mensagem ):
                comandos.gerar_semanais(ultima_mensagem,data_hoje)
            #Envia relatório de situação de aditivos de revisão prévia
            elif('!gerar_situacao_aditivos_revisao_previa' in ultima_mensagem):
                comandos.gerar_situacao_aditivos_revisao_previa(ultima_mensagem,data_hoje)
            
            #Envia relatório de situação de aditivos Geral
            elif('!gerar_situacao_GERAL' in ultima_mensagem ):
                comandos.gerar_situacao_geral(ultima_mensagem)   
            
            elif('!gerar_licitacao_por_assessor' in ultima_mensagem ):
                comandos.gerar_licitacao_por_consultor_juridico(ultima_mensagem,data_hoje)

            elif('!gerar_licitacao_sem_processo_aberto' in ultima_mensagem ):
                comandos.gerar_licitacao_sem_processo_aberto(ultima_mensagem,data_hoje)
                
            #Envia relatório de LICITAÇÃO
            elif('!gerar_licitacao' in ultima_mensagem ):
                comandos.gerar_licitacao(ultima_mensagem)
            
            elif('!gerar_planilha_contratos' in ultima_mensagem ):
                comandos.gerar_contratos_planilha(ultima_mensagem,data_hoje)
            
            elif('!gerar_medicoes_subprojetos' in ultima_mensagem):
                comandos.enviar_arquivos(path_dropbox+'base do BI dos subprojetos\\',['Relatório de acompanhamento da alimentação das medições no SMI SETHAS.pdf',
                                                                                        'Relatório de acompanhamento da alimentação das medições no SMI SAPE.pdf'])
            
            elif('!gerar_pendencias_step_contratos' in ultima_mensagem):
                comandos.gerar_pendencias_step_contratos(ultima_mensagem,data_hoje)
            elif('!gerar_pendencias_step_licitacao' in ultima_mensagem):
                comandos.gerar_pendencias_step_licitacao(ultima_mensagem,data_hoje)

            elif('!gerar_investimentos' in ultima_mensagem):
                comandos.gerar_relatorio_investimentos(ultima_mensagem,data_hoje)
            elif('!gerar_prazo_investimentos_licitacao' in ultima_mensagem):
                comandos.gerar_relatorio_prazo_investimentos_licitacao(ultima_mensagem,data_hoje)
            elif('!gerar_prestacao_de_contas' in ultima_mensagem):
                comandos.gerar_prestacao_de_contas(ultima_mensagem,data_hoje)

            elif('!enviar_obras_atrasadas' in ultima_mensagem):
                comandos.enviar_obras_atrasadas()
            elif('!enviar_arquivo' in ultima_mensagem):
                comandos.enviar_arquivos(path_dropbox+ comandos.filtrar('caminho:',ultima_mensagem),[comandos.filtrar('arquivo:',ultima_mensagem)])

            elif('!excel_notificacoes_enviadas' in ultima_mensagem):
                comandos.enviar_excel_notificacoes_enviadas(ultima_mensagem,data_hoje)

            elif('!excel_prestacao_de_contas' in ultima_mensagem):
                comandos.enviar_arquivos(path_dropbox+'\\base do BI dos subprojetos\\',['relatorio de prestação de contas.xlsx'])
            elif('!excel_pagamentos' in ultima_mensagem):
                comandos.enviar_excel_pagamentos()
            
            elif('!print' in ultima_mensagem):
                comandos.print(ultima_mensagem)
              
            #Comandos Gerais ----------------------------------------------------------
            elif('!enviar_notificacoes' in ultima_mensagem ):
                whats.envia_msg('🤖 Enviando Notificações!')
                comandos.enviar_notificacoes_e_mensagens_agendadas()


            #Reiniciar bot
            elif('!restart' in ultima_mensagem ):
                comandos.restart()
            elif('!finalizar' in ultima_mensagem):
                whats.finalizar()

            elif('!atualizar_excel_apuracao' in ultima_mensagem):
                comandos.atualizar_excel_apuracao()

            elif('!adicionar_permissao_contato'in ultima_mensagem):
                comandos.add_lista_permitidos(comandos.filtrar(':',ultima_mensagem))
                lista_permitidos = comandos.get_lista_permitidos()
            
            elif('!remover_permissao_contato'in ultima_mensagem):
                comandos.remove_lista_permitidos(comandos.filtrar(':',ultima_mensagem))
                lista_permitidos = comandos.get_lista_permitidos()

            elif('!agendar_mensagem' in ultima_mensagem  ):
                comandos.agendar_mensagem(ultima_mensagem)
            
            elif('Cida ' in ultima_mensagem):
                whats.envia_msg('Oi')
                
            #Envia mensagem informando que está online e o tempo de execução
            elif('!status' in ultima_mensagem):
                comandos.exibir_status(tempoinicio)
            elif('!historico' in ultima_mensagem):
                comandos.exibir_historico()
            
            elif('!inicia_conversa' in ultima_mensagem):
                whats.envia_msg('🤖 Iniciando Conversa!')
                whats.inicia_conversa(comandos.filtrar('numero:',ultima_mensagem),comandos.filtrar('mensagem:',ultima_mensagem))
            #Envia comandos possíveis
            elif('!comandos' in ultima_mensagem or '!contatos' in ultima_mensagem):
                comandos.exibir_comandos(ultima_mensagem)
                
            elif('!dados_processo' in ultima_mensagem):
                comandos.exibir_dados_processo(ultima_mensagem)
            
            elif('!report' in ultima_mensagem):
                comandos.report(ultima_mensagem)
            if('!' in ultima_mensagem):
                comandos.atualizar_historico(ultima_mensagem)

            

        if(whats.conversa_aberta() == 'Patrimonio Avisos'):
            if('!setor' in ultima_mensagem):
                comandos.exibir_dados_processo_setor(ultima_mensagem)

            elif('!gerar_pagamentos_patrimonio' in ultima_mensagem ):
                comandos.gerar_pagamentos_patrimonio(ultima_mensagem,data_hoje)
       
        #o que fazer caso alguém não altorizado entre em contato com o bot
        elif(not whats.esta_na_lista(lista_permitidos)  and  ultima_mensagem != ''  ):
            whats.envia_msg('🤖 Você não é autorizado a fazer requisições ao BOT')

        # a cada 5 minutos verifica se há notificações para enviar  
        if( agora.minute %5 ==0 and is_horario_de_trabalho and agora.minute != ultimo_envio_notificacoes_minutos and not modo_teste):
            comandos.enviar_notificacoes_e_mensagens_agendadas()
            ultimo_envio_notificacoes_minutos = agora.minute
        
        if(not modo_teste):
            whats.abre_notificacao()

    except Exception as e:
        if('NoneType' in str(type(ultima_mensagem))):
            ultima_mensagem = ''
        elif('Failed to establish a new connection' in str(e) or 'HTTPSConnectionPool' in str(e) ):
        
            whats.envia_msg('😴 Erro ao estabelecer conexão, sem acesso a internet! ')
            whats.abre_conversa(contato_manutencao)
        else:           
            # Envia mensagem de erro para usuário simplificada
            whats.envia_msg('⚠️ Erro ao Executar comando '+ultima_mensagem+' : '+str(e))
            # salva print da conversa com usuário que gerou erro
            url = whats.salvar_print()

            # abre o contato de manutenção para reportar erro
            whats.abre_conversa(contato_manutencao)
            # envia print do erro para contato de manutenção
            whats.envia_lista_arquivos(path_bot,[url])
            # envia erro detalhado para usuário
            whats.envia_msg('⚠️ Erro ao Executar comando '+ultima_mensagem+' : '+traceback.format_exc())
