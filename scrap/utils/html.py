import os
def save_html_content(html_content, filename):
    """
    Método para guardar el contenido HTML de un comentario en un archivo.

    Args:
    - html_content: El contenido HTML del comentario.
    - filename: El nombre del archivo donde se guardará el contenido.

    Returns:
    - True si la operación de guardado fue exitosa, False en caso contrario.
    """
    try:
        with open(filename, "w+", encoding="utf-8") as html_file:
            html_file.write(html_content)

        print("Contenido HTML guardado en '{}'".format(filename))
        return True
    except Exception as e:
        print("Ocurrió un error al guardar el contenido HTML:", e)
        return False

