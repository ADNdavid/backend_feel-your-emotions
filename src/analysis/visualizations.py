"""
Generador de visualizaciones.
Crea gráficos y dashboards para análisis de datos emocionales.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
import os
import math
import textwrap
from datetime import datetime

from .data_analyzer import EmotionalDataAnalyzer

# Agregar el directorio raíz al path para permitir importaciones absolutas
#import sys
#root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#if root_dir not in sys.path:
#    sys.path.append(root_dir)
#from src.analysis.data_analyzer import EmotionalDataAnalyzer

class VisualizationGenerator:
    """
    Generador de visualizaciones para análisis emocional.
    
    Crea gráficos, dashboards y reportes visuales para el
    análisis de datos del sistema EmoTracker.
    """
    
    # Constantes para etiquetas
    LABEL_BIENESTAR = 'Puntuación de Bienestar'
    UMBRAL_RIESGO = 3.0  # Umbral de riesgo para el bienestar
    
    # Formatos de imagen soportados
    SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'svg', 'pdf']
    
    def __init__(self, analyzer: Optional[EmotionalDataAnalyzer] = None,
                output_path: str = "data/exports",
                output_format: str = "png"):
        """
        Inicializa el generador de visualizaciones.
        
        Args:
            analyzer (EmotionalDataAnalyzer, optional): Analizador de datos
            output_path (str): Ruta para guardar las visualizaciones
            output_format (str): Formato de salida para las imágenes ('png', 'jpg', 'svg', 'pdf')
        """
        self.analyzer = analyzer or EmotionalDataAnalyzer()
        self.output_path = output_path
        self.context_colors = {}  # Se inicializará con los datos
        
        # Validar y establecer formato de salida
        output_format = output_format.lower().strip('.')
        if output_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Formato no soportado. Use uno de: {', '.join(self.SUPPORTED_FORMATS)}")
        self.output_format = output_format
        
        # Configurar estilo de matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        
        # Crear directorio de salida
        os.makedirs(output_path, exist_ok=True)
        
    def _initialize_color_palette(self, contexts):
        """
        Inicializa una paleta de colores para los contextos existentes.
        
        Args:
            contexts: Lista de contextos únicos en los datos
        """
        if not self.context_colors:  # Solo inicializar si no existe
            # Usar una paleta de colores suave pero distintiva
            n_colors = len(contexts)
            colors = sns.color_palette("husl", n_colors)
            # Asegurar que los colores sean suficientemente diferentes
            self.context_colors = dict(zip(sorted(contexts), colors))
    
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
            ax1.set_title('Distribución de Estados de Ánimo', fontsize=18)
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
            ax2.set_title('Distribución de Puntuaciones de Bienestar', fontsize=18)
            ax2.set_xlabel('Puntuación de Bienestar (1-5)')
            ax2.set_ylabel('Frecuencia')
            ax2.grid(True, alpha=0.3)
            
            # Añadir línea de promedio
            mean_wellness = surveys_df['wellness_score'].mean()
            ax2.axvline(mean_wellness, color='red', linestyle='--',
                    label=f'Promedio: {mean_wellness:.1f}')
            ax2.legend()
        
        plt.tight_layout()
        
        filename = f"mood_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self.output_format}"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', format=self.output_format)
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
        
        date_format = '%d %b %Y'
        if trends_df.empty:
            print("❌ No hay datos suficientes para análisis de tendencias")
            return ""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Convertir fecha a datetime para mejor visualización
        trends_df['date'] = pd.to_datetime(trends_df['date'])
        print(f"trends_df:\n{trends_df}")
        # Gráfico 1: Tendencia de ánimo promedio
        if 'mood_mean' in trends_df.columns:
            axes[0, 0].plot(trends_df['date'], trends_df['mood_mean'], 
                           marker='o', linewidth=2, color='blue')
            axes[0, 0].set_title('Tendencia del Estado de Ánimo Promedio', fontsize=18)
            axes[0, 0].set_ylabel('Ánimo Promedio (1-5)')
            axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].tick_params(axis='x', rotation=90)
        
        # Gráfico 2: Tendencia de bienestar promedio
        if 'wellness_score_mean' in trends_df.columns:
            axes[0, 1].plot(trends_df['date'], trends_df['wellness_score_mean'], 
                           marker='s', linewidth=2, color='green')
            axes[0, 1].set_title('Tendencia del Bienestar Promedio', fontsize=18)
            axes[0, 1].set_ylabel('Bienestar Promedio (1-5)')
            axes[0, 1].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].tick_params(axis='x', rotation=90)
        
        # Gráfico 3: Número de encuestas por día
        if 'mood_count' in trends_df.columns:
            axes[1, 0].bar(trends_df['date'], trends_df['mood_count'], 
                          alpha=0.7, color='orange')
            axes[1, 0].set_title('Número de Encuestas por Día', fontsize=18)
            axes[1, 0].set_ylabel('Número de Encuestas')
            axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            axes[1, 0].tick_params(axis='x', rotation=90)
        
        # Gráfico 4: Alertas de crisis por día
        if 'crisis_alert_sum' in trends_df.columns:
            axes[1, 1].bar(trends_df['date'], trends_df['crisis_alert_sum'], 
                          alpha=0.7, color='red')
            axes[1, 1].set_title('Alertas de Crisis por Día', fontsize=18)
            axes[1, 1].set_ylabel('Número de Alertas')
            axes[1, 1].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            axes[1, 1].tick_params(axis='x', rotation=90)
        
        plt.tight_layout()
        
        filename = f"trend_analysis_{days}days_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self.output_format}"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', format=self.output_format)
        plt.close()
        
        print(f"✅ Gráfico de tendencias guardado: {filepath}")
        return filepath
    
    def create_gender_analysis_plot(self) -> str:
        """
        Crea visualizaciones específicas de análisis por género.
        
        Returns:
            str: Ruta del archivo generado
        """
        users_df, surveys_df = self.analyzer.load_data()
        gender_analysis = self.analyzer.analyze_gender_patterns()
        
        if users_df.empty or 'gender' not in users_df.columns:
            print("❌ No hay datos suficientes para análisis por género")
            return ""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Gráfico 1: Distribución por género
        gender_counts = pd.Series(gender_analysis['distribution'])
        gender_labels = [textwrap.fill(str(label), width=15) for label in gender_counts.index]
        _, texts, autotexts = axes[0, 0].pie(
            gender_counts.values,
            labels=gender_labels,
            colors=plt.cm.Set3(np.linspace(0, 1, len(gender_counts))),
            autopct='%1.1f%%',
            startangle=90
        )
        axes[0, 0].set_title('Distribución por Género', fontsize=18)
        
        # Gráfico 2: Edad promedio por género
        if 'age_by_gender' in gender_analysis:
            age_data = pd.DataFrame(gender_analysis['age_by_gender']).T
            print(f"age_data:\n{age_data}")
            ax = age_data['mean'].plot(
                kind='bar',
                #yerr=age_data['max'] - age_data['min'],
                ax=axes[0, 1],
                color='skyblue',
                capsize=5
            )
            axes[0, 1].set_title('Edad Promedio por Género', fontsize=18)
            axes[0, 1].set_ylabel('Edad')
            # Agregar etiquetas encima de cada barra
            for container in ax.containers:
                ax.bar_label(container, fmt='%.2f', label_type='edge', padding=3)
            
            
        # Gráfico 3: Bienestar promedio por género
        if 'wellness_by_gender' in gender_analysis:
            wellness_data = pd.DataFrame(gender_analysis['wellness_by_gender'])
            wellness_metrics = pd.DataFrame({
                'Bienestar': wellness_data.loc['wellness_score', 'mean'],
                'Estado de Ánimo': wellness_data.loc['mood', 'mean']
            })
            ax = wellness_metrics.plot(
                kind='bar',
                ax=axes[1, 0],
                color=['green', 'orange'],
                alpha=0.7
            )
            axes[1, 0].set_title('Indicadores de Bienestar por Género', fontsize=18)
            axes[1, 0].set_ylabel('Puntuación Promedio')
            # Agregar etiquetas encima de cada barra
            for container in ax.containers:
                ax.bar_label(container, fmt='%.2f', label_type='edge', padding=3)
        
        # Gráfico 4: Tasa de crisis por género
        if 'crisis_by_gender' in gender_analysis:
            crisis_data = pd.DataFrame(gender_analysis['crisis_by_gender'])
            print(f"crisis_data: \n{crisis_data}")
            if 'users_with_crisis' in crisis_data.columns:
                crisis_rate = (crisis_data['total_users'] / 
                            crisis_data['users_with_crisis'] * 100).round(1)
                print(f"crisis_rate: \n{crisis_rate}")
                ax = crisis_rate.plot(
                    kind='bar',
                    ax=axes[1, 1],
                    color='red',
                    alpha=0.7
                )
                axes[1, 1].set_title('Tasa de Crisis por Género', fontsize=18)
                axes[1, 1].set_ylabel('Porcentaje de Usuarios (%)')
                for container in ax.containers:
                    ax.bar_label(container, fmt='%.2f', label_type='edge', padding=3)
        
        plt.tight_layout()
        
        filename = f"gender_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self.output_format}"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', format=self.output_format)
        plt.close()
        
        print(f"✅ Análisis por género guardado: {filepath}")
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
                  fontsize=18, pad=20)
        plt.tight_layout()
        
        filename = f"correlation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self.output_format}"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', format=self.output_format)
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
        axes[0, 0].set_title('Distribución de Puntuaciones de Bienestar', fontsize=18)
        axes[0, 0].set_xlabel(self.LABEL_BIENESTAR)
        axes[0, 0].set_ylabel('Número de Usuarios')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfico 2: Relación entre edad y bienestar
        scatter = axes[0, 1].scatter(user_analysis['age'], user_analysis['avg_wellness'], 
                                    c=user_analysis['crisis_rate'], cmap='RdYlGn', alpha=0.6)
        axes[0, 1].set_title('Relación Edad vs Bienestar', fontsize=18)
        axes[0, 1].set_xlabel('Edad')
        axes[0, 1].set_ylabel(self.LABEL_BIENESTAR)
        plt.colorbar(scatter, ax=axes[0, 1], label='Tasa de Crisis (%)')
        
        # Gráfico 3: Distribución de tendencias
        if 'mood_trend' in user_analysis.columns:
            trend_counts = user_analysis['mood_trend'].value_counts()
            # Envolver etiquetas largas
            wrapped_labels = [textwrap.fill(label.capitalize(), width=15, break_long_words=False) 
                            for label in trend_counts.index]
            # Crear gráfico de torta con etiquetas envueltas
            wedges, texts, autotexts = axes[1, 0].pie(
                trend_counts.values, 
                labels=wrapped_labels,
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85,
                labeldistance=1.1
            )
            # Ajustar el tamaño de las etiquetas
            plt.setp(texts, size=9)
            plt.setp(autotexts, size=8)
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
                    print(f"low_wellness:\n{low_wellness}")
                    context_counts = low_wellness['context'].value_counts().head(5)
                    print(f"context_counts:{context_counts}")
                    wrapped_labels = [textwrap.fill(label.capitalize(), width=20, break_long_words=False) 
                            for label in context_counts.index]
                    axes[1, 1].barh(wrapped_labels, context_counts.values, color='orange')
                    axes[1, 1].set_title('Contextos con Menor Nivel de Bienestar')
                    axes[1, 1].set_xlabel('Número de Encuestas')
        
        plt.tight_layout()
        
        filename = f"risk_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self.output_format}"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', format=self.output_format)
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
        
        # Gráfico 1: Distribución por contexto y género
        if 'context' in users_df.columns and 'gender' in users_df.columns:
            # Panel izquierdo: Distribución por contexto
            context_counts = users_df['context'].value_counts()
            
            # Panel derecho: Distribución por género
            gender_counts = users_df['gender'].value_counts()
            
            # Inicializar la paleta de colores si es necesario
            if not self.context_colors:
                self._initialize_color_palette(users_df['context'].unique())
            
            # Envolver etiquetas largas
            wrapped_labels = [textwrap.fill(label, width=20, break_long_words=False) 
                            for label in context_counts.index]
            # Obtener colores para cada contexto
            context_colors = [self.context_colors.get(context, '#CCCCCC') for context in context_counts.index]
            
            # Crear gráfico de torta con etiquetas envueltas y colores consistentes
            wedges, texts, autotexts = axes[0, 0].pie(
                context_counts.values, 
                labels=wrapped_labels,
                colors=context_colors,
                autopct='%1.1f%%', 
                startangle=90,
                pctdistance=0.85,  # Mover los porcentajes más hacia afuera
                labeldistance=1.1   # Mover las etiquetas más hacia afuera
            )
            # Ajustar el tamaño de las etiquetas
            plt.setp(texts, size=9)
            plt.setp(autotexts, size=8)
            axes[0, 0].set_title('Distribución de Usuarios por Contexto', fontsize=18)
        
        # Gráfico 2: Edad promedio por contexto
        if 'context' in users_df.columns and 'age' in users_df.columns:
            context_age = users_df.groupby('context')['age'].mean()
            print(f"context_age:\n{context_age}")
            # Usar los colores ya inicializados
            context_colors = [self.context_colors.get(context, '#CCCCCC') for context in context_age.index]
            axes[0, 1].bar(range(len(context_age)), context_age.values, color=context_colors)
            axes[0, 1].set_title('Edad Promedio por Contexto', fontsize=18)
            axes[0, 1].set_ylabel('Edad Promedio')
            # Ajustar etiquetas del eje x
            axes[0, 1].set_xticks(range(len(context_age)))
            # Envolver el texto de las etiquetas largas
            wrapped_labels = [textwrap.fill(label, width=25, break_long_words=False) 
                            for label in context_age.index]
            axes[0, 1].set_xticklabels(wrapped_labels, rotation=45, ha='right')
            # Ajustar los márgenes para las etiquetas
            plt.setp(axes[0, 1].get_xticklabels(), fontsize=9)
        
        # Gráfico 3: Bienestar promedio por contexto
        if not surveys_df.empty and 'context' in users_df.columns:
            # Combinar encuestas con contexto de usuarios
            surveys_with_context = surveys_df.merge(
                users_df[['user_id', 'context']], on='user_id', how='left'
            )
            if 'wellness_score' in surveys_with_context.columns:
                context_wellness = surveys_with_context.groupby('context')['wellness_score'].mean()
                print(f"context_wellness\n{context_wellness}")
                # Usar los colores ya inicializados
                context_colors = [self.context_colors.get(context, '#CCCCCC') for context in context_wellness.index]
                bars = axes[1, 0].bar(range(len(context_wellness)), context_wellness.values, 
                                    color=context_colors, alpha=0.8)
                axes[1, 0].axhline(y=self.UMBRAL_RIESGO, color='red', linestyle='--', 
                                  label='Umbral de Riesgo')
                axes[1, 0].set_title('Puntuación de Bienestar Promedio por Contexto', fontsize=18)
                axes[1, 0].set_ylabel(self.LABEL_BIENESTAR)
                axes[1, 0].legend()
                # Ajustar etiquetas del eje x
                axes[1, 0].set_xticks(range(len(context_wellness)))
                # Envolver el texto de las etiquetas largas
                wrapped_labels = [textwrap.fill(label, width=25, break_long_words=False) 
                                for label in context_wellness.index]
                axes[1, 0].set_xticklabels(wrapped_labels, rotation=45, ha='right')
                # Ajustar los márgenes para las etiquetas
                plt.setp(axes[1, 0].get_xticklabels(), fontsize=9)
                # Añadir valores sobre las barras
                for idx, v in enumerate(context_wellness.values):
                    axes[1, 0].text(idx, v + 0.05, f'{v:.2f}', ha='center', va='bottom')
        
        # Gráfico 4: Número de encuestas por contexto (si hay datos de encuestas)
        if not surveys_df.empty and 'user_id' in surveys_df.columns:
            # Combinar con datos de usuario para obtener contexto
            surveys_with_context = surveys_df.merge(
                users_df[['user_id', 'context']], on='user_id', how='left'
            )
            if 'context' in surveys_with_context.columns:
                context_surveys = surveys_with_context.groupby('context').size()
                print(f"context_surveys:\n{context_surveys}")
                # Usar los colores ya inicializados
                context_colors = [self.context_colors.get(context, '#CCCCCC') for context in context_surveys.index]
                axes[1, 1].bar(range(len(context_surveys)), context_surveys.values, color=context_colors)
                axes[1, 1].set_title('Número de Encuestas por Contexto', fontsize=18)
                axes[1, 1].set_ylabel('Número de Encuestas')
                # Ajustar etiquetas del eje x
                axes[1, 1].set_xticks(range(len(context_surveys)))
                # Envolver el texto de las etiquetas largas
                wrapped_labels = [textwrap.fill(label, width=25, break_long_words=False) 
                                for label in context_surveys.index]
                axes[1, 1].set_xticklabels(wrapped_labels, rotation=45, ha='right')
                # Ajustar los márgenes para las etiquetas
                plt.setp(axes[1, 1].get_xticklabels(), fontsize=9)
                # Añadir valores sobre las barras
                for idx, v in enumerate(context_surveys.values):
                    axes[1, 1].text(idx, v + 0.05, str(v), ha='center', va='bottom')
        
        # Ajustar el espaciado entre subplots para acomodar las etiquetas envueltas
        plt.tight_layout(pad=3.0, h_pad=4.0, w_pad=3.0)
        
        # Ajustar los márgenes inferiores para dar espacio a las etiquetas
        plt.subplots_adjust(bottom=0.2)
        
        filename = f"context_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self.output_format}"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0.5, format=self.output_format)
        plt.close()
        
        print(f"✅ Análisis por contexto guardado: {filepath}")
        return filepath
    
    def create_avg_emotional_state_by_context(self) -> str:
        """
        Genera un gráfico de barras que muestra el estado emocional promedio por contexto.
        
        Returns:
            str: Ruta del archivo generado
        """
        # Cargar los datos base
        users_df, surveys_df = self.analyzer.load_data()

        # Validaciones
        if surveys_df.empty or 'wellness_score' not in surveys_df.columns:
            print("❌ No hay datos suficientes en encuestas para generar el gráfico.")
            return ""

        if 'context' not in users_df.columns:
            print("❌ No se encontró la columna 'context' en los datos de usuarios.")
            return ""

        # Combinar encuestas con contexto
        surveys_with_context = surveys_df.merge(
            users_df[['user_id', 'context']], on='user_id', how='left'
        )

        # Calcular promedio por contexto
        avg_emotional_state = (
            surveys_with_context.groupby('context')['wellness_score']
            .mean()
            .sort_values(ascending=False)
        )

        if avg_emotional_state.empty:
            print("❌ No hay datos válidos para graficar el estado emocional por contexto.")
            return ""
        print(f"avg_emotional_state:\n{avg_emotional_state}")
        
        # Umbral
        threshold = 3.0

        # Crear colores con transparencia según distancia al umbral
        colors = []
        for val in avg_emotional_state.values:
            if val >= threshold:
                base_color = mcolors.to_rgba("green")
            else:
                base_color = mcolors.to_rgba("red")
            # Cuanto más cerca del umbral, más transparente
            alpha = min(1.0, 0.3 + abs(val - threshold) / 2.5)
            color = (base_color[0], base_color[1], base_color[2], alpha)
            colors.append(color)

        # Crear índices numéricos para reemplazar textos largos
        context_labels = avg_emotional_state.index.tolist()
        numeric_positions = range(1, len(context_labels) + 1)

        # Crear figura
        plt.figure(figsize=(14, 10))
        bars = plt.bar(numeric_positions, avg_emotional_state.values, color=colors)

        # Línea de referencia
        plt.axhline(y=threshold, color='gray', linestyle='--', linewidth=1.5, label=f'Umbral de bienestar ({threshold})')

        # Etiquetas y título
        plt.title("Estado Emocional Promedio por Contexto", fontsize=18)
        plt.xlabel("ID de Contexto", fontsize=14)
        plt.ylabel("Puntuación Promedio de Bienestar", fontsize=14)

        # Mostrar valores sobre cada barra
        for bar, value in zip(bars, avg_emotional_state.values):
            plt.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.05,
                f"{value:.2f}",
                ha='center',
                va='bottom',
                fontsize=10
            )

        plt.xticks(numeric_positions)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.legend()

        plt.tight_layout(rect=[0, 0.35, 1, 1])  # deja espacio para tabla inferior

        # ===== Crear tabla de contextos en 2 columnas =====
        n = len(context_labels)
        mid = math.ceil(n / 2)

        # Dividir contextos y colores
        left_contexts = context_labels[:mid]
        right_contexts = context_labels[mid:]
        left_colors = colors[:mid]
        right_colors = colors[mid:]

        # Preparar filas de la tabla (alinear dos columnas)
        max_rows = max(len(left_contexts), len(right_contexts))
        cell_text = []
        cell_colors = []

        for i in range(max_rows):
            row = []
            color_row = []
            # Columna izquierda
            if i < len(left_contexts):
                left_color_hex = mcolors.to_hex(left_colors[i][:3])
                row.extend([f"{i+1}", left_contexts[i]])
                color_row.extend([left_color_hex, "white"])
            else:
                row.extend(["", ""])
                color_row.extend(["white", "white"])
            # Columna derecha
            if i < len(right_contexts):
                idx_right = mid + i + 1
                right_color_hex = mcolors.to_hex(right_colors[i][:3])
                row.extend([f"{idx_right}", right_contexts[i]])
                color_row.extend([right_color_hex, "white"])
            else:
                row.extend(["", ""])
                color_row.extend(["white", "white"])
            cell_text.append(row)
            cell_colors.append(color_row)

        col_labels = ["ID", "Contexto", "ID", "Contexto"]

        table = plt.table(
            cellText=cell_text,
            colLabels=col_labels,
            cellLoc='left',
            loc='bottom',
            colWidths=[0.3, 4, 0.3, 4],
            colColours=['#f0f0f0'] * 4,
            cellColours=cell_colors,
            bbox=[0.05, -0.42, 0.9, 0.3]  # posición y tamaño: x, y, ancho, alto
        )

        table.auto_set_font_size(False)
        table.set_fontsize(9)

        # Ajustes visuales
        for (row, col), cell in table.get_celld().items():
            cell.set_edgecolor('gray')
            cell.set_linewidth(0.5)
            if col in [1, 3]:  # contextos
                cell._text.set_wrap(True)  # permitir salto de línea
                cell._text.set_fontsize(8)

        # Guardar archivo
        filename = f"avg_emotional_state_by_context_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{self.output_format}"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight', format=self.output_format)
        plt.close()

        print(f"✅ Gráfico generado y guardado en: {filepath}")
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

        avg_emotional_state_plot = self.create_avg_emotional_state_by_context()
        if context_plot:
            plots_created.append("Análisis estado emocional promedio por contexto")
        
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
            self.create_user_context_analysis,
            self.create_gender_analysis_plot
        ]
        
        for method in visualization_methods:
            try:
                result = method()
                if result:
                    exported_files.append(result)
            except Exception as e:
                print(f"⚠️ Error generando visualización: {str(e)}")
        
        # Crear dashboard resumen
        #summary = self.create_dashboard_summary()
        #if summary:
        #    exported_files.append(summary)
        
        print(f"✅ Proceso completo: {len(exported_files)} archivos generados")
        return exported_files

if __name__ == "__main__":
    viz_generator = VisualizationGenerator()
    viz_generator.export_all_visualizations()