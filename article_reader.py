from PyPDF2 import PdfReader
from dataclasses import dataclass

@dataclass
class ArticlePdfReader:
    """
    # Read a pdf file and extract text from it.
    
    # Example:
    reader = ArticlePdfReader(pdf_path="./downloads/1803.01944.pdf")
    
    # extract all texts
    reader.text
    
    # extract texts page by page, as generator
    reader.gen()
    """
    
    pdf_path:str
    
    def __post_init__(self):
        self.reader = PdfReader(self.pdf_path)
        self.num_pages = len(self.reader.pages)
    
    def gen(self):
        pages = self.reader.pages
        for i,page in enumerate(pages):
            text = page.extract_text()
            yield i+1, text
            
    @property    
    def text(self):
        return "\n".join([text for _, text in self.gen()])