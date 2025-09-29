# Documento de Planeación del Proyecto
## Plataforma de Monitoreo Emocional - _Feel your emotions_

### 1. INFORMACIÓN GENERAL

**Nombre del Proyecto**: _Feel your emotions_ - Plataforma de Monitoreo Emocional  
**Fecha de Inicio**: Septiembre 2025  
**Duración Estimada**: 3 meses  
**Desarrolladores**: Anderson David Sepulveda Gomez, Lina Marcela Alvarez, Zorany Pamplona Chaverra
**Institución**: CESDE - Desarrollo de Software  

### 2. OBJETIVO GENERAL

Diseñar y desarrollar una plataforma web que permita monitorear el estado emocional y mental de jóvenes en contextos vulnerables, integrando herramientas de análisis de datos con Python para identificar patrones de riesgo, generar alertas tempranas y ofrecer recursos de apoyo personalizados.

### 3. OBJETIVOS ESPECÍFICOS

1. **Objetivo Técnico**: Implementar un sistema de registro y seguimiento emocional usando Python
2. **Objetivo Analítico**: Desarrollar algoritmos de análisis de datos para detectar patrones de riesgo
3. **Objetivo Social**: Crear una herramienta de apoyo para jóvenes en situación vulnerable
4. **Objetivo Académico**: Aplicar conocimientos de programación y análisis de datos

### 4. ALCANCE DEL PROYECTO

#### 4.1 Incluye:
- Sistema de registro de usuarios con perfiles emocionales
- Módulo de encuestas periódicas sobre estado de ánimo
- Análisis de datos y detección de patrones de riesgo
- Dashboard con visualizaciones de datos agregados
- Sistema de alertas tempranas
- Base de datos local en formato CSV
- Documentación técnica completa

#### 4.2 No Incluye:
- Base de datos en la nube
- Sistema de notificaciones en tiempo real
- Integración con redes sociales
- Aplicación móvil

### 5. USUARIOS DEL SISTEMA

#### 5.1 Usuario Principal: Jóvenes Vulnerables
- **Edad**: 13-25 años
- **Características**: En situación de vulnerabilidad social, emocional o económica
- **Necesidades**: Expresar su estado emocional, recibir apoyo, acceder a recursos
- **Nivel técnico**: Básico-intermedio

#### 5.2 Usuario Secundario: Profesionales de Apoyo
- **Perfil**: Psicólogos, trabajadores sociales, consejeros
- **Necesidades**: Monitorear múltiples usuarios, identificar casos de riesgo
- **Nivel técnico**: Intermedio

#### 5.3 Usuario Administrativo: Instituciones
- **Perfil**: ONG, instituciones educativas, centros de salud mental
- **Necesidades**: Reportes agregados, estadísticas generales
- **Nivel técnico**: Básico-intermedio

### 6. FUNCIONALIDADES INICIALES
#### 6.1 Primera Entrega

1. **Registro de Usuarios**
   - Crear perfil básico (nombre, edad, contexto)
   - Configuración inicial de perfil emocional
   - Validación de datos de entrada

2. **Sistema de Encuestas**
   - Encuestas de estado de ánimo diarias/semanales
   - Preguntas sobre hábitos y situaciones
   - Almacenamiento en archivos CSV

3. **Gestión de Datos**
   - Carga y guardado de información en CSV
   - Estructura de datos organizada
   - Validación de integridad de datos

#### 6.2 Segunda Entrega
1. **Procesamiento de Datos**
   - Limpieza y transformación de datos
   - Análisis exploratorio de datos (EDA)
   - Cálculo de estadísticas descriptivas

#### 6.3 Tercera Entrega
2. **Visualizaciones**
   - Gráficos de tendencias emocionales
   - Distribuciones de estados de ánimo
   - Correlaciones entre variables

3. **Dashboard Básico**
   - Estado emocional promedio por grupo
   - Alertas de riesgo según puntuaciones
   - Evolución temporal del bienestar

### 7. ARQUITECTURA TÉCNICA

#### 7.1 Estructura de Carpetas
```
src/
├── models/         # Clases User, Survey, EmotionalProfile
├── services/       # Lógica de negocio (UserService, SurveyService)
├── utils/          # Helpers (csv_handler, validators)
├── routers/        # Controladores para peticiones HTTP
└── analysis/       # Scripts de análisis y visualización

data/
├── raw/            # Datos originales
├── processed/      # Datos limpios
└── exports/        # Reportes generados
```

#### 7.2 Tecnologías
- **Python 3.8+**: Lenguaje principal
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **Matplotlib/Seaborn**: Visualizaciones
- **CSV**: Almacenamiento temporal
- **fastAPI**: 

### 8. METODOLOGÍA DE DESARROLLO

#### 8.1 Control de Versiones
- **Git**: Sistema de control de versiones
- **GitHub**: Repositorio remoto
- **Branching**: main, feature/branches
- **Commits**: Mensajes descriptivos siguiendo convenciones

#### 8.2 Estándares de Calidad
- **PEP8**: Estilo de código Python
- **Modularidad**: Separación de responsabilidades
- **Documentación**: Docstrings en funciones y clases
- **Testing**: Pruebas unitarias básicas

### 9. CRONOGRAMA DE ENTREGAS

| Fase | Período | Entregables | Estado |
|------|---------|-------------|---------|
| **Segunda Entrega** | Sep 2025 | Fundamentos y versionado | ✅ En desarrollo |
| **Tercera Entrega** | Oct 2025 | Análisis y visualización | 📋 Planificado |
| **Presentación Final** | Nov 2025 | Proyecto completo | 📅 Pendiente |

### 10. CRITERIOS DE ÉXITO

#### 10.1 Técnicos
- [ ] Código funcional y sin errores
- [ ] Cumplimiento de estándares PEP8
- [ ] Documentación completa
- [ ] Control de versiones activo

#### 10.2 Funcionales
- [ ] Registro de usuarios operativo
- [ ] Encuestas funcionando correctamente
- [ ] Análisis de datos implementado
- [ ] Visualizaciones generadas

#### 10.3 Académicos
- [ ] Aplicación de conceptos aprendidos
- [ ] Demostración de habilidades técnicas
- [ ] Presentación profesional del proyecto

---

**Documento preparado por**: Anderson David Sepulveda Gomez  
**Fecha**: Septiembre 28, 2025  
**Versión**: 1.0