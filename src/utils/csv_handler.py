"""
Manejador de archivos CSV para el sistema de monitoreo emocional.
Proporciona funciones para leer, escribir y manipular archivos CSV de forma segura.
"""

import pandas as pd
import os
from typing import Dict, List, Any, Optional

class CSVHandler:
    """
    Clase para manejar operaciones con archivos CSV.
    
    Proporciona métodos seguros para leer, escribir y manipular
    archivos CSV con validación de datos.
    """
    
    @staticmethod
    def read_csv(file_path: str, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        Lee un archivo CSV y retorna un DataFrame.
        
        Args:
            file_path (str): Ruta del archivo CSV
            encoding (str): Codificación del archivo
            
        Returns:
            pd.DataFrame: DataFrame con los datos del CSV
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            pd.errors.EmptyDataError: Si el archivo está vacío
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")
        
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            return df
        except pd.errors.EmptyDataError:
            # Retorna DataFrame vacío si el archivo está vacío
            return pd.DataFrame()
        except Exception as e:
            raise IOError(f"Error al leer el archivo CSV: {str(e)}")
    
    @staticmethod
    def write_csv(data: pd.DataFrame, file_path: str, 
                encoding: str = 'utf-8', index: bool = False) -> None:
        """
        Escribe un DataFrame a un archivo CSV.
        
        Args:
            data (pd.DataFrame): DataFrame a escribir
            file_path (str): Ruta del archivo de destino
            encoding (str): Codificación del archivo
            index (bool): Si incluir el índice en el archivo
        """
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            data.to_csv(file_path, index=index, encoding=encoding)
        except Exception as e:
            raise IOError(f"Error al escribir el archivo CSV: {str(e)}")
    
    @staticmethod
    def append_to_csv(new_data: Dict[str, Any], file_path: str,
                    encoding: str = 'utf-8') -> None:
        """
        Añade una nueva fila a un archivo CSV existente.
        
        Args:
            new_data (dict): Diccionario con los nuevos datos
            file_path (str): Ruta del archivo CSV
            encoding (str): Codificación del archivo
        """
        # Crear DataFrame con los nuevos datos
        new_df = pd.DataFrame([new_data])
        
        if os.path.exists(file_path):
            # Leer archivo existente y concatenar
            existing_df = CSVHandler.read_csv(file_path, encoding)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df
        
        CSVHandler.write_csv(combined_df, file_path, encoding)
    
    @staticmethod
    def validate_csv_structure(file_path: str, 
                            required_columns: List[str]) -> bool:
        """
        Valida que un archivo CSV tenga las columnas requeridas.
        
        Args:
            file_path (str): Ruta del archivo CSV
            required_columns (List[str]): Lista de columnas requeridas
            
        Returns:
            bool: True si la estructura es válida
        """
        try:
            df = CSVHandler.read_csv(file_path)
            return all(col in df.columns for col in required_columns)
        except (FileNotFoundError, pd.errors.EmptyDataError, IOError):
            return False
    
    @staticmethod
    def clean_csv_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia y normaliza datos de un DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame a limpiar
            
        Returns:
            pd.DataFrame: DataFrame limpio
        """
        # Crear copia para no modificar el original
        clean_df = df.copy()
        
        # Eliminar filas completamente vacías
        clean_df = clean_df.dropna(how='all')
        
        # Limpiar espacios en strings
        string_columns = clean_df.select_dtypes(include=['object']).columns
        clean_df[string_columns] = clean_df[string_columns].apply(
            lambda x: x.str.strip() if x.dtype == "object" else x
        )
        
        # Convertir strings vacíos a NaN
        clean_df = clean_df.replace('', pd.NA)
        
        return clean_df
    
    @staticmethod
    def merge_csv_files(file_paths: List[str], output_path: str,
                    encoding: str = 'utf-8') -> None:
        """
        Combina múltiples archivos CSV en uno solo.
        
        Args:
            file_paths (List[str]): Lista de rutas de archivos CSV
            output_path (str): Ruta del archivo de salida
            encoding (str): Codificación de los archivos
        """
        dataframes = []
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                df = CSVHandler.read_csv(file_path, encoding)
                dataframes.append(df)
        
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            CSVHandler.write_csv(combined_df, output_path, encoding)
        else:
            raise ValueError("No se encontraron archivos válidos para combinar")
    
    @staticmethod
    def get_csv_info(file_path: str) -> Dict[str, Any]:
        """
        Obtiene información sobre un archivo CSV.
        
        Args:
            file_path (str): Ruta del archivo CSV
            
        Returns:
            dict: Información del archivo CSV
        """
        if not os.path.exists(file_path):
            return {'exists': False}
        
        try:
            df = CSVHandler.read_csv(file_path)
            
            return {
                'exists': True,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'file_size_kb': os.path.getsize(file_path) / 1024,
                'has_null_values': df.isnull().any().any(),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024)
            }
        except Exception as e:
            return {
                'exists': True,
                'error': str(e)
            }
    
    @staticmethod
    def backup_csv(file_path: str, backup_dir: str = "data/backups") -> str:
        """
        Crea una copia de seguridad de un archivo CSV.
        
        Args:
            file_path (str): Ruta del archivo a respaldar
            backup_dir (str): Directorio de respaldos
            
        Returns:
            str: Ruta del archivo de respaldo
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")
        
        # Crear directorio de respaldo
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generar nombre de respaldo con timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        backup_filename = f"{name}_backup_{timestamp}{ext}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copiar archivo
        df = CSVHandler.read_csv(file_path)
        CSVHandler.write_csv(df, backup_path)
        
        return backup_path
    
    @staticmethod
    def export_filtered_data(df: pd.DataFrame, filters: Dict[str, Any],
                        output_path: str) -> None:
        """
        Exporta datos filtrados a un nuevo archivo CSV.
        
        Args:
            df (pd.DataFrame): DataFrame original
            filters (dict): Filtros a aplicar
            output_path (str): Ruta del archivo de salida
        """
        filtered_df = df.copy()
        
        for column, condition in filters.items():
            if column in filtered_df.columns:
                if isinstance(condition, dict):
                    # Filtro con operadores
                    if 'min' in condition:
                        filtered_df = filtered_df[filtered_df[column] >= condition['min']]
                    if 'max' in condition:
                        filtered_df = filtered_df[filtered_df[column] <= condition['max']]
                    if 'equals' in condition:
                        filtered_df = filtered_df[filtered_df[column] == condition['equals']]
                    if 'contains' in condition:
                        filtered_df = filtered_df[
                            filtered_df[column].str.contains(condition['contains'], na=False)
                        ]
                else:
                    # Filtro simple de igualdad
                    filtered_df = filtered_df[filtered_df[column] == condition]
        
        CSVHandler.write_csv(filtered_df, output_path)
    
    @staticmethod
    def create_summary_csv(df: pd.DataFrame, output_path: str,
                        group_by: Optional[str] = None) -> None:
        """
        Crea un resumen estadístico de los datos en formato CSV.
        
        Args:
            df (pd.DataFrame): DataFrame a resumir
            output_path (str): Ruta del archivo de resumen
            group_by (str, optional): Columna para agrupar
        """
        if group_by and group_by in df.columns:
            # Resumen agrupado
            summary = df.groupby(group_by).agg({
                col: ['count', 'mean', 'std', 'min', 'max'] 
                for col in df.select_dtypes(include=['number']).columns
            }).round(2)
            
            # Aplanar columnas multinivel
            summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
            summary = summary.reset_index()
        else:
            # Resumen general
            summary = df.describe().transpose()
            summary = summary.reset_index()
            summary.rename(columns={'index': 'column'}, inplace=True)
        
        CSVHandler.write_csv(summary, output_path)