from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def iniciar_driver():
    service = Service(executable_path="geckodriver")
    return webdriver.Firefox(service=service)

def login(driver):
    driver.get("https://appoia-app.glide.page")

    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "is-signin")))

    campo_email = driver.find_element(By.CLASS_NAME, "is-signin")
    campo_email.clear()
    campo_email.send_keys("appoiaapp@gmail.com" + Keys.ENTER)

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "is-signin")))

    codigo = input("Código recebido no email: ")
    campo_codigo = driver.find_element(By.CLASS_NAME, "is-signin")
    campo_codigo.clear()
    campo_codigo.send_keys(codigo + Keys.ENTER)

def navegar_para_tarefas(driver):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Definir Tarefas')]"))
    )
    botao_tarefas = driver.find_element(By.XPATH, "//span[contains(text(), 'Definir Tarefas')]/ancestor::button")
    botao_tarefas.click()

def abrir_primeira_tarefa(driver):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='collection-item-0']"))
    )
    detalhes_tarefa = driver.find_element(By.CSS_SELECTOR, "[data-testid='collection-item-0']")
    detalhes_tarefa.click()

def finalizar_tarefa(driver):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Finalizar Tarefa']"))
    )
    botao_finalizar = driver.find_element(By.XPATH, "//button[@aria-label='Finalizar Tarefa']")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", botao_finalizar)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", botao_finalizar)

def main():
    driver = iniciar_driver()
    try:
        login(driver)
        navegar_para_tarefas(driver)
        abrir_primeira_tarefa(driver)
        finalizar_tarefa(driver)

        time.sleep(20)  # Só para visualização antes de fechar
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
