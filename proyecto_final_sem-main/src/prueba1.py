import pygame
import sys
import threading
import os
from MediosExtraibles import MenuMediosExtraibles
from ServiciosStreaming import ServiciosStreaming
from MusicaStreaming import MusicaStreaming
from time import sleep
# Inicializa pygame
pygame.init()
sleep(1)

#Creamos un hilo para los medios extraibles
menu = MenuMediosExtraibles()
streaming = ServiciosStreaming()
musica = MusicaStreaming()


# Configura el tamaño de la ventana y los colores

COLOR_FONDO = (0, 0, 0)  # Negro
COLOR_TEXTO = (0, 0, 0)  # Blanco
COLOR_SELECCION = (255, 0, 0)  # Rojo para resaltar la opción seleccionada
COLOR_OPCIONES= (173, 216, 230) #Gris para la interaccion

# Configura la ventana de pygame
pantalla = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
ancho_ventana, largo_ventana = pantalla.get_size()
pygame.display.set_caption("Centro de Entretenimiento")

# Configura la fuente
fuente = pygame.font.SysFont("Arial", 36)

# Lista de opciones del menú
opciones = ["Video en Línea", "Música en Línea", "Medio Extraíble", "Configuración de Red", "Salir"]
indice_opcion = 0  # Para rastrear qué opción está seleccionada

fondo=pygame.image.load('images/fondo.jpg')

def dibujar_menu():
    #Función para establecer el fondo de la ventana
    def Background_sky(fondo):
    	size=pygame.transform.scale(fondo,(2048,1500))
    	pantalla.blit(size, (0,0))

    #pantalla.fill(COLOR_FONDO)
    textoFlechas = fuente.render("↑↓ - Moverse entre las opciones", True, COLOR_OPCIONES)
    pantalla.blit(textoFlechas,(100,400))
    textoSeleccion = fuente.render("ENTER - Seleccionar opcion", True, COLOR_OPCIONES)
    pantalla.blit(textoSeleccion,(100,450))
    y = 100  # Posición inicial vertical para las opciones
    Background_sky(fondo) #Dibuja el fondo en la ventana
    # Dibuja cada opción
    for i, opcion in enumerate(opciones):
        if i == indice_opcion:
            texto = fuente.render(opcion, True, COLOR_SELECCION)  # Opción seleccionada en rojo
        else:
            texto = fuente.render(opcion, True, COLOR_TEXTO)  # Otras opciones en blanco
        pantalla.blit(texto, (100, y))
        y += 50  # Espaciado entre opciones
    
    pygame.display.flip()  # Actualiza la pantalla

def manejar_eventos():
    global indice_opcion
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                indice_opcion = (indice_opcion + 1) % len(opciones)  # Navega hacia abajo
            elif evento.key == pygame.K_UP:
                indice_opcion = (indice_opcion - 1) % len(opciones)  # Navega hacia arriba
            elif evento.key == pygame.K_RETURN:
                ejecutar_opcion(indice_opcion)  # Ejecuta la opción seleccionada
def mostrar_texto(self, texto, x, y, color=None):
        if color is None:
            color = self.NEGRO
        superficie_texto = self.fuente.render(texto, True, color)
        self.pantalla.blit(superficie_texto, (x, y))
def ejecutar_opcion(indice):
    if indice == 0:
        print("Seleccionado: Video en Línea")
        # Llama a la función para manejar servicios de video en línea
        streaming.iniciar_menu()
    elif indice == 1:
        print("Seleccionado: Música en Línea")
        # Llama a la función para manejar servicios de música en línea
        musica.iniciar_menu()
    elif indice == 2:
        print("Seleccionado: Medio Extraíble")
        menu.iniciar_menu()
    elif indice == 3:
        print("Seleccionado: Configuración de Red")
        # Llama a la función para configurar la red
    elif indice == 4:
        print("Saliendo...")
        pygame.quit()
        #os.system("shutdown now")


# Bucle principal
ejecutando = True
while ejecutando:
    manejar_eventos()  # Maneja los eventos de teclado
    dibujar_menu()  # Dibuja el menú en la pantalla
