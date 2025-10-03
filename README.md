# Selenium ChromeDriver Backend

Este es el servidor Python que ejecuta Selenium y ChromeDriver para la aplicación web.

## Opción 1: Railway.app (Recomendado)

### Pasos:

1. **Crear cuenta en Railway.app**
   - Ve a https://railway.app/
   - Regístrate con GitHub

2. **Crear nuevo proyecto**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio

3. **Configurar el servicio**
   - Railway detectará automáticamente el Dockerfile
   - El proyecto se desplegará automáticamente

4. **Obtener la URL del servicio**
   - Una vez desplegado, Railway te dará una URL como: `https://tu-proyecto.railway.app`
   - Copia esta URL

5. **Configurar en Supabase**
   - Ve a tu proyecto de Supabase
   - Settings → Edge Functions → Secrets
   - Agrega: `PYTHON_BACKEND_URL` = `https://tu-proyecto.railway.app`

## Opción 2: Render.com (Gratis)

### Pasos:

1. **Crear cuenta en Render.com**
   - Ve a https://render.com/
   - Regístrate con GitHub

2. **Crear nuevo Web Service**
   - Click en "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub

3. **Configurar el servicio**
   - Name: `selenium-backend`
   - Environment: `Docker`
   - Dockerfile Path: `./python-backend/Dockerfile`
   - Plan: Free

4. **Deploy**
   - Click en "Create Web Service"
   - Espera a que se complete el deployment

5. **Obtener la URL**
   - Render te dará una URL como: `https://selenium-backend-xxxx.onrender.com`

6. **Configurar en Supabase**
   - Ve a tu proyecto de Supabase
   - Settings → Edge Functions → Secrets
   - Agrega: `PYTHON_BACKEND_URL` = `https://selenium-backend-xxxx.onrender.com`

## Opción 3: Ejecutar localmente (Para pruebas)

### Requisitos:
- Python 3.11+
- Chrome instalado

### Pasos:

```bash
cd python-backend

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

El servidor estará disponible en `http://localhost:8080`

Para usarlo localmente, configura en tu `.env`:
```
PYTHON_BACKEND_URL=http://localhost:8080
```

## Comandos soportados

El backend soporta los siguientes comandos de Selenium:

- `driver.get("url")` - Navegar a una URL
- `driver.title` - Obtener el título de la página
- `driver.current_url` - Obtener la URL actual
- `driver.page_source` - Obtener el HTML de la página
- `driver.back()` - Ir hacia atrás
- `driver.forward()` - Ir hacia adelante
- `driver.refresh()` - Recargar la página
- `driver.find_element(By.NAME, "q").send_keys("texto")` - Buscar elemento y escribir
- `driver.find_element(By.ID, "id").click()` - Buscar elemento y hacer click
- `driver.find_element(By.XPATH, "//button").text` - Obtener texto de elemento
- `driver.execute_script("return document.title")` - Ejecutar JavaScript

## Estructura de archivos

```
python-backend/
├── app.py              # Servidor Flask principal
├── requirements.txt    # Dependencias Python
├── Dockerfile         # Configuración Docker
├── railway.json       # Configuración Railway
├── render.yaml        # Configuración Render
└── README.md          # Esta documentación
```

## Troubleshooting

### Error: "Chrome binary not found"
- Asegúrate de que Chrome esté instalado en el servidor
- En Railway/Render, el Dockerfile instala Chrome automáticamente

### Error: "Session not found"
- Las sesiones se crean automáticamente cuando ejecutas el primer comando
- Si cierras una sesión en el frontend, se eliminará del backend

### El servidor no responde
- Verifica que la URL del backend esté correctamente configurada en Supabase
- Revisa los logs en Railway/Render para ver errores

## Seguridad

- Este servidor solo debe ser accedido a través de la Edge Function de Supabase
- No expongas directamente la URL del backend Python a usuarios
- Considera agregar autenticación adicional si es necesario
