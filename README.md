## Creación del entorno virtual para ejecución

1. Tener una carpeta propia del proyecto
2. Ejecutar el comando
```python3.13 -m venv venv```

## Para poder instalar librerías del proyecto
Las librerías ya instaladas serán visibles en el archivo *requirements.txt*. Si necesitas instalar otra librería:

1. Activar el entorno virtual con:
   ```source venv/bin/activate```
3. Instalar las librerías necesarias
4. Guardar las nuevas librerías en el *txt* con:
   ```pip freeze > requirements.txt```

Si necesitan crear más carpetas, hacerlo sin problema.

Cada persona ya tiene su rama creada, favor de verificar que cada persona esté trabajando en su rama. Si hay 2 personas trabajando en la misma rama, al hacer *commit* el proyecto puede **explotar**. 

**Verificar que el commit se haga en su rama**

Miembro 1: Login y gestión de usuarios (CRUD).
Miembro 2: Gestión de dentistas (CRUD).
Miembro 3: Gestión de pacientes y citas.
Miembro 4: Elaboración y actualización de expedientes.
Miembro 5: Integración, menú principal y validaciones generales.
