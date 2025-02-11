from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import urllib.parse
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

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
                messagebox.showinfo("Éxito", "SMS enviado correctamente.")
                print(Fore.CYAN + "Detalles:", result)
                status_label.config(text="SMS enviado correctamente.", fg="green")
    except urllib.error.URLError as e:
        messagebox.showerror("Error", f"Error de conexión: {e}")
        status_label.config(text=f"Error de conexión: {e}", fg="red")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error al decodificar la respuesta de la API.")
        status_label.config(text="Error al decodificar la respuesta de la API.", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Error al enviar el SMS: {e}")
        status_label.config(text=f"Error al enviar el SMS: {e}", fg="red")

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
    messagebox.showerror("Error", f"Error {error_code}: {error_messages.get(error_code, 'Error desconocido.')}")
    status_label.config(text=f"Error {error_code}: {error_messages.get(error_code, 'Error desconocido.')}", fg="red")

# Función para mostrar el banner
def mostrar_banner():
    banner = f"""
   {Fore.CYAN}K I Z 4 R U    
"""
    print(banner)

# Función para enviar SMS desde la interfaz gráfica
def enviar_sms():
    api_key = entry_api_key.get()
    sender = entry_sender.get()
    number = entry_number.get()
    message = text_message.get("1.0", tk.END).strip()
    test_mode = test_mode_var.get()
    
    if not api_key:
        messagebox.showerror("Error", "La clave API es obligatoria.")
        status_label.config(text="La clave API es obligatoria.", fg="red")
        return
    
    if not sender:
        messagebox.showerror("Error", "El remitente es obligatorio.")
        status_label.config(text="El remitente es obligatorio.", fg="red")
        return
    
    if not number.startswith("+") or not number[1:].isdigit():
        messagebox.showerror("Error", "Formato de número inválido.")
        status_label.config(text="Formato de número inválido.", fg="red")
        return
    
    if len(message) > 765:
        messagebox.showerror("Error", "El mensaje es demasiado largo. Máximo 765 caracteres.")
        status_label.config(text="El mensaje es demasiado largo. Máximo 765 caracteres.", fg="red")
        return
    
    send_sms(api_key, number, sender, message, test_mode)

# Función para cerrar la ventana
def cerrar_ventana():
    root.destroy()

# Función para limpiar los campos de entrada
def limpiar_campos():
    entry_api_key.delete(0, tk.END)
    entry_sender.delete(0, tk.END)
    entry_number.delete(0, tk.END)
    text_message.delete("1.0", tk.END)
    status_label.config(text="")

# Función para copiar el mensaje al portapapeles
def copiar_mensaje():
    root.clipboard_clear()
    root.clipboard_append(text_message.get("1.0", tk.END).strip())
    root.update()  # Actualiza el portapapeles

# Función para guardar el mensaje en un archivo
def guardar_mensaje():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_message.get("1.0", tk.END).strip())

# Función para cargar un mensaje desde un archivo
def cargar_mensaje():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_message.delete("1.0", tk.END)
            text_message.insert(tk.END, file.read())

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("SMS KIZ4RU")
root.geometry("600x700")
root.configure(bg="#FFC107")  # Amarillo

# Añadir imagen
img = Image.open("./img/smsimg.png")
img = img.resize((100, 100), Image.LANCZOS)
photo = ImageTk.PhotoImage(img)
tk.Label(root, image=photo, bg="#FFC107").pack(pady=10)

tk.Label(root, text="KIZ4RU", font=("Helvetica", 16, "bold"), bg="#FFC107", fg="#FF0000").pack(pady=10)

tk.Label(root, text="Clave API:", bg="#FFC107", fg="#FF0000").pack(pady=5)
entry_api_key = tk.Entry(root, width=50)
entry_api_key.pack(pady=5)

tk.Label(root, text="Remitente:", bg="#FFC107", fg="#FF0000").pack(pady=5)
entry_sender = tk.Entry(root, width=30)
entry_sender.pack(pady=5)

tk.Label(root, text="Número de teléfono (ej. +34XXXXXXXXX):", bg="#FFC107", fg="#FF0000").pack(pady=5)
entry_number = tk.Entry(root, width=30)
entry_number.pack(pady=5)

tk.Label(root, text="Mensaje:", bg="#FFC107", fg="#FF0000").pack(pady=5)
text_message = tk.Text(root, height=10, width=50)
text_message.pack(pady=5)

test_mode_var = tk.BooleanVar()
tk.Checkbutton(root, text="Modo de prueba", variable=test_mode_var, bg="#FFC107", fg="#FF0000").pack(pady=5)

frame_buttons = tk.Frame(root, bg="#FFC107")
frame_buttons.pack(pady=20)

tk.Button(frame_buttons, text="Enviar SMS", command=enviar_sms, bg="#FF0000", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="Limpiar", command=limpiar_campos, bg="#FF0000", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="Cerrar", command=cerrar_ventana, bg="#FF0000", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="Copiar", command=copiar_mensaje, bg="#FF0000", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="Guardar", command=guardar_mensaje, bg="#FF0000", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="Cargar", command=cargar_mensaje, bg="#FF0000", fg="white").pack(side=tk.LEFT, padx=10)

status_label = tk.Label(root, text="", bg="#FFC107", fg="red")
status_label.pack(pady=10)

root.mainloop()