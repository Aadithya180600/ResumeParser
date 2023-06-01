import PyPDF2
import docx2txt

class Conversions:

    def __init__(self) -> None:
        self.file1 = open(r"ResumeText.txt", "w")
    
    # Method To convert PDF file to Text file
    def pdftotextconversion(self, filePath):
        
        pdffileobj = open(filePath, 'rb')

        pdfreader = PyPDF2.PdfFileReader(pdffileobj)

        x = pdfreader.numPages

        pageobj = pdfreader.getPage(0)
        text = pageobj.extractText()

        self.file1.writelines(text)
    

    # Method to convert Word Document to Text File
    def DocxToTextConversion(self, filePath):
        txt = docx2txt.process(filePath)
        text = ''
        if txt:
            text = txt.replace('\t', ' ')

        self.file1.writelines(text)
