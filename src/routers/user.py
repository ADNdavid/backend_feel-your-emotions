from fastapi import APIRouter, HTTPException, status
from ..models.user import User
from db import session_dependency
from sqlmodel import select

router = APIRouter(tags=["Users"], prefix="/api")

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user_data: User, session: session_dependency):
    """
    Endpoint para crear un nuevo usuario.
    
    Args:
        user_data (User): Datos del usuario a crear
        
    Returns:
        dict: Datos del usuario creado
    """
    # Aquí iría la lógica para guardar el usuario en la base de datos
    # Por ahora, simplemente devolvemos los datos recibidos
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data.to_dict()

@router.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int, session: session_dependency):
    """
    Endpoint para obtener un usuario por su ID.
    
    Args:
        user_id (int): ID del usuario a obtener
        
    Returns:
        dict: Datos del usuario
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user.to_dict()

@router.get("/users", response_model=list[User])
async def list_users(session: session_dependency):
    """
    Endpoint para listar todos los usuarios.
    
    Returns:
        list: Lista de usuarios
    """
    users = session.exec(select(User)).all()
    return [user.to_dict() for user in users]

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: session_dependency):
    """
    Endpoint para eliminar un usuario por su ID.
    
    Args:
        user_id (int): ID del usuario a eliminar
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    session.delete(user)
    session.commit()
    return {"detail": "Usuario eliminado exitosamente"}
