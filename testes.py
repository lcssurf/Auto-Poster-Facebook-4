import mysql.connector as mysql
import pandas as pd
from tqdm import tqdm
import docx

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


msg = readtxt('msg.docx')
print(msg)

# # Importa Tabela de Grupos
# grupos_df = pd.read_excel("config/groups.xlsx")

# # Importa Tabela Config
# config_df = pd.read_excel("Auto-Poster/config/config.xlsx")
# df = pd.DataFrame(config_df)
# email = df.at[0, 'email']
# espera = str(df.at[0, 'time'])
# img = df.at[0, 'img']
# licenca = df.at[0, "license"]

# print(espera)