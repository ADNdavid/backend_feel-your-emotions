"""
Utilidad para generar datos de demostración en el sistema.
"""

from typing import List
import random
from datetime import datetime, timedelta
from faker import Faker
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

    def generate_demo_data(self) -> int:
        """Ejecuta una demostración del sistema con datos de prueba."""
        print("\n🎬 MODO DEMOSTRACIÓN")
        print("="*50)
        print("Creando datos de prueba para demostrar el sistema...")
        
        try:
            vulnerability_context = [
                "Violencia familiar y abuso doméstico",
                "Abuso de sustancias (drogas, alcohol, etc.)",
                "Condiciones de pobreza y marginación",
                "Baja autoestima y problemas de salud mental (ansiedad, depresión)",
                "Falta de acceso a educación de calidad",
                "Exclusión social y discriminación (por género, orientación sexual, raza, etc.)",
                "Maternidad/paternidad temprana y embarazos adolescentes no deseados",
                "Violencia escolar (bullying, acoso escolar)",
                "Problemas de adaptación social (dificultad para hacer amigos, aislamiento)",
                "Falta de apoyo emocional o parental",
                "Expresión de identidad de género y orientación sexual no aceptada por la familia o comunidad",
                "Desigualdad de oportunidades laborales y educativas",
                "Acceso limitado a servicios de salud (física y mental)",
                "Exposición a contenidos dañinos (pornografía, violencia, etc.) en internet",
                "Migración forzada y desplazamiento forzoso",
                "Criminalidad juvenil y pertenencia a pandillas",
                "Abusos sexuales y explotación",
                "Riesgo de involucrarse en conductas delictivas o peligrosas",
                "Desempleo juvenil y falta de perspectivas laborales",
                "Dificultades para acceder a tecnología y recursos digitales (brecha digital)"
            ]
            # Crear usuarios de prueba
            demo_users = []
            for _ in range(random.randint(5, 20)):
                fake = Faker(locale='es_CO')
                demo_users.append((fake.name(), random.randint(13, 25), random.choice(vulnerability_context), fake.passport_gender()))
                            
            print("\n👥 Registrando usuarios de prueba...")
            created_users = []
            for name, age, context, gender in demo_users:
                try:
                    user_data = {
                        "name": name,
                        "age": age,
                        "context": context,
                        "gender": gender
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
            return len(created_users)
        except Exception as e:
            print(f"❌ Error en modo demostración: {str(e)}")
            raise e