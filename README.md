# Plataforma de Monitoreo Emocional - _Feel your emotions_

## 📋 Descripción del Proyecto

Consiste en una plataforma web diseñada para monitorear el estado emocional y mental de jóvenes en contextos vulnerables, utilizando análisis de datos con Python para identificar patrones de riesgo y ofrecer apoyo temprano.

## 🎯 Objetivo

Desarrollar una herramienta tecnológica que permita:
- Detectar tempranamente situaciones de riesgo emocional en jóvenes
- Proporcionar recursos de apoyo personalizados
- Generar insights mediante análisis de datos para intervenciones efectivas

## 🔧 Tecnologías Utilizadas

- **Backend**: Python 3.8+
- **Análisis de Datos**: Pandas, NumPy, Matplotlib, Seaborn, FastAPI
- **Almacenamiento**: CSV (fase inicial y respaldo), mySQL
- **Control de Versiones**: Git & GitHub

## 📁 Estructura del Proyecto

```
root/
├── src/
│   ├── models/          # Modelos de datos
│   ├── services/        # Lógica de negocio
│   ├── routers/         # Controladores para peticiones HTTP
│   ├── utils/           # Utilidades y helpers
│   └── analysis/        # Scripts de análisis y generación de gráficos
├── data/
│   ├── raw/             # Datos sin procesar
│   ├── processed/       # Datos procesados
│   └── exports/         # Reportes y visualizaciones
├── docs/                # Documentación
├── tests/               # Pruebas unitarias
├── requirements.txt     # Dependencias
└── LICENSE              # Licencia del proyecto
```

## 🚀 Instalación y Uso

1. Clonar el repositorio:
```bash
git clone https://github.com/ADNdavid/backend_feel-your-emotions
cd backend_feel-your-emotions
```

2. Crear entorno virtual:
```bash
python -m venv env
source env/Scripts/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar el sistema:
```bash
python fastapi dev
```

## 📊 Funcionalidades Principales

### Fase 1 (Segunda Entrega)
- [x] Registro de usuarios y perfiles
- [x] Sistema de encuestas emocionales
- [x] Almacenamiento local en CSV
- [x] Control de versiones con Git

### Fase 2 (Tercera Entrega)
- [x] Base de datos estructurada
- [x] Análisis exploratorio de datos
- [x] Visualizaciones interactivas
- [x] Dashboard de monitoreo
- [x] Sistema de alertas básico

### Fase 3 (Futuras mejoras)
- [x] Algoritmos de ML para detección de riesgo
- [x] Recomendaciones personalizadas
- [x] Interfaz web completa
- [x] Integración con bases de datos

## 🌐 Enlaces 
- **Repositorio Frontend**: [repo](https://github.com/zorany26/frontend_feel-your-emotions)
- **Sitio en vivo**: [GitHub Pages]()

## 📈 Estado del Proyecto

**Versión actual**: 1.0.0

## 🤝 Contribuciones

Proyecto integrador desarrollado como parte del programa de Desarrollo de Software en CESDE del curso de 'Nuevas Tecnologías'.

## 🧑‍💻 Desarrolladores

- **Anderson Sepúlveda**: [@ADNdavid](https://github.com/ADNdavid) - LinkedIn: [Anderson Sepúlveda](https://www.linkedin.com/in/adndavid/)
- **Zorany Pamplona**: [@zorany26](https://github.com/zorany26)
- **Lina Alvarez**: [@Lina-1205](https://github.com/LINA-1205)