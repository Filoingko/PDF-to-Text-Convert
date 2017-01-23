from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox,LTChar, LTFigure
import sys

storeobjects = []

class PdfMinerWrapper(object):

    def __init__(self, pdf_doc, password):
        self.pdf_doc = pdf_doc
        self.pdf_pwd = password
 
    def __enter__(self):
        #open the pdf file
        self.fp = open(self.pdf_doc, 'rb')
        # create a parser object associated with the file object
        parser = PDFParser(self.fp)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument(parser, password=self.pdf_pwd)
        # connect the parser and document objects
        parser.set_document(doc)
        self.doc=doc
        return self
    
    def _parse_pages(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams(char_margin=3.5, all_texts = True)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
    
        for page in PDFPage.create_pages(self.doc):
            interpreter.process_page(page)
            # receive the LTPage object for this page
            layout = device.get_result()
            # layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
            yield layout
    def __iter__(self): 
        return iter(self._parse_pages())
    
    def __exit__(self, _type, value, traceback):
        self.fp.close()
            
def main(path, password):
    text = ''
    with PdfMinerWrapper(path , password) as doc:
        for page in doc:     
            #print 'Page no.', page.pageid     
            for tbox in page:
                if not isinstance(tbox, LTTextBox):
                    continue
                if isinstance(tbox, LTTextBox):
                    #print('\n')
                    text = text + '\n'
                for obj in tbox: 
                    storeobjects.append(obj)
                    #print type(obj);
                    for c in obj : 
                        #c.fontname
                        if not isinstance(c, LTChar):
                            continue
                        text = text + c.get_text()
                        #sys.stdout.write(c.get_text())

    return text