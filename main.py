# main.py
from scrap.github_issue_comment import GitHubIssueCommentScraper
from scrap.github_issues import GitHubIssueScraper
import os

def get_all_issues(issues_url, output_dir="output"):
    """
    Función para obtener todas las issues de un repositorio en GitHub y guardar sus comentarios.

    Args:
    - issues_url: La URL de la página de GitHub que contiene las issues.
    - output_dir: Directorio de salida donde se guardarán los archivos. Por defecto, "output".
    """
    try:
        # Crear el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        output_issues_dir = os.path.join(output_dir, "issues")
        os.makedirs(output_issues_dir, exist_ok=True)

        # Crear una instancia de GitHubIssueScraper y extraer las issues
        issue_scrapper = GitHubIssueScraper(issues_url)
        issues = issue_scrapper.scrape_issues() # list or None

        if issues:
            # Guardar las issues en un archivo JSON
            issues_filename = os.path.join(output_dir, "issues.json")

            # Recorrer las issues y extraer el primer comentario de cada una de ellas
            for issue in issues:
                index = issue["issue_number"]
                issue_url = f"{issues_url}/{index}"
                comment_scrapper = GitHubIssueCommentScraper(issue_url)
                comment_json = comment_scrapper.scrape_comment()
                if comment_json:
                    # Guardar el contenido JSON del comentario en un archivo
                    filename = os.path.join(output_issues_dir, f"issue_{index}_comment.json")
                    comment_scrapper.fetch_comment_issue(filename)
                else:
                    print(f"No se pudo extraer el comentario de la issue {index}")

            # Guardar las issues en un archivo JSON después de haber obtenido los comentarios
            issue_scrapper.fetch_issues(issues_filename)
            print("Proceso completado exitosamente.")
        else:
            print("No se pudieron extraer las issues.")
    except Exception as e:
        print("Ocurrió un error durante la extracción de las issues:", e)


if __name__ == "__main__":
    issues_url = "https://github.com/tssw2024/sprint-2/issues"
    GitHubIssueScraper(issues_url).fetch_issues("issues.json")
    

   
