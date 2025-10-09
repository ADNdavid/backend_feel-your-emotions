from fastapi import APIRouter, HTTPException, status
from ..models.survey import Survey, SurveyBase, get_all_questions
from ..models.user import User
from db import session_dependency
from sqlmodel import select
from typing import List, Dict

router = APIRouter(tags=["Surveys"], prefix="/api")

@router.get("/survey/questions", response_model=Dict[str, str], status_code=status.HTTP_200_OK)
async def get_survey_questions():
    """
    Endpoint para obtener todas las preguntas disponibles para las encuestas.
    
    Returns:
        Dict[str, str]: Diccionario con las preguntas de la encuesta
    """
    return get_all_questions()

@router.post("/survey", status_code=status.HTTP_201_CREATED, response_model=Survey)
async def create_survey(survey_data: SurveyBase, session: session_dependency):
    """
    Endpoint para crear una nueva encuesta.
    
    Args:
        survey_data (SurveyBase): Datos de la encuesta a crear
        
    Returns:
        Survey: Datos de la encuesta creada
    """
    # Crear una nueva instancia de Survey con los datos
    survey = Survey(**survey_data.model_dump())
    # Verificar que el usuario exista
    user_id = survey_data.user_id
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    # Asegurar que se calculen los campos
    survey._update_calculated_fields()
    session.add(survey)
    session.commit()
    session.refresh(survey)
    return survey

@router.get("/survey/{survey_id}", response_model=Survey)
async def get_survey(survey_id: str, session: session_dependency):
    """
    Endpoint para obtener una encuesta por su ID.
    
    Args:
        survey_id (str): ID de la encuesta a obtener
        
    Returns:
        Survey: Datos de la encuesta
    """
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada")
    return survey

@router.get("/surveys", response_model=List[Survey])
async def list_surveys(session: session_dependency):
    """
    Endpoint para listar todas las encuestas.
    
    Returns:
        List[Survey]: Lista de encuestas
    """
    surveys = session.exec(select(Survey)).all()
    return surveys

@router.get("/surveys/user/{user_id}", response_model=List[Survey])
async def get_user_surveys(user_id: str, session: session_dependency):
    """
    Endpoint para obtener todas las encuestas de un usuario específico.
    
    Args:
        user_id (str): ID del usuario
        
    Returns:
        List[Survey]: Lista de encuestas del usuario
    """
    surveys = session.exec(select(Survey).where(Survey.user_id == user_id)).all()
    return surveys

@router.delete("/survey/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_survey(survey_id: str, session: session_dependency):
    """
    Endpoint para eliminar una encuesta por su ID.
    
    Args:
        survey_id (str): ID de la encuesta a eliminar
    """
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada")
    session.delete(survey)
    session.commit()
    return {"detail": "Encuesta eliminada exitosamente"}

@router.put("/survey/{survey_id}", response_model=Survey)
async def update_survey(survey_id: str, survey_data: SurveyBase, session: session_dependency):
    """
    Endpoint para actualizar una encuesta por su ID.
    
    Args:
        survey_id (str): ID de la encuesta a actualizar
        survey_data (SurveyBase): Nuevos datos de la encuesta
        
    Returns:
        Survey: Datos de la encuesta actualizada
    """
    survey = session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada")
    
    survey_data_dict = survey_data.model_dump(exclude_unset=True)
    for key, value in survey_data_dict.items():
        setattr(survey, key, value)
    
    # Recalcular los campos después de actualizar los valores
    survey._update_calculated_fields()
    session.add(survey)
    session.commit()
    session.refresh(survey)
    return survey


@router.get("/surveys/crisis", response_model=List[Survey])
async def get_crisis_surveys(session: session_dependency):
    """
    Endpoint para obtener todas las encuestas que indican una situación de crisis.
    
    Returns:
        List[Survey]: Lista de encuestas en estado de crisis
    """
    all_surveys = session.exec(select(Survey)).all()
    crisis_surveys = [survey for survey in all_surveys if survey.is_crisis_alert()]
    return crisis_surveys

#@router.get("/survey/{survey_id}/risk-indicators", response_model=List[str])
#async def get_survey_risk_indicators(survey_id: str, session: session_dependency):
#    """
#    Endpoint para obtener los indicadores de riesgo de una encuesta específica.
#    
#    Args:
#        survey_id (str): ID de la encuesta
#        
#    Returns:
#        List[str]: Lista de indicadores de riesgo detectados
#    """
#    survey = session.get(Survey, survey_id)
#    if not survey:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encuesta no encontrada")
#    return survey.get_risk_indicators()