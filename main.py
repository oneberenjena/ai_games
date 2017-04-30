from kinematics import *
import pygame, sys
from pygame.locals import *

def main():
	# Permite que pygame funcione
	pygame.init()

	FPS = 30 # frames per second
	fpsClock = pygame.time.Clock() # Permite que el juego corra a una velocidad 2normal"

	# Configuracion de la ventana y fondo de la pantalla en formato (RGB)
	VENTANA = pygame.display.set_mode((800, 500), 0, 32)
	pygame.display.set_caption('Badteria - Version beta')
	WHITE = (255, 255, 255)

	# Se cargan los personajes y se escalan las imagenes - Las coordenadas son: z, x, y
	globuloBlanco = pygame.image.load('blanco.jpg')
	globuloBlanco = pygame.transform.scale(globuloBlanco, (50, 50))
	bacteria = pygame.image.load('bacteria.jpg')
	bacteria = pygame.transform.scale(bacteria, (50, 50))
	
	# Se crea la instancia de "character" y "target" respectivamente
	gb = Kinematic(np.array([[10],[10],[1]]), 1.5)
	b = Kinematic(np.array([[220],[250],[1]]), 1.0)

	# Se define el comportamiento deseado
	busqueda = KinematicSeek(gb, b)
	time = 0

	while True:
		print(time)
		VENTANA.fill(WHITE)
		time += 1
		""" ESTO PERMITE CAPTURAR TECLAS APENAS SON PRESIONADAS
		for event in pygame.event.get():
			# Teclado
			if event.type == KEYDOWN:
				if event.key in (K_LEFT, K_a):
					print("Izquierda")
				if event.key in (K_UP, K_w):
					print("Arriba")
				if event.key in (K_RIGHT, K_d):
					print("Derecha")
				if event.key in (K_DOWN, K_s):
					print("Abajo")
		"""
		# Movimiento y actualizacion de posiciones
		conduccion = busqueda.getSteering()
		gb.updateKinematic(conduccion, time)
		
		# Actualizacion de imagenes en la ventana de juego
		VENTANA.blit(globuloBlanco, (gb.position[0][0], gb.position[1][0]))
		VENTANA.blit(bacteria, (b.position[0][0], b.position[1][0]))

		for event in pygame.event.get():
			# Salir del programa
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update() # Se actualiza la pantalla
		fpsClock.tick(FPS) # Permite llevar un ritmo equilibrado de juego

if __name__ == '__main__':
	main()