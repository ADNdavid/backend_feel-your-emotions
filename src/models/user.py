"""
Modelo de Usuario para el sistema.
Representa a un joven que utiliza la plataforma para monitoreo emocional.
"""

from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Dict, Any, Optional
import uuid

class User(SQLModel, table=True):
    user_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    name: str = Field(index=True)
    age: int = Field(ge=13, le=25, description="Edad del usuario (entre 13 y 25 años)")
    context: str = Field(description="Contexto de vulnerabilidad del usuario")
    registration_date: datetime = Field(default_factory=datetime.now)
    #emotional_profile: Optional[Dict[str, Any]] = Field(default_factory=lambda: None, sa_column_kwargs={"nullable": True})

#class UserCreate(User):
#    """
#    Clase que representa a un usuario del sistema de monitoreo emocional.
#    
#    Attributes:
#        user_id (str): Identificador único del usuario
#        name (str): Nombre completo del usuario
#        age (int): Edad del usuario
#        context (str): Contexto de vulnerabilidad del usuario
#        registration_date (datetime): Fecha de registro en el sistema
#        emotional_profile (dict): Perfil emocional inicial del usuario
#    """
#    
#    def __init__(self, name: str, age: int, context: str, 
#                emotional_profile: Optional[Dict[str, Any]] = None):
#        """
#        Inicializa un nuevo usuario.
#        
#        Args:
#            name (str): Nombre completo del usuario
#            age (int): Edad del usuario (debe estar entre 13 y 25 años)
#            context (str): Contexto de vulnerabilidad
#            emotional_profile (dict, optional): Perfil emocional inicial
#        
#        Raises:
#            ValueError: Si la edad no está en el rango válido
#        """
#        if not 13 <= age <= 25:
#            raise ValueError("La edad debe estar entre 13 y 25 años")
#        
#        self.user_id = str(uuid.uuid4())
#        self.name = name.strip()
#        self.age = age
#        self.context = context.strip()
#        self.registration_date = datetime.now()
#        self.emotional_profile = emotional_profile or self._create_default_profile()
#    
#    def _create_default_profile(self) -> Dict[str, Any]:
#        """
#        Crea un perfil emocional por defecto.
#        
#        Returns:
#            dict: Perfil emocional con valores iniciales
#        """
#        return {
#            'anxiety_level': 3,  # Escala 1-5
#            'depression_level': 3,
#            'stress_level': 3,
#            'social_support': 3,
#            'self_esteem': 3,
#            'risk_factors': [],
#            'strengths': []
#        }
#    
#    def update_emotional_profile(self, **kwargs) -> None:
#        """
#        Actualiza el perfil emocional del usuario.
#        
#        Args:
#            **kwargs: Campos del perfil emocional a actualizar
#        """
#        for key, value in kwargs.items():
#            if key in self.emotional_profile:
#                self.emotional_profile[key] = value
#    
#    def add_risk_factor(self, factor: str) -> None:
#        """
#        Añade un factor de riesgo al perfil.
#        
#        Args:
#            factor (str): Factor de riesgo a añadir
#        """
#        if factor not in self.emotional_profile['risk_factors']:
#            self.emotional_profile['risk_factors'].append(factor)
#    
#    def add_strength(self, strength: str) -> None:
#        """
#        Añade una fortaleza al perfil.
#        
#        Args:
#            strength (str): Fortaleza a añadir
#        """
#        if strength not in self.emotional_profile['strengths']:
#            self.emotional_profile['strengths'].append(strength)
#    
#    def get_risk_score(self) -> float:
#        """
#        Calcula un puntaje de riesgo basado en el perfil emocional.
#        
#        Returns:
#            float: Puntaje de riesgo (0-10, donde 10 es mayor riesgo)
#        """
#        # Algoritmo simple de cálculo de riesgo
#        anxiety = self.emotional_profile.get('anxiety_level', 3)
#        depression = self.emotional_profile.get('depression_level', 3)
#        stress = self.emotional_profile.get('stress_level', 3)
#        social_support = self.emotional_profile.get('social_support', 3)
#        self_esteem = self.emotional_profile.get('self_esteem', 3)
#        
#        # Factores negativos (más alto = más riesgo)
#        negative_score = (anxiety + depression + stress) / 3
#        
#        # Factores protectivos (más alto = menos riesgo)
#        protective_score = (social_support + self_esteem) / 2
#        
#        # Puntuación final (escala 0-10)
#        risk_score = ((negative_score * 2) - protective_score) * 2
#        
#        # Ajustar por factores de riesgo adicionales
#        risk_factors_count = len(self.emotional_profile.get('risk_factors', []))
#        risk_score += risk_factors_count * 0.5
#        
#        # Asegurar que esté en rango 0-10
#        return max(0, min(10, risk_score))
#    
#    def to_dict(self) -> Dict[str, Any]:
#        """
#        Convierte el usuario a diccionario para almacenamiento.
#        
#        Returns:
#            dict: Representación del usuario como diccionario
#        """
#        return {
#            'user_id': self.user_id,
#            'name': self.name,
#            'age': self.age,
#            'context': self.context,
#            'registration_date': self.registration_date.isoformat(),
#            'emotional_profile': self.emotional_profile,
#            'risk_score': self.get_risk_score()
#        }
#    
#    @classmethod
#    def from_dict(cls, data: Dict[str, Any]) -> 'User':
#        """
#        Crea un usuario a partir de un diccionario.
#        
#        Args:
#            data (dict): Datos del usuario
#            
#        Returns:
#            User: Instancia de usuario
#        """
#        user = cls(
#            name=data['name'],
#            age=data['age'],
#            context=data['context'],
#            emotional_profile=data['emotional_profile']
#        )
#        user.user_id = data['user_id']
#        user.registration_date = datetime.fromisoformat(data['registration_date'])
#        return user
#    
#    def __str__(self) -> str:
#        """Representación en string del usuario."""
#        return f"Usuario: {self.name}, Edad: {self.age}, Riesgo: {self.get_risk_score():.1f}/10"
#    
#    def __repr__(self) -> str:
#        """Representación técnica del usuario."""
#        return f"User(id='{self.user_id}', name='{self.name}', age={self.age})"