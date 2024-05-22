import os
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import csv

nltk.download('punkt')
nltk.download('stopwords')


def extract_keywords_from_pdf(pdf_folder,keywords):
    # Abre el archivo PDF
    with open(pdf_folder, 'rb') as file:
        # Crea un objeto de lectura PDF
        reader = PyPDF2.PdfReader(file)
        
        # Inicializa una cadena vacía para almacenar el texto extraído
        text = ''
        
        # Itera sobre cada página del PDF
        for page_num in range(len(reader.pages)):
            # Extrae el texto de la página actual
            text += reader.pages[page_num].extract_text()
    
    # Tokeniza el texto y elimina las palabras vacías (stop words) en español
    tokens = word_tokenize(text, language='spanish')
    stop_words = set(stopwords.words('spanish'))
    filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words and not word.isdigit()]
    
    # Calcula la frecuencia de cada palabra
    word_freq = Counter(filtered_tokens)
    
    # Palabras a buscar
    #keywords = 'ibs,eibs,tester,prueba,pruebas,istqb,sql,banco,sistemas,software,datapro'  # Palabras que se quieren consultar
    words_to_check_list = [word.strip() for word in keywords.split(',')]
    
    # Lista para almacenar los resultados
    results = []
    
    # Imprimir la frecuencia de cada palabra
    for word_to_check in words_to_check_list:
        if word_to_check.lower() in word_freq or word_to_check in word_freq:
            # Agregar el resultado a la lista
            results.append((word_to_check, 1))
        else:
            results.append((word_to_check, 0))
    
    return results

#**************************************************
# LLAMADO DE LA FUNCION
#*************************************************
# Carpeta que contiene los archivos PDF
def filter_candidate(path, destination, *args):
    # carpeta_pdf = 'C:\\Users\\Franklin Perez\\Downloads\\TESTER'
    # Palabras Clave que se quieren consultar
    # keywords = 'sql,plsql,dataclean,analista,dato,testing' 
    #Archivo de salida
    # resultFile = 'resultadosTester5.csv'

    # Lista para almacenar los resultados finales
    resultados_finales = []
    processed_args = "".join(args)

    # Iterar sobre los archivos PDF en la carpeta
    for archivo in os.listdir(path):
        if archivo.endswith('.pdf'):
            # Extraer palabras clave del archivo PDF
            resultados = extract_keywords_from_pdf(os.path.join(path, archivo), processed_args)

            # Agregar el nombre del archivo a los resultados
            for resultado in resultados:
                resultados_finales.append((archivo, resultado[0], resultado[1]))

    # # Escribir los resultados en un archivo CSV
    with open(destination, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        # Escribir encabezados
        writer.writerow(['Candidato', 'keyword', 'total'])

    #     # Escribir resultados
        for resultado_final in resultados_finales:
            writer.writerow(resultado_final)

    print("Se han guardado los resultados en: " + destination)
    return resultados_finales