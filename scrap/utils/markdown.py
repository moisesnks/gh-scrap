import re
import json
from datetime import datetime
from bs4 import BeautifulSoup

def html_to_markdown(html):
    # Analizar el HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Inicializar una cadena para almacenar el markdown generado
    markdown = ''
    current_header = None

    # Recorrer todos los elementos dentro de <td class="d-block comment-body markdown-body js-comment-body">
    for element in soup.select('td.d-block.comment-body.markdown-body.js-comment-body > *'):
        if element.name == 'h2':
            # Si el elemento es un encabezado <h2>, actualizar el encabezado actual
            current_header = element.get_text(strip=True)
            markdown += '## ' + current_header + '\n\n'
        elif element.name == 'p':
            # Si el elemento es un párrafo, agregarlo debajo del encabezado actual
            if current_header:
                markdown += element.get_text(strip=True) + '\n\n'
        elif element.name == 'ul' and 'contains-task-list' in element.get('class', []):
            # Si el elemento es una lista de tareas, agregar cada tarea debajo del encabezado actual
            if current_header:
                for li in element.find_all('li'):
                    markdown += '* [ ] ' + li.get_text(strip=True) + '\n'
        elif element.name == 'blockquote':
            # Si el elemento es un blockquote, agregarlo al markdown
            markdown += '> ' + element.get_text(strip=True) + '\n\n'

    return markdown

def save_md_content(md_content, filename):
    """
    Método para guardar el contenido Markdown de un comentario en un archivo.

    Args:
    - md_content: El contenido Markdown del comentario.
    - filename: El nombre del archivo donde se guardará el contenido.

    Returns:
    - True si la operación de guardado fue exitosa, False en caso contrario.
    """
    try:
        with open(filename, "w+", encoding="utf-8") as md_file:
            md_file.write(md_content)

        print("Contenido Markdown guardado en '{}'".format(filename))
        return True
    except Exception as e:
        print("Ocurrió un error al guardar el contenido Markdown:", e)
        return False




