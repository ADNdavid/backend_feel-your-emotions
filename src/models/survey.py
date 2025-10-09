"""
Modelo de Encuesta para el sistema EmoTracker.
Representa las encuestas de seguimiento emocional de los usuarios.
"""

from enum import Enum
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlmodel import SQLModel, Field
import uuid

# Preguntas estándar de la encuesta
STANDARD_QUESTIONS = {
    'mood': "¿Cómo te sientes hoy en una escala del 1 al 5?",
    'anxiety': "¿Qué tan ansioso/a te sientes? (1-5)",
    'sleep': "¿Cómo calificarías tu calidad de sueño? (1-5)",
    'social': "¿Te sentiste conectado/a con otros hoy? (1-5)",
    'energy': "¿Cuál es tu nivel de energía? (1-5)",
    'stress': "¿Qué tan estresado/a te sientes? (1-5)",
    'hopeful': "¿Qué tan esperanzado/a te sientes sobre el futuro? (1-5)"
}

def get_all_questions() -> Dict[str, str]:
    """Devuelve todas las preguntas estándar de la encuesta."""
    return STANDARD_QUESTIONS

class SurveyType(str, Enum):
    DAILY = "diaria"
    WEEKLY = "semanal"
    SPECIAL = "especial"
    QUICK = "rapida"

class SurveyBase(SQLModel):
    mood: int | None= Field(default=None, ge=1, le=5, description="Puntuación del estado de ánimo (1-5)")
    anxiety: int | None = Field(default=None, ge=1, le=5, description="Nivel de ansiedad (1-5)")
    sleep: int | None = Field(default=None, ge=1, le=5, description="Calidad de sueño (1-5)")
    social: int | None = Field(default=None, ge=1, le=5, description="Conexión social (1-5)")
    energy: int | None = Field(default=None, ge=1, le=5, description="Nivel de energía (1-5)")
    stress: int | None = Field(default=None, ge=1, le=5, description="Nivel de estrés (1-5)")
    hopeful: int | None = Field(default=None, ge=1, le=5, description="Nivel de esperanza (1-5)")
    survey_type: SurveyType = Field(default=SurveyType.DAILY, description="Tipo de encuesta (diaria, semanal, especial)")
    user_id: str = Field(description="ID del usuario que responde la encuesta")
    
class Survey(SurveyBase, table=True):
    survey_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.user_id", description="ID del usuario que responde la encuesta")
    date: datetime = Field(default_factory=datetime.now, description="Fecha y hora de la encuesta")
    wellness_score: float = Field(default=0.0, description="Puntaje de bienestar calculado")
    crisis_alert: bool = Field(default=False, description="Indica si la encuesta señala una situación de crisis")

    def __init__(self, **data):
        super().__init__(**data)
        #self._update_calculated_fields()
        
    def _update_calculated_fields(self):
        """Actualiza los campos calculados de la encuesta."""
        self.wellness_score = self._calculate_wellness_score()
        self.crisis_alert = self._check_crisis_alert()

    def _calculate_wellness_score(self) -> float:
        """Calcula el puntaje de bienestar basado en todas las respuestas."""
        if not any([self.mood, self.anxiety, self.sleep, self.social, self.energy, self.stress, self.hopeful]):
            return 0.0
            
        positive_factors = ['sleep', 'social', 'energy', 'hopeful']
        negative_factors = ['anxiety', 'stress']
        
        # Obtener valores de factores positivos
        positive_values = [getattr(self, factor) or 3 for factor in positive_factors]
        positive_avg = sum(positive_values) / len(positive_factors)
        
        # Obtener valores de factores negativos
        negative_values = [getattr(self, factor) or 3 for factor in negative_factors]
        negative_avg = sum(negative_values) / len(negative_factors)
        
        # Calcular puntaje final
        wellness = (
            (self.mood or 3) * 0.4 +  # Peso del estado de ánimo
            (positive_avg * 0.3) +  # Peso de factores positivos
            ((6 - negative_avg) * 0.3)  # Peso de factores negativos (invertidos)
        )
        return float(max(1, min(5, wellness)))

    def _check_crisis_alert(self) -> bool:
        """Determina si la encuesta indica una situación de crisis."""
        risk_count = 0
        
        # Verificar estado de ánimo muy bajo
        if self.mood and self.mood <= 2:
            risk_count += 1
            
        # Verificar niveles altos de ansiedad y estrés
        if self.anxiety and self.anxiety >= 4:
            risk_count += 1
        if self.stress and self.stress >= 4:
            risk_count += 1
            
        # Verificar niveles bajos de factores positivos
        for factor in ['sleep', 'social', 'energy', 'hopeful']:
            value = getattr(self, factor)
            if value and value <= 2:
                risk_count += 1
                
        # Condiciones especiales de crisis
        crisis_conditions = [
            self.mood and self.mood <= 2,  # Estado de ánimo muy bajo
            self.hopeful and self.hopeful <= 1,  # Pérdida severa de esperanza
            risk_count >= 4  # Múltiples indicadores de riesgo
        ]
        
        return any(crisis_conditions)
    
    def is_crisis_alert(self) -> bool:
        """Devuelve si la encuesta indica una situación de crisis."""
        return self.crisis_alert
