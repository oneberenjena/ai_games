import numpy as np
import random		

class Static():
	"""docstring for Static"""
	def __init__(self, position=np.zeros((1,3)), orientation=0.0):
		self.position = position
		self.orientation = orientation

class Kinematic():
	"""docstring for Kinematic"""
	def __init__(self, position = np.zeros((3,1)), orientation = 0.0, velocity = np.zeros((3,1)), rotation = 0.0):
		self.position = position
		self.orientation = orientation
		self.velocity = velocity
		self.rotation = rotation

	def orientationAsVector(self):
		return np.array([[np.sin(self.orientation)],[np.cos(self.orientation)], [0]])

	def updateKinematic(self, steering, time):
		#Actualizar la posicion y la orientacion
		np.add(self.position, self.velocity * time, out = self.position, casting = "unsafe")
		self.orientation += self.rotation * time
		#Actualizar velocidad y rotacion
		self.velocity = steering.velocity
		self.rotation = steering.rotation

	def updateSteering(self, steering, time):
		#Actualizar la posicion y la orientacion
		np.add(self.position, self.velocity * time, out = self.position, casting = "unsafe")
		self.orientation += self.rotation * time
		#Actualizar velocidad y rotacion
		self.velocity += steering.linear * time
		self.rotation += steering.angular * time
	
	def getNewOrientation(self, velocity):
		#Si el agente va con una velocidad
		if np.linalg.norm(self.velocity) > 0:
			# Calculate orientation using an arc tangent of the velocity components.
			return np.arctan2(-self.velocity[0], self.velocity[1])
		# Si no hay velocidad retornamos la orientacion actual
		else: 
			return self.orientation

	"""
	def update(self,steering, time):
		
		#Actualizar la posicion y la orientacion
		#self.position = self.velocity*time
		np.add(self.position, self.velocity * time, out = self.position, casting = "unsafe")
		self.orientation = self.rotation * time

		#Actualizar velocidad y rotacion
		self.velocity = steering.linear * time
		self.orientation = steering.angular * time
	"""

class SteeringOutput():
	"""docstring for SteeringOutput"""
	def __init__(self, linear = np.zeros((3,1)), angular = 0.0):
		self.linear = linear
		self.angular = angular
		
class KinematicSteeringOutput():
	"""docstring for KinematicSteeringOutput"""
	def __init__(self, velocity = np.zeros((3,1)), rotation = 0.0): 
		self.velocity = velocity
		self.rotation = rotation
						
class KinematicSeek():
	"""docstring for KinematicSeek"""
	def __init__(self, character, target, maxSpeed = 0.1):
		# Datos estaticos del agente y su objetivo
		self.character = character
		self.target = target
		# Velocidad maxima que puede alcanzar el agente
		self.maxSpeed = maxSpeed

	def getSteering(self, isSeek = True):
		# Estructura de salida
		steering = KinematicSteeringOutput()

		# Se obtiene la direccion del objetivo
		if isSeek:
			steering.velocity = self.target.position - self.character.position
		else:			
			steering.velocity = self.character.position - self.target.position 

		# La velocidad va en esta direccion a toda marcha
		# normalize(steering.velocity[:np.newaxis], axis=0).ravel()
		if np.linalg.norm(steering.velocity) > 0:
			steering.velocity =  steering.velocity / np.linalg.norm(steering.velocity)
		#steering.velocity /= np.linalg.norm(steering.velocity)
		steering.velocity *= self.maxSpeed

		# Se observa hacia la direccion que se quiere mover
		self.character.orientation = self.character.getNewOrientation(steering.velocity)

		# Retornamos la direccion
		steering.rotation = 0.0
		return steering

class KinematicArrive():
	"""docstring for KinematicArrive"""
	def __init__(self, character, target, maxSpeed = 0.1, radius = 3.0, timeToTarget = 0.25):
		self.character = character
		self.target = target
		self.maxSpeed = maxSpeed

		# El radio en el que empieza a disminuir la velocidad
		self.radius = radius

		# El tiempo que tardara en llegar al objetivo (constante)
		self.timeToTarget = timeToTarget

	def getSteering(self):
		# Estructura de salida
		steering = KinematicSteeringOutput()

		# Obtenemos la direccion del objetivo
		steering.velocity = self.target.position - self.character.position

		# Si estamos en el radio
		if np.linalg.norm(steering.velocity) < self.radius:
			# No podemos retornar la direccion
			return None

		# Para movernos hacia el objetivo. Se quiere hacer en
		# timeToTarget segundos 
		steering.velocity = steering.velocity / self.timeToTarget

		# Si es demasiado rapido, acortamos la velocidad a la maxima
		if np.linalg.norm(steering.velocity) > self.maxSpeed:
			steering.velocity = steering.velocity / np.linalg.norm(steering.velocity)
			steering.velocity *= self.maxSpeed
			#print("Arriving")
			#print(steering.velocity,steering.velocity.shape)
		# Hacemos que se observe a la direccion que queremos movernos
		self.character.orientation = self.character.getNewOrientation(steering.velocity)

		# Retornamos la direccion
		steering.rotation = 0.0
		return steering

class KinematicWandering():
	"""docstring for KinematicWandering"""
	def __init__(self, character, maxSpeed=0.01, maxRotation=1.0):
		self.character = character
		self.maxSpeed = maxSpeed
		self.maxRotation = maxRotation

	def getSteering(self):
		# Estructura de salida
		steering = KinematicSteeringOutput()
		# Obtener la velocidad del vector de orientacion
		steering.velocity = self.maxSpeed * self.character.orientationAsVector()
		#print("Wandering")
		#print(steering.velocity,steering.velocity.shape)
		# Cambia la orientacion aleatoriamente
		steering.rotation = randomBinomial() * self.maxRotation
		# Retorna la direccion 
		return steering
	
def randomBinomial():
	return random.random() - random.random()