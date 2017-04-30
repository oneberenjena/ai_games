from kinematics import *
import pygame, sys
from pygame.locals import *

def main():
	# Permite que pygame funcione
	pygame.init()

	FPS = 30 # frames per second
	fpsClock = pygame.time.Clock() # Permite que el juego corra a una velocidad 2normal"

	# Configuracion de la ventana y fondo de la pantalla en formato (RGB)
	WIDTH = 800
	HEIGHT = 600
	VENTANA = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
	pygame.display.set_caption('Badteria - Version beta')
	WHITE = (255, 255, 255)

	# Se cargan los personajes y se escalan las imagenes
	globuloBlanco = pygame.image.load('blanco.jpg')
	globuloBlanco = pygame.transform.scale(globuloBlanco, (50, 50))
	badteria = pygame.image.load('bacteria.jpg')
	badteria = pygame.transform.scale(badteria, (50, 50))
	
	# Lugares random donde saldran los personajes
	z1 = random.randint(0,WIDTH) 
	z2 = random.randint(0,WIDTH)
	x1 = random.randint(0,HEIGHT)
	x2 = random.randint(0,HEIGHT)

	# Se crea la instancia de "character" y "target" respectivamente - Las coordenadas son: z, x, y
	gb = Kinematic(np.array([[z1],[x1],[1]]), 1.5)
	bad = Kinematic(np.array([[z2],[x2],[1]]), 1.5)

	# Se define el comportamiento deseado:
	#
	#busqueda = KinematicSeek(gb, bad)
	#huida = KinematicSeek(bad, gb)
	#
	#llegar = KinematicArrive(gb, bad)
	
	deambular = KinematicWandering(gb)

	time = 0

	while True:
		#print(time)
		VENTANA.fill(WHITE)
		time += 1
		""" ESTO PERMITE CAPTURAR TECLAS APENAS SON PRESIONADAS - DT: Lo dejo por si tenemos que jugar o queremos probar eventos
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
		
		## SEEK AND FLEE
		#acercar = busqueda.getSteering()
		#alejar = huida.getSteering(False)
		#gb.updateKinematic(acercar, time)
		#bad.updateKinematic(alejar, time)

		## ARRIVE - DT: Da peos con maxSpeed > 0.1 si el radio es <= 4.0 (Se vuelve loco tipo Seek) 
		#llegada = llegar.getSteering()
		#gb.updateKinematic(llegada, time)
		
		## WANDER
		deambulando = deambular.getSteering()
		gb.updateKinematic(deambulando, time)

		# Actualizacion de imagenes en la ventana de juego
		VENTANA.blit(globuloBlanco, (gb.position[0][0], gb.position[1][0]))
		VENTANA.blit(badteria, (bad.position[0][0], bad.position[1][0]))

		for event in pygame.event.get():
			# Salir del programa
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update() # Se actualiza la pantalla
		fpsClock.tick(FPS) # Permite llevar un ritmo equilibrado de juego

if __name__ == '__main__':
	main()