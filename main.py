import tkinter as tk
from tkinter import messagebox
import json


def agregar_contacto():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    email = entry_email.get()

    if nombre and telefono and email:
        contacto = {"nombre": nombre, "telefono": telefono, "email": email}
        contactos.append(contacto)
        guardar_contactos()
        messagebox.showinfo("Éxito", "Contacto agregado correctamente")
        limpiar_campos()
        mostrar_contactos()
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos")


def mostrar_contactos():
    lista_contactos.delete(0, tk.END)
    for contacto in contactos:
        nombre = contacto["nombre"]
        lista_contactos.insert(tk.END, nombre)


def seleccionar_contacto(event):
    indice = lista_contactos.curselection()
    if indice:
        indice = int(indice[0])
        contacto = contactos[indice]
        nombre = contacto["nombre"]
        telefono = contacto["telefono"]
        email = contacto["email"]
        texto_detalles.config(
            text=f"Nombre: {nombre}\nTeléfono: {telefono}\nEmail: {email}")
        boton_actualizar.config(state=tk.NORMAL)
        boton_eliminar.config(state=tk.NORMAL)
    else:
        texto_detalles.config(text="")
        boton_actualizar.config(state=tk.DISABLED)
        boton_eliminar.config(state=tk.DISABLED)


def actualizar_contacto():
    indice = lista_contactos.curselection()
    if indice:
        indice = int(indice[0])
        contacto = contactos[indice]
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        email = entry_email.get()
        if nombre and telefono and email:
            contacto["nombre"] = nombre
            contacto["telefono"] = telefono
            contacto["email"] = email
            guardar_contactos()
            messagebox.showinfo("Éxito", "Contacto actualizado correctamente")
            limpiar_campos()
            mostrar_contactos()
        else:
            messagebox.showerror(
                "Error", "Por favor, completa todos los campos")
    else:
        messagebox.showerror("Error", "Por favor, selecciona un contacto")


def eliminar_contacto():
    indice = lista_contactos.curselection()
    if indice:
        indice = int(indice[0])
        confirmacion = messagebox.askyesno(
            "Confirmar", "¿Estás seguro de eliminar este contacto?")
        if confirmacion:
            del contactos[indice]
            guardar_contactos()
            messagebox.showinfo("Éxito", "Contacto eliminado correctamente")
            limpiar_campos()
            mostrar_contactos()
    else:
        messagebox.showerror("Error", "Por favor, selecciona un contacto")


def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)


def guardar_contactos():
    with open("contactos.json", "w") as archivo:
        json.dump(contactos, archivo, indent=4)


def cargar_contactos():
    try:
        with open("contactos.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


contactos = cargar_contactos()

root = tk.Tk()
root.title("Agenda de Contactos")
root.geometry("600x300")

root.configure(bg="#F0F0F0")
root.resizable(False, False)

label_nombre = tk.Label(root, text="Nombre:")
label_nombre.grid(row=0, column=0, sticky="E")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, sticky="WE")

label_telefono = tk.Label(root, text="Teléfono:")
label_telefono.grid(row=1, column=0, sticky="E")
entry_telefono = tk.Entry(root)
entry_telefono.grid(row=1, column=1, sticky="WE")

label_email = tk.Label(root, text="Email:")
label_email.grid(row=2, column=0, sticky="E")
entry_email = tk.Entry(root)
entry_email.grid(row=2, column=1, sticky="WE")

button_agregar = tk.Button(root, text="Agregar", command=agregar_contacto)
button_agregar.grid(row=3, column=0, pady=10)

lista_contactos = tk.Listbox(root, width=30)
lista_contactos.grid(row=0, column=2, rowspan=4, padx=10, pady=5, sticky="NS")

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=0, column=3, rowspan=4, sticky="NS")

lista_contactos.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=lista_contactos.yview)

texto_detalles = tk.Label(root, justify="left")
texto_detalles.grid(row=0, column=4, rowspan=4, padx=10, pady=5, sticky="W")

boton_actualizar = tk.Button(
    root, text="Actualizar", command=actualizar_contacto, state=tk.DISABLED)
boton_actualizar.grid(row=4, column=0, padx=10, pady=5, sticky="WE")

boton_eliminar = tk.Button(root, text="Eliminar",
                           command=eliminar_contacto, state=tk.DISABLED)
boton_eliminar.grid(row=4, column=1, padx=10, pady=5, sticky="WE")

lista_contactos.bind("<<ListboxSelect>>", seleccionar_contacto)

mostrar_contactos()

root.mainloop()
