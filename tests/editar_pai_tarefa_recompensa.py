from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuração Global ---
APP_URL = "https://appoia-app.glide.page/"
EMAIL_PAI = "appoiaapp@gmail.com"

# --- Função de Login ---
def login_com_codigo(driver):
    driver.get(APP_URL)
    print("Acessando a página de login...")
    try:
        campo_email = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="wf-input"]')))
        campo_email.send_keys(EMAIL_PAI)
        print("SUCESSO: E-mail inserido.")
        botao_enviar_codigo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Continue']")))
        botao_enviar_codigo.click()
        print("SUCESSO: Botão 'Continue' foi clicado. Verifique seu e-mail.")
        codigo_acesso = input("\n>>> Por favor, verifique seu e-mail e insira o código de acesso aqui: ")
        campo_codigo = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="tel"]')))
        campo_codigo.send_keys(codigo_acesso)
        print("SUCESSO: Código inserido na página.")
        botao_signin = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sign In')]")))
        botao_signin.click()
        print("SUCESSO: Botão 'Sign In' clicado.")
        time.sleep(5)
        print("SUCESSO: Login realizado.\n")
    except Exception as e:
        print(f"FALHA no login. Erro: {e}")
        driver.quit()
        exit()

# --- Função de Teste para Páginas com URL Direta e Botão 'Editar' ---
def testar_edicao_direta(driver, nome_teste, url_item, dados_para_editar, seletor_botao_editar, seletor_botao_salvar):
    print(f"--- INICIANDO TESTE: {nome_teste} ---")
    try:
        driver.get(url_item)
        print(f"Acessando item em: {url_item}")
        
        botao_editar = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor_botao_editar)))
        botao_editar.click()
        print("SUCESSO: Botão 'Editar' clicado.")
        
        print("Preenchendo formulário...")
        for tipo_seletor, seletor, novo_valor in dados_para_editar:
            campo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((tipo_seletor, seletor)))
            campo.clear()
            campo.send_keys(novo_valor)
            print(f"  - Campo '{seletor}' preenchido.")

        botao_salvar = driver.find_element(By.CSS_SELECTOR, seletor_botao_salvar)
        driver.execute_script("arguments[0].click();", botao_salvar)
        print(f"SUCESSO: Botão Salvar ('{seletor_botao_salvar}') clicado.")
        print(f"VERIFICAÇÃO CONCLUÍDA: {nome_teste} executado com sucesso!")
    except Exception as e:
        print(f"FALHA no teste '{nome_teste}'. Verifique se a URL e os seletores estão corretos. Erro: {e}")
    print(f"--- TESTE FINALIZADO: {nome_teste} ---\n")

# --- Execução Principal ---
if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.maximize_window()
    login_com_codigo(driver)

    # === [PAI] - Editar Tarefa (Campos do formulário ATUALIZADOS) ===
    testar_edicao_direta(
        driver,
        nome_teste="[PAI] - Editar Tarefa",
        url_item="https://appoia-app.glide.page/dl/a400f7/s/b5b7e7/r/UsyRKe-qQTe1wz0R3PG6zA",
        seletor_botao_editar='button[aria-label="Editar Tarefa"]',
        dados_para_editar=[
            (By.XPATH, '(//textarea[@data-testid="wf-input"])[1]', "Estudar para a prova de Geografia"),
            (By.XPATH, '(//textarea[@data-testid="wf-input"])[2]', "Ler o capítulo sobre Mapas"),
            (By.CSS_SELECTOR, 'input[type="number"]', "80"),
            (By.XPATH, '(//textarea[@data-testid="wf-input"])[3]', "Prova Estudo")
        ],
        seletor_botao_salvar='button[aria-label="Submit"]'
    )

    # === [PAI] - Editar Recompensa (Campos do formulário ATUALIZADOS) ===
    testar_edicao_direta(
        driver,
        nome_teste="[PAI] - Editar Recompensa",
        url_item="https://appoia-app.glide.page/dl/da19fa/s/78dceb/r/a.cZbq77ZSF2EQGnvZ26Tgg",
        seletor_botao_editar='button[aria-label="Editar"]',
        dados_para_editar=[
            (By.XPATH, '(//textarea[@data-testid="wf-input"])[1]', "Uma hora de videogame"),
            (By.XPATH, '(//textarea[@data-testid="wf-input"])[2]', "Pode jogar qualquer jogo do console"),
            (By.CSS_SELECTOR, 'input[type="number"]', "35")
        ],
        seletor_botao_salvar='button[aria-label="Submit"]'
    )
    
    print("\nTodos os testes foram concluídos.")
    driver.quit()