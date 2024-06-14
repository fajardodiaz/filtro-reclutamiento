import os
from PyPDF2 import PdfMerger

class PDFMerger:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.merger = PdfMerger()

    def merge_pdfs(self):
        pdf_files = sorted([f for f in os.listdir(self.folder_path) if f.endswith('.pdf')])
        for pdf_file in pdf_files:
            file_path = os.path.join(self.folder_path, pdf_file)
            self.merger.append(file_path)

        merged_file_path = os.path.join(self.folder_path, 'InfosgroupCopa.pdf')
        self.merger.write(merged_file_path)
        self.merger.close()

        return merged_file_path

# Ejemplo de uso
folder_path = 'C:\\Temp'
pdf_merger = PDFMerger(folder_path)
merged_pdf_path = pdf_merger.merge_pdfs()
print(f'Se ha creado el archivo fusionado en: {merged_pdf_path}')