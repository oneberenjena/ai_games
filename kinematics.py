import numpy as np

class Static():
	"""docstring for Static"""
	def __init__(self, position=np.zeros((1,3)), orientation=0.0):
		self.position = position
		self.orientation = orientation

class Kinematic():
			"""docstring for Kinematic"""
			def __init__(self, position=np.zeros((1,3)), orientation=0.0, velocity=np.zeros((1,3)), rotation=0.0):
				self.position = position
				self.orientation = orientation
				self.velocity = velocity
				self.rotation = rotation

			def update(steering, time):
				
				#Actualizar la posicion y la orientacion
				self.position = self.velocity*time
				self.orientation = self.rotation*time

				#Actualizar velocidad y rotacion
				self.velocity = steering.linear*time
				self.orientation = steering.angular*time

			def getNewOrientation(currentOrientation, velocity):

				#Si el agente va con una velocidad
				if np.linalg.norm(self.velocity) > 0:
					
					# Retornamos la orientacion
					return np.arctan2(-self.velocity[0], self.velocity[1])

				# Si no hay velocidad retornamos la orientacion actual
				else:
					return currentOrientation

class SteeringOutput():
	"""docstring for SteeringOutput"""
	def __init__(self, linear=np.zeros((1,3)), angular=0.0):
		self.linear = linear
		self.angular = angular
		
						
class KinematicSeek():
	"""docstring for KinematicSeek"""
	def __init__(self, character, target, maxSpeed):
		# Datos estaticos del agente y su objetivo
		self.character = character
		self.target = target
		# Velocidad maxima que puede alcanzar el agente
		self.maxSpeed = maxSpeed

	def getSteering():
		# Estructura de salida
		steering = KinematicSteeringOutput()

		# Se obtiene la direccion del objetivo
		steering.velocity = target.position - character.position

		# La velocidad va en esta direccion a toda marcha
		# normalize(steering.velocity[:np.newaxis], axis=0).ravel()
		steering.velocity /= np.linalg.norm(steering.velocity)
		steering.velocity *= maxSpeed

		# Se observa hacia la direccion que se quiere mover
		character.orientation = getNewOrientation(character.orientation, steering.velocity)

		# Retornamos la direccion
		steering.rotation = 0.0
		return steering


class KinematicSteeringOutput():
	"""docstring for KinematicSteeringOutput"""
	def __init__(self, velocity=np.zeros((1,3)), rotation=0.0):
		self.velocity = velocity
		self.rotation = rotation
		