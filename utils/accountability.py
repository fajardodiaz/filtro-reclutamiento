import pandas as pd
import os

def is_integer(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

"""
        ESTA FUNCIÓN OBTIENE LOS CODIGOS DE EMPLEADO DEL ARCHIVO DE PLANILLA Y LOS COMPARA
        CON LOS ARCHIVOS DE SOPORTE PARA DESCUBRIR SI FALTA UN CODIGO DE EMPLEADO EN LOS SOPORTES
        
        :param reference_file_path: Nombre del archivo de PLANILLA principal
        :param other_files: Lista de los archivos de soporte a comparar
"""
def compare_codes(reference_file_path, *other_files):

    # Leer el archivo Excel de planilla
    try:
        reference_df = pd.read_excel(reference_file_path, sheet_name=0)
    except Exception as e:
        return f"No se pudo leer el archivo: {e}"
    
    # Validar los campos de la primera pestaña del archivo de planilla
    columnas_esperadas = ["Codigo de empleado", "Nombre de empleado", "Facturable", "Cliente / Proyecto"]
    if not all(col in reference_df.columns for col in columnas_esperadas):
        return "Los campos no coinciden. Los campos esperados son: 'Codigo de empleado', 'Nombre de empleado', 'Facturable', 'Cliente / Proyecto'"

    # Se extraen los códigos de empleado del archivo de planilla
    reference_codes = set(filter(lambda x: x is not None, reference_df['Codigo de empleado'].dropna().map(is_integer)))

    # Leer y comparar los otros archivos
    not_found_codes = reference_codes.copy()

    for file in other_files:
        # Obtener los nombres de las pestañas del archivo actual
        try:
            sheet_names = pd.ExcelFile(file).sheet_names
        except Exception as e:
            return f"No se pudo leer las pestañas del archivo {file}: {e}"
        
        # Leer cada pestaña y extraer los códigos
        for sheet in sheet_names:
            df = pd.read_excel(file, sheet_name=sheet)
            file_codes = set(filter(lambda x: x is not None, df.iloc[:, 1].dropna().map(is_integer)))
            not_found_codes -= file_codes

    # Agregar la columna "ExisteEnSoporte" al DataFrame de referencia
    reference_df['ExisteEnSoporte'] = reference_df['Codigo de empleado'].map(lambda x: 'NO' if x in not_found_codes else 'SI')
    
    return reference_df
"""
*********************
*Llamada a la función
*********************
"""
# # Directorio donde se encuentran los archivos de Excel
# directory_path = 'C:\\Temp\\Contabilidad'

# # Nombre del archivo de PLANILLA principal
# reference_file = 'Listado de colaboradores por planilla 2024.xlsx'

# # Lista de los archivos de soporte a comparar
# other_files = ['Soporte1.xlsx','Soporte2.xlsx']

# # Ruta completa de los archivos
# reference_file_path = os.path.join(directory_path, reference_file)
# other_files_paths = [os.path.join(directory_path, file) for file in other_files]

# # Ejecutar la comparación
# dfPlanilla = compare_codes(reference_file_path, *other_files_paths)

# dfPlanilla.to_csv('C:\\Temp\\Contabilidad\\resultado.csv',sep=';')