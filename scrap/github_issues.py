import requests
from bs4 import BeautifulSoup
import json
import re
from scrap.github_issue_comment import GitHubIssueCommentScraper

class GitHubIssueScraper:
    def __init__(self, url):
        self.url = url

    def scrape_issues(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                issues_divs = soup.find_all("div", class_="flex-auto min-width-0 p-2 pr-3 pr-md-2")
                issues_data = []

                for issue_div in issues_divs:
                    title_anchor = issue_div.find("a", class_="Link--primary")
                    title = title_anchor.text.strip()
                    tag = ""
                    if title.startswith("(") and ")" in title:
                        tag, title = title.split(") ", 1)
                        tag = tag[1:]  # Eliminar el paréntesis inicial
                    issue_number = re.search(r'\d+', issue_div.find("span", class_="opened-by").text.strip()).group()
                    opened_by = issue_div.find("a", class_="Link--muted").text.strip()
                    opened_date = issue_div.find("relative-time").text.strip()

                    # Obtener la cantidad de tareas
                    tasks_span = issue_div.find("span", class_="text-normal no-wrap mr-1 ml-1")
                    num_tasks = tasks_span.text.split()[0] if tasks_span else "0"

                    # Obtener el project_info de la issue
                    issue_url = f"{self.url}/{issue_number}"
                    comment_scraper = GitHubIssueCommentScraper(issue_url)
                    project_info = comment_scraper.scrape_project_info()

                    # Crear un diccionario con los datos de la issue
                    issue_info = {
                        "title": title,
                        "tag": tag,
                        "issue_number": issue_number,
                        "opened_by": opened_by,
                        "opened_date": opened_date,
                        "num_tasks": num_tasks,
                        "project_info": project_info if project_info else "No project info found."
                    }
                    issues_data.append(issue_info)

                return issues_data
            else:
                print("No se pudo acceder a la página web")
                return None
        except Exception as e:
            print("Ocurrió un error durante el scraping:", e)
            return None

    def save_issues_to_json(self, issues_data, filename):
        """
        Método para guardar los datos de las issues en un archivo JSON.

        Args:
        - issues_data: Una lista de diccionarios, donde cada diccionario contiene los datos de una issue.
        - filename: El nombre del archivo JSON donde se guardarán los datos.

        Returns:
        - True si la operación de guardado fue exitosa, False en caso contrario.
        """
        try:
            # Convertir la lista de datos de issues a formato JSON
            json_data = json.dumps(issues_data, indent=4, ensure_ascii=False)

            # Guardar el JSON en un archivo
            with open(filename, "w+", encoding="utf-8") as json_file:
                json_file.write(json_data)

            print("Resultados guardados en '{}'".format(filename))
            return True
        except Exception as e:
            print("Ocurrió un error al guardar los datos:", e)
            return False

    def fetch_issues(self, json_filename="github_issues.json"):
        """
        Método para extraer los datos de las issues de una página de GitHub y guardarlos en un archivo JSON.

        Returns:
        - El nombre del archivo JSON donde se guardaron los datos de las issues, o None si ocurrió un error.
        """
        try:
            issues_data = self.scrape_issues()
            if issues_data is not None:
                filename = json_filename
                if self.save_issues_to_json(issues_data, filename):
                    return filename
            return None
        except Exception as e:
            print("Ocurrió un error:", e)
            return None

# Ejemplo de uso:
# url = "https://github.com/owner/repository/issues"
# scraper = GitHubIssueScraper(url)
# scraper.fetch_issues()
