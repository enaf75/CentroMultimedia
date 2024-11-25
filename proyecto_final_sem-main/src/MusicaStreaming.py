import pygame
import sys
import subprocess
from time import sleep
class MusicaStreaming:
    def __init__(self):
        pygame.init()
        sleep(1)
        self.pantalla=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.ancho_ventana, self.largo_ventana=self.pantalla.get_size()
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.GRIS = (200, 200, 200)
        self.AZUL_CLARO = (173, 216, 230)
        self.fuente = pygame.font.SysFont("Arial", 30)
        self.opciones = ["Spotify", "Dezeer", "Amazon Music", "Salir"]
        self.opcion_seleccionada = 0
        self.ejecutando = False
        self.urls = {
            "Spotify": "https://open.spotify.com/intl-es",
            "Dezeer": "https://www.deezer.com/mx/",
            "Amazon Music": "https://music.amazon.com.mx/"
        }

    def mostrar_texto(self, texto, x, y, color=None):
        if color is None:
            color = self.NEGRO
        superficie_texto = self.fuente.render(texto, True, color)
        self.pantalla.blit(superficie_texto, (x, y))
    def open_service(self, service_name):
      if service_name in self.urls:
          url=self.urls[service_name]
          subprocess.Popen(["chromium-browser", "--kiosk", "--disable-infobars","--disable-notifications","--disable-save-password-bubble",
                            "--disable-popup-blocking","--no-first-run","--no-default-browser-check" "--disable-gpu",
                            "--start-fullscreen","--no-sandbox",f"--user-data-dir=/tmp/chromium-{service_name}", url])
      
    def iniciar_menu(self):
      self.ejecutando = True
      while self.ejecutando:
          self.pantalla.fill(self.BLANCO)
          self.mostrar_texto("Selecciona una opción:", 50, 50)
        
          y_offset = 150
          for indice, texto in enumerate(self.opciones):
              color = self.AZUL_CLARO if indice == self.opcion_seleccionada else self.NEGRO
              self.mostrar_texto(texto, 60, y_offset, color)
              y_offset += 70

          self.mostrar_texto("ESC - Volver al menú principal", 50, self.ancho_ventana - 60, self.GRIS)
          self.mostrar_texto("ENTER - Seleccionar opción", 50, self.ancho_ventana - 30, self.GRIS)
          self.mostrar_texto("↑↓ - Moverse entre las opciones", 50, self.ancho_ventana - 90, self.GRIS)
        
          for evento in pygame.event.get():
              if evento.type == pygame.QUIT:
                  self.ejecutando = False
                  sys.exit()
              elif evento.type == pygame.KEYDOWN:
                  if evento.key == pygame.K_DOWN:
                      self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                  elif evento.key == pygame.K_UP:
                      self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                  elif evento.key == pygame.K_RETURN:
                      if self.opciones[self.opcion_seleccionada] == "Spotify":
                          self.open_service(self.opciones[self.opcion_seleccionada])
                      elif self.opciones[self.opcion_seleccionada] == "Dezeer":
                          self.open_service(self.opciones[self.opcion_seleccionada])
                      elif self.opciones[self.opcion_seleccionada] == "Amazon Music":
                          self.open_service(self.opciones[self.opcion_seleccionada])
                      elif self.opciones[self.opcion_seleccionada] == "Salir":
                          self.ejecutando = False
                  elif evento.key == pygame.K_ESCAPE:
                      self.ejecutando = False  # Agregar acción para el ESC
        
          pygame.display.flip()
                
    def detener_menu(self):
        self.ejecutando = False
        pygame.quit()