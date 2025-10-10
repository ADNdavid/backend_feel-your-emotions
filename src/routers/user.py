from fastapi import APIRouter, HTTPException, status
from ..models.user import User, UserBase
from db import session_dependency
from sqlmodel import select

router = APIRouter(tags=["Users"], prefix="/api")

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user_data: UserBase, session: session_dependency):
    """
    Endpoint para crear un nuevo usuario.
    
    Args:
        user_data (User): Datos del usuario a crear
        
    Returns:
        dict: Datos del usuario creado
    """
    user = User.model_validate(user_data.model_dump())
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
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