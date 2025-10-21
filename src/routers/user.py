from fastapi import APIRouter, HTTPException, status

from src.utils.demo_info import DemoGenerator
from ..models.user import User, UserBase

# Mensajes y constantes reutilizables
_MSG_USER_NOT_FOUND = "Usuario no encontrado"
from db import session_dependency
from sqlmodel import select

router = APIRouter(tags=["Users"], prefix="/api")

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user_data: UserBase, session: session_dependency):
    """
    Endpoint para crear un nuevo usuario.
    
    Args:
        user_data (UserBase): Datos del usuario a crear incluyendo:
            - name (str): Nombre completo
            - age (int): Edad (13-25 años)
            - context (str): Contexto de vulnerabilidad
            - gender (str, opcional): Género del usuario
        
    Returns:
        User: Datos del usuario creado
    """
    # Construir una instancia mapeada de User a partir del payload
    user_dict = user_data.model_dump()
    user = User(**user_dict)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/user/{user_id}", response_model=User)
async def get_user(user_id: str, session: session_dependency):
    """
    Endpoint para obtener un usuario por su ID.
    
    Args:
        user_id (str): ID del usuario a obtener
        
    Returns:
        dict: Datos del usuario
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_MSG_USER_NOT_FOUND)
    return user

@router.get("/users", response_model=list[User])
async def list_users(session: session_dependency):
    """
    Endpoint para listar todos los usuarios.
    
    Returns:
        list: Lista de usuarios
    """
    users = session.exec(select(User)).all()
    return users

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, session: session_dependency):
    """
    Endpoint para eliminar un usuario por su ID.
    
    Args:
        user_id (str): ID del usuario a eliminar
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_MSG_USER_NOT_FOUND)
    session.delete(user)
    session.commit()
    return {"detail": "Usuario eliminado exitosamente"}

@router.put("/user/{user_id}", response_model=User)
async def update_user(user_id: str, user_data: UserBase, session: session_dependency):
    """
    Endpoint para actualizar un usuario por su ID.
    
    Args:
        user_id (str): ID del usuario a actualizar
        user_data (User): Nuevos datos del usuario
        
    Returns:
        dict: Datos del usuario actualizado
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    user_data_dict = user_data.model_dump(exclude_unset=True)
    for key, value in user_data_dict.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/users/random", status_code=status.HTTP_201_CREATED)
async def generate_random_users():
    """
    Endpoint para generar usuarios de demostración aleatorios.
    Returns:
        dict: Detalle del resultado de la operación
    """
    #Crear el generador de datos
    demo = DemoGenerator()
    demo.generate_demo_data()
    return {"detail": "Usuarios de demostración generados exitosamente"}