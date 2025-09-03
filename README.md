# Portafolio Profesional de Data Analyst

Una aplicación web profesional desarrollada en Django para mostrar el portafolio de un Analista de Datos. El proyecto incluye un sistema completo de gestión de proyectos, perfil profesional, autenticación de usuarios y un panel de administración.

## 🚀 Características Principales

### 📊 Gestión de Proyectos
- **Proyectos Destacados**: Muestra proyectos en tarjetas con scroll horizontal
- **Filtros por Categoría**: BI, Python, Machine Learning, SQL, Data Analysis, ETL
- **Buscador**: Búsqueda por palabra clave en proyectos
- **Sistema de Votos**: Likes/dislikes por usuario único
- **Comentarios**: Sistema de comentarios para usuarios registrados
- **Archivos Adjuntos**: Soporte para PDF, Excel, CSV por proyecto
- **Tecnologías**: Etiquetas de tecnologías utilizadas

### 👤 Perfil Profesional
- **Página "Sobre Mí"**: Perfil tipo LinkedIn editable
- **Experiencia Laboral**: Gestión completa de experiencias profesionales
- **Certificaciones**: Sistema de certificaciones con fechas y organizaciones
- **Habilidades**: Badges de tecnologías dominadas con niveles de experiencia

### 🔐 Autenticación y Permisos
- **Sistema de Login/Register**: Autenticación completa de usuarios
- **Permisos Granulares**: Solo superusuarios pueden crear/editar proyectos
- **Usuarios Normales**: Pueden comentar y votar proyectos

### 🎨 Diseño UI/UX
- **Diseño Profesional**: Colores claros (blanco, gris profesional, negro)
- **Responsive**: Layout adaptativo para todos los dispositivos
- **Bootstrap 5**: Framework CSS moderno
- **Font Awesome**: Iconografía profesional

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2+
- **Base de Datos**: SQLite3 (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Iconos**: Font Awesome
- **Fuentes**: Google Fonts

## 📦 Instalación

### Prerrequisitos
- Python 3.8+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd nuevo-portafolio
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Agregar datos de ejemplo (opcional)**
```bash
python add_sample_data.py
```

8. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

## 🔧 Configuración

### Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuración de Archivos Media
El proyecto está configurado para servir archivos media en desarrollo. Para producción, configurar un servidor web como Nginx.

## 📁 Estructura del Proyecto

```
nuevo-portafolio/
├── portfolio_project/          # Configuración principal de Django
├── portfolio_projects/         # App de gestión de proyectos
├── core/                      # App principal (perfil, experiencia, etc.)
├── auth_users/                # App de autenticación
├── templates/                 # Templates HTML
├── static/                    # Archivos estáticos (CSS, JS, imágenes)
├── media/                     # Archivos subidos por usuarios
├── add_sample_data.py         # Script para datos de ejemplo
└── README.md                  # Este archivo
```

## 🎯 Funcionalidades por Usuario

### 👤 Usuario No Autenticado
- Ver página de inicio con proyectos destacados
- Explorar todos los proyectos
- Filtrar proyectos por categoría
- Buscar proyectos
- Ver página "Sobre Mí"
- Registrarse/Iniciar sesión

### 👤 Usuario Registrado
- Todas las funcionalidades de usuario no autenticado
- Comentar proyectos
- Votar (like/dislike) proyectos
- Ver perfil personal

### 🔧 Superusuario (Admin)
- Todas las funcionalidades de usuario registrado
- Crear, editar y eliminar proyectos
- Gestionar perfil profesional
- Agregar/editar experiencias laborales
- Gestionar certificaciones
- Acceso completo al panel de administración

## 🎨 Personalización

### Colores y Estilo
Los colores principales están definidos en `static/css/style.css`:
- **Primario**: `#007bff` (azul Bootstrap)
- **Secundario**: `#6c757d` (gris profesional)
- **Fondo**: `#ffffff` (blanco)
- **Texto**: `#212529` (negro)

### Agregar Nuevas Categorías
1. Ir al panel de administración
2. Navegar a "Categories"
3. Agregar nueva categoría con slug único

### Agregar Nuevas Tecnologías
1. Ir al panel de administración
2. Navegar a "Technologies"
3. Agregar nueva tecnología

## 📊 Datos de Ejemplo

El script `add_sample_data.py` incluye:

### Proyectos de Ejemplo
- Análisis de Ventas E-commerce
- Dashboard de KPIs Empresariales
- Sistema de Recomendación de Productos
- ETL Pipeline para Datos de Redes Sociales
- Análisis de Sentimientos en Tiempo Real

### Perfil de Ejemplo
- Información profesional completa
- 3 experiencias laborales
- 3 certificaciones
- 10 habilidades técnicas

## 🔒 Seguridad

- **CSRF Protection**: Habilitado en todos los formularios
- **XSS Protection**: Django incluye protección automática
- **SQL Injection**: Protegido por ORM de Django
- **File Upload**: Validación de tipos de archivo
- **Authentication**: Sistema robusto de Django

## 🚀 Despliegue

### Para Producción
1. Configurar `DEBUG=False`
2. Usar base de datos PostgreSQL
3. Configurar servidor web (Nginx/Apache)
4. Configurar archivos estáticos
5. Usar variables de entorno para secretos

### Recomendaciones
- Usar HTTPS en producción
- Configurar backup de base de datos
- Monitorear logs de errores
- Optimizar consultas de base de datos

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en el repositorio
- Contactar al desarrollador principal

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] Sistema de notificaciones
- [ ] API REST para integración externa
- [ ] Sistema de tags avanzado
- [ ] Analytics de visitas
- [ ] Exportación de datos
- [ ] Integración con LinkedIn
- [ ] Sistema de portafolios múltiples

---

**Desarrollado con ❤️ usando Django** 