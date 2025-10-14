"""
Generador de visualizaciones.
Crea gráficos y dashboards para análisis de datos emocionales.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
import os
from datetime import datetime

#from .data_analyzer import EmotionalDataAnalyzer

# Agregar el directorio raíz al path para permitir importaciones absolutas
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)
from src.analysis.data_analyzer import EmotionalDataAnalyzer

class VisualizationGenerator:
    """
    Generador de visualizaciones para análisis emocional.
    
    Crea gráficos, dashboards y reportes visuales para el
    análisis de datos del sistema EmoTracker.
    """
    
    # Constantes para etiquetas
    LABEL_BIENESTAR = 'Puntuación de Bienestar'
    UMBRAL_RIESGO = 3.0  # Umbral de riesgo para el bienestar
    
    def __init__(self, analyzer: Optional[EmotionalDataAnalyzer] = None,
                output_path: str = "data/exports"):
        """
        Inicializa el generador de visualizaciones.
        
        Args:
            analyzer (EmotionalDataAnalyzer, optional): Analizador de datos
            output_path (str): Ruta para guardar las visualizaciones
        """
        self.analyzer = analyzer or EmotionalDataAnalyzer()
        self.output_path = output_path
        
        # Configurar estilo de matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        
        # Crear directorio de salida
        os.makedirs(output_path, exist_ok=True)
    
    def create_mood_distribution_plot(self) -> str:
        """
        Crea un gráfico de distribución de estados de ánimo.
        
        Returns:
            str: Ruta del archivo generado
        """
        users_df, surveys_df = self.analyzer.load_data()
        
        if surveys_df.empty:
            print("❌ No hay datos de encuestas para visualizar")
            return ""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Distribución de mood
        if 'mood' in surveys_df.columns:
            surveys_df['mood'].hist(bins=5, ax=ax1, alpha=0.7, color='skyblue')
            ax1.set_title('Distribución de Estados de Ánimo')
            ax1.set_xlabel('Puntuación de Ánimo (1-5)')
            ax1.set_ylabel('Frecuencia')
            ax1.grid(True, alpha=0.3)
            
            # Añadir línea de promedio
            mean_mood = surveys_df['mood'].mean()
            ax1.axvline(mean_mood, color='red', linestyle='--', 
                    label=f'Promedio: {mean_mood:.1f}')
            ax1.legend()
        
        # Distribución de wellness_score
        if 'wellness_score' in surveys_df.columns:
            surveys_df['wellness_score'].hist(bins=10, ax=ax2, alpha=0.7, color='lightgreen')
            ax2.set_title('Distribución de Puntuaciones de Bienestar')
            ax2.set_xlabel('Puntuación de Bienestar (1-5)')
            ax2.set_ylabel('Frecuencia')
            ax2.grid(True, alpha=0.3)
            
            # Añadir línea de promedio
            mean_wellness = surveys_df['wellness_score'].mean()
            ax2.axvline(mean_wellness, color='red', linestyle='--',
                    label=f'Promedio: {mean_wellness:.1f}')
            ax2.legend()
        
        plt.tight_layout()
        
        filename = f"mood_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico de distribución guardado: {filepath}")
        return filepath
    
    def create_trend_analysis_plot(self, days: int = 30) -> str:
        """
        Crea un gráfico de análisis de tendencias temporales.
        
        Args:
            days (int): Número de días a analizar
            
        Returns:
            str: Ruta del archivo generado
        """
        trends_df = self.analyzer.analyze_mood_trends(days)
        
        if trends_df.empty:
            print("❌ No hay datos suficientes para análisis de tendencias")
            return ""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Convertir fecha a datetime para mejor visualización
        trends_df['date'] = pd.to_datetime(trends_df['date'])
        
        # Gráfico 1: Tendencia de ánimo promedio
        if 'mood_mean' in trends_df.columns:
            axes[0, 0].plot(trends_df['date'], trends_df['mood_mean'], 
                           marker='o', linewidth=2, color='blue')
            axes[0, 0].set_title('Tendencia del Estado de Ánimo Promedio')
            axes[0, 0].set_ylabel('Ánimo Promedio (1-5)')
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Gráfico 2: Tendencia de bienestar promedio
        if 'wellness_score_mean' in trends_df.columns:
            axes[0, 1].plot(trends_df['date'], trends_df['wellness_score_mean'], 
                           marker='s', linewidth=2, color='green')
            axes[0, 1].set_title('Tendencia del Bienestar Promedio')
            axes[0, 1].set_ylabel('Bienestar Promedio (1-5)')
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Gráfico 3: Número de encuestas por día
        if 'mood_count' in trends_df.columns:
            axes[1, 0].bar(trends_df['date'], trends_df['mood_count'], 
                          alpha=0.7, color='orange')
            axes[1, 0].set_title('Número de Encuestas por Día')
            axes[1, 0].set_ylabel('Número de Encuestas')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Gráfico 4: Alertas de crisis por día
        if 'crisis_alert_sum' in trends_df.columns:
            axes[1, 1].bar(trends_df['date'], trends_df['crisis_alert_sum'], 
                          alpha=0.7, color='red')
            axes[1, 1].set_title('Alertas de Crisis por Día')
            axes[1, 1].set_ylabel('Número de Alertas')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        filename = f"trend_analysis_{days}days_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico de tendencias guardado: {filepath}")
        return filepath
    
    def create_correlation_heatmap(self) -> str:
        """
        Crea un mapa de calor de correlaciones entre indicadores emocionales.
        
        Returns:
            str: Ruta del archivo generado
        """
        correlation_matrix = self.analyzer.analyze_correlations()
        
        if correlation_matrix.empty:
            print("❌ No hay datos suficientes para análisis de correlaciones")
            return ""
        
        plt.figure(figsize=(12, 10))
        
        # Renombrar columnas para mejor visualización
        column_labels = {
            'mood': 'Estado de Ánimo',
            'anxiety': 'Ansiedad',
            'sleep': 'Sueño',
            'social': 'Conexión Social',
            'energy': 'Energía',
            'stress': 'Estrés',
            'hopeful': 'Esperanza',
            'wellness_score': 'Bienestar'
        }
        
        correlation_matrix = correlation_matrix.rename(columns=column_labels)
        correlation_matrix = correlation_matrix.rename(index=column_labels)
        
        # Crear mapa de calor
        sns.heatmap(correlation_matrix, 
                    annot=True, 
                    cmap='RdBu_r', 
                    center=0,
                    square=True,
                    fmt='.2f',
                    cbar_kws={'shrink': 0.8})
        
        plt.title('Matriz de Correlaciones - Indicadores Emocionales', 
                  fontsize=16, pad=20)
        plt.tight_layout()
        
        filename = f"correlation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Mapa de calor guardado: {filepath}")
        return filepath
    
    def create_risk_analysis_plot(self) -> str:
        """
        Crea visualizaciones de análisis de riesgo.
        
        Returns:
            str: Ruta del archivo generado
        """
        users_df, surveys_df = self.analyzer.load_data()
        user_analysis = self.analyzer.analyze_user_risk_patterns()
        
        if user_analysis.empty:
            print("❌ No hay datos de usuarios para análisis de riesgo")
            return ""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Gráfico 1: Distribución de puntuaciones de bienestar
        axes[0, 0].hist(user_analysis['avg_wellness'], bins=10, alpha=0.7, color='red')
        axes[0, 0].axvline(3.0, color='darkred', linestyle='--', 
                          label='Umbral de Riesgo (3.0)')
        axes[0, 0].set_title('Distribución de Puntuaciones de Bienestar')
        axes[0, 0].set_xlabel(self.LABEL_BIENESTAR)
        axes[0, 0].set_ylabel('Número de Usuarios')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfico 2: Relación entre edad y bienestar
        scatter = axes[0, 1].scatter(user_analysis['age'], user_analysis['avg_wellness'], 
                                    c=user_analysis['crisis_rate'], cmap='RdYlGn', alpha=0.6)
        axes[0, 1].set_title('Relación Edad vs Bienestar')
        axes[0, 1].set_xlabel('Edad')
        axes[0, 1].set_ylabel(self.LABEL_BIENESTAR)
        plt.colorbar(scatter, ax=axes[0, 1], label='Tasa de Crisis (%)')
        
        # Gráfico 3: Distribución de tendencias
        if 'mood_trend' in user_analysis.columns:
            trend_counts = user_analysis['mood_trend'].value_counts()
            axes[1, 0].pie(trend_counts.values, labels=trend_counts.index, autopct='%1.1f%%')
            axes[1, 0].set_title('Distribución de Tendencias de Ánimo')
        
        # Gráfico 4: Contextos con menor bienestar
        if not surveys_df.empty and 'context' in users_df.columns:
            surveys_with_context = surveys_df.merge(
                users_df[['user_id', 'context']], on='user_id', how='left'
            )
            if 'wellness_score' in surveys_with_context.columns:
                # Filtrar por bajo bienestar (menor a 3.0)
                low_wellness = surveys_with_context[surveys_with_context['wellness_score'] < 3.0]
                if not low_wellness.empty:
                    context_counts = low_wellness['context'].value_counts().head(5)
                    axes[1, 1].barh(context_counts.index, context_counts.values, color='orange')
                    axes[1, 1].set_title('Contextos con Menor Nivel de Bienestar')
                    axes[1, 1].set_xlabel('Número de Encuestas')
        
        plt.tight_layout()
        
        filename = f"risk_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Análisis de riesgo guardado: {filepath}")
        return filepath
    
    def create_user_context_analysis(self) -> str:
        """
        Crea análisis visual por contexto de usuarios.
        
        Returns:
            str: Ruta del archivo generado
        """
        users_df, surveys_df = self.analyzer.load_data()
        
        if users_df.empty:
            print("❌ No hay datos de usuarios disponibles")
            return ""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Gráfico 1: Distribución por contexto
        if 'context' in users_df.columns:
            context_counts = users_df['context'].value_counts()
            axes[0, 0].pie(context_counts.values, labels=context_counts.index, 
                          autopct='%1.1f%%', startangle=90)
            axes[0, 0].set_title('Distribución de Usuarios por Contexto')
        
        # Gráfico 2: Edad promedio por contexto
        if 'context' in users_df.columns and 'age' in users_df.columns:
            context_age = users_df.groupby('context')['age'].mean()
            axes[0, 1].bar(context_age.index, context_age.values, color='skyblue')
            axes[0, 1].set_title('Edad Promedio por Contexto')
            axes[0, 1].set_ylabel('Edad Promedio')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Gráfico 3: Bienestar promedio por contexto
        if not surveys_df.empty and 'context' in users_df.columns:
            # Combinar encuestas con contexto de usuarios
            surveys_with_context = surveys_df.merge(
                users_df[['user_id', 'context']], on='user_id', how='left'
            )
            if 'wellness_score' in surveys_with_context.columns:
                context_wellness = surveys_with_context.groupby('context')['wellness_score'].mean()
                bars = axes[1, 0].bar(context_wellness.index, context_wellness.values, 
                                    color='lightgreen', alpha=0.7)
                axes[1, 0].axhline(y=self.UMBRAL_RIESGO, color='red', linestyle='--', 
                                  label='Umbral de Riesgo')
                axes[1, 0].set_title('Puntuación de Bienestar Promedio por Contexto')
                axes[1, 0].set_ylabel(self.LABEL_BIENESTAR)
                axes[1, 0].legend()
                axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Gráfico 4: Número de encuestas por contexto (si hay datos de encuestas)
        if not surveys_df.empty and 'user_id' in surveys_df.columns:
            # Combinar con datos de usuario para obtener contexto
            surveys_with_context = surveys_df.merge(
                users_df[['user_id', 'context']], on='user_id', how='left'
            )
            if 'context' in surveys_with_context.columns:
                context_surveys = surveys_with_context.groupby('context').size()
                axes[1, 1].bar(context_surveys.index, context_surveys.values, color='green')
                axes[1, 1].set_title('Número de Encuestas por Contexto')
                axes[1, 1].set_ylabel('Número de Encuestas')
                axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        filename = f"context_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Análisis por contexto guardado: {filepath}")
        return filepath
    
    def create_dashboard_summary(self) -> str:
        """
        Crea un dashboard resumen con múltiples visualizaciones.
        
        Returns:
            str: Ruta del archivo generado
        """
        print("📊 Creando dashboard resumen...")
        
        # Crear todas las visualizaciones
        plots_created = []
        
        mood_plot = self.create_mood_distribution_plot()
        if mood_plot:
            plots_created.append("Distribución de estados de ánimo")
        
        trend_plot = self.create_trend_analysis_plot()
        if trend_plot:
            plots_created.append("Análisis de tendencias")
        
        correlation_plot = self.create_correlation_heatmap()
        if correlation_plot:
            plots_created.append("Matriz de correlaciones")
        
        risk_plot = self.create_risk_analysis_plot()
        if risk_plot:
            plots_created.append("Análisis de riesgo")
        
        context_plot = self.create_user_context_analysis()
        if context_plot:
            plots_created.append("Análisis por contexto")
        
        # Crear un archivo de resumen
        summary_file = os.path.join(
            self.output_path,
            f"dashboard_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("DASHBOARD - RESUMEN DE VISUALIZACIONES\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Visualizaciones generadas:\n")
            for i, plot_name in enumerate(plots_created, 1):
                f.write(f"{i}. {plot_name}\n")
            
            if not plots_created:
                f.write("No se pudieron generar visualizaciones - datos insuficientes\n")
            
            f.write(f"\nTotal de visualizaciones: {len(plots_created)}\n")
            f.write(f"Archivos guardados en: {self.output_path}\n")
        
        print(f"✅ Dashboard resumen completado: {len(plots_created)} visualizaciones")
        print(f"📄 Resumen guardado en: {summary_file}")
        
        return summary_file
    
    def export_all_visualizations(self) -> List[str]:
        """
        Exporta todas las visualizaciones disponibles.
        
        Returns:
            List[str]: Lista de rutas de archivos generados
        """
        print("🎨 Generando todas las visualizaciones...")
        
        exported_files = []
        
        # Lista de métodos de visualización
        visualization_methods = [
            self.create_mood_distribution_plot,
            self.create_trend_analysis_plot,
            self.create_correlation_heatmap,
            self.create_risk_analysis_plot,
            self.create_user_context_analysis
        ]
        
        for method in visualization_methods:
            try:
                result = method()
                if result:
                    exported_files.append(result)
            except Exception as e:
                print(f"⚠️ Error generando visualización: {str(e)}")
        
        # Crear dashboard resumen
        summary = self.create_dashboard_summary()
        if summary:
            exported_files.append(summary)
        
        print(f"✅ Proceso completo: {len(exported_files)} archivos generados")
        return exported_files

if __name__ == "__main__":
    viz_generator = VisualizationGenerator()
    viz_generator.export_all_visualizations()