import requests
from bs4 import BeautifulSoup
from scrap.utils.markdown import html_to_markdown, save_md_content
from scrap.utils.html import save_html_content
from scrap.utils.json import save_json, md_to_json


class GitHubIssueCommentScraper:
    def __init__(self, issue_url):
        self.issue_url = issue_url

    def scrape_html_comment(self):
        """
        Método para extraer el primer comentario de una issue específica en GitHub en formato HTML.

        Returns:
        - El contenido del primer comentario en formato HTML, o None si ocurrió un error.
        """
        try:
            # Hacer una solicitud GET a la página de la issue
            response = requests.get(self.issue_url)

            # Verificar si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Parsear el contenido HTML con BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")

                # Encontrar el primer comentario
                comment_div = soup.find("div", class_="timeline-comment")

                # Extraer el contenido del primer comentario si existe
                if comment_div:
                    # Obtener el contenido del comentario en formato HTML
                    comment_html = comment_div.find("td", class_="d-block").prettify()
                    return comment_html
                else:
                    print("No se encontró ningún comentario en la issue.")
                    return None
            else:
                print("No se pudo acceder a la página de la issue")
                return None
        except Exception as e:
            print("Ocurrió un error durante la extracción del comentario HTML:", e)
            return None
        
    def fetch_comment_issue(self, filename):
        """
        Método para extraer el primer comentario de una issue específica en GitHub y guardarlo en un archivo.

        Args:
        - filename: El nombre del archivo donde se guardará el contenido del comentario.

        Returns:
        - Guarda el contenido del comentario en un archivo. Si la extensión del archivo es .html, el contenido se guardará en formato HTML. 
        Si la extensión es .md, el contenido se guardará en formato Markdown.
        Si la extensión es .json, el contenido se guardará en formato json.
        Retorna True si la operación fue exitosa.
        Sino retorna False.
        """
        # Extraer el contenido del primer comentario en formato HTML
        comment_html = self.scrape_html_comment()

        if comment_html:
            # Guardar el contenido HTML en un archivo
            if filename.endswith(".html"):
                save_html_content(comment_html, filename)
                return True
            # Guardar el contenido Markdown en un archivo
            elif filename.endswith(".md"):
                comment_md = html_to_markdown(comment_html)
                save_md_content(comment_md, filename)
                return True
            # Guardar el contenido JSON en un archivo
            elif filename.endswith(".json"):
                comment_md = html_to_markdown(comment_html)
                comment_json = md_to_json(comment_md)
                save_json(comment_json, filename)
                return True
            else:
                print("Extensión de archivo no válida. Use .html, .md o .json")
                return False
        return False
    
    def scrape_comment(self):
        """
        Método para extraer el primer comentario de una issue específica en GitHub en formato JSON.

        Returns:
        - El contenido del primer comentario en formato JSON, o None si ocurrió un error.
        """
        try:
            # Extraer el contenido del primer comentario en formato HTML
            comment_html = self.scrape_html_comment()

            if comment_html:
                # Convertir el contenido HTML a formato Markdown
                comment_md = html_to_markdown(comment_html)

                # Convertir el contenido Markdown a formato JSON
                comment_json = md_to_json(comment_md)
                return comment_json
            return None
        except Exception as e:
            print("Ocurrió un error durante la extracción del comentario JSON:", e)
            return None    
# Ejemplo de uso:
# issue_url = "https://github.com/owner/repository/issues/1"
# scraper = GitHubIssueCommentScraper(issue_url)
# scraper.fetch_comment_issue("comment.json")
