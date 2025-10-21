"""
Servicio para gestión de usuarios en el sistema.
Maneja operaciones CRUD y lógica de negocio relacionada con usuarios.
Permite almacenamiento dual: Base de datos SQL y respaldo en CSV local.
"""

import pandas as pd
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
from sqlmodel import Session, select
from db import engine
from ..models.user import User, UserBase, UserCreate

class UserService:
    """
    Servicio para gestionar usuarios.
    
    Maneja el registro, actualización, búsqueda y eliminación de usuarios,
    así como la persistencia de datos en la base de datos y respaldo en CSV.
    """
    
    def __init__(self, data_path: str = "data/processed"):
        """
        Inicializa el servicio de usuarios.
        
        Args:
            data_path (str): Ruta donde se almacenan los archivos de respaldo CSV
        """
        self.data_path = data_path
        self.users_file = os.path.join(data_path, "users.csv")
        self._ensure_data_directory()
        
    def _ensure_data_directory(self) -> None:
        """Crea el directorio de datos si no existe."""
        os.makedirs(self.data_path, exist_ok=True)
        
    def _sync_to_csv(self) -> None:
        """Sincroniza los datos de la base de datos al archivo CSV."""
        with Session(engine) as session:
            users = session.exec(select(User)).all()
            if not users:
                return
            
            data = []
            for user in users:
                user_dict = {
                    'user_id': user.user_id,
                    'name': user.name,
                    'age': user.age,
                    'context': user.context,
                    'gender': user.gender,
                    'registration_date': user.registration_date.isoformat() if user.registration_date else None
                }
                data.append(user_dict)
            
            df = pd.DataFrame(data)
            df.to_csv(self.users_file, index=False)
    
    def register_user(self, name: str, age: int, context: str, gender: str) -> User:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            name (str): Nombre completo del usuario
            age (int): Edad del usuario (entre 13 y 25 años)
            context (str): Contexto de vulnerabilidad
            gender (str): Género del usuario
        Returns:
            User: Usuario creado y registrado
            
        Raises:
            ValueError: Si los datos no son válidos o el usuario ya existe
        """
        with Session(engine) as session:
            # Verificar si el usuario ya existe
            existing_user = session.exec(
                select(User).where(User.name == name)
            ).first()
            
            if existing_user:
                raise ValueError(f"Ya existe un usuario con el nombre: {name}")
            
            # Crear nuevo usuario
            user_data = {
                "name": name.strip(),
                "age": age,
                "context": context.strip(),
                "gender": gender.strip()
            }
            
            user = User(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            
            # Sincronizar con CSV
            self._sync_to_csv()
            
            print(f"✅ Usuario registrado exitosamente: {user.name}")
            return user
    
    def _save_user_to_csv(self, user: User) -> None:
        """
        Guarda un usuario en el archivo CSV.
        
        Args:
            user (User): Usuario a guardar
        """
        user_data = user.to_dict()
        
        # Convertir perfil emocional a columnas individuales
        profile = user_data.pop('emotional_profile')
        for key, value in profile.items():
            if isinstance(value, list):
                user_data[f'profile_{key}'] = str(value)
            else:
                user_data[f'profile_{key}'] = value
        
        # Crear DataFrame
        df = pd.DataFrame([user_data])
        
        # Guardar o agregar al archivo existente
        if os.path.exists(self.users_file):
            existing_df = pd.read_csv(self.users_file)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_csv(self.users_file, index=False)
    
    def get_all_users(self) -> List[User]:
        """
        Obtiene todos los usuarios registrados.
        
        Returns:
            List[User]: Lista de todos los usuarios
        """
        with Session(engine) as session:
            return session.exec(select(User)).all()
    
    def _row_to_user_dict(self, row: pd.Series) -> Dict[str, Any]:
        """
        Convierte una fila del DataFrame a diccionario de usuario.
        
        Args:
            row (pd.Series): Fila del DataFrame
            
        Returns:
            dict: Datos del usuario
        """
        # Extraer perfil emocional
        emotional_profile = {}
        for col in row.index:
            if col.startswith('profile_'):
                key = col.replace('profile_', '')
                value = row[col]
                if key in ['risk_factors', 'strengths']:
                    # Convertir string de lista de vuelta a lista
                    emotional_profile[key] = eval(value) if pd.notna(value) else []
                else:
                    emotional_profile[key] = value
        
        return {
            'user_id': row['user_id'],
            'name': row['name'],
            'age': int(row['age']),
            'gender': row['gender'],
            'context': row['context'],
            'registration_date': row['registration_date'],
            'emotional_profile': emotional_profile
        }
    
    def find_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Busca un usuario por su ID.
        
        Args:
            user_id (str): ID del usuario a buscar
            
        Returns:
            Optional[User]: Usuario encontrado o None
        """
        with Session(engine) as session:
            return session.get(User, user_id)
    
    def find_user_by_name(self, name: str) -> Optional[User]:
        """
        Busca un usuario por su nombre.
        
        Args:
            name (str): Nombre del usuario a buscar
            
        Returns:
            Optional[User]: Usuario encontrado o None
        """
        with Session(engine) as session:
            return session.exec(
                select(User).where(User.name == name)
            ).first()
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """
        Actualiza los datos de un usuario.
        
        Args:
            user_id (str): ID del usuario a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            bool: True si se actualizó correctamente
        """
        with Session(engine) as session:
            user = session.get(User, user_id)
            if not user:
                return False
            
            # Validar y actualizar campos permitidos
            valid_fields = {'name', 'age', 'context', 'gender'}
            update_data = {k: v for k, v in kwargs.items() if k in valid_fields}
            
            # Validar y limpiar valores
            if 'gender' in update_data and update_data['gender']:
                update_data['gender'] = update_data['gender'].strip()
            
            for key, value in update_data.items():
                setattr(user, key, value)
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            # Sincronizar con CSV
            self._sync_to_csv()
            
            print(f"✅ Usuario actualizado: {user.name}")
            return True
    
    def _save_all_users(self, users: List[User]) -> None:
        """
        Guarda todos los usuarios en el archivo CSV.
        
        Args:
            users (List[User]): Lista de usuarios a guardar
        """
        if not users:
            return
        
        all_data = []
        for user in users:
            user_data = user.to_dict()
            profile = user_data.pop('emotional_profile')
            for key, value in profile.items():
                if isinstance(value, list):
                    user_data[f'profile_{key}'] = str(value)
                else:
                    user_data[f'profile_{key}'] = value
            all_data.append(user_data)
        
        df = pd.DataFrame(all_data)
        df.to_csv(self.users_file, index=False)
    
    def delete_user(self, user_id: str) -> bool:
        """
        Elimina un usuario del sistema.
        
        Args:
            user_id (str): ID del usuario a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        with Session(engine) as session:
            user = session.get(User, user_id)
            if not user:
                return False
            
            session.delete(user)
            session.commit()
            
            # Sincronizar con CSV
            self._sync_to_csv()
            
            print("✅ Usuario eliminado correctamente")
            return True
    
    def get_users_by_context(self, context: str) -> List[User]:
        """
        Obtiene usuarios filtrados por contexto.
        
        Args:
            context (str): Contexto a filtrar
            
        Returns:
            List[User]: Lista de usuarios con ese contexto
        """
        with Session(engine) as session:
            return session.exec(
                select(User).where(User.context.contains(context.lower()))
            ).all()
    
    def get_users_at_risk(self, risk_threshold: float = 6.0) -> List[User]:
        """
        Obtiene usuarios con puntaje de riesgo alto.
        
        Args:
            risk_threshold (float): Umbral de riesgo
            
        Returns:
            List[User]: Lista de usuarios en riesgo
        """
        users = self.get_all_users()
        return [user for user in users if user.get_risk_score() >= risk_threshold]
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de usuarios.
        
        Returns:
            dict: Estadísticas de usuarios
        """
        users = self.get_all_users()
        
        if not users:
            return {
                'total_users': 0,
                'avg_age': 0,
                'avg_risk_score': 0,
                'contexts': {},
                'users_at_risk': 0
            }
        
        ages = [user.age for user in users]
        risk_scores = [user.get_risk_score() for user in users]
        contexts = {}
        
        # Contar contextos
        for user in users:
            contexts[user.context] = contexts.get(user.context, 0) + 1
        
        # Usuarios en riesgo
        users_at_risk = len([user for user in users if user.get_risk_score() >= 6.0])
        
        return {
            'total_users': len(users),
            'avg_age': sum(ages) / len(ages),
            'avg_risk_score': sum(risk_scores) / len(risk_scores),
            'contexts': contexts,
            'users_at_risk': users_at_risk,
            'risk_percentage': (users_at_risk / len(users)) * 100
        }
    
    def export_users_data(self, filename: str = None) -> str:
        """
        Exporta los datos de usuarios a un archivo CSV.
        
        Args:
            filename (str, optional): Nombre del archivo de exportación
            
        Returns:
            str: Ruta del archivo exportado
        """
        if filename is None:
            filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        export_path = os.path.join("data/exports", filename)
        os.makedirs("data/exports", exist_ok=True)
        
        # Obtener datos actualizados y exportar
        with Session(engine) as session:
            users = session.exec(select(User)).all()
            if not users:
                print("❌ No hay datos de usuarios para exportar")
                return export_path
            
            data = []
            for user in users:
                data.append({
                    'user_id': user.user_id,
                    'name': user.name,
                    'age': user.age,
                    'context': user.context,
                    'gender': user.gender,
                    'registration_date': user.registration_date.isoformat() if user.registration_date else None
                })
            
            df = pd.DataFrame(data)
            df.to_csv(export_path, index=False)
            print(f"✅ Datos exportados a: {export_path}")
        
        return export_path