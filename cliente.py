import requests

URL_BASE = "http://127.0.0.1:5000"

def registrar_usuario():
    usuario = input("Ingrese nombre de usuario: ")
    contrasena = input("Ingrese contraseña: ")
    datos = {"usuario": usuario, "contraseña": contrasena}
    try:
        respuesta = requests.post(f"{URL_BASE}/registro", json=datos)
        print("Estado:", respuesta.status_code)
        print("Respuesta:", respuesta.json())
    except Exception as e:
        print("Error de conexion:", e)

def iniciar_sesion():
    usuario = input("Ingrese nombre de usuario: ")
    contrasena = input("Ingrese contraseña: ")
    datos = {"usuario": usuario, "contraseña": contrasena}
    try:
        respuesta = requests.post(f"{URL_BASE}/login", json=datos)
        print("Estado:", respuesta.status_code)
        print("Respuesta:", respuesta.json())
    except Exception as e:
        print("Error de conexion:", e)

def consultar_tareas():
    try:
        respuesta = requests.get(f"{URL_BASE}/tareas")
        print("Estado:", respuesta.status_code)
        if respuesta.status_code == 200:
            print("HTML recibido correctamente:")
            print(respuesta.text[:200] + "...")
        else:
            print("No se pudo obtener la pagina de tareas")
    except Exception as e:
        print("Error de conexion:", e)

def menu():
    while True:
        print("\n=== SISTEMA DE TAREAS ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesion")
        print("3. Ver tareas")
        print("4. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            consultar_tareas()
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opcion no valida, intente nuevamente.")

if __name__ == "__main__":
    menu()
