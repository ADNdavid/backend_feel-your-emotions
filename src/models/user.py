"""
Modelo de Usuario para el sistema de monitoreo emocional.
Representa a un joven que utiliza la plataforma para monitoreo emocional.
"""

from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Dict, Any, Optional
import uuid

class UserBase(SQLModel):
    name: str = Field(description="Nombre completo del usuario")
    age: int = Field(ge=13, le=25, description="Edad del usuario (entre 13 y 25 años)")
    context: str = Field(description="Contexto de vulnerabilidad del usuario")
    gender: str = Field(default=None, description="Género del usuario")

class User(UserBase, table=True):
    user_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    registration_date: Optional[datetime] = Field(default_factory=datetime.now, description="Fecha de registro en el sistema")
    
class UserCreate(User):
    """
    Clase que representa a un usuario del sistema de monitoreo emocional.
    
    Attributes:
        user_id (str): Identificador único del usuario
        name (str): Nombre completo del usuario
        age (int): Edad del usuario
        context (str): Contexto de vulnerabilidad del usuario
        gender (str): Género del usuario
        registration_date (datetime): Fecha de registro en el sistema
    """
    
    def __init__(self, name: str, age: int, context: str, gender: str):
        """
        Inicializa un nuevo usuario.
        
        Args:
            name (str): Nombre completo del usuario
            age (int): Edad del usuario (debe estar entre 13 y 25 años)
            context (str): Contexto de vulnerabilidad 
            gender (str): Género del usuario
        Raises:
            ValueError: Si la edad no está en el rango válido
        """
        if not 13 <= age <= 25:
            raise ValueError("La edad debe estar entre 13 y 25 años")
        
        self.user_id = str(uuid.uuid4())
        self.name = name.strip()
        self.age = age
        self.context = context.strip()
        self.gender = gender.strip() if gender else None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Crea un usuario a partir de un diccionario.
        
        Args:
            data (dict): Datos del usuario
            
        Returns:
            User: Instancia de usuario
        """
        user = cls(
            name=data['name'],
            age=data['age'],
            context=data['context'],
            gender=data['gender']
        )
        user.user_id = data['user_id']
        user.registration_date = data['registration_date']
        return user
    
    def __str__(self) -> str:
        """Representación en string del usuario."""
        return f"Usuario: {self.name}, Edad: {self.age}, Contexto: {self.context}"
    
    def __repr__(self) -> str:
        """Representación técnica del usuario."""
        return f"User(id='{self.user_id}', name='{self.name}', age={self.age})"