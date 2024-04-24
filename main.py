# main.py

# Importar la clase GitHubIssueCommentScraper del módulo github_issue_comment
from scrap.github_issue_comment import GitHubIssueCommentScraper

# Importar la clase GitHubIssueScraper
from scrap.github_issues import GitHubIssueScraper

def main():
    
    # URL de la página de GitHub que contiene las issues
    issues_url = "https://github.com/TSSW2024/sprint-2/issues"
    
    # Crear una instancia de GitHubIssueScraper y extraer las issues
    issue_scrapper = GitHubIssueScraper(issues_url)
    issues = issue_scrapper.scrape_issues() # list or None

    if issues:
        # Recorrer las issues y extraer el primer comentario de cada una de ellas. La key que nos lleva al issue es "issue_number"
        for issue in issues:
            index = issue["issue_number"]
            issue_url = f"{issues_url}/{index}"
            comment_scrapper = GitHubIssueCommentScraper(issue_url)
            comment_json = comment_scrapper.scrape_comment()
            if comment_json:
                # Guardar el contenido JSON del comentario en un archivo
                filename = f"output/issues/issue_{index}_comment.json"
                comment_scrapper.fetch_comment_issue(filename)
            else:
                print(f"No se pudo extraer el comentario de la issue {index}")
        issue_scrapper.fetch_issues("output/issues.json")
    else:
        print("No se pudieron extraer las issues")

            
    

     

if __name__ == "__main__":

    main()
