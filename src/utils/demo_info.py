"""
Utilidad para generar datos de demostración en el sistema.
"""

from typing import List
import random
from datetime import datetime, timedelta
from ..models.user import User, UserBase
from ..models.survey import Survey, SurveyBase, SurveyType
from ..services.user import UserService
from ..services.survey import SurveyService

class DemoGenerator:
    """Clase para generar datos de demostración del sistema."""
    
    def __init__(self):
        """Inicializa el generador de datos de demostración."""
        self.user_service = UserService()
        self.survey_service = SurveyService()

    def generate_demo_data(self) -> None:
        """Ejecuta una demostración del sistema con datos de prueba."""
        print("\n🎬 MODO DEMOSTRACIÓN")
        print("="*50)
        print("Creando datos de prueba para demostrar el sistema...")
        
        try:
            # Crear usuarios de prueba
            demo_users = [
                ("Ana García", 17, "Estudiante en situación de vulnerabilidad económica"),
                ("Carlos Rodríguez", 20, "Joven en contexto de violencia familiar"),
                ("María López", 19, "Adolescente con ansiedad social"),
                ("Diego Martínez", 22, "Universitario con depresión"),
                ("Sofía Hernández", 18, "Joven madre soltera")
            ]
            
            print("\n👥 Registrando usuarios de prueba...")
            created_users = []
            for name, age, context in demo_users:
                try:
                    user_data = {
                        "name": name,
                        "age": age,
                        "context": context
                    }
                    user = self.user_service.register_user(**user_data)
                    created_users.append(user)
                    print(f"  ✅ {name}")
                except Exception as e:
                    print(f"  ❌ Error al crear usuario {name}: {str(e)}")
            
            # Crear encuestas de prueba
            print("\n📝 Generando encuestas de prueba...")
            
            for user in created_users:
                # Crear 3-5 encuestas por usuario
                num_surveys = random.randint(3, 5)
                for i in range(num_surveys):
                    # Crear datos de la encuesta con valores aleatorios
                    survey_data = SurveyBase(
                        user_id=user.user_id,
                        mood=random.randint(1, 5),
                        anxiety=random.randint(1, 5),
                        stress=random.randint(1, 5),
                        sleep=random.randint(1, 5),
                        social=random.randint(1, 5),
                        energy=random.randint(1, 5),
                        hopeful=random.randint(1, 5),
                        survey_type=random.choice(list(SurveyType))
                    )
                    
                    try:
                        survey = self.survey_service.create_survey(survey_data)
                        print(f"  ✅ Encuesta {i+1} creada para {user.name}")
                    except Exception as e:
                        print(f"  ❌ Error al crear encuesta para {user.name}: {str(e)}")
            
            print("\n✅ Datos de demostración creados exitosamente!")
            print("🎯 Ahora puedes explorar todas las funcionalidades del sistema")
            
        except Exception as e:
            print(f"❌ Error en modo demostración: {str(e)}")
            raise e