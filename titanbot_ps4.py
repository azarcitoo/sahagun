
import time
import pygame
import serial
import serial.tools.list_ports

# ==========================================
# CONFIGURACION DE TITANBOT
# ==========================================

PUERTO_COM = "COM7"  # Cambia esto por el puerto Bluetooth correcto
BAUDIOS = 9600
INTERVALO_ENVIO = 0.10

# Botones de la cruceta detectados en tu mando
BOTON_ARRIBA = 11
BOTON_ABAJO = 12
BOTON_IZQUIERDA = 13
BOTON_DERECHA = 14

# ==========================================
# DETECCION DE PUERTOS
# ==========================================

def listar_puertos():
    print("\nPUERTOS SERIALES DISPONIBLES:")
    puertos = list(serial.tools.list_ports.comports())

    if not puertos:
        print("No se encontraron puertos seriales.")
    else:
        for puerto in puertos:
            print(f"{puerto.device} - {puerto.description}")

# ==========================================
# LECTURA DE LA CRUCETA
# ==========================================

def comando_cruceta(mando):
    if mando.get_button(BOTON_ARRIBA):
        return "F"

    if mando.get_button(BOTON_ABAJO):
        return "B"

    if mando.get_button(BOTON_IZQUIERDA):
        return "L"

    if mando.get_button(BOTON_DERECHA):
        return "R"

    return "S"

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():
    pygame.init()
    pygame.joystick.init()

    listar_puertos()

    if pygame.joystick.get_count() == 0:
        print("\nERROR: No se detecta el mando PS4.")
        pygame.quit()
        return

    mando = pygame.joystick.Joystick(0)
    mando.init()

    print(f"\nMando detectado: {mando.get_name()}")
    print(f"Botones disponibles: {mando.get_numbuttons()}")

    # Comprobar que los indices configurados existen
    if mando.get_numbuttons() <= max(
        BOTON_ARRIBA,
        BOTON_ABAJO,
        BOTON_IZQUIERDA,
        BOTON_DERECHA
    ):
        print("ERROR: El mando no expone todos los botones configurados.")
        pygame.quit()
        return

    # Conectar Bluetooth serial
    try:
        bt = serial.Serial(
            PUERTO_COM,
            BAUDIOS,
            timeout=0.05,
            write_timeout=0.2
        )
    except serial.SerialException as error:
        print(f"\nERROR al abrir {PUERTO_COM}: {error}")
        print("Cambia PUERTO_COM por el puerto Bluetooth correcto.")
        pygame.quit()
        return

    # Algunos módulos reinician al abrir el puerto
    time.sleep(2)

    print(f"\nBluetooth abierto en {PUERTO_COM}")
    print("ARRIBA: avanzar")
    print("ABAJO: retroceder")
    print("IZQUIERDA: girar a la izquierda")
    print("DERECHA: girar a la derecha")
    print("SOLTAR CRUCETA: detener")
    print("ESPACIO: parada de emergencia mientras se mantiene")
    print("ESC: detener y salir\n")

    reloj = pygame.time.Clock()
    ultimo_envio = 0
    ultimo_comando = None
    salir = False

    try:
        while not salir:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    salir = True

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        salir = True

            pygame.event.pump()

            teclas = pygame.key.get_pressed()
            parada_emergencia = teclas[pygame.K_SPACE]

            if parada_emergencia:
                comando = "S"
            else:
                comando = comando_cruceta(mando)

            ahora = time.monotonic()

            # Enviar cada cambio y repetir el comando cada 100 ms
            if (
                comando != ultimo_comando
                or ahora - ultimo_envio >= INTERVALO_ENVIO
            ):
                bt.write(comando.encode("ascii"))
                ultimo_comando = comando
                ultimo_envio = ahora

            estado = "PARADO" if comando == "S" else "MOVIENDOSE"
            print(
                f"\rComando: {comando} | Estado: {estado}     ",
                end="",
                flush=True
            )

            reloj.tick(60)

    except (serial.SerialException, OSError) as error:
        print(f"\nERROR de comunicacion: {error}")

    finally:
        # Intentar enviar la orden de parada antes de cerrar
        try:
            bt.write(b"S")
            time.sleep(0.1)
            bt.close()
        except (serial.SerialException, OSError):
            pass

        pygame.quit()
        print("\nTitanBot detenido. Programa cerrado.")


if __name__ == "__main__":
    main()
