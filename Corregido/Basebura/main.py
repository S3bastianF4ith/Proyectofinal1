import tkinter as tk
import folium
import os
import datetime
from tkinter import Toplevel
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import sys

def obtener_ruta_relativa(ruta_relativa):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, ruta_relativa)

solicitudes_servicios = []

USUARIOS_txt = obtener_ruta_relativa("Datos/datos.txt")
SOLICITUDES_txt = obtener_ruta_relativa("Datos/solicitudes.txt")

def cargar_usuarios():
    usuarios = {}
    try:
        with open(USUARIOS_txt, "r") as file:
            for line in file:
                tipo, usuario, contrasena = line.strip().split(":")
                usuarios[tipo] = (usuario, contrasena)
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo de usuarios no se encontró.")
    return usuarios

usuarios = cargar_usuarios()

ventana = tk.Tk()
ventana.title("Basebura")
ventana.geometry("600x400") 
ventana.configure(bg='teal')

def comenzar():
    ventana.withdraw()

    nueva_ventana = tk.Toplevel(ventana)
    nueva_ventana.title("Inicio de sesión")
    nueva_ventana.geometry("600x400")  
    nueva_ventana.configure(bg='teal')
    
    etiqueta_nueva = tk.Label(nueva_ventana, text="Seleccione qué tipo de cuenta es usted", 
                              font=("Arial", 16), bg='teal', fg='white')
    etiqueta_nueva.pack(pady=20)

    boton_lider = tk.Button(nueva_ventana, text="Administrador", command=lambda: abrir_ventana_datos("Admin", nueva_ventana), 
                            font=("Arial", 14), bg='springgreen', fg='black')
    boton_lider.pack(pady=10)

    boton_trabajador = tk.Button(nueva_ventana, text="Trabajador de la basura", command=lambda: abrir_ventana_datos("Trabajador", nueva_ventana), 
                                  font=("Arial", 14), bg='springgreen', fg='black')
    boton_trabajador.pack(pady=10)

    boton_tianguis = tk.Button(nueva_ventana, text="Representante del Tianguis", command=lambda: abrir_ventana_datos("Tianguis", nueva_ventana),
                            font=("Arial", 14), bg='springgreen', fg='black')
    boton_tianguis.pack(pady=10)

    boton_cerrar = tk.Button(nueva_ventana, text="Volver", command=lambda: volver(nueva_ventana), 
                             font=("Arial", 14), bg='lightcoral', fg='white')
    boton_cerrar.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10) 

def abrir_ventana_datos(tipo, ventana_anterior):
    ventana_anterior.withdraw()  

    ventana_ingreso = tk.Toplevel(ventana)
    ventana_ingreso.title(f"Inicio de sesión - {tipo}")
    ventana_ingreso.geometry("400x600")
    ventana_ingreso.configure(bg='dark sea green')

    etiqueta_nombre = tk.Label(ventana_ingreso, text=f"Ingrese su usuario de {tipo}:", 
                                font=("Arial", 14), bg='dark sea green', fg='darkblue')
    etiqueta_nombre.pack(pady=(20,0))

    entrada_nombre = tk.Entry(ventana_ingreso, font=("Arial", 14))
    entrada_nombre.pack(pady=(0,10))

    etiqueta_contrasena = tk.Label(ventana_ingreso, text="Ingrese su contraseña:", 
                                    font=("Arial", 14), bg='dark sea green', fg='darkblue')
    etiqueta_contrasena.pack(pady=(20,0))

    entrada_contrasena = tk.Entry(ventana_ingreso, font=("Arial", 14), show='*')
    entrada_contrasena.pack(pady=(0,10))

    def alternar_contrasena():
        if entrada_contrasena.cget('show') == '*':
            entrada_contrasena.config(show='')  # Muestra la contraseña
        else:
            entrada_contrasena.config(show='*')  # Oculta la contraseña

    boton_alternar = tk.Button(ventana_ingreso, text="Mostrar/Ocultar Contraseña", command=alternar_contrasena, 
                               font=("Arial", 14), bg='lightblue', fg='black')
    boton_alternar.pack(pady=10)

    boton_enviar = tk.Button(ventana_ingreso, text="Enviar", command=lambda: enviar_datos(tipo, entrada_nombre.get(), entrada_contrasena.get(), ventana_ingreso), 
                             font=("Arial", 14), bg='springgreen', fg='black')
    boton_enviar.pack(pady=10)

    boton_volver = tk.Button(ventana_ingreso, text="Volver", command=lambda: volver_a_seleccion(ventana_ingreso, ventana_anterior), 
                             font=("Arial", 14), bg='lightcoral', fg='white')
    boton_volver.pack(pady=10)

def enviar_datos(tipo, nombre, contrasena, ventana_ingreso):
    if not nombre or not contrasena:  
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    usuario_correcto, contrasena_correcta = usuarios.get(tipo, (None, None))
    if usuario_correcto == nombre and contrasena_correcta == contrasena:
        mostrar_ventana_usuario(tipo)  
        ventana_ingreso.destroy()  
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def mostrar_ventana_usuario(tipo):
    if tipo == "Admin":
        ventana_admin = tk.Toplevel(ventana)
        ventana_admin.title("Ventana de Administrador")
        ventana_admin.geometry("800x600")
        ventana_admin.configure(bg='teal')

        etiqueta_mensaje = tk.Label(ventana_admin, text="Bienvenido, Administrador!", 
                                     font=("Arial", 16), bg='teal', fg='black')
        etiqueta_mensaje.pack(pady=20)

        boton_crear_cuenta = tk.Button(ventana_admin, text="Crear Cuenta", command=lambda: crear_cuenta(tipo, ventana_admin), 
                                        font=("Arial", 14), bg='lightblue', fg='black')
        boton_crear_cuenta.pack(pady=10)

        boton_editar_cuenta = tk.Button(ventana_admin, text="Editar Cuenta", command=lambda: editar_cuenta(ventana_admin), 
                                         font=("Arial", 14), bg='lightblue', fg='black')
        boton_editar_cuenta.pack(pady=10)

        boton_eliminar_cuenta = tk.Button(ventana_admin, text="Eliminar Cuenta", command=lambda: eliminar_cuenta(ventana_admin), 
                                           font=("Arial", 14), bg='lightblue', fg='black')
        boton_eliminar_cuenta.pack(pady=10)

        boton_cerrar = tk.Button(ventana_admin, text="Salir", font=("Arial", 14), bg='red', fg='white', command=lambda :[comenzar(), ventana_admin.destroy()])
        boton_cerrar.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

    elif tipo == "Trabajador":
        ventana_trabajador = tk.Toplevel(ventana)
        ventana_trabajador.title("Ventana de Trabajador")
        ventana_trabajador.geometry("800x600")
        ventana_trabajador.configure(bg='teal')

        etiqueta_mensaje = tk.Label(ventana_trabajador, text="Bienvenido, Trabajador!", 
                                     font=("Arial", 16), bg='teal', fg='black')
        etiqueta_mensaje.pack(pady=20)

        boton_revisar_mapa = tk.Button(ventana_trabajador, text="Revisar mapa", command=ventana4, 
                                    font=("Arial", 14), bg='lightblue', fg='black')
        boton_revisar_mapa.pack(pady=10)

        boton_consulta_reporte = tk.Button(ventana_trabajador, text="Consultar reportes", command=ventana2, 
                                    font=("Arial", 14), bg='lightblue', fg='black')
        boton_consulta_reporte.pack(pady=10)

        boton_recoleccion = tk.Button(ventana_trabajador, text="Estatus de recolección", command=ventana5, 
                                    font=("Arial", 14), bg='lightblue', fg='black')
        boton_recoleccion.pack(pady=10)

        boton_comunicarse_administradores = tk.Button(ventana_trabajador, text="Contacto de los administradores", command=ventana3, 
                                    font=("Arial", 14), bg='lightblue', fg='black')
        boton_comunicarse_administradores.pack(pady=10)

        boton_cerrar = tk.Button(ventana_trabajador, text="Salir", font=("Arial", 14), bg='red', fg='white', command=lambda :[comenzar(), ventana_trabajador.destroy()])
        boton_cerrar.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

    elif tipo == "Tianguis":
        ventana_tianguis = tk.Toplevel(ventana)
        ventana_tianguis.title("Ventana de Representante del Tianguis")
        ventana_tianguis.geometry("800x600")
        ventana_tianguis.configure(bg='teal')

        etiqueta_mensaje = tk.Label(ventana_tianguis, text="Bienvenido, Representante del Tianguis!", 
                                     font=("Arial", 16), bg='teal', fg='black')
        etiqueta_mensaje.pack(pady=20)

        boton_realizar_servicio = tk.Button(ventana_tianguis, text="Solicitar servicio", command=ventana1, 
                                    font=("Arial", 14), bg='lightblue', fg='black')
        boton_realizar_servicio.pack(pady=10)

        boton_consulta_reporte = tk.Button(ventana_tianguis, text="Consultar reportes", command=ventana2, 
                                    font=("Arial", 14), bg='lightblue', fg='black')
        boton_consulta_reporte.pack(pady=10)

        boton_comunicarse_administradores = tk.Button(ventana_tianguis, text="Contacto de los administradores", command=ventana3, 
                                    font=("Arial", 14), bg='lightblue', fg='black')
        boton_comunicarse_administradores.pack(pady=10)

        boton_cerrar = tk.Button(ventana_tianguis, text="Salir", font=("Arial", 14), bg='red', fg='white', command=lambda :[comenzar(), ventana_tianguis.destroy()])
        boton_cerrar.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

def ventana1():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Solicitud de sevicios")
    ventana_nueva.geometry("600x400")
    ventana_nueva.configure(bg='dark sea green')
    etiqueta = tk.Label(ventana_nueva, text="Solicitud de servicios", font=("Arial", 14), bg='dark sea green')
    etiqueta.pack(pady=20)

    etiqueta_servicio = tk.Label(ventana_nueva, text="Ingrese su nombre", 
                                 font=("Arial", 14), bg='dark sea green', fg='black')
    etiqueta_servicio.pack(pady=(20,0))

    entrada_servicio = tk.Entry(ventana_nueva, font=("Arial", 14))
    entrada_servicio.pack(pady=(0,10))

    etiqueta_mail = tk.Label(ventana_nueva, text="Ingrese una correo electronico:", 
                                    font=("Arial", 14), bg='dark sea green', fg='black')
    etiqueta_mail.pack(pady=(20,0))

    entrada_mail = tk.Entry(ventana_nueva, font=("Arial", 14))
    entrada_mail.pack(pady=(0,10))

    etiqueta_tianguis = tk.Label(ventana_nueva, text="Seleccione el tipo de cuenta:", 
                                    font=("Arial", 14), bg='dark sea green', fg='black')
    etiqueta_tianguis.pack(pady=(20,0))

    tipo_tianguis = ttk.Combobox(ventana_nueva, values= ["Tianguis 1", "Tianguis 2", "Tianguis 3", "Tianguis 4", "Tianguis 5", "Tianguis 6", "Tianguis 7", "Tianguis8"], font=("Arial", 14))
    tipo_tianguis.pack(pady=(10,0))

    boton_guardar = tk.Button(ventana_nueva, text="Guardar", command=lambda: guardar_solicitud(entrada_servicio.get(), entrada_mail.get(), tipo_tianguis.get()), 
                               font=("Arial", 14), bg='springgreen', fg='black')
    boton_guardar.pack(pady=10)

    boton_volver = tk.Button(ventana_nueva, text="Volver", command=lambda: volver_a_tianguis(ventana_nueva), 
                             font=("Arial", 14), bg='lightcoral', fg='white')
    boton_volver.pack(pady=10)

def guardar_solicitud(nombre, correo, tipo):
    if not nombre or not correo or not tipo:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    solicitud = f"Nombre: {nombre}, Correo: {correo}, Tipo: {tipo}\n"
    solicitudes_servicios.append(solicitud)

    with open(SOLICITUDES_txt, "a") as file:
        file.write(solicitud)

    messagebox.showinfo("Éxito", "Solicitud guardada exitosamente.")


def ventana2():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Consultar reportes")
    ventana_nueva.geometry("600x400")
    ventana_nueva.configure(bg='dark sea green')
    tk.Label(ventana_nueva, text="Consulta de reportes", font=("Arial", 14), bg='dark sea green').pack(pady=20)

    try:
        with open(USUARIOS_txt, "r") as file:
            lineas = file.readlines()
            for index, line in enumerate(lineas):
                etiqueta_solicitud = tk.Label(ventana_nueva, text=line.strip(), font=("Arial", 12), bg='dark sea green')
                etiqueta_solicitud.pack(pady=5)

                boton_modificar = tk.Button(ventana_nueva, text="Modificar", command=lambda idx=index: modificar_solicitud(idx, lineas), 
                                             font=("Arial", 12), bg='lightblue', fg='black')
                boton_modificar.pack(pady=5)

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron solicitudes guardadas.")

def modificar_solicitud(index, lineas):
    ventana_modificar = tk.Toplevel(ventana)
    ventana_modificar.title("Modificar Solicitud")
    ventana_modificar.geometry("600x400")
    ventana_modificar.configure(bg='teal')

    solicitud_actual = lineas[index].strip()
    partes = solicitud_actual.split(", ")

    tk.Label(ventana_modificar, text="Datos existentes:", font=("Arial", 14), bg='teal').pack(pady=10)
    tk.Label(ventana_modificar, text=solicitud_actual, font=("Arial", 12), bg='teal').pack(pady=10)

    tk.Label(ventana_modificar, text="Ingresa la cantidad de basura recogida", font=("Arial", 14), bg='teal').pack(pady=5)
    entrada_cantidad_basura = tk.Entry(ventana_modificar, font=("Arial", 14))
    entrada_cantidad_basura.pack(pady=10)

    tk.Label(ventana_modificar, text="Ingresa el tiempo que duró la recolección", font=("Arial", 14), bg='teal').pack(pady=5)
    entrada_tipo_basura = tk.Entry(ventana_modificar, font=("Arial", 14))
    entrada_tipo_basura.pack(pady=10)

    tk.Label(ventana_modificar, text="Ingresa el número de trabajadores que participaron", font=("Arial", 14), bg='teal').pack(pady=5)
    entrada_comentarios = tk.Entry(ventana_modificar, font=("Arial", 14))
    entrada_comentarios.pack(pady=10)

    def guardar_modificacion():
        if not entrada_cantidad_basura.get() or not entrada_tipo_basura.get() or not entrada_comentarios.get():
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        nueva_linea = f"{solicitud_actual}, Cantidad de basura: {entrada_cantidad_basura.get()}, Tipo de basura: {entrada_tipo_basura.get()}, Comentarios: {entrada_comentarios.get()}\n"
        
        lineas[index] = nueva_linea
        
        with open(SOLICITUDES_txt, "w") as file:
            file.writelines(lineas)

        messagebox.showinfo("Éxito", "Solicitud modificada exitosamente.")
        ventana_modificar.destroy()
    
    tk.Button(ventana_modificar, text="Guardar Cambios", command=guardar_modificacion, 
              font=("Arial", 12), bg='springgreen', fg='black').pack(pady=10)

def salir():
    ventana.destroy()

def volver_a_tianguis(ventana_secundaria):
    ventana_secundaria.destroy()
    mostrar_ventana_usuario("Tianguis")

def ventana3():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Comunicarse con los administradores")
    ventana_nueva.geometry("600x400")
    ventana_nueva.configure(bg='teal')
    etiqueta = tk.Label(ventana_nueva, text="Sobre los administradores", font=("Arial", 14), bg='teal')
    etiqueta.pack(pady=20)
    explicacion = tk.Label(ventana_nueva, text="Aqui podras comunicarte con los desarrolladores/administradores de este sistema por cualquier duda, error o problema que presentes", font=("Arial", 14), bg='teal')
    explicacion.pack(pady=20)
    admin1 = tk.Label(ventana_nueva, text="Cervantes Arrigaga Daniel""55 3654 0346", font=("Arial", 14), bg='teal')
    admin1.pack(pady=(10,5))
    admin2 = tk.Label(ventana_nueva, text="Galicia Garcia Briana Sofia""55 8322 5689", font=("Arial", 14), bg='teal')
    admin2.pack(pady=(10,5))
    admin3 = tk.Label(ventana_nueva, text="Maldonado Avellaneda Carlos Lain""55 8237 4942", font=("Arial", 14), bg='teal')
    admin3.pack(pady=(10,5))
    admin4 = tk.Label(ventana_nueva, text="Martinez Chavez Sebastian""55 3081 3963", font=("Arial", 14), bg='teal')
    admin4.pack(pady=(10,5))
    admin5 = tk.Label(ventana_nueva, text="Rangel Alcantara Alvaro Abdiel""55 2070 7645", font=("Arial", 14), bg='teal')
    admin5.pack(pady=(10,5))
    admin6 = tk.Label(ventana_nueva, text="Sanchez Bravo Sebastian""55 6504 0329", font=("Arial", 14), bg='teal')
    admin6.pack(pady=(10,5))

def ventana4():
    ventana_nueva = Toplevel(ventana)
    ventana_nueva.title("Consulta de mapa")
    ventana_nueva.geometry("800x600")
    ventana_nueva.configure(bg='dark sea green')

    etiqueta = tk.Label(ventana_nueva, text="Consultas de mapa", font=("Arial", 14), bg='dark sea green')
    etiqueta.pack(pady=20)

    mapa_file_path = "mapa.png"  
    if not os.path.exists(mapa_file_path):
        messagebox.showerror("Error", "No se pudo encontrar el archivo de la imagen del mapa.")
        return

    imagen_mapa = Image.open(mapa_file_path)
    imagen_mapa = imagen_mapa.resize((800, 500), Image.ANTIALIAS)  
    imagen_mapa_tk = ImageTk.PhotoImage(imagen_mapa)

    label_imagen = tk.Label(ventana_nueva, image=imagen_mapa_tk, bg='dark sea green')
    label_imagen.image = imagen_mapa_tk 
    label_imagen.pack(pady=10)

    boton_cerrar = tk.Button(ventana_nueva, text="Cerrar", command=ventana_nueva.destroy, 
                             font=("Arial", 14), bg='red', fg='white')
    boton_cerrar.pack(pady=10)

    boton_abrir_mapa = tk.Button(ventana, text="Abrir Mapa", command=ventana4, font=("Arial", 14))
    boton_abrir_mapa.pack(pady=20)


def ventana5():
    ventana_nueva = tk.Toplevel(ventana)
    ventana_nueva.title("Estatus de recolección")
    ventana_nueva.geometry("800x400")
    ventana_nueva.configure(bg='dark sea green')

    etiqueta = tk.Label(ventana_nueva, text="Estatus de la recolección", font=("Arial", 14), bg='dark sea green')
    etiqueta.pack(pady=20)

    try:
        with open(SOLICITUDES_txt, "r") as file:
            lineas = file.readlines()
            for index, line in enumerate(lineas):
                marco_solicitud = tk.Frame(ventana_nueva, bg='dark sea green')
                marco_solicitud.pack(pady=10)

                etiqueta_solicitud = tk.Label(marco_solicitud, text=line.strip(), font=("Arial", 12), bg='dark sea green')
                etiqueta_solicitud.pack()

                estado = "No Iniciada"

                estado_button = tk.Button(marco_solicitud, text=f"Estado: {estado}", 
                                          command=lambda idx=index: cambiar_estado(idx, estado_button), 
                                          font=("Arial", 12), bg='lightblue', fg='black')
                estado_button.pack(pady=5)

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron solicitudes guardadas.")

estados_recoleccion = {}

def cambiar_estado(index, estado_button):
    if index not in estados_recoleccion:
        estados_recoleccion[index] = "En Proceso"
    elif estados_recoleccion[index] == "En Proceso":
        estados_recoleccion[index] = "Completada"
    else:
        estados_recoleccion[index] = "En Proceso"

    estado_button.config(text=f"Estado: {estados_recoleccion[index]}")

def crear_cuenta(tipo, ventana_anterior):
    ventana_anterior.withdraw()

    ventana_crear = tk.Toplevel(ventana)
    ventana_crear.title(f"Crear Cuenta - {tipo}")
    ventana_crear.geometry("400x400")
    ventana_crear.configure(bg='dark sea green')

    etiqueta_usuario = tk.Label(ventana_crear, text="Ingrese un nuevo usuario:", 
                                 font=("Arial", 14), bg='dark sea green', fg='black')
    etiqueta_usuario.pack(pady=(20,0))

    entrada_usuario = tk.Entry(ventana_crear, font=("Arial", 14))
    entrada_usuario.pack(pady=(0,10))

    etiqueta_contrasena = tk.Label(ventana_crear, text="Ingrese una contraseña:", 
                                    font=("Arial", 14), bg='dark sea green', fg='black')
    etiqueta_contrasena.pack(pady=(20,0))

    entrada_contrasena = tk.Entry(ventana_crear, font=("Arial", 14), show='*')
    entrada_contrasena.pack(pady=(0,10))

    etiqueta_tipo = tk.Label(ventana_crear, text="Seleccione el tipo de cuenta:", 
                                    font=("Arial", 14), bg='dark sea green', fg='black')
    etiqueta_tipo.pack(pady=(20,0))

    tipo_cuenta = ttk.Combobox(ventana_crear, values=["Administrador", "Trabajador", "Representante"], font=("Arial", 14))
    tipo_cuenta.pack(pady=(10,0))

    def guardar_cuenta():
        usuario = entrada_usuario.get()
        contrasena = entrada_contrasena.get()
        guardar_cuenta_real(usuario, contrasena, ventana_crear)

    def guardar_cuenta_real(usuario, contrasena, ventana_crear):
        print(f"Usuario: {usuario}, Contraseña: {contrasena}")

    boton_guardar = tk.Button(ventana_crear, text="Guardar Cuenta", command=lambda: guardar_cuenta(entrada_usuario.get(), entrada_contrasena.get(), ventana_crear), font=("Arial", 14), bg='springgreen', fg='black')
    boton_guardar.pack(pady=10)

    boton_volver = tk.Button(ventana_crear, text="Volver", command=lambda: volver_a_administrador(ventana_crear), 
                             font=("Arial", 14), bg='lightcoral', fg='white')
    boton_volver.pack(pady=10)

def editar_cuenta(ventana_anterior):
    ventana_anterior.withdraw()

    ventana_editar = tk.Toplevel(ventana)
    ventana_editar.title("Editar Cuenta")
    ventana_editar.geometry("400x400")
    ventana_editar.configure(bg='dark sea green')

    etiqueta_usuario = tk.Label(ventana_editar, text="Ingrese el usuario a editar:", 
                                 font=("Arial", 14), bg='dark sea green', fg='black')
    etiqueta_usuario.pack(pady=(20,0))

    entrada_usuario = tk.Entry(ventana_editar, font=("Arial", 14))
    entrada_usuario.pack(pady=(0,10))

    etiqueta_contrasena = tk.Label(ventana_editar, text="Ingrese la nueva contraseña:", 
                                    font=("Arial", 14 ), bg='dark sea green', fg='black')
    etiqueta_contrasena.pack(pady=(20,0))

    entrada_contrasena = tk.Entry(ventana_editar, font=("Arial", 14), show='*')
    entrada_contrasena.pack(pady=(0,10))

    boton_guardar = tk.Button(ventana_editar, text="Guardar Cambios", command=lambda: guardar_cambios(entrada_usuario.get(), entrada_contrasena.get(), ventana_editar), 
                              font=("Arial", 14), bg='springgreen', fg='black')
    boton_guardar.pack(pady=10)

    boton_volver = tk.Button(ventana_editar, text="Volver", command=lambda: volver_a_administrador(ventana_editar), 
                             font=("Arial", 14), bg='lightcoral', fg='white')
    boton_volver.pack(pady=10)

def volver_a_administrador(ventana_secundaria):
    ventana_secundaria.destroy()
    mostrar_ventana_usuario("Admin")

def guardar_cambios(usuario, nueva_contrasena, ventana_editar):
    if not usuario or not nueva_contrasena:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    usuarios_actualizados = {}
    for tipo, (user, contrasena) in usuarios.items():
        if user == usuario:
            usuarios_actualizados[tipo] = (user, nueva_contrasena)
        else:
            usuarios_actualizados[tipo] = (user, contrasena)

    with open(USUARIOS_txt, "w") as file:
        for tipo, (user, contrasena) in usuarios_actualizados.items():
            file.write(f"{tipo}:{user}:{contrasena}\n")

    messagebox.showinfo("Éxito", "Contraseña actualizada exitosamente.")
    ventana_editar.destroy()

def eliminar_cuenta(ventana_anterior):
    ventana_anterior.withdraw()

    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.title("Eliminar Cuenta")
    ventana_eliminar.geometry("400x400")
    ventana_eliminar.configure(bg='dark sea green')

    etiqueta_usuario = tk.Label(ventana_eliminar, text="Ingrese el usuario a eliminar:", 
                                 font=("Arial", 14), bg='dark sea green', fg='black')
    etiqueta_usuario.pack(pady=(20,0))

    entrada_usuario = tk.Entry(ventana_eliminar, font=("Arial", 14))
    entrada_usuario.pack(pady=(0,10))

    boton_eliminar = tk.Button(ventana_eliminar, text="Eliminar Cuenta", command=lambda: confirmar_eliminar(entrada_usuario.get(), ventana_eliminar), 
                                font=("Arial", 14), bg='red', fg='white')
    boton_eliminar.pack(pady=10)

    boton_volver = tk.Button(ventana_eliminar, text="Volver", command=lambda: volver_a_administrador(ventana_eliminar), 
                                font=("Arial", 14), bg='lightcoral', fg='white')
    boton_volver.pack(pady=10)

def confirmar_eliminar(usuario, ventana_eliminar):
    if not usuario:
        messagebox.showerror("Error", "Por favor, ingrese un usuario.")
        return

    usuario_encontrado = False
    usuarios_actualizados = {}

    for tipo, (user, contrasena) in usuarios.items():
        if user == usuario:
            usuario_encontrado = True  
        else:
            usuarios_actualizados[tipo] = (user, contrasena)  

    if not usuario_encontrado:
        messagebox.showerror("Error", "Usuario no encontrado.")
    else:
        with open(USUARIOS_txt, "w") as file:
            for tipo, (user, contrasena) in usuarios_actualizados.items():
                file.write(f"{tipo}:{user}:{contrasena}\n")
        messagebox.showinfo("Éxito", "Cuenta eliminada exitosamente.")
        ventana_eliminar.destroy()

def volver_a_seleccion(ventana_ingreso, ventana_anterior):
    ventana_ingreso.destroy()  
    ventana_anterior.deiconify()  

def volver(ventana_secundaria):
    ventana_secundaria.destroy()  
    ventana.deiconify()

def salir():
    ventana.destroy()  

etiqueta = tk.Label(ventana, text="Bienvenido a Basebura", font=("Arial", 20), bg='teal', fg='white')
etiqueta.pack(pady=(100,0)) 
etiqueta = tk.Label(ventana, text="Sistema de comunicación entre trabajadores de la basura y líderes de tianguis.", font=("Arial", 12), bg='teal', fg='white')
etiqueta.pack(pady=(5,0))

boton_comenzar = tk.Button(ventana, text="Comenzar", command=comenzar, font=("Arial", 16), width=10, height=1, bg='palegreen', fg='black')
boton_comenzar.pack(pady=22)


ventana.mainloop()