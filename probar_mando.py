
import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No se detecta el mando.")
    raise SystemExit

mando = pygame.joystick.Joystick(0)
mando.init()

print("Mando:", mando.get_name())
print("Pulsa las flechas de la cruceta. Cierra con ESC.")

reloj = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit

    pygame.event.pump()

    print(
        "Cruceta:", mando.get_hat(0) if mando.get_numhats() else "Sin hat",
        "| Botones:", [
            i for i in range(mando.get_numbuttons())
            if mando.get_button(i)
        ],
        end="\r"
    )

    reloj.tick(30)
