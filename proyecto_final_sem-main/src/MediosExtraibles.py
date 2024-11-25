import pyudev
import os
import pygame
import sys
import vlc
import subprocess
from time import sleep

class MenuMediosExtraibles:
    def __init__(self):
        pygame.init()
        self.contexto=pyudev.Context()
        self.player = vlc.MediaPlayer()
        self.monitor = pyudev.Monitor.from_netlink(self.contexto)
        self.monitor.filter_by(subsystem='block', device_type='partition')
        self.ruta_montaje="/mnt/usb"
        self.pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.alto_ventana, self.largo_ventana=self.pantalla.get_size()
        pygame.display.set_caption("Menú de Medios Extraíbles")

        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.GRIS = (200, 200, 200)
        self.AZUL_CLARO = (173, 216, 230)

        self.fuente = pygame.font.SysFont("Arial", 30)
        self.opciones = ["Reproducir Videos", "Reproducir Música", "Ver Fotos en Bucle", "Salir"]
        self.opcion_seleccionada = 0
        self.ejecutando = False

    def manejar_evento_dispositivo(self, action, device):
      if action == 'add':
        print(f"Dispositivo conectado: {device.device_node}")
        ruta_montaje = self.montar_dispositivo(device.device_node)
 #       if ruta_montaje:
 #         self.analizar_contenido(ruta_montaje)
      elif action == 'remove':
        print(f"Dispositivo desconectado: {device.device_node}")
        self.desmontar_dispositivo(device.device_node)

    

    def montar_dispositivo(self,device_node):
      ruta_montaje = "/mnt/usb"
      if not os.path.exists(ruta_montaje):
        os.makedirs(ruta_montaje)
      resultado = os.system(f"sudo mount {device_node} {ruta_montaje}")
      if resultado == 0:
        print(f"Dispositivo montado en: {ruta_montaje}")
        return ruta_montaje
      else:
        print("Error al montar el dispositivo.")
        return None
    def desmontar_dispositivo(self,device_node):
      resultado = os.system(f"sudo umount {device_node}")
      if resultado == 0:
        print(f"Dispositivo desmontado: {device_node}")
      else:
        print("Error al desmontar el dispositivo.")


    def mostrar_texto(self, texto, x, y, color=None):
        if color is None:
            color = self.NEGRO
        superficie_texto = self.fuente.render(texto, True, color)
        self.pantalla.blit(superficie_texto, (x, y))

    def detener_presentacion(self):
        try:
            if hasattr(self, 'proceso_slideshow'):
                self.proceso_slideshow.terminate()
                os.system("killall vlc 2>/dev/null")
                # Restaurar la ventana de Pygame
                pygame.display.set_mode((self.ancho_ventana, self.alto_ventana))
                pygame.display.flip()
        except Exception as e:
            print(f"Error al detener la presentación: {str(e)}")
    def detener_video(self):
        try:
            if hasattr(self, 'proceso_videos'):
                self.proceso_videos.terminate()
                os.system("killall vlc 2>/dev/null")
                pygame.display.set_mode((self.ancho_ventana, self.alto_ventana))
                pygame.display.flip()
        except Exception as e:
            print(f"Error al detener video: {str(e)}")

    def detener_musica(self):
        try:
            if hasattr(self, 'proceso_musica'):
                self.proceso_musica.terminate()
                os.system("killall vlc 2>/dev/null")
                pygame.display.set_mode((self.ancho_ventana, self.alto_ventana))
                pygame.display.flip()
        except Exception as e:
            print(f"Error deteniendo la musica: {str(e)}")

    def analizar_contenido_images(self, ruta_montaje):
    # Lista de extensiones de imagen soportadas
      extensiones_imagen = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    
    # Buscar archivos de imagen en la ruta
      image_files = []
      try:
          for file in os.listdir(ruta_montaje):
              if file.lower().endswith(extensiones_imagen):
                  ruta_completa = os.path.join(ruta_montaje, file)
                  if os.path.isfile(ruta_completa):
                      image_files.append(ruta_completa)
      except Exception as e:
          print(f"Error al buscar imágenes: {str(e)}")

    # Verificar si se encontraron imágenes
      if not image_files:
        print("No se encontraron archivos de imagen en la ruta proporcionada")
        

      try:
          # Ordenar las imágenes alfabéticamente
          image_files.sort()
        
          # Configurar los parámetros de VLC para la presentación
          vlc_params = [
              "vlc",
             "--fullscreen",              # Pantalla completa
             "--no-osd",                  # Sin información en pantalla
             "--loop",                    # Reproducción en bucle
             "--no-video-title-show",     # No mostrar título del video
             #"--slide-show-duration=5",   # 5 segundos por imagen
             "--no-audio",                # Sin audio
             "--no-video-deco",           # Sin decoraciones de ventana
             "--no-embedded-video",        # Sin video embebido
             "--play-and-exit"
          ]
        
          # Agregar todas las imágenes a la lista de reproducción
          vlc_params.extend(image_files)
        
          # Detener cualquier instancia previa de VLC
          os.system("killall vlc 2>/dev/null")
        
          # Iniciar la reproducción
          proceso = subprocess.Popen(vlc_params)
        
          # Guardar una referencia al proceso si necesitas controlarlo después
          self.proceso_slideshow = proceso
        
      except Exception as e:
          print(f"Error al iniciar la presentación: {str(e)}")

#Misma funcion para los videos
    def analizar_contenido_videos(self, ruta_montaje):
    # Lista de extensiones de imagen soportadas
      extensiones_video = ('.mp4', '.avi', '.mkv', '.mov', '.wmv','.flv')
    
    # Buscar archivos de imagen en la ruta
      video_files = []
      try:
          for file in os.listdir(ruta_montaje):
              if file.lower().endswith(extensiones_video):
                  ruta_completa = os.path.join(ruta_montaje, file)
                  if os.path.isfile(ruta_completa):
                      video_files.append(ruta_completa)
      except Exception as e:
          print(f"Error al buscar videos: {str(e)}")

    # Verificar si se encontraron imágenes
      if not video_files:
        print("No se encontraron archivos de video en la ruta proporcionada")
        

      try:
          # Ordenar los videos alfabéticamente
          video_files.sort()
        
          # Configurar los parámetros de VLC para la presentación
          vlc_params = [
              "vlc",
             "--fullscreen",              # Pantalla completa
             "--no-osd",                  # Sin información en pantalla
             "--loop",                    # Reproducción en bucle
             "--no-video-title-show",     # No mostrar título del video
             #"--slide-show-duration=5",   # 5 segundos por imagen
             "--no-video-deco",           # Sin decoraciones de ventana
             "--no-embedded-video",        # Sin video embebido
             "--play-and-exit"
          ]
        
          # Agregar todas las imágenes a la lista de reproducción
          vlc_params.extend(video_files)
        
          # Detener cualquier instancia previa de VLC
          os.system("killall vlc 2>/dev/null")
        
          # Iniciar la reproducción
          proceso = subprocess.Popen(vlc_params)
        
          # Guardar una referencia al proceso si necesitas controlarlo después
          self.proceso_videos = proceso
        
      except Exception as e:
          print(f"Error al iniciar la presentación: {str(e)}")

    def analizar_contenido_musica(self, ruta_montaje):
    # Lista de extensiones de imagen soportadas
      extensiones_musica = ('.mp3', '.wav', '.ogg', '.m4a', '.flac')
      music_files=[]
      try:
          for file in os.listdir(ruta_montaje):
              if file.endswith(extensiones_musica):
                  ruta_completa = os.path.join(ruta_montaje, file)
                  if os.path.isfile(ruta_completa):
                      music_files.append(ruta_completa)
      except Exception as e:
          print(f"Error al buscar videos: {str(e)}")

      if not music_files:
          print("Error al cargar archivos de musica")
      try:
          music_files.sort()

          vlc_params=["vlc",
                      "--loop",
                      "--fullscreen"]
          vlc_params.extend(music_files)
          os.system("killall vlc 2>/dev/null")
        
          # Iniciar la reproducción
          proceso = subprocess.Popen(vlc_params)
        
          # Guardar una referencia al proceso si necesitas controlarlo después
          self.proceso_musica = proceso
      except Exception as e:
          print(f"Error al iniciar la presentación: {str(e)}")

    
    def iniciar_menu(self):
        self.ejecutando = True
        observer=pyudev.MonitorObserver(self.monitor, self.manejar_evento_dispositivo)
        observer.start()
        while self.ejecutando:
            self.pantalla.fill(self.BLANCO)
            self.mostrar_texto("Selecciona una opción:", 50, 50)

            y_offset = 150
            for indice, texto in enumerate(self.opciones):
                color = self.AZUL_CLARO if indice == self.opcion_seleccionada else self.NEGRO
                self.mostrar_texto(texto, 60, y_offset, color)
                y_offset += 70
            self.mostrar_texto("ESC - Volver al menú principal", 50, self.alto_ventana - 60, self.GRIS)
            self.mostrar_texto("ENTER - Seleccionar opcion", 50,self.alto_ventana-30,self.GRIS)
            self.mostrar_texto("↑↓ - Moverse entre las opciones", 50, self.alto_ventana-90, self.GRIS)
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
                        if self.opciones[self.opcion_seleccionada] == "Reproducir Videos":
                            self.analizar_contenido_videos(self.ruta_montaje)
                        elif self.opciones[self.opcion_seleccionada] == "Reproducir Música":
                            self.analizar_contenido_musica(self.ruta_montaje)
                        elif self.opciones[self.opcion_seleccionada] == "Ver Fotos en Bucle":
                            self.analizar_contenido_images(self.ruta_montaje)
                        elif self.opciones[self.opcion_seleccionada] == "Salir":
                            self.ejecutando = False
                    elif evento.key == pygame.K_ESCAPE:
                        self.detener_presentacion()
                        self.detener_video()
                        self.detener_musica()        

            pygame.display.flip()

    def detener_menu(self):
        self.ejecutando = False
        pygame.quit()
