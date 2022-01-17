#Criado por Carlos Vinícius dos Santos (@Carlos1999)
#imports
import pandas as pd
from time import sleep
from datetime import datetime

import os
from pathlib import Path
import pickle

#relatorios e outros scripts
# Scripts removidos para evitar vazamento de dados sensíveis de organização do projeto

# from Relatorios.Gerar_relatório_situacao_aditivos_GERAL import gerar_relatorio_aditivos_GERAL

# from Notificacoes.PEGA_ALTERACOES_CONTRATOS_ENVIA_WHATS import envia_novas_notificacoes_CONTRATOS
# from Notificacoes.PEGA_ALTERACOES_LICITACOES_ENVIA_WHATS import envia_novas_notificacoes_LICITACOES
# from Notificacoes.ETL_dados_notificacoes.Obras_Atrasadas import get_dados_obras_atrasadas
# from Notificacoes.Notificacoes_Gerais import enviar_notificacoes_vigencia_contratos_aditivos
# from Notificacoes.PEGA_NOTIFICACOES_ETAPAS_LICITACAO import envia_notificacoes_etapas_LICITACOES


#agendar mensagens
# from ScriptsUteis.susi import connect, agendarMensagem, obterDicionarioMensagens, enviar_mensagens

class Comandos:
    whats = ""
    contato_manutencao = ""
    # paths do bot
    path_dropbox = str(Path.home()) + '\\Dropbox\\'
    path_bot = path_dropbox + 'Tramitação de Processos\\CONTRATOS\\BOT-Whats-e-Relatorios-Contratos\\'
    path_relatorios = path_bot+'Relatorios\\Relatorios\\'
    # para que não reenvie mensagens caso o bot seja reiniciado
    ultimo_envio_hora = datetime.now().hour
    senha_exec = ""
    # ultimo_envio_hora = 0
    def __init__(self, whats,contato_manutencao):
        self.contato_manutencao = contato_manutencao
        self.whats = whats
        self.pegar_comandos_criados()
        self.pegar_comandos_exemplos_criados()

        print("Comandos Iniciado!")
             
    #Gerar e Enviar Relatórios e Notificações --------------------------------------------------------
    
    def gerar_situacao_geral(self, mensagem):
        """ Relatório situação dos aditivos de revisão prévia. ->exemplos:!gerar_situacao_GERAL,consultor:CARLOS"""
        self.whats.envia_msg('🤖 Gerando Relatório de Situação GERAL dos aditivos!')
        
        consultor,tipo_aditivo,dias_max,ues = self.filtrar_lista(["consultor:",
                                                                    "tipo_aditivo:",
                                                                    "dias_max:",
                                                                    "ues:"],mensagem)

        caminho,arquivo = gerar_relatorio_aditivos_GERAL(consultor,tipo_aditivo,dias_max,ues)
        self.whats.envia_lista_arquivos(caminho,[arquivo,"aditivos_obras - GERAL.xlsx"])

    def enviar_notificacoes_e_mensagens_agendadas(self):
        """ Envia Notificações e mensagens agendadas. -> exemplos:!enviar_notificacoes"""
        try:
            envia_novas_notificacoes_CONTRATOS(self.whats)
            envia_novas_notificacoes_LICITACOES(self.whats)
            envia_notificacoes_etapas_LICITACOES(self.whats)
            self.ultimo_envio_hora = enviar_notificacoes_vigencia_contratos_aditivos(self.whats,["Notificações Carlos","Ana Guedes Vivo Seplan"],self.ultimo_envio_hora)
            enviar_mensagens(whats=self.whats)
        except Exception as e:
            print('Falha no envio: ',e)
    
    
    # Métodos gerais -------------------------------------------------------------------------------------    
    def enviar_arquivos(self,caminho,lista_arquivos):
        """ Enviar arquivos . -> exemplos:!enviar_arquivo"""
        self.whats.envia_msg("🤖Enviando Arquivos!")
        try:
            self.whats.envia_lista_arquivos(caminho,lista_arquivos)
        except:
            self.whats.envia_msg("Caminho ou nome do arquivo inválido!")

    def print(self,mensagem):
        """ salva e envia print da tela do bot. -> exemplos:!print:Notificações Carlos"""
        conversa_aberta = self.whats.conversa_aberta()
        contato_printar = self.filtrar(":",mensagem,",")

        if(contato_printar != ""):
            self.whats.abre_conversa(contato_printar)
        url = self.whats.salvar_print()
        self.whats.abre_conversa(conversa_aberta)
        self.whats.envia_msg("🤖Enviando Print!")
        self.whats.envia_lista_arquivos(self.path_bot,[url])
    
    def restart(self):
        """ Reiniciar bot. -> exemplos:!restart"""
        
        
        self.whats.reiniciar()


    def exibir_status(self, tempoinicio):
        """ Enviar mensagem mostrando tempo online. -> exemplos:!status"""
        tempo_online = str( str((datetime.now() - tempoinicio) ).split(".")[0])
        self.whats.envia_msg('🤖 Estou online! \nTempo Online: '+tempo_online.split(":")[0]+" Horas "+tempo_online.split(":")[1]+" Minutos e "+tempo_online.split(":")[2]+" Segundos ⏱️")
            
    def exibir_comandos(self,mensagem):
        """ envia comandos. -> exemplos:!comandos,id:5,buscar:contratos|!comandos_exemplos,id:5,buscar:contratos|!contatos,id:5,buscar:Carlos"""
        lista_comandos = []

        if("exemplos" in mensagem):
            lista_comandos = self.get_comandos_exemplos()
        elif("contatos" in mensagem):
            lista_comandos = self.get_lista_permitidos()
        else:
            lista_comandos = self.get_comandos_validos()

        comandos_final = ""
        contador = 1
        numero_comando,buscar = self.filtrar_lista(["id:","buscar:"],mensagem)
        if(numero_comando == ""):
            for comando in lista_comandos:
                if(buscar != ""):
                    if(buscar in comando):
                        comando = comando.replace(",",",*")
                        comando = comando.replace("\n","\n          *")
                        comandos_final += str(contador)+"-> *"+comando+"* \n"
                else:
                    comando = comando.replace(",",",*")
                    comando = comando.replace("\n","\n          *")
                    comandos_final += str(contador)+"-> *"+comando+"* \n" 
                contador += 1
            
            self.whats.envia_msg("🤖 Comandos disponíveis: \n"+comandos_final)
            # self.whats.envia_msg(".")

        else:
            self.whats.envia_msg(lista_comandos[int(numero_comando)-1])
            # self.whats.envia_msg(".")
    def exibir_historico(self):
        """ Envia 10 últimos comandos usados. -> exemplos:!historico"""
        lista_historico = pickle.load( open( "Planilhas\LISTA_HISTORICO_COMANDOS.p", "rb") )
        index = 0
        mensagem_enviar = ""
        for indice_lista in range(len(lista_historico)-1,-1,-1):
            index +=1
            mensagem_enviar += str(index)+"-> *"+str(lista_historico[indice_lista])+"* \n"
        mensagem_enviar
        self.whats.envia_msg(mensagem_enviar)
        
        
    def comando_exec(self,mensagem):
        """ Executa comandos contidos em uma string. -> exemplos:!exec,comando:print(teste),senha:****"""
        comando,senha = self.filtrar_lista(["comando:","senha:"],mensagem,";")
        if(senha == self.senha_exec):
            self.whats.envia_msg("Executando comando!")
            exec(comando)
            
        else:
            self.whats.envia_msg("Senha inválida!")

    def report(self,mensagem):
        """ Envia print para que seja realizada manutenção ou repasse de informação. -> exemplos:!report"""

        conversa_aberta = self.whats.conversa_aberta()
        self.whats.envia_msg("🤖Enviando Report!")
        url = self.whats.salvar_print()

        self.whats.abre_conversa(self.contato_manutencao)
        self.whats.envia_msg(f"🤖Enviando Report de {conversa_aberta}!")
        self.whats.envia_lista_arquivos(self.path_bot,[url])
    
    def atualizar_historico(self,mensagem):
        """ Atualiza o histórico de comandos e salva em uma lista pickle """
        lista_historico = pickle.load( open( "Planilhas\LISTA_HISTORICO_COMANDOS.p", "rb") )
        lista_historico.pop(0)
        lista_historico.append(mensagem)
        pickle.dump(lista_historico, open("Planilhas\LISTA_HISTORICO_COMANDOS.p", "wb"))
    
    def get_comandos_validos(self):
        """ Retorna comandos validos do bot """
        df = pd.read_excel(r'Planilhas\Configurações BOT\Comandos.xlsx',engine="openpyxl")
        
        return  df.Comandos.to_list()

    def get_comandos_exemplos(self):
        """ Retorna exemplos de comandos funcionais """
        df = pd.read_excel(r'Planilhas\Configurações BOT\Comandos_exemplos.xlsx',engine="openpyxl")
        return df.Comandos_exemplos.to_list()

    def get_lista_permitidos(self):
        """ Retorna contatos e grupos com permissão de requisitar comandos ao bot """
        df = pd.read_excel(r'Planilhas\Configurações BOT\Contatos_e_grupos_permitidos.xlsx',engine="openpyxl")
        return df.permitidos.to_list()
    
    def add_lista_permitidos(self,contato):
        """ Adiciona contato a lista de permitidos do bot """
        lista_contatos = self.get_lista_permitidos()
        lista_contatos.append(contato)
        df = pd.DataFrame()
        df["permitidos"] = lista_contatos
        df.to_excel(r'Planilhas\Configurações BOT\Contatos_e_grupos_permitidos.xlsx', index = False, header=True)
        self.whats.envia_msg("🤖 Contato adicionado!")
    

    def remove_lista_permitidos(self,contato):
        """ Remove contato a lista de permitidos do bot """
        lista_contatos = self.get_lista_permitidos()
        del(lista_contatos[int(contato)-1])
        df = pd.DataFrame()
        df["permitidos"] = lista_contatos
        df.to_excel(r'Planilhas\Configurações BOT\Contatos_e_grupos_permitidos.xlsx', index = False, header=True)
        self.whats.envia_msg("🤖 Contato Removido!")

    

    def filtrar(self, filtro, mensagem, parar=","):
        """ filtra um determinado parâmetro de uma mensagem string"""
        valor = ""
        if(filtro in mensagem and len(mensagem.split(filtro)) > 1):
            valor = mensagem.split(filtro)[1]
            if(len(mensagem.split(parar)) > 1):
                valor = valor.split(parar)[0]
        return valor

    def filtrar_lista(self, lista_filtros, mensagem, fim_parametro=","):
        """ filtra uma lista de parâmetros e retorna uma lista com os valores passados, por exemplo: filtrar_lista(["setor:","consultor:","etapa:","ordenacao:"],mensagem) """ 
        lista_parametros = []
        for filtro in lista_filtros:
            lista_parametros.append(self.filtrar(filtro, mensagem, fim_parametro))
        return lista_parametros

    def pegar_comandos_criados(self):
        """ lê arquivo Bot_whats_geral e pega os todos os comandos já criados""" 
        arquivo_bot_geral = open("Bot_whats_geral.py", "r", encoding='utf-8')
        arquivo_comandos = open("classe_comandos.py", "r", encoding='utf-8')

        texto_comandos = arquivo_comandos.read()
        contador = 0
        lista_comandos = []
        resultado = ""

        for linha in arquivo_bot_geral:
            contador += 1
            
            if("in ultima_mensagem" in linha ):
                lista_comandos.append(resultado.replace('"', ""))
                resultado = ""
                resultado += linha.split("'")[1]
            
            if("comandos." in linha ):
                comando = linha.split("(")[0].replace(" ", "")[9:]
                funcao_do_comando = self.filtrar(comando, texto_comandos, "def")
                if("self.filtrar_lista([" in funcao_do_comando):
                    resultado +=  "," + self.filtrar("self.filtrar_lista([", funcao_do_comando, "],")
                    resultado = resultado.replace(",", ",\n")

            if("whats.conversa_aberta() == 'Patrimonio Avisos'" in linha ):
                lista_comandos.append(resultado.replace('"', ""))
                break
                

        arquivo_bot_geral.close()
        arquivo_comandos.close()
        df_comandos = pd.DataFrame()
        df_comandos["Comandos"] = lista_comandos[1:]
        # return df_comandos
        df_comandos.to_excel(r'Planilhas\Configurações BOT\Comandos.xlsx', index = False, header=True)

    def pegar_comandos_exemplos_criados(self):
        """ lê arquivo classe_comandos e pega os exemplos de comandos colocados em cada método"""    
        arquivo_comandos = open("classe_comandos.py","r",encoding='utf-8')

        lista_comandos = []

        for linha in arquivo_comandos:
            
            if(". -> exemplos:" in linha ):
                comandos = self.filtrar(". -> exemplos:",linha,'"""')
                for comando in comandos.split("|"):
                    lista_comandos.append(comando.replace(",",",\n"))
     
            if("def pegar_comandos_exemplos_criados(self):" in linha):
                break
        arquivo_comandos.close()
        df_comandos = pd.DataFrame()
        df_comandos["Comandos_exemplos"] = lista_comandos[1:]
        # return df_comandos
        df_comandos.to_excel(r'Planilhas\Configurações BOT\Comandos_exemplos.xlsx', index = False, header=True)
