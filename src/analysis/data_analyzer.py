"""
Módulo de análisis exploratorio de datos (EDA).
Proporciona funciones para analizar patrones en los datos emocionales.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple
import os
from datetime import datetime, timedelta

from ..services.user import UserService
from ..services.survey import SurveyService


class EmotionalDataAnalyzer:
    """
    Analizador de datos emocionales.
    
    Proporciona métodos para análisis exploratorio, detección de patrones
    y generación de insights sobre el estado emocional de los usuarios.
    """
    
    def __init__(self, data_path: str = "data/processed", 
                output_path: str = "data/exports"):
        """
        Inicializa el analizador de datos.
        
        Args:
            data_path (str): Ruta de los datos procesados
            output_path (str): Ruta para guardar resultados
        """
        self.data_path = data_path
        self.output_path = output_path
        self.user_service = UserService(data_path)
        self.survey_service = SurveyService(data_path)
        
        # Configurar estilo de gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Crear directorios si no existen
        os.makedirs(output_path, exist_ok=True)
    
    def _ensure_csv_files(self) -> bool:
        """
        Asegura que los archivos CSV existan y estén actualizados.
        Genera los archivos si no existen o actualiza si hay cambios en la base de datos.
        
        Returns:
            bool: True si los archivos están listos para usar, False si hubo errores
        """
        try:
            # Crear directorio si no existe
            os.makedirs(self.data_path, exist_ok=True)
            
            users_file = os.path.join(self.data_path, "users.csv")
            surveys_file = os.path.join(self.data_path, "surveys.csv")
            
            # Obtener usuarios y encuestas de los servicios
            users = self.user_service.get_all_users()
            surveys = self.survey_service.get_all_surveys()
            
            # Convertir a DataFrames
            users_data = []
            for user in users:
                users_data.append({
                    'user_id': user.user_id,
                    'name': user.name,
                    'age': user.age,
                    'context': user.context,
                    'gender': user.gender
                })
            
            surveys_data = []
            for survey in surveys:
                surveys_data.append({
                    'survey_id': survey.survey_id,
                    'user_id': survey.user_id,
                    'date': survey.date,
                    'mood': survey.mood,
                    'wellness_score': survey.wellness_score,
                    'crisis_alert': survey.crisis_alert,
                    'anxiety': survey.anxiety,
                    'sleep': survey.sleep,
                    'social': survey.social,
                    'energy': survey.energy,
                    'stress': survey.stress,
                    'hopeful': survey.hopeful,
                    'survey_type': survey.survey_type
                })
            
            # Guardar a CSV
            if users_data:
                pd.DataFrame(users_data).to_csv(users_file, index=False)
                print(f"✅ Archivo de usuarios actualizado: {len(users_data)} registros")
            
            if surveys_data:
                pd.DataFrame(surveys_data).to_csv(surveys_file, index=False)
                print(f"✅ Archivo de encuestas actualizado: {len(surveys_data)} registros")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al generar/actualizar archivos CSV: {str(e)}")
            return False
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Carga los datos de usuarios y encuestas.
        Si los archivos CSV no existen o están desactualizados, los genera.
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: DataFrames de usuarios y encuestas
        """
        # Asegurar que los archivos existan y estén actualizados
        self._ensure_csv_files()
        
        users_file = os.path.join(self.data_path, "users.csv")
        surveys_file = os.path.join(self.data_path, "surveys.csv")
        
        users_df = pd.DataFrame()
        surveys_df = pd.DataFrame()
        
        if os.path.exists(users_file):
            users_df = pd.read_csv(users_file)
            print(f"✅ Cargados {len(users_df)} usuarios")
        else:
            print("⚠️ No se encontró el archivo de usuarios")
        
        if os.path.exists(surveys_file):
            surveys_df = pd.read_csv(surveys_file)
            surveys_df['date'] = pd.to_datetime(surveys_df['date'])
            print(f"✅ Cargadas {len(surveys_df)} encuestas")
        else:
            print("⚠️ No se encontró el archivo de encuestas")
        
        return users_df, surveys_df
    
    def generate_descriptive_statistics(self) -> Dict[str, Any]:
        """
        Genera estadísticas descriptivas de los datos.
        
        Returns:
            dict: Estadísticas descriptivas
        """
        users_df, surveys_df = self.load_data()
        
        stats = {
            'fecha_analisis': datetime.now().isoformat(),
            'usuarios': {},
            'encuestas': {},
            'general': {}
        }
        
        # Estadísticas de usuarios
        if not users_df.empty:
            stats['usuarios'] = {
                'total': len(users_df),
                'edad_promedio': users_df['age'].mean() if 'age' in users_df.columns else 0,
                'edad_mediana': users_df['age'].median() if 'age' in users_df.columns else 0,
                'edad_min': users_df['age'].min() if 'age' in users_df.columns else 0,
                'edad_max': users_df['age'].max() if 'age' in users_df.columns else 0
            }
            
            # Distribución por contexto y género
            if 'context' in users_df.columns:
                context_counts = users_df['context'].value_counts().to_dict()
                stats['usuarios']['contextos'] = context_counts
            
            if 'gender' in users_df.columns:
                gender_counts = users_df['gender'].value_counts().to_dict()
                stats['usuarios']['generos'] = gender_counts
        
        # Estadísticas de encuestas
        if not surveys_df.empty:
            stats['encuestas'] = {
                'total': len(surveys_df),
                'usuarios_unicos': surveys_df['user_id'].nunique() if 'user_id' in surveys_df.columns else 0,
                'mood_promedio': surveys_df['mood'].mean() if 'mood' in surveys_df.columns else 0,
                'wellness_promedio': surveys_df['wellness_score'].mean() if 'wellness_score' in surveys_df.columns else 0,
                'crisis_total': surveys_df['crisis_alert'].sum() if 'crisis_alert' in surveys_df.columns else 0,
                'encuestas_por_usuario': len(surveys_df) / surveys_df['user_id'].nunique() if 'user_id' in surveys_df.columns and surveys_df['user_id'].nunique() > 0 else 0
            }
            
            # Distribución por tipo de encuesta
            if 'survey_type' in surveys_df.columns:
                type_counts = surveys_df['survey_type'].value_counts().to_dict()
                stats['encuestas']['tipos'] = type_counts
        
        # Estadísticas generales
        if not users_df.empty and not surveys_df.empty:
            stats['general'] = {
                'tasa_participacion': (surveys_df['user_id'].nunique() / len(users_df)) * 100 if len(users_df) > 0 else 0,
                'tasa_crisis': (surveys_df['crisis_alert'].sum() / len(surveys_df)) * 100 if len(surveys_df) > 0 else 0,
                'periodo_datos': {
                    'inicio': surveys_df['date'].min().isoformat() if 'date' in surveys_df.columns else None,
                    'fin': surveys_df['date'].max().isoformat() if 'date' in surveys_df.columns else None
                }
            }
        
        return stats
    
    def analyze_mood_trends(self, days: int = 30) -> pd.DataFrame:
        """
        Analiza tendencias del estado de ánimo.
        
        Args:
            days (int): Número de días a analizar
            
        Returns:
            pd.DataFrame: Análisis de tendencias
        """
        _, surveys_df = self.load_data()
        
        if surveys_df.empty:
            return pd.DataFrame()
        
        # Filtrar últimos N días
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        recent_surveys = surveys_df[
            (surveys_df['date'] >= start_date) & 
            (surveys_df['date'] <= end_date)
        ].copy()
        
        if recent_surveys.empty:
            return pd.DataFrame()
        
        # Agregar por día
        daily_trends = recent_surveys.groupby(recent_surveys['date'].dt.date).agg({
            'mood': ['mean', 'std', 'count'],
            'wellness_score': ['mean', 'std'],
            'crisis_alert': 'sum'
        }).round(2)
        
        # Aplanar columnas multinivel
        daily_trends.columns = ['_'.join(col).strip() for col in daily_trends.columns.values]
        daily_trends = daily_trends.reset_index()
        
        return daily_trends
    
    def analyze_user_risk_patterns(self) -> pd.DataFrame:
        """
        Analiza patrones de riesgo por usuario.
        
        Returns:
            pd.DataFrame: Análisis de riesgo por usuario
        """
        users_df, surveys_df = self.load_data()
        
        if users_df.empty or surveys_df.empty:
            return pd.DataFrame()
        
        # Combinar datos de usuarios y encuestas
        user_analysis = []
        
        for _, user in users_df.iterrows():
            user_id = user['user_id']
            user_surveys = surveys_df[surveys_df['user_id'] == user_id]
            
            if not user_surveys.empty:
                # Calcular indicadores de bienestar
                wellness_indicators = {
                    'anxiety': user_surveys['anxiety'].mean() if 'anxiety' in user_surveys else None,
                    'sleep': user_surveys['sleep'].mean() if 'sleep' in user_surveys else None,
                    'social': user_surveys['social'].mean() if 'social' in user_surveys else None,
                    'energy': user_surveys['energy'].mean() if 'energy' in user_surveys else None,
                    'stress': user_surveys['stress'].mean() if 'stress' in user_surveys else None,
                    'hopeful': user_surveys['hopeful'].mean() if 'hopeful' in user_surveys else None
                }
                
                analysis = {
                    'user_id': user_id,
                    'name': user.get('name', 'N/A'),
                    'age': user.get('age', 0),
                    'context': user.get('context', 'N/A'),
                    'total_surveys': len(user_surveys),
                    'avg_mood': user_surveys['mood'].mean() if 'mood' in user_surveys else 0,
                    'avg_wellness': user_surveys['wellness_score'].mean() if 'wellness_score' in user_surveys else 0,
                    'avg_anxiety': wellness_indicators['anxiety'],
                    'avg_sleep': wellness_indicators['sleep'],
                    'avg_social': wellness_indicators['social'],
                    'avg_energy': wellness_indicators['energy'],
                    'avg_stress': wellness_indicators['stress'],
                    'avg_hopeful': wellness_indicators['hopeful'],
                    'crisis_count': user_surveys['crisis_alert'].sum(),
                    'crisis_rate': (user_surveys['crisis_alert'].sum() / len(user_surveys)) * 100 if len(user_surveys) > 0 else 0,
                    'mood_trend': self._calculate_trend(user_surveys['mood'].tolist() if 'mood' in user_surveys else []),
                    'last_survey': user_surveys['date'].max(),
                    'days_since_last': (datetime.now() - user_surveys['date'].max()).days
                }
                user_analysis.append(analysis)
        
        return pd.DataFrame(user_analysis)
    
    def _calculate_trend(self, values: List[float]) -> str:
        """
        Calcula la tendencia de una serie de valores.
        
        Args:
            values (List[float]): Lista de valores
            
        Returns:
            str: 'mejorando', 'empeorando', o 'estable'
        """
        if len(values) < 2:
            return 'estable'
        
        # Usar correlación con índices para determinar tendencia
        indices = list(range(len(values)))
        correlation = np.corrcoef(indices, values)[0, 1]
        
        if correlation > 0.3:
            return 'mejorando'
        elif correlation < -0.3:
            return 'empeorando'
        else:
            return 'estable'
    
    def analyze_gender_patterns(self) -> Dict[str, Any]:
        """
        Analiza patrones específicos por género.
        
        Returns:
            dict: Análisis de patrones por género
        """
        users_df, surveys_df = self.load_data()
        
        if users_df.empty or 'gender' not in users_df.columns:
            return {}
            
        gender_analysis = {
            'distribution': users_df['gender'].value_counts().to_dict(),
            'age_by_gender': {},
            'wellness_by_gender': {},
            'crisis_by_gender': {}
        }
        
        # Análisis de edad por género
        age_stats = users_df.groupby('gender')['age'].agg(['mean', 'median', 'min', 'max']).round(1)
        gender_analysis['age_by_gender'] = age_stats.to_dict('index')
        
        # Análisis de bienestar por género
        if not surveys_df.empty:
            surveys_with_gender = surveys_df.merge(
                users_df[['user_id', 'gender']], 
                on='user_id', 
                how='left'
            )
            
            wellness_stats = surveys_with_gender.groupby('gender').agg({
                'wellness_score': 'mean',
                'mood': 'mean',
                'crisis_alert': ['sum', 'mean']
            }).round(2)
            
            gender_analysis['wellness_by_gender'] = wellness_stats.to_dict('index')
            
            # Calcular tasas de crisis por género
            total_users_by_gender = users_df['gender'].value_counts()
            users_with_crisis = surveys_with_gender[surveys_with_gender['crisis_alert'] > 0]['user_id'].nunique()
            gender_analysis['crisis_by_gender'] = {
                'total_users': total_users_by_gender.to_dict(),
                'users_with_crisis': users_with_crisis
            }
        
        return gender_analysis
    
    def analyze_correlations(self) -> pd.DataFrame:
        """
        Analiza correlaciones entre variables emocionales.
        
        Returns:
            pd.DataFrame: Matriz de correlaciones
        """
        _, surveys_df = self.load_data()
        
        if surveys_df.empty:
            return pd.DataFrame()
        
        # Seleccionar columnas numéricas para correlación
        emotional_columns = [
            'mood', 'wellness_score', 'anxiety', 'sleep', 
            'social', 'energy', 'stress', 'hopeful'
        ]
        available_columns = [col for col in emotional_columns if col in surveys_df.columns]
        
        if len(available_columns) < 2:
            return pd.DataFrame()
        
        correlation_matrix = surveys_df[available_columns].corr().round(3)
        
        return correlation_matrix
    
    def detect_risk_patterns(self, risk_threshold: float = 6.0) -> Dict[str, Any]:
        """
        Detecta patrones en usuarios de alto riesgo.
        
        Args:
            risk_threshold (float): Umbral de riesgo (basado en wellness_score)
            
        Returns:
            dict: Análisis de patrones de riesgo
        """
        user_analysis = self.analyze_user_risk_patterns()
        
        if user_analysis.empty:
            return {}
        
        # Identificar usuarios de alto riesgo basado en wellness_score y crisis_rate
        high_risk_users = user_analysis[
            (user_analysis['avg_wellness'] <= risk_threshold) |
            (user_analysis['crisis_rate'] >= 30) |  # Más del 30% de encuestas en crisis
            (user_analysis['avg_hopeful'] <= 2)     # Baja esperanza como indicador de riesgo
        ]
        
        patterns = {
            'total_users': len(user_analysis),
            'high_risk_count': len(high_risk_users),
            'high_risk_percentage': (len(high_risk_users) / len(user_analysis)) * 100,
            'risk_patterns': {}
        }
        
        if not high_risk_users.empty:
            patterns['risk_patterns'] = {
                'avg_age_high_risk': high_risk_users['age'].mean(),
                'avg_mood_high_risk': high_risk_users['avg_mood'].mean(),
                'avg_crisis_rate': high_risk_users['crisis_rate'].mean(),
                'common_contexts': high_risk_users['context'].value_counts().to_dict(),
                'gender_distribution': high_risk_users['gender'].value_counts().to_dict() if 'gender' in high_risk_users.columns else {},
                'trend_distribution': high_risk_users['mood_trend'].value_counts().to_dict()
            }        
            return patterns
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Genera un reporte completo de análisis.
        
        Returns:
            dict: Reporte completo de análisis
        """
        print("📊 Generando reporte completo de análisis...")
        
        report = {
            'estadisticas_descriptivas': self.generate_descriptive_statistics(),
            'analisis_correlaciones': self.analyze_correlations().to_dict() if not self.analyze_correlations().empty else {},
            'patrones_riesgo': self.detect_risk_patterns(),
            'tendencias_recientes': self.analyze_mood_trends().to_dict('records') if not self.analyze_mood_trends().empty else [],
            'analisis_usuarios': self.analyze_user_risk_patterns().to_dict('records') if not self.analyze_user_risk_patterns().empty else []
        }
        
        # Guardar reporte
        report_file = os.path.join(
            self.output_path, 
            f"reporte_analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        import json
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Reporte guardado en: {report_file}")
        
        return report
    
    def force_update_csv_files(self) -> bool:
        """
        Fuerza la actualización de los archivos CSV desde la base de datos.
        Útil cuando se sabe que ha habido cambios en la base de datos.
        
        Returns:
            bool: True si la actualización fue exitosa, False si hubo errores
        """
        print("🔄 Forzando actualización de archivos CSV...")
        return self._ensure_csv_files()
    
    def export_analysis_summary(self) -> str:
        """
        Exporta un resumen del análisis a CSV.
        
        Returns:
            str: Ruta del archivo exportado
        """
        user_analysis = self.analyze_user_risk_patterns()
        
        if user_analysis.empty:
            print("❌ No hay datos suficientes para generar resumen")
            return ""
        
        # Crear resumen agregado
        summary = {
            'total_usuarios': len(user_analysis),
            'usuarios_alto_riesgo': len(user_analysis[
                (user_analysis['avg_wellness'] <= 6.0) |
                (user_analysis['crisis_rate'] >= 30) |
                (user_analysis['avg_hopeful'] <= 2)
            ]),
            'promedio_mood': user_analysis['avg_mood'].mean(),
            'promedio_wellness': user_analysis['avg_wellness'].mean(),
            'promedio_ansiedad': user_analysis['avg_anxiety'].mean(),
            'promedio_sueno': user_analysis['avg_sleep'].mean(),
            'promedio_social': user_analysis['avg_social'].mean(),
            'promedio_energia': user_analysis['avg_energy'].mean(),
            'promedio_estres': user_analysis['avg_stress'].mean(),
            'promedio_esperanza': user_analysis['avg_hopeful'].mean(),
            'total_crisis': user_analysis['crisis_count'].sum(),
            'usuarios_trend_mejorando': len(user_analysis[user_analysis['mood_trend'] == 'mejorando']),
            'usuarios_trend_empeorando': len(user_analysis[user_analysis['mood_trend'] == 'empeorando']),
            'usuarios_trend_estable': len(user_analysis[user_analysis['mood_trend'] == 'estable']),
        }
        
        summary_df = pd.DataFrame([summary])
        
        export_file = os.path.join(
            self.output_path,
            f"resumen_analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        summary_df.to_csv(export_file, index=False)
        user_analysis.to_csv(
            export_file.replace('resumen_', 'detalle_usuarios_'),
            index=False
        )
        
        print(f"✅ Resumen exportado a: {export_file}")
        return export_file
    
    def convert_numpy(self, obj):
        if isinstance(obj, np.generic):
            return obj.item()  # Convierte np.float64 -> float, np.int64 -> int, etc.
        raise TypeError(f"Tipo no serializable: {type(obj)}")