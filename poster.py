from datetime import date
import os
import time
import webbrowser
#import pyautogui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QFormLayout, QCheckBox, QLabel, QLineEdit, QPushButton, QMenuBar, QMenu, QAction, QFileDialog
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from register import Ui_registerWindow
import sys
import mysql.connector as mysql
import pandas as pd
from tqdm import tqdm
import docx
# Selenium
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import TimeoutException
from botautoposter.botautoposter import bot
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


msg = readtxt('config/msg.docx')

# Importa Tabela de Grupos
grupos_df = pd.read_excel("config/groups.xlsx")

# Importa Tabela Config
config_df = pd.read_excel("config/config.xlsx")
df = pd.DataFrame(config_df)
email = df.at[0, 'email']
espera = str(df.at[0, 'time'])
img = df.at[0, 'img']
licenca = df.at[0, "license"]

navegador = None

# enter your server IP address/domain name
HOST = "universoreabilitar.com.br"  # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "univ5173_auto_poster"
# this is the user you create
USER = "univ5173_reader"
# user password
PASSWORD = "295622"

iniciarBot = bot.Bot()

# Interface


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load UI File
        uic.loadUi("interface/interface.ui", self)
            
        # Valores Padroes
        # self.emailEntry.setText(email)
        self.intervalEntry.setText(espera)

        # Start Button
        self.startButton.clicked.connect(self.start)
        # Start Button
        self.stopButton.clicked.connect(self.stop)

        # Menu Superior
        # Imagem
        self.actionImage.triggered.connect(self.upImagem)
        # Mensagem
        self.actionMessage.triggered.connect(self.openMessage)
        # Grupos
        self.actionGroups.triggered.connect(self.openGroups)
        # Registro Licença
        self.actionRegister.triggered.connect(self.register)
        # Help Link
        self.actionHelp.triggered.connect(self.help)
        # Top Server Link
        self.actionTop_Server_Ragnarok.triggered.connect(self.topServer)
        
        #Checkbox Termos e condições
        self.checkBox.toggled.connect(self.termosCondicoes)
        self.checkBox.setChecked(True)
        self.refresh()
        
        self.version()
        # Show App
        self.show()

    def termosCondicoes(self):
        if self.checkBox.isChecked():
            self.liberar_post(True)
            self.refresh()
            self.version()
            logging.info("Termos de uso foi marcado")
        else:
            self.liberar_post(False)
            self.refresh()
            logging.warning("Termos de uso foi desmarcado")
            
            
    #Confere se pode postar
    def liberar_post(self, pode_postar):
        if pode_postar != True:
            self.startButton.setEnabled(False)
            self.startButton.setStyleSheet("background-color:red;")
        else:
            self.startButton.setEnabled(True)
            self.startButton.setStyleSheet("background-color:rgb(103, 58, 183);")
    
    def refresh(self):
        if type(licenca) in (list, tuple, dict, str) and len(licenca) == 31:
            if img != 'Null':
                menagem_erro = self.erroLabel.setText('All Ready')
                self.erroLabel.setStyleSheet("color: green;")
                
            else:
                self.erroLabel.setText(
                    'Please input a Image at Config')
                self.liberar_post(False)
        else:
            self.erroLabel.setText(
                "Please register a valid license and restart the app")
            self.liberar_post(False)
    def version(self):      
                #Sua Versão do APP
        your_version = 4.35
        self.sua_versao.setText(f'│ Your version: {your_version}')
                
                #Versão Atual do APP
        db_connection = mysql.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD)
            #print("Connected to:", db_connection.get_server_info())
        cursor = db_connection.cursor()
        sql = """
        SELECT version FROM info
        """
        cursor.execute(sql)
        myresult = cursor.fetchone()[0]

        self.versaoatual.setText(f"│ Current version: {myresult}")
        self.liberar_post(True)

        if not your_version == myresult:
            self.sua_versao.setStyleSheet("color: red;")
            self.liberar_post(False)
                    
        try:
                #Limite de Grupos para postar
            sql = f"""
            SELECT post_limit, Plan FROM licenca WHERE license='{licenca}'
            """
            cursor.execute(sql)
            myresult = cursor.fetchall()[0]
            post_limit = myresult[0]
            my_plan = myresult[1]
            self.post_limit_label.setStyleSheet("color: green;")
            self.post_limit_label.setText(f'Your Plan: {my_plan} │ Group limit to post: {post_limit}')
            self.liberar_post(True)
        except:
            self.post_limit_label.setStyleSheet("color: red;")
            self.post_limit_label.setText('Your license not found')
            self.liberar_post(False)

    def upImagem(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imagemCaminho, _ = QFileDialog.getOpenFileName(self, "Input the Image", "",
                                                       "All Files (*)", options=options)
        if imagemCaminho:
            imageURL = imagemCaminho.replace('/', '\\')
            global img
            img = config_df.loc[0, 'img'] = imageURL
            config_df.to_excel("config/config.xlsx", index=False)
            logging.info(f'Imagem selecionada: {img}')

        self.refresh()

    # Abre arquivo da Mensagem
    def openMessage(self):
        cwd = os.getcwd()
        path = fr"{cwd}\config\msg.docx"
        os.startfile(f"{path}")
        self.refresh()
        logging.info('O arquivo de mensagem foi aberto')

    # Abre arquivo dos Grupos
    def openGroups(self):
        cwd = os.getcwd()
        path = fr"{cwd}\config\groups.xlsx"
        os.startfile(f"{path}")
        self.refresh()
        logging.info('O arquivo dos grupos foi aberto')

    # Janela de Registro de Licença
    def register(self):
        self.refresh()
        logging.info('O License Register foi aberto')
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_registerWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.refresh()

    # Abre link Help
    def help(self):
        webbrowser.open('https://autoposter.universoreabilitar.com.br/blog')
        self.refresh()
        logging.info('O link de AJUDA foi aberto')
    # Abre Link Top Server Ragnarok
    def topServer(self):
        webbrowser.open('https://autoposter.universoreabilitar.com.br')
        self.refresh()
        logging.info('O link do Auto Poster foi aberto')

    def stop(self):
        # global navegador

        # if navegador:
        #     navegador.close()
        #     navegador = None

        self.refresh()
        logging.warning('O programa foi finalizado')
        exit()

    def start(self):
        self.refresh()

        logging.warning('O bot irá iniciar')

        #global navegador
        # connect to MySQL server
        db_connection = mysql.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        #print("Connected to:", db_connection.get_server_info())
        data_atual = date.today()

        sql = f"""
        SELECT license, fim FROM licenca WHERE license='{licenca}' 
        """
        cursor = db_connection.cursor()
        cursor.execute(sql)
        myresult = cursor.fetchall()

        if myresult:
            for license, fim in myresult:
                licensa, data_final = license, fim
            if data_atual < data_final:
                logging.info('A data da licenca esta correta')
                # inicia bot
                iniciarBot.action()
        else:
            menagem_erro = self.erroLabel.setText('Invalid License')
            self.erroLabel.setStyleSheet("color: red; font-size: 14px;")
            logging.warning('Licenca Invalida')

        # Define as variaveis da interface
        #email = self.emailEntry.text()
        #senha = self.passwordEntry.text()
        #espera = self.intervalEntry.text()

        # if len(email) == 0 or len(senha) == 0:
        #self.erroLabel.setText("Please input all fields")
        # else:
        # Atualiza os Dados Padroes da Config
        #config_df.loc[0, 'email'] = email
        #config_df.loc[0, 'time'] = int(espera)
        #config_df.to_excel("config/config.xlsx", index=False)

        # DESABILITA POP UP
        #chrome_options = webdriver.ChromeOptions()
        #prefs = {"profile.default_content_setting_values.notifications": 2}
        #chrome_options.add_experimental_option("prefs", prefs)

        # if not navegador:
        #     # Cria Navegador
        #     navegador = webdriver.Chrome(chrome_options=chrome_options,
        #                                  service=Service(ChromeDriverManager().install()))
        #     # Acessa o facebook
        #     navegador.get("https://www.facebook.com")

        #     wait = WebDriverWait(navegador, 10)

        #     wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))).send_keys(email)
        #     wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pass"]'))).send_keys(senha, Keys.ENTER)

        #     #Autenticação de dois fatores
        #     # while len(navegador.find_element(By.ID, 'ssrb_root_start')) > 1:
        #     #     time.sleep(1)

        #     for i, link in tqdm(enumerate(grupos_df['Grupos'])):
        #         time.sleep(2)
        #         navegador.get(link)
        #         time.sleep(2)

        #         try:
        #             # modelo1
        #             # O programa clica no "criar publicação
        #             crie_publicacao = navegador.find_element_by_xpath(
        #                 '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[1]/span')
        #             post_input = crie_publicacao.find_element_by_xpath('..')
        #             post_input.click()
        #             time.sleep(15)

        #         except Exception as erro:
        #             print(f'Deu ruim, o erro foi {erro.__class__}')
        #             continue


# Inicia App
app = QApplication(sys.argv)
UIWindow = UI()
sys.exit(app.exec_())
