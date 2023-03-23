import arxiv
from dataclasses import dataclass
from database import SuperBase
from models import create_article_meta, ArticleCrud
import os

@dataclass
class ArxivController:
    """
    # you are going to create a sqlite database named arxiv.db
    # you are going to download pdf files into folder ./downloads
    ar = ArxivController(database_name="arxiv", 
        download_path="./downloads")

    # search for arxiv papers user query `deep learning`
    ar.search_articles(query="deep learning")

    # save articles and download pdf files
    ar.save_download()
    """


    database_name:str = 'arxiv'
    download_path:str = './downloads'

    def __post_init__(self):
        self.superbase = SuperBase(self.database_name)
        self.ArticleMeta = create_article_meta(self.superbase)
        self.article_crud = ArticleCrud(self.superbase, self.ArticleMeta)
        self.superbase.Base.metadata.create_all(bind=self.superbase.engine)
        self.search = None
        os.makedirs(self.download_path, exist_ok=True)

    def search_articles(self, 
               query:str,
               id_list:list = None, 
               max_results:int = 10, 
               sort_by = arxiv.SortCriterion.Relevance,
               sort_order = arxiv.SortOrder.Descending):
        
        search = arxiv.Search(
            query=query,
            id_list= [] if id_list is None else id_list,
            max_results= max_results,
            sort_by= sort_by,
            sort_order= sort_order
        )
        self.search = search

    def save_download(self):
        for result in self.search.results():

            print("Downloading pdf {}".format(result.pdf_url))
            pdf_path = result.download_pdf(dirpath=self.download_path)
            pdf_path = os.path.abspath(pdf_path)

            article_meta = self.ArticleMeta(
                entry_id=result.entry_id,
                updated=result.updated,
                published=result.published,
                title=result.title,
                authors=', '.join([a.name for a in result.authors]),
                summary=result.summary,
                comment=result.comment,
                journal_ref=result.journal_ref,
                doi=result.doi,
                primary_category=result.primary_category,
                categories=', '.join([c for c in result.categories]),
                links=', '.join([l.href for l in result.links]),
                pdf_url=result.pdf_url,
                pdf_path = pdf_path
            )
            

            self.article_crud.create(article_meta)


if __name__ == "__main__":
    ar = ArxivController()
    ar.search_articles(query="deep learning")
    ar.save_download()