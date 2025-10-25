from fastapi import APIRouter, Response, Query, HTTPException, status
from fastapi.responses import FileResponse
from ..analysis.visualizations import VisualizationGenerator
from ..analysis.data_analyzer import EmotionalDataAnalyzer
from typing import Dict, Any
import json

# Constantes reutilizables
_MSG_NO_DATA = "No hay datos suficientes para generar la visualización"
_MSG_INVALID_TYPE = "Tipo de visualización no válido"
_MEDIA_TEXT = "text/plain"
_MEDIA_SVG = "image/svg+xml"
_DEFAULT_DAYS = 30

router = APIRouter(tags=["Visualizations"], prefix="/api")

from enum import Enum
from typing import Optional

class VisualizationType(str, Enum):
    """Tipos de visualizaciones disponibles"""
    MOOD_DISTRIBUTION = "mood-distribution"
    TREND_ANALYSIS = "trend-analysis"
    CORRELATION_HEATMAP = "correlation-heatmap"
    RISK_ANALYSIS = "risk-analysis"
    CONTEXT_ANALYSIS = "context-analysis"
    GENDER_ANALYSIS = "gender-analysis"

@router.get("/visualization/{viz_type}", response_class=Response)
async def get_visualization(
    viz_type: VisualizationType,
    days: Optional[int] = Query(30, ge=1, le=365, description="Número de días para análisis de tendencias")
):
    """
    Endpoint para obtener visualizaciones SVG según el tipo especificado.
    
    Args:
        viz_type (VisualizationType): Tipo de visualización a generar
        days (int, opcional): Número de días para el análisis de tendencias (1-365)
    
    Returns:
        Response: Imagen SVG con la visualización
    """
    # Crear el generador con formato SVG
    analyzer = EmotionalDataAnalyzer()
    viz_generator = VisualizationGenerator(analyzer=analyzer, output_format="svg")
    
    # Mapeo de tipos de visualización a métodos del generador
    visualization_methods = {
        VisualizationType.MOOD_DISTRIBUTION: 
            (viz_generator.create_mood_distribution_plot, "mood_distribution"),
        VisualizationType.TREND_ANALYSIS: 
            (lambda: viz_generator.create_trend_analysis_plot(days=days), f"trend_analysis_{days}days"),
        VisualizationType.CORRELATION_HEATMAP: 
            (viz_generator.create_correlation_heatmap, "correlation_heatmap"),
        VisualizationType.RISK_ANALYSIS: 
            (viz_generator.create_risk_analysis_plot, "risk_analysis"),
        VisualizationType.CONTEXT_ANALYSIS: 
            (viz_generator.create_user_context_analysis, "context_analysis"),
        VisualizationType.GENDER_ANALYSIS:
            (viz_generator.create_gender_analysis_plot, "gender_analysis")
    }
    
    # Obtener el método y nombre de archivo correspondiente
    method, filename = visualization_methods[viz_type]
    
    # Generar la visualización
    svg_path = method()
    
    if not svg_path:
        return Response(content=_MSG_NO_DATA, media_type=_MEDIA_TEXT, status_code=404)
    
    # Retornar el archivo SVG
    return FileResponse(
        svg_path,
        media_type=_MEDIA_SVG,
        headers={"Content-Disposition": f"inline; filename={filename}.svg"}
    )

@router.get("/statistics")
async def get_descriptive_statistics():
    """
    Endpoint para obtener estadísticas descriptivas de los datos emocionales.
    
    Returns:
        Response: Estadísticas descriptivas en formato JSON
    """
    analyzer = EmotionalDataAnalyzer()
    stats_text = analyzer.generate_descriptive_statistics()
    stats_json_text = json.dumps(stats_text, default=analyzer.convert_numpy)
    return json.loads(stats_json_text)