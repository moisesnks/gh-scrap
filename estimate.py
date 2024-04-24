from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# URL de la página
url = "https://github.com/lumonidy-dev/lumo-pos/issues/7"

# Inicializar el navegador
driver = webdriver.Chrome()

# Cargar la página
driver.get(url)

# Esperar a que el botón "+6 more" esté presente y hacer clic en él
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '+6 more')]"))).click()

# Esperar a que la nueva información cargue completamente
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".partial-discussion-sidebar")))

# Crear un objeto BeautifulSoup con el contenido actualizado de la página
soup = BeautifulSoup(driver.page_source, "html.parser")

# Encontrar el elemento con la clase 'partial-discussion-sidebar'
partial_discussion_sidebar = soup.find(class_="partial-discussion-sidebar")

# Guardar el contenido actualizado como HTML
if partial_discussion_sidebar:
    with open("issue_7_updated.html", "w") as file:
        file.write(str(partial_discussion_sidebar))

# Cerrar el navegador
driver.quit()
