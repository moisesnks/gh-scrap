import json
from datetime import datetime
import re

def md_to_json(md_content):
    """
    Converts Markdown content to a JSON object using regular expressions.

    Args:
    md_content (str): The Markdown content.

    Returns:
    str: A JSON-formatted string of the Markdown content.
    """
    # Initialize the object to be returned
    task_object = {}

    # Use regular expressions to identify sections and content
    # Sections are delimited by "## "
    sections = re.split(r'\n## ', md_content)
    for section in sections:
        if not section.strip():  # Skip empty sections
            continue
        # Check for a newline character to split the title and content
        if '\n' in section:
            title, content = section.strip().split('\n', 1)
        else:
            title = section.strip()
            content = ''
        title = title.strip()
        
        # Process tasks if the title is 'Tareas'
        if 'Tareas' in title:
            # Find tasks within the section content
            tasks = re.findall(r'\* \[ \] (.+)', content)
            task_object['Tareas'] = [{"Descripción": task.strip(), "Completada": False} for task in tasks]
        # Process the observation if present
        elif title.startswith('>'):
            task_object['Observación'] = title[2:].strip()
        # Process the due date if present
        elif 'Fecha de Vencimiento' in title:
            # Extract date from the content
            due_date_text = re.search(r'\d{2}-\d{2}-\d{4}', content)
            if due_date_text:
                due_date = datetime.strptime(due_date_text.group(), '%d-%m-%Y').date()
                task_object['Fecha de Vencimiento'] = due_date.strftime("%Y-%m-%d")
        else:
            # Add the section content to the resulting object
            # Remove the '##' prefix from the title
            task_object[title[2:].strip()] = content.strip()

    # Convert the dictionary object to a JSON string
    return json.dumps(task_object, indent=4, ensure_ascii=False)

def save_json(json, filename):
    """
    Método para guardar el contenido JSON de un comentario en un archivo.

    Args:
    - json: El contenido JSON del comentario.
    - filename: El nombre del archivo donde se guardará el contenido.

    Returns:
    - True si la operación de guardado fue exitosa, False en caso contrario.
    """
    try:
        with open(filename, "w+", encoding="utf-8") as json_file:
            json_file.write(json)

        print("Contenido JSON guardado en '{}'".format(filename))
        return True
    except Exception as e:
        print("Ocurrió un error al guardar el contenido JSON:", e)
        return False