#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import subprocess
import os
import time
from urllib.parse import urlparse        

def mostrar_menu():
    
    color_reset = "\033[0m"  # Restablecer el color
    # Colores básicos
    color_azul = "\033[94m"
    color_verde = "\033[92m"
    color_amarillo = "\033[33m"
    color_magenta = "\033[35m"
    color_cyan = "\033[36m"
    color_rojo = "\033[91m"
    color_reset = "\033[0m"
    color_dit = "\033[1m\033[91m"

    print(color_azul + "Contacto Telegram: @Shadow_Eminencie")
    print(color_rojo + """
  ____  _               _
 / ___|| |__   __ _  __| | _____      __
 \___ \| '_ \ / _` |/ _` |/ _ \ \ /\ / /
  ___) | | | | (_| | (_| | (_) \ V  V /
 |____/|_| |_|\__,_|\__,_|\___/ \_/\_/
    """)
    print(color_verde + "V= 1.0                      𝙎𝙃𝘼𝘿𝙊𝙒_𝙀𝙈𝙄𝙉𝙀𝙉𝘾𝙄𝙀    " + color_reset)
    print("")
    print(color_cyan + "1. Extractor de Host ")
    print("2. Extractor de Subdominios ")
    print("3. Extractor de dominios DNS ")
    print("4. Verificar el estado de Host ")
    print("5. Generador de payload Pro ")
    print("6. Ver puertos abiertos ")
    print("7. Geolocalizacion por IP")
    print("8. Mas informacion y creditos")
    print("0. Salir" + color_reset)
    print("")


def extraer_links():
    url = input("\033[1;32mIngresar Host: ")
    if not url.startswith("http"):
        url = "http://" + url

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        href_regex = re.compile(r'href=[\'|"](.*?)[\'"]')
        href_matches = re.findall(href_regex, response.text)
        unique_urls = set()

        for href in href_matches:
            if href.startswith("http"):
                unique_urls.add(href)
            elif href.startswith("/"):
                unique_urls.add(url + href)
            else:
                unique_urls.add(url + "/" + href)

        sorted_urls = sorted(unique_urls)
        for url in sorted_urls:
            print(url)

        guardar_archivo(sorted_urls)
    else:
        print("Error al acceder a la URL.")


def guardar_archivo(urls):
    archivo = "hosts.txt"
    with open(archivo, 'w') as file:
        for url in urls:
            file.write(url + '\n')
            
    print("")
    print("Los resultados se han guardado en el archivo:", archivo)
    print("Puedes editar el archivo de texto para agregar otras URL y mostrar los estados.")
    print("")


def extract_urls(text):
    url_regex = r"https?://[^\s/$.?#].[^\s]*"
    return re.findall(url_regex, text)

def extract_internal_subdomains(url, urls):
    base_domain = urlparse(url).netloc
    internal_subdomains = set()

    for u in urls:
        netloc = urlparse(u).netloc
        if netloc.endswith(base_domain) and not netloc == base_domain:
            internal_subdomains.add(netloc)

    return internal_subdomains

def extract_external_subdomains(url, urls):
    base_domain = urlparse(url).netloc
    external_subdomains = set()

    for u in urls:
        netloc = urlparse(u).netloc
        if not netloc.endswith(base_domain):
            external_subdomains.add(netloc)

    return external_subdomains

def extraer_subdominios():
    url = input("\033[32mIngrese la URL Completa: ")
    print("Puede ocurrir un error en algunos sitios...")
    time.sleep(2)
    print("")
    response = requests.get(url)
    html_content = response.text

    urls = extract_urls(html_content)

    internal_subdomains = extract_internal_subdomains(url, urls)
    external_subdomains = extract_external_subdomains(url, urls)
    
    print("\033[31mURLS ENCONTRADOS:")
    print("")
    for u in urls:
        print("\033[32m", u)

    print("\033[31mSUBDOMINIOS INTERNOS:")
    print("")
    for subdomain in internal_subdomains:
        print("\033[32m", subdomain)
        
    print("\033[31mSUBDOMINIOS EXTERNOS:")
    print("")
    for subdomain in external_subdomains:
        print("\033[32m", subdomain)

    else:
        print("Error al acceder a la URL.")


def generar_payload():   
    time.sleep(1)
    os.system("python3 payload.py")      

def verificar_estado_hosts():
    archivo = "hosts.txt"
    try:
        with open(archivo, 'r') as file:
            urls = file.readlines()
            urls = [url.strip() for url in urls]

        for url in urls:
            response = requests.head(url, verify=False)
            print(response.status_code, url)

    except FileNotFoundError:
        print("El archivo", archivo, "no existe.")

    except Exception as e:
        print("Error al verificar el estado de los hosts:", str(e))
        print("")


def ver_puertos_abiertos():
    host = input("\033[32mIngrese la URL o IP: ")
    print("")
    print("Escaneando puertos abiertos... Esto puede demorar!")
    print("")
    try:
        resultado = subprocess.check_output(["nmap", "-p-", host])
        print("")
        print(resultado.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando nmap:", str(e))

def trace_ip_address(ip):
    response = requests.get(f"http://ipinfo.io/{ip}")
    data = response.json()
    return data 

def ejecutar_opcion(opcion):
    if opcion == 1:
        print("\033[32m")
        extraer_links()
    elif opcion == 2:
        print("")
        extraer_subdominios()
    elif opcion == 3:
        print("")
        os.system("python3 dns.py")
    elif opcion == 4:
        print("\033[32m")
        verificar_estado_hosts()
    elif opcion == 5:
        print("")
        generar_payload()
    elif opcion == 6:
        print("")
        ver_puertos_abiertos()
    elif opcion == 7:
        ip = input("\033[1;32mIngresar direccion IP: ")
        print("")
        ip_data = trace_ip_address(ip)
        print(f"Hostname: {ip_data.get('hostname', '')}")
        print(f"Organizacion: {ip_data.get('org', '')}")
        print(f"Ubicacion: {ip_data.get('city', '')}, {ip_data.get('region', '')}, {ip_data.get('country', '')}")
        print(f"Direccion IP: {ip_data['ip']}")
        print(f"Codigo Postal: {ip_data.get('postal', '')}")
        print(f"Coordenadas: {ip_data.get('loc', '')}")
        print(f"Proveedor de servicios de Internet: {ip_data.get('isp', '')}")
        print(f"Zona horaria: {ip_data.get('timezone', '')}")
        print("")
        print(f"\033[1;36mGeolocalizacion Link: https://www.google.com/maps/place/{ip_data.get('loc', '')}")
    elif opcion == 8:
        time.sleep(1)
        #Cambiar cat por type para windows
        print("\033[91m")
        os.system("cat README.md") 
    elif opcion == 0:
        print("\033[32m")
        print("¡Gracias por usar Shadow_Eminencie Vuelve pronto.")
        print("")
        return False
    else:
        print("Opcion invalida.")

    input("\nPresione Enter para continuar...")
    return True


continuar = True
while continuar:
    os.system("clear")
    mostrar_menu()
    try:
        opcion = int(input("\033[31mIngresar una opcion en numero: "))
        continuar = ejecutar_opcion(opcion)
    except ValueError:
        print("Opcion invalida. Vuelve a intentarlo de otra manera.")
        input("\nPresione Enter para continuar...")

