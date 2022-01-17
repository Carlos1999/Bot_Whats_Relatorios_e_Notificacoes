#Criado por Carlos Vinícius dos Santos (@Carlos1999)

#Criado por Carlos Vinícius dos Santos (@Carlos1999)
#imports
from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta,date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import os
import psutil
class Zapbot:
    
    # Firefox.exe -ProfileManager -no-remote
   
    primeiro_anexo = True
    gecko_path = 'Driver\geckodriver.exe'
    fp = webdriver.FirefoxProfile('Profile')
    driver = ''
    

    def __init__(self,usar_profile = True):
        print("Iniciando BOT ----------------------")
        if(usar_profile):
            self.driver = webdriver.Firefox(firefox_profile=self.fp,executable_path=self.gecko_path)
        else:
            self.driver = webdriver.Firefox(executable_path=self.gecko_path)
        print("BOT iniciado! ----------------------")
        self.driver.maximize_window()
        self.primeira_conversa = True
        # Abre o whatsappweb
        print("Abrindo Whats Web! ------------------")
        self.driver.get("https://web.whatsapp.com/")
        
        self.wait = WebDriverWait(self.driver, 10)
        self.entrou = False
        while(self.entrou == False):            
            try:
                # Aguarda alguns segundos para validação manual do QrCode
                WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.ID, "pane-side"))
                )
                self.entrou = True
            except Exception as e:
                if("Message:" in str(e)):
                    print("Não logado ou sem acesso a internet!")
                   
                else:
                    print(e)
             
    def inicia_conversa(self, numero,mensagem=None):
        """ Inicia conversa com número novo """
        try:
            self.driver.get("https://web.whatsapp.com/send?phone="+numero+"&text&app_absent=0")
            sleep(4)
            
            #self.wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
            if mensagem != None:
                self.wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "_4sWnG")))
                self.envia_msg(mensagem)
            return True

        except Exception as e:
            print(str(e))
            return False
            
    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            if(not self.primeira_conversa):
                if( self.conversa_aberta() == contato):
                    return True
            else:
                self.primeira_conversa = False

            sleep(1)
            self.wait.until(ec.visibility_of_element_located((By.XPATH,"/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/label/div/div[2]")))
            # Envia nome do contato para caixa de pesquisa
            caixa_de_pesquisa = self.driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/label/div/div[2]")
            caixa_de_pesquisa.send_keys(contato)
            sleep(2)
            # Seleciona o contato
            try:
                self.wait.until(ec.visibility_of_element_located((By.XPATH, "//span[@title = '{}']".format(contato))))
                elementos = self.driver.find_elements_by_xpath("//span[@title = '{}']".format(contato))
                # primeira conversa
                elementos[-1].click()
            except:
                print(f"contato {contato} não encontrato!")
            
            # Seleciona para apagar nome do contato da caixa de mensagens
            self.wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/button")))
            self.driver.find_element_by_xpath( "/html/body/div/div[1]/div[1]/div[3]/div/div[1]/div/button").click()
            
            # Seleciona para descer até primeira mensagem
            try:
                self.driver.find_element_by_xpath( "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/div/div[1]/span/div").click()
            except:
                pass

            # Sobe para começo da página
            self.driver.find_element_by_xpath('//*[@id="pane-side"]').send_keys(Keys.CONTROL + Keys.HOME)
            return True
        except Exception as e:
            print(str(e))
            return False
               
                
    
    def abre_notificacao(self):
        """ Verifica se há novas mensagens não lidas e abre a conversa caso exista """
        try:
            # Seleciona a caixa de pesquisa de conversa
            self.caixa_de_pesquisa = self.driver.find_element_by_class_name("_1pJ9J")
            # Digita o nome ou numero do contato
            self.caixa_de_pesquisa.click()
            sleep(0.5)
            self.caixa_de_pesquisa.click()
            sleep(0.5)
            self.caixa_de_pesquisa.click()
        except Exception as e:
            if("argument of type 'NoneType' is not iterable" in str(e) or "_1pJ9J" in str(e)):
                print('\r------------ Nenhuma notificação '+str(datetime.now().strftime('DATA: %d/%m/%Y - HORA: %H:%M:%S')),end = "")
            
        
    
    
            
    def esta_na_lista(self,lista):
        """ Verifica se o contato com a conversa aberta está na lista de permitidos """
        try:
            # Seleciona a caixa de pesquisa de conversa
            
            contato = self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span').text
            if(contato in lista):
                return True
            else: 
                return False
   
        except Exception as e:
            pass
            # print("\r Erro verificação de está na lista!", end = "")
    
    def conversa_aberta(self):
        """ Retorna qual a conversa aberta no momento """
        try:
            # Seleciona a caixa de pesquisa de conversa
            contato = self.driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span').text
            return contato
   
        except Exception as e:
            print("erro ao verificar conversa aberta",e)
            return ""
            # print("\r Erro verificação de está na lista!", end = "")
    
    def salvar_print(self):
        """ salva print de tela na pasta Prints """
        try:
            
            hora = 'Prints\screen'+str(datetime.now())+'.png'
            hora = hora.replace(":",".")
            # Seleciona a caixa de pesquisa de conversa
            # self.driver.save_screenshot(hora)
            self.driver.get_screenshot_as_file(hora)
            return hora
        except Exception as e:
            print(e)
            # print("\r Erro verificação de está na lista!", end = "")
            
            
    def anexa_media(self, caminho_arquivo):
        """ anexa media """
        try:
            sleep(1)
            if(self.primeiro_anexo == True):    
                # Clica no botão adicionar
                self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
                self.primeiro_anexo = False
            # Seleciona input
            attach = self.driver.find_element_by_css_selector("input[type='file']")
            attach.send_keys(caminho_arquivo)
      
        except Exception as e:
            print("Erro ao anexar media", e)
            # self.envia_msg("Erro ao anexar media")
            
        
    def envia_media(self):
        """ Envia media """
        try:
            sleep(3)
            # Seleciona botão enviar
            self.wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "span[data-icon='send']")))
            self.driver.find_element_by_css_selector("span[data-icon='send']").click()
      
        except Exception as e:
            print("Erro ao enviar media", e)

    def envia_lista_arquivos(self,caminho,arquivos):
        """ Envia lista de arquivos em um determinado caminho """
        try:
            sleep(1)  
            # Clica no botão adicionar
            self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
            
            # Seleciona input
            for arquivo in arquivos:
                sleep(0.5)
                attach = self.driver.find_element_by_css_selector("input[type='file']")
                attach.send_keys(caminho+arquivo)
            
            sleep(1) 
            self.wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "span[data-icon='send']")))
            self.driver.find_element_by_css_selector("span[data-icon='send']").click()
      
        except Exception as e:
            print("Erro ao enviar lista de arquivos", e)
            # self.envia_msg("Erro ao anexar media")
    
            

    def ultima_msg(self):
        """ Captura a ultima mensagem da conversa """
        try:
            post = self.driver.find_elements_by_class_name("_22Msk")
            ultimo = len(post)-1
            
            # O texto da ultima mensagem
            texto = post[ultimo].find_element_by_css_selector("span.selectable-text").text
            remetente = post[ultimo].get_attribute("innerHTML").split(']')[1].split(' "><div')[0]
            
            if("Cida" in remetente and not "§" in texto ):
                return ""

            return texto
        except Exception as e:
            pass
            # print("\r Erro ao ler msg, tentando novamente!",e, end = "")

    def envia_msg(self, msg):
        """ Envia uma mensagem para a conversa aberta """
        try:
            xpath_caixa_de_texto = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]"
            # Seleciona acaixa de mensagem
            self.caixa_de_mensagem = self.driver.find_element_by_xpath(xpath_caixa_de_texto)                              
            self.driver.find_element_by_xpath(xpath_caixa_de_texto).click()

            
            for line in msg.split('\n'):
                ActionChains(self.driver).send_keys(line).perform()
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            

            # self.caixa_de_mensagem.send_keys(msg)

            # Seleciona botão enviar
            self.wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "_4sWnG")))
            self.driver.find_element_by_class_name ( "_4sWnG").click()
            return True
        except Exception as e:
            print("Erro ao enviar msg", e)
            return False
    
    def get_driver(self):
        """ Retorna o driver do selenium, para uso em testes"""
        return self.driver

    def reiniciar(self):
        """ Inicia uma nova execução do Bot e finaliza a anterior para reiniciar por completo """
        self.envia_msg("🤖 Reiniciando Bot!")
        os.startfile("inicia_bot_whats - servidor.bat")
        self.driver.quit()     
        
        sys.exit(0)

    def finalizar(self):
        """ Finaliza por completo o bot e qualquer processo python rodando"""
        self.envia_msg("Finalizando...")
        self.driver.quit()     
        lista_processos = ["python.exe"]
        for proc in psutil.process_iter():
            if proc.name() in  lista_processos:
                print(proc)
                proc.kill()
        sys.exit(0)
