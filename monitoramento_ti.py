import os
import csv
from datetime import datetime
import platform
import time
import smtplib
from email.mime.text import MIMEText

# Configurações de e-mail
EMAIL_REMETENTE = ""
EMAIL_SENHA = ""
EMAIL_DESTINATARIO = ""


def enviar_email(host, status):
    assunto = f"[ALERTA] {host} está {status}"
    corpo = f"O ativo {host} foi verificado como {status} em {datetime.now()}"

    msg = MIMEText(corpo)
    msg["Subject"] = assunto
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINATARIO

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        servidor.quit()
        print(f"Email enviado para {EMAIL_DESTINATARIO} sobre {host} {status}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")


def verificar_disponibilidade(host):
    sistema = platform.system()

    if sistema == "Windows":
        resposta = os.system(f"ping -n 1 {host} > nul")
    else:
        resposta = os.system(f"ping -c 1 {host} > /dev/null 2>&1")

    status = "ONLINE" if resposta == 0 else "OFFLINE"
    print(f"{host} está {status}")
    salvar_log(host, status)

    if status == "OFFLINE":
        enviar_email(host, status)


def salvar_log(host, status):
    arquivo_existe = os.path.isfile("log_monitoramento.csv")
    with open("log_monitoramento.csv", "a", newline="") as arquivo:
        writer = csv.writer(arquivo)
        if not arquivo_existe:
            writer.writerow(["Data/Hora", "Host", "Status"])
        writer.writerow([datetime.now(), host, status])


# Lista de ativos para monitoramento
ativos = ["google.com", "github.com", "8.8.8.8"]

print("Iniciando Monitoramento de Ativos de TI")
while True:
    for ativo in ativos:
        verificar_disponibilidade(ativo)
    print("Aguardando 60 segundos para nova verificação...\n")
    time.sleep(60)
