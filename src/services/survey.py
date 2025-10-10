"""
Servicio para gestión de encuestas.
Maneja operaciones CRUD y análisis de encuestas emocionales.
Permite almacenamiento dual: Base de datos SQL y respaldo en CSV local.
"""

import pandas as pd
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import os
from sqlmodel import Session, select
from db import engine
from ..models.survey import Survey, SurveyBase, SurveyType


class SurveyService:
    """
    Servicio para gestionar encuestas.
    
    Maneja la creación, almacenamiento, búsqueda y análisis de encuestas
    de seguimiento emocional de los usuarios. Mantiene sincronización entre
    base de datos SQL y archivos CSV locales.
    """
    
    def __init__(self, data_path: str = "data/processed"):
        """
        Inicializa el servicio de encuestas.
        
        Args:
            data_path (str): Ruta donde se almacenan los archivos de respaldo CSV
        """
        self.data_path = data_path
        self.surveys_file = os.path.join(data_path, "surveys.csv")
        self._ensure_data_directory()
        
    def _ensure_data_directory(self) -> None:
        """Crea el directorio de datos si no existe."""
        os.makedirs(self.data_path, exist_ok=True)
        
    def _sync_to_csv(self) -> None:
        """Sincroniza los datos de la base de datos al archivo CSV."""
        with Session(engine) as session:
            surveys = session.exec(select(Survey)).all()
            if not surveys:
                return
                
            data = []
            for survey in surveys:
                survey_dict = {
                    'survey_id': survey.survey_id,
                    'user_id': survey.user_id,
                    'date': survey.date.isoformat(),
                    'mood': survey.mood,
                    'anxiety': survey.anxiety,
                    'sleep': survey.sleep,
                    'social': survey.social,
                    'energy': survey.energy,
                    'stress': survey.stress,
                    'hopeful': survey.hopeful,
                    'survey_type': survey.survey_type,
                    'wellness_score': survey.wellness_score,
                    'crisis_alert': survey.crisis_alert
                }
                data.append(survey_dict)
                
            df = pd.DataFrame(data)
            df.to_csv(self.surveys_file, index=False)
            
    def create_survey(self, survey_data: SurveyBase) -> Survey:
        """
        Crea una nueva encuesta para un usuario.
        
        Args:
            survey_data (SurveyBase): Datos de la encuesta a crear
            
        Returns:
            Survey: Encuesta creada
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        with Session(engine) as session:
            # Crear nueva encuesta con los datos proporcionados
            survey = Survey(**survey_data.model_dump())
            
            # Calcular campos derivados
            survey._update_calculated_fields()
            
            # Guardar en la base de datos
            session.add(survey)
            session.commit()
            session.refresh(survey)
            
            # Sincronizar con CSV
            self._sync_to_csv()
            
            print(f"✅ Encuesta creada para usuario: {survey.user_id}")
            
            # Verificar si hay alerta de crisis
            if survey.is_crisis_alert():
                print(f"🚨 ALERTA DE CRISIS detectada para usuario {survey.user_id}")
                self._handle_crisis_alert(survey)
            
            return survey
    
    def _save_survey_to_csv(self, survey: Survey) -> None:
        """
        Guarda una encuesta en el archivo CSV.
        
        Args:
            survey (Survey): Encuesta a guardar
        """
        survey_data = survey.to_dict()
        
        # Convertir listas a strings para almacenamiento CSV
        if 'risk_indicators' in survey_data:
            survey_data['risk_indicators'] = str(survey_data['risk_indicators'])
        
        # Expandir responses a columnas individuales
        responses = survey_data.pop('responses', {})
        for key, value in responses.items():
            survey_data[f'response_{key}'] = value
        
        # Crear DataFrame
        df = pd.DataFrame([survey_data])
        
        # Guardar o agregar al archivo existente
        if os.path.exists(self.surveys_file):
            existing_df = pd.read_csv(self.surveys_file)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_csv(self.surveys_file, index=False)
    
    def _handle_crisis_alert(self, survey: Survey) -> None:
        """
        Maneja una alerta de crisis.
        
        Args:
            survey (Survey): Encuesta que generó la alerta
        """
        # En una implementación completa, esto podría:
        # - Enviar notificaciones a profesionales
        # - Crear tickets de seguimiento urgente
        # - Activar protocolos de intervención
        
        alert_data = {
            'alert_id': f"CRISIS_{survey.survey_id}",
            'user_id': survey.user_id,
            'date': survey.date.isoformat(),
            'mood': survey.mood,
            'wellness_score': survey.wellness_score,
            'crisis_alert': survey.crisis_alert,
            'status': 'PENDING'
        }
        
        # Guardar alerta en archivo separado
        alerts_file = os.path.join(self.data_path, "crisis_alerts.csv")
        alert_df = pd.DataFrame([alert_data])
        
        if os.path.exists(alerts_file):
            existing_alerts = pd.read_csv(alerts_file)
            alert_df = pd.concat([existing_alerts, alert_df], ignore_index=True)
        
        alert_df.to_csv(alerts_file, index=False)
    
    def create_interactive_survey(self, user_id: str) -> Survey:
        """
        Crea una encuesta de forma interactiva.
        
        Args:
            user_id (str): ID del usuario
            
        Returns:
            Survey: Encuesta creada
        """
        print("\n=== ENCUESTA DE ESTADO EMOCIONAL ===")
        print("Por favor responde las siguientes preguntas (1-5):")
        
        survey_data = {
            'user_id': user_id,
            'survey_type': SurveyType.DAILY
        }
        
        # Preguntas de la encuesta
        questions = [
            ('mood', '1. ¿Cómo te sientes hoy?'),
            ('anxiety', '2. ¿Qué tan ansioso/a te sientes?'),
            ('sleep', '3. ¿Cómo calificarías tu calidad de sueño?'),
            ('social', '4. ¿Te sentiste conectado/a con otros hoy?'),
            ('energy', '5. ¿Cuál es tu nivel de energía?'),
            ('stress', '6. ¿Qué tan estresado/a te sientes?'),
            ('hopeful', '7. ¿Qué tan esperanzado/a te sientes sobre el futuro?')
        ]
        
        for key, question in questions:
            while True:
                try:
                    value = int(input(f"\n{question} (1-5): "))
                    if 1 <= value <= 5:
                        survey_data[key] = value
                        break
                    else:
                        print("Por favor ingresa un número entre 1 y 5")
                except ValueError:
                    print("Por favor ingresa un número válido")
        
        # Crear la encuesta usando el modelo SurveyBase
        survey_base = SurveyBase(**survey_data)
        return self.create_survey(survey_base)
    
    def get_all_surveys(self) -> List[Survey]:
        """
        Obtiene todas las encuestas registradas.
        
        Returns:
            List[Survey]: Lista de todas las encuestas
        """
        with Session(engine) as session:
            return session.exec(select(Survey)).all()
    
    def _row_to_survey_dict(self, row: pd.Series) -> Dict[str, Any]:
        """
        Convierte una fila del DataFrame a diccionario de encuesta.
        
        Args:
            row (pd.Series): Fila del DataFrame
            
        Returns:
            dict: Datos de la encuesta
        """
        # Extraer responses
        responses = {}
        for col in row.index:
            if col.startswith('response_'):
                key = col.replace('response_', '')
                responses[key] = row[col]
        
        return {
            'survey_id': row['survey_id'],
            'user_id': row['user_id'],
            'date': row['date'],
            'mood_score': int(row['mood_score']),
            'responses': responses,
            'survey_type': row.get('survey_type', 'daily')
        }
    
    def get_surveys_by_user(self, user_id: str, 
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Survey]:
        """
        Obtiene encuestas de un usuario específico.
        
        Args:
            user_id (str): ID del usuario
            start_date (datetime, optional): Fecha de inicio
            end_date (datetime, optional): Fecha de fin
            
        Returns:
            List[Survey]: Lista de encuestas del usuario
        """
        with Session(engine) as session:
            query = select(Survey).where(Survey.user_id == user_id)
            
            if start_date:
                query = query.where(Survey.date >= start_date)
            if end_date:
                query = query.where(Survey.date <= end_date)
                
            query = query.order_by(Survey.date)
            return session.exec(query).all()
    
    def get_recent_surveys(self, days: int = 7) -> List[Survey]:
        """
        Obtiene encuestas de los últimos N días.
        
        Args:
            days (int): Número de días hacia atrás
            
        Returns:
            List[Survey]: Encuestas recientes
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with Session(engine) as session:
            query = select(Survey).where(Survey.date >= cutoff_date)
            return session.exec(query).all()
    
    def get_crisis_alerts(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las alertas de crisis.
        
        Returns:
            List[dict]: Lista de alertas de crisis
        """
        alerts_file = os.path.join(self.data_path, "crisis_alerts.csv")
        
        if not os.path.exists(alerts_file):
            return []
        
        df = pd.read_csv(alerts_file)
        return df.to_dict('records')
    
    def calculate_user_trends(self, user_id: str, 
                            days: int = 30) -> Dict[str, Any]:
        """
        Calcula tendencias emocionales para un usuario.
        
        Args:
            user_id (str): ID del usuario
            days (int): Período de análisis en días
            
        Returns:
            dict: Análisis de tendencias
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        surveys = self.get_surveys_by_user(user_id, start_date, end_date)
        
        if not surveys:
            return {
                'user_id': user_id,
                'period_days': days,
                'total_surveys': 0,
                'trends': {}
            }
        
        # Calcular métricas
        mood_scores = [s.mood_score for s in surveys]
        wellness_scores = [s.calculate_wellness_score() for s in surveys]
        
        # Tendencias
        mood_trend = self._calculate_trend(mood_scores)
        wellness_trend = self._calculate_trend(wellness_scores)
        
        # Análisis de respuestas específicas
        response_trends = {}
        response_keys = ['anxiety', 'sleep', 'social', 'energy', 'stress', 'hopeful']
        
        for key in response_keys:
            values = [s.responses.get(key) for s in surveys if key in s.responses]
            if values:
                response_trends[key] = {
                    'average': sum(values) / len(values),
                    'trend': self._calculate_trend(values),
                    'latest': values[-1] if values else None
                }
        
        return {
            'user_id': user_id,
            'period_days': days,
            'total_surveys': len(surveys),
            'mood_average': sum(mood_scores) / len(mood_scores),
            'wellness_average': sum(wellness_scores) / len(wellness_scores),
            'mood_trend': mood_trend,
            'wellness_trend': wellness_trend,
            'response_trends': response_trends,
            'crisis_count': sum(1 for s in surveys if s.is_crisis_alert()),
            'latest_survey_date': surveys[-1].date.isoformat() if surveys else None
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """
        Calcula la tendencia de una serie de valores.
        
        Args:
            values (List[float]): Lista de valores
            
        Returns:
            str: 'improving', 'declining', o 'stable'
        """
        if len(values) < 2:
            return 'stable'
        
        # Comparar primera mitad vs segunda mitad
        mid = len(values) // 2
        first_half_avg = sum(values[:mid]) / mid if mid > 0 else values[0]
        second_half_avg = sum(values[mid:]) / len(values[mid:])
        
        diff = second_half_avg - first_half_avg
        
        if diff > 0.5:
            return 'improving'
        elif diff < -0.5:
            return 'declining'
        else:
            return 'stable'
    
    def get_survey_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de encuestas.
        
        Returns:
            dict: Estadísticas de encuestas
        """
        surveys = self.get_all_surveys()
        
        if not surveys:
            return {
                'total_surveys': 0,
                'unique_users': 0,
                'avg_mood_score': 0,
                'avg_wellness_score': 0,
                'crisis_alerts': 0
            }
        
        # Métricas básicas
        mood_scores = [s.mood_score for s in surveys]
        wellness_scores = [s.calculate_wellness_score() for s in surveys]
        unique_users = len({s.user_id for s in surveys})
        crisis_count = sum(1 for s in surveys if s.is_crisis_alert())
        
        # Distribución por tipo de encuesta
        survey_types = {}
        for survey in surveys:
            survey_types[survey.survey_type] = survey_types.get(survey.survey_type, 0) + 1
        
        return {
            'total_surveys': len(surveys),
            'unique_users': unique_users,
            'avg_mood_score': sum(mood_scores) / len(mood_scores),
            'avg_wellness_score': sum(wellness_scores) / len(wellness_scores),
            'crisis_alerts': crisis_count,
            'crisis_rate': (crisis_count / len(surveys)) * 100,
            'survey_types': survey_types,
            'surveys_per_user': len(surveys) / unique_users if unique_users > 0 else 0
        }
    
    def export_surveys_data(self, filename: str = None) -> str:
        """
        Exporta los datos de encuestas a un archivo CSV.
        
        Args:
            filename (str, optional): Nombre del archivo de exportación
            
        Returns:
            str: Ruta del archivo exportado
        """
        if filename is None:
            filename = f"surveys_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        export_path = os.path.join("data/exports", filename)
        os.makedirs("data/exports", exist_ok=True)
        
        if os.path.exists(self.surveys_file):
            df = pd.read_csv(self.surveys_file)
            df.to_csv(export_path, index=False)
            print(f"✅ Datos de encuestas exportados a: {export_path}")
        else:
            print("❌ No hay datos de encuestas para exportar")
        
        return export_path