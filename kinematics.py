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

	def updateKinematic(self, steering, time, maxSpeed=0.05):
		#Actualizar la posicion y la orientacion
		np.add(self.position, self.velocity * time, out = self.position, casting = "unsafe")
		self.orientation += self.rotation * time
		#Actualizar velocidad y rotacion
		self.velocity = steering.velocity
		self.rotation = steering.rotation

		if np.linalg.norm(self.velocity) > maxSpeed:
			self.velocity = self.velocity / np.linalg.norm(self.velocity)
			self.velocity *= maxSpeed

	def updateSteering(self, steering, time, maxSpeed=0.1):
		#Actualizar la posicion y la orientacion
		np.add(self.position, self.velocity * time, out = self.position, casting = "unsafe")
		self.orientation += self.rotation * time
		#Actualizar velocidad y rotacion
		self.velocity += steering.linear * time
		self.rotation += steering.angular * time

		if np.linalg.norm(self.velocity) > maxSpeed:
			self.velocity = self.velocity / np.linalg.norm(self.velocity)
			self.velocity *= maxSpeed
	
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
	def __init__(self, character, target, maxSpeed = 0.05, radius = 5.0, timeToTarget = 0.25):
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
			# retornabamos None, ahora hacemos que la velocidad desaparezca para 
			# frenar al character y emular la llegada correctamente
			steering.velocity = 0.0
			return steering

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
	def __init__(self, character, maxSpeed=0.001, maxRotation=1.0):
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
	
class Seek():
	"""docstring for Seek"""
	def __init__(self, character, target, maxAcceleration=0.1):
		self.character = character
		self.target = target
		# La maxima aceleracion que puede tener el agente
		self.maxAcceleration = maxAcceleration

	def getSteering(self, isSeek=True):
		steering = SteeringOutput()

		if isSeek:
			steering.linear = self.target.position - self.character.position
		else:
			steering.linear = self.character.position - self.target.position
		print("Got linear: ")
		print(steering.linear)

		steering.linear = np.linalg.norm(steering.linear)
		steering.linear *= self.maxAcceleration

		# Hay que darle una orientacion 
		# Deberia ir aqui
		
		steering.angular = 0.0
		return steering

class Arrive():
	"""docstring for Arrive"""
	def __init__(self, character, target, maxAcceleration=0.01, maxSpeed=0.05, targetRadius=5., slowRadius=10., timeToTarget=2.):
		self.character = character
		self.target = target
		self.maxAcceleration = maxAcceleration
		self.maxSpeed = maxSpeed
		self.targetRadius = targetRadius
		self.slowRadius = slowRadius
		self.timeToTarget = timeToTarget

	def getSteering(self):
		steering = SteeringOutput()

		# Obtenemos la direccion al objetivo
		direction = self.target.position - self.character.position
		distance = np.linalg.norm(direction)

		# Si estamos en el radio del objetivo, devolvemos direccion nula (llegamos)
		if distance < self.targetRadius:
			steering.linear = np.zeros((3,1))
			steering.angular = 0.0
			return steering

		# Si estamos fuera del radio de frenado, aceleramos
		if distance > self.slowRadius:
			targetSpeed = self.maxSpeed
		# Caso contrario escalamos la velocidad  
		else:
			targetSpeed = self.maxSpeed*distance / self.slowRadius

		# Calculamos el vector velocidad del target que combina la velocidad y la direccion
		targetVelocity = direction
		targetVelocity = targetVelocity / np.linalg.norm(targetVelocity)
		targetVelocity *= targetSpeed

		# La aceleracion trata de acercar la velocidad a la del target
		steering.linear = targetVelocity - self.character.velocity
		steering.linear = steering.linear / self.timeToTarget

		# Chequeamos si la aceleracion excedera la llegada
		if np.linalg.norm(steering.linear) > self.maxAcceleration:
			steering.linear = steering.linear / np.linalg.norm(steering.linear)
			steering.linear *= self.maxAcceleration

		steering.angular = 0.0
		return steering

def randomBinomial():
	return random.random() - random.random()