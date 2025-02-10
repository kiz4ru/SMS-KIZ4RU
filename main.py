from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import urllib.parse
import json
from config import API_KEY, SENDER

# Inicializa colorama
init(autoreset=True)

# Función para enviar SMS usando la API de Textlocal
def send_sms(api_key, number, sender, message, test_mode=False):
    data = urllib.parse.urlencode({
        'apikey': api_key,
        'numbers': number,
        'sender': sender,
        'message': message,
        'test': test_mode
    }).encode('utf-8')
    
    request = urllib.request.Request("https://api.txtlocal.com/send/")
    try:
        with urllib.request.urlopen(request, data) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get("status") == "failure":
                error_code = result.get("errors")[0].get("code")
                handle_error(error_code)
            else:
                print(Fore.GREEN + "SMS enviado correctamente.")
                print(Fore.CYAN + "Detalles:", result)
    except urllib.error.URLError as e:
        print(Fore.RED + "Error de conexión:", e)
    except json.JSONDecodeError:
        print(Fore.RED + "Error al decodificar la respuesta de la API.")
    except Exception as e:
        print(Fore.RED + "Error al enviar el SMS:", e)

# Función para manejar códigos de error específicos en SMS
def handle_error(error_code):
    error_messages = {
        4: "No se especificaron destinatarios.",
        5: "No se proporcionó el contenido del mensaje.",
        6: "El mensaje es demasiado largo.",
        7: "Créditos insuficientes.",
        8: "Fecha de programación inválida.",
        9: "Fecha de programación en el pasado.",
        32: "Formato de número inválido.",
        43: "Nombre del remitente inválido."
    }
    print(Fore.RED + f"Error {error_code}: {error_messages.get(error_code, 'Error desconocido.')}")

# Función para mostrar el banner
def mostrar_banner():
    banner = f"""

   {Fore.CYAN}K - I - Z - 4 - R - U    
"""
    print(banner)

# Menú principal de la aplicación
def main():
    mostrar_banner()
    print(Fore.YELLOW + "********** K-I-Z-4-R-U Comunicación **********")
    while True:
        print("\n" + Fore.BLUE + "Selecciona una opción:")
        print(Fore.GREEN + "1." + Fore.YELLOW + " Enviar SMS")
        print(Fore.RED + "2." + Fore.YELLOW + " Salir")
        choice = input(Fore.CYAN + "Opción: " + Style.RESET_ALL)
        
        if choice == "1":
            enviar_sms()
        elif choice == "2":
            print(Fore.CYAN + "Saliendo de la aplicación...")
            break
        else:
            print(Fore.RED + "Opción no válida. Inténtalo de nuevo.")

# Función para solicitar los datos del SMS y enviarlo
def enviar_sms():
    print(Fore.YELLOW + "\n******** Enviar SMS ********")
    
    number = input(Fore.CYAN + "Ingresa el número de teléfono (ej. +34XXXXXXXXX): " + Style.RESET_ALL)
    if not number.startswith("+") or not number[1:].isdigit():
        print(Fore.RED + "Formato de número inválido.")
        return
    
    message = input(Fore.CYAN + "Escribe el mensaje que deseas enviar: " + Style.RESET_ALL)
    if len(message) > 765:
        print(Fore.RED + "El mensaje es demasiado largo. Máximo 765 caracteres.")
        return
    
    print(Fore.YELLOW + "\nEnviando mensaje...")
    send_sms(API_KEY, number, SENDER, message)


if __name__ == "__main__":
    main()
