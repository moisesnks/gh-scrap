import requests
from bs4 import BeautifulSoup
from scrap.utils.markdown import html_to_markdown, save_md_content
from scrap.utils.html import save_html_content
from scrap.utils.json import save_json, md_to_json
import json


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
        
    def scrape_project_info(self):
        """
        Método para obtener la información del proyecto desde un comentario en una issue de GitHub.
        """
        try:
            # Realizar la solicitud GET a la página de la issue
            response = requests.get(self.issue_url)

            # Parsear el contenido HTML con BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Encontrar el elemento con el ID 'discussion_bucket'
            discussion_bucket = soup.find(id="discussion_bucket")
            layout_div = discussion_bucket.find("div", class_="Layout")
            layout_sidebar = layout_div.find("div", class_="Layout-sidebar")
            desired_div = layout_sidebar.select_one("div:nth-child(3)")
            collapsible_widget = desired_div.find('collapsible-sidebar-widget')
            
            if collapsible_widget:
                url = collapsible_widget['url']
                newUrl = "https://github.com" + url
                newSoup = BeautifulSoup(requests.get(newUrl).text, "html.parser")

                # Buscar todos los elementos <li> dentro de newSoup, excluyendo los últimos 3
                items = newSoup.find_all('li')[:-3]

                data = {}

                for item in items:
                    label = item.find('label').get_text(strip=True)
                    value = item.find('div', class_='form-group-body').find('span').get_text(strip=True)
                    data[label] = value

                # Limpiar la información del proyecto
                project_info = self.clean_project_info(data)
                return project_info
            else:
                print(f"No se encontró ningún widget collapsible en la página {self.issue_url}")
                return None
        except Exception as e:
            print("Ocurrió un error durante la extracción de la información del proyecto:", e)
            return None

    def clean_project_info(self, project_info):
        """
        Método para limpiar la información del proyecto obtenida de la página de GitHub.
        Reemplaza los valores no deseados por cadenas vacías.

        Args:
        - project_info: El diccionario de información del proyecto obtenido de la página de GitHub.

        Returns:
        - El diccionario de información del proyecto limpio.
        """
        # Definir los valores no deseados que se deben reemplazar por cadenas vacías
        unwanted_values = ["Choose an option ...", "Enter a number ..."]

        # Recorrer el diccionario de información del proyecto y reemplazar los valores no deseados
        for key, value in project_info.items():
            if value in unwanted_values:
                project_info[key] = ""

        return project_info

        
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
                comment_json_str = md_to_json(comment_md)
                
                # Convertir la cadena JSON a un diccionario
                comment_json = json.loads(comment_json_str)
                
                # Obtener la información del proyecto
                project_info = self.scrape_project_info()

                if project_info:
                    comment_json["project_info"] = project_info
                else:
                    print("No se pudo obtener la información del proyecto.")
                
                # Convertir el diccionario a una cadena JSON nuevamente
                comment_json_str = json.dumps(comment_json, indent=4, ensure_ascii=False)
                
                # Guardar la cadena JSON en un archivo
                save_json(comment_json_str, filename)
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
