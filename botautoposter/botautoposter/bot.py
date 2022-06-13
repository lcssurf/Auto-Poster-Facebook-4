from botcity.web import WebBot, Browser
from botcity.core import DesktopBot
# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
# from botcity.maestro import *
import time
import pandas as pd
from tqdm import tqdm
import docx
import os
import sys
import mysql.connector as mysql

import logging
logging.basicConfig(
    filename = "poster.log",
    level = logging.INFO,
    format = "%(levelname)s // %(asctime)s // Linha: %(lineno)d // Arquivo: %(filename)s // Funcao: %(funcName)s // MSG: %(message)s")


# PARA LER A MSG (DOCX)

def readtxt(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


msg = readtxt('./config/msg.docx')

# Importa Tabela de Grupos
grupos_df = pd.read_excel("./config/groups.xlsx")

# Importa Tabela Config
config_df = pd.read_excel("./config/config.xlsx")
df = pd.DataFrame(config_df)
email = df.at[0, 'email']
espera = str(df.at[0, 'time'])
img = df.at[0, 'img']
licenca = df.at[0, "license"]

# enter your server IP address/domain name
HOST = "universoreabilitar.com.br"  # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "univ5173_auto_poster"
# this is the user you create
USER = "univ5173_reader"
# user password
PASSWORD = "295622"

class Bot(DesktopBot):

    def setup_images(self):
        # Add images manually to the map if we are using pyinstaller
        # pyinstaller injects the `_MEIPASS` variable into the `sys` module
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        #         # Remember to change here from `botPython` to your bot ID.
            res_path = os.path.join(sys._MEIPASS, "botautoposter", "resources")
            #         # Add all images needed to the image map
            self.add_image("acharChat", os.path.join(res_path, "acharChat.png"))
            self.add_image("addFoto_click", os.path.join(res_path, "addFoto_click.png"))
            self.add_image("addFoto2_click", os.path.join(res_path, "addFoto2_click.png"))
            self.add_image("escreverFoto_click", os.path.join(res_path, "escreverFoto_click.png"))
            self.add_image("modelo1", os.path.join(res_path, "modelo1.png"))
            self.add_image("modelo2", os.path.join(res_path, "modelo2.png"))
            self.add_image("modelo3", os.path.join(res_path, "modelo3.png"))
            self.add_image("publicar_clicar", os.path.join(res_path, "publicar_clicar.png"))
            self.add_image("publick_post_click", os.path.join(res_path, "publick_post_click.png"))
            self.add_image("start", os.path.join(res_path, "start.png"))
            self.add_image("write_somenthing_click", os.path.join(res_path, "write_somenthing_click.png"))
            self.add_image("addFoto2-219", os.path.join(res_path, "addFoto2-219.png"))
            self.add_image("photo-video-219", os.path.join(res_path, "photo-video-219.png"))
            self.add_image("escrever2-219", os.path.join(res_path, "escrever2-219.png"))
            self.add_image("pubilcar-219", os.path.join(res_path, "pubilcar-219.png"))
            self.add_image("escreverMsgText-219", os.path.join(res_path, "escreverMsgText-219.png"))
            self.add_image("modeloPhotoText-219", os.path.join(res_path, "modeloPhotoText-219.png"))
            self.add_image("addFoto-click-219", os.path.join(res_path, "addFoto-click-219.png"))
            self.add_image("escreveFoto-219", os.path.join(res_path, "escreveFoto-219.png"))
            self.add_image("addfoto2-click-219", os.path.join(res_path, "addfoto2-click-219.png"))
            self.add_image("escreverpublicacao1-219", os.path.join(res_path, "escreverpublicacao1-219.png"))
            self.add_image("modelo1-219", os.path.join(res_path, "modelo1-219.png"))
            self.add_image("acharchat-2", os.path.join(res_path, "acharchat-2.png"))

            logging.info("Leitura de imagens feita")

    # Função para adicionar foto
    def addFoto(self):
        if self.find( "addFoto_click", matching=0.97, waiting_time=10000):
            self.click()
            self.move_relative(0, -100)
            self.scroll_down(999)
            if self.find( "addFoto2_click", matching=0.97, waiting_time=10000):
                self.click()
                if self.find( "escreverFoto_click", matching=0.97, waiting_time=10000):
                    self.click()
                    self.paste(img)
                    self.enter()
    
    def addFoto_219(self):
        self.scroll_down(999)
        if self.find( "addfoto2-click-219", matching=0.97, waiting_time=10000) or self.find_text( "addFoto2-219", threshold=230, waiting_time=10000):
            self.click()
            if self.find( "escreveFoto-219", matching=0.97, waiting_time=10000):
                self.click()
                self.paste(img)
                self.enter()
                
            
        

    def action(self, execution=None):
        #logging.warning('O bot esta sendo iniciado')
        self.setup_images()

        #Busca Banco de Dados
        db_connection = mysql.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD)
            #print("Connected to:", db_connection.get_server_info())
        cursor = db_connection.cursor()
        
        try:
            #Limite de Grupos para postar
            sql = f"""
            SELECT post_limit, Plan FROM licenca WHERE license='{licenca}'
            """
            cursor.execute(sql)
            myresult = cursor.fetchall()[0]
            post_limit = myresult[0]
            my_plan = myresult[1]
            postou = 0
            
        except:
            logging.error('ocorreu um erro ao receber os parametros')

        
        
        # Configure whether or not to run on headless mode
        #self.headless = False

        # Instantiate a DesktopBot
        #desktop_bot = DesktopBot()
        # Execute operations with the DesktopBot as desired
        # desktop_bot.control_a()
        # desktop_bot.control_c()
        # desktop_bot.get_clipboard()

        # Uncomment to change the default Browser to Firefox
        # self.browser = Browser.FIREFOX

        # Uncomment to set the WebDriver path
        #self.driver_path = '/Auto Poster Facebook/chromedriver.exe'

        # Fetch the Activity ID from the task:
        # task = self.maestro.get_task(execution.task_id)
        # activity_id = task.activity_id

        # Opens the BotCity website.

        self.browse("https://www.facebook.com")

        # Espera enquanto faz o login
        while not self.find( "acharChat", matching=0.97, waiting_time=10000):
            logging.info('Esperando fazer login no Facebook')
            if self.find( "acharchat-2", matching=0.97, waiting_time=10000):
                break
            
                          
        # Entra em cada link
        for i, link in tqdm(enumerate(grupos_df['Grupos'])):

            #Coloca os limites de postagens
            if not post_limit == None:
                if postou >= post_limit:
                    logging.warning('Limite de postagens atingido! O programa foi encerrado')
                    exit()
                    
            if not postou == 0:
                time.sleep(int(espera))

            self.browse(link)
            logging.info(f'Acessou Nº: {i}; Link: {link}')
            
            try:
                # Modelo 21:9
                if self.find( "photo-video-219", matching=0.97, waiting_time=10000) or self.find( "modeloPhotoVideo-219", matching=0.97, waiting_time=10000) or self.find_text( "modeloPhotoText-219", threshold=230, waiting_time=10000):
                    self.click()
                    
                    if self.find_text( "escreverMsgText-219", threshold=230, waiting_time=10000):
                        self.click()
                        self.paste(msg)

                        #Se o Plano for Free coloca publicidade
                        if my_plan == 'Free':
                            self.paste("\nPublished by Auto Poster Facebook - https://autoposter.universoreabilitar.com.br/")

                        self.addFoto_219()
                        if self.find_text( "pubilcar-219", threshold=230, waiting_time=10000):
                            logging.info(f'Publicou no grupo Nº: {i}; Modelo: 21:9')
                            postou += 1 
                            self.click()
                    elif self.find_text( "escrever2-219", threshold=230, waiting_time=10000):
                        self.click()
                        self.paste(msg)

                        #Se o Plano for Free coloca publicidade
                        if my_plan == 'Free':
                            self.paste("\nPublished by Auto Poster Facebook - https://autoposter.universoreabilitar.com.br/")

                        self.addFoto_219()
                   
                        if self.find_text( "pubilcar-219", threshold=230, waiting_time=10000):
                            logging.info(f'Publicou no grupo Nº: {i}; Modelo: 21:9')
                            postou += 1 
                            self.click()
                            
                        
                # Modelo 1
                elif self.find( "modelo1", matching=0.97, waiting_time=10000):
                    self.click()

                    # Escrever publicaçao 1
                    if self.find( "publick_post_click", matching=0.97, waiting_time=10000):
                        self.paste(msg)
                        #Se o Plano for Free coloca publicidade
                        if my_plan == 'Free':
                            self.paste("\nPublished by Auto Poster Facebook - https://autoposter.universoreabilitar.com.br/")
                        # Add Foto
                        self.addFoto()
                        # Publicar
                        if self.find( "publicar_clicar", matching=0.97, waiting_time=10000):
                            logging.info(f'Publicou no grupo Nº: {i}; Modelo: 1, Publicacao 1')
                            postou += 1 
                            self.click()

                    # Escrever publicaçao 2
                    elif self.find( "write_somenthing_click", matching=0.97, waiting_time=10000):
                        self.paste(msg)
                        #Se o Plano for Free coloca publicidade
                        if my_plan == 'Free':
                            self.paste("\nPublished by Auto Poster Facebook - https://autoposter.universoreabilitar.com.br/")
                        # Add Foto
                        self.addFoto()
                        # Publicar
                        if self.find( "publicar_clicar", matching=0.97, waiting_time=10000):
                            logging.info(f'Publicou no grupo Nº: {i}; Modelo: 1, Publicacao 2')
                            postou += 1 
                            self.click()

                # Modelo 2
                elif self.find( "modelo2", matching=0.97, waiting_time=10000):
                    self.click()

                    # Escrever publicaçao 1
                    if self.find( "publick_post_click", matching=0.97, waiting_time=10000):
                        self.paste(msg)
                        #Se o Plano for Free coloca publicidade
                        if my_plan == 'Free':
                            self.paste("\nPublished by Auto Poster Facebook - https://autoposter.universoreabilitar.com.br/")
                        # Add Foto
                        self.addFoto()
                        # Publicar
                        if self.find( "publicar_clicar", matching=0.97, waiting_time=10000):
                            logging.info(f'Publicou no grupo Nº: {i}; Modelo: 2, Publicacao 1')
                            postou += 1 
                            self.click()
                    # Escrever publicaçao 2
                    elif self.find( "write_somenthing_click", matching=0.97, waiting_time=10000):
                        self.paste(msg)
                        #Se o Plano for Free coloca publicidade
                        if my_plan == 'Free':
                            self.paste("\nPublished by Auto Poster Facebook - https://autoposter.universoreabilitar.com.br/")
                        # Add Foto
                        self.addFoto()
                        # Publicar
                        if self.find( "publicar_clicar", matching=0.97, waiting_time=10000):
                            logging.info(f'Publicou no grupo Nº: {i}; Modelo: 2, Publicacao 2')
                            postou += 1 
                            self.click()

                # Modelo3
                elif self.find( "modelo3", matching=0.97, waiting_time=10000):
                    self.click()

                    # Escrever publicaçao 1
                    if self.find( "publick_post_click", matching=0.97, waiting_time=10000):
                        self.paste(msg)
                        #Se o Plano for Free coloca publicidade
                        if my_plan == 'Free':
                            self.paste("\nPublished by Auto Poster Facebook - https://autoposter.universoreabilitar.com.br/")
                        # Add Foto
                        self.addFoto()
                        # Publicar
                        if self.find( "publicar_clicar", matching=0.97, waiting_time=10000):
                            logging.info(f'Publicou no grupo Nº: {i}; Modelo: 3, Publicacao 1')
                            postou += 1 
                            self.click()
                    # Escrever publicaçao 2
                    elif self.find( "write_somenthing_click", matching=0.97, waiting_time=10000):
                        self.paste(msg)
                        #Se o Plano for Free coloca publicidade
                        if my_plan == 'Free':
                            self.paste("\nPublished by Auto Poster Facebook - https://autoposter.universoreabilitar.com.br/")
                        # Add Foto
                        self.addFoto()
                        # Publicar
                        if self.find( "publicar_clicar", matching=0.97, waiting_time=10000):
                            logging.info(f'Publicou no grupo Nº: {i}; Modelo: 3, Publicacao 2')
                            postou += 1 
                            self.click()
                        
            except:
                logging.critical(f'Nao encontrou modelo de publicacao, pulando grupo {i}')
                time.sleep(3)
                continue

            
                # Uncomment to mark this task as finished on BotMaestro
                # self.maestro.finish_task(
                #     task_id=execution.task_id,
                #     status=AutomationTaskFinishStatus.SUCCESS,
                #     message="Task Finished OK."
                # )

                # Wait for 10 seconds before closing
        self.wait(10000)

        # Stop the browser and clean up
        # self.stop_browser()

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()










