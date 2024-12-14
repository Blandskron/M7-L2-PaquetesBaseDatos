# Proyecto Django con PostgreSQL y ORM Avanzado

Este proyecto tiene como objetivo demostrar el uso de Django con PostgreSQL como base de datos principal. Incluye la configuración del entorno, creación de modelos, migraciones, consultas avanzadas utilizando el ORM de Django y carga de datos inicial desde el shell interactivo.

## Tecnologías utilizadas

- **Django**: Framework web en Python.
- **PostgreSQL**: Base de datos relacional.

## Configuración inicial

1. **Crear el proyecto Django**

   Ejecuta los siguientes comandos para configurar el proyecto y la aplicación:
   ```bash
   django-admin startproject my_project
   cd my_project
   python manage.py startapp my_app
   ```

2. **Instalar el conector para PostgreSQL**

   Instala el paquete `psycopg2` para conectar Django con PostgreSQL:
   ```bash
   pip install psycopg2
   ```

3. **Configurar la base de datos**

   En el archivo `my_project/settings.py`, configura PostgreSQL como el motor de base de datos:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'my_database',
           'USER': 'my_user',
           'PASSWORD': 'my_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## Creación de modelos

En el archivo `my_app/models.py`, define los modelos para gestionar usuarios y productos:
```python
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country_iso = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

## Migraciones

1. **Crear y aplicar migraciones**

   Ejecuta los siguientes comandos para reflejar los modelos en la base de datos:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Comandos adicionales para gestionar migraciones**

   - Mostrar el estado de las migraciones:
     ```bash
     python manage.py showmigrations
     ```
   - Ver las instrucciones SQL generadas:
     ```bash
     python manage.py sqlmigrate my_app 0001
     ```

## Consultas avanzadas con el ORM

1. **Filtrar registros con `filter`**
   ```python
   users_from_canada = User.objects.filter(country_iso="CAN")
   ```

2. **Excluir registros con `exclude`**
   ```python
   non_mexican_users = User.objects.exclude(country_iso="MEX")
   ```

3. **Combinar filtros**
   ```python
   recent_users = User.objects.filter(created_at__year=2022).exclude(email="")
   ```

4. **Obtener un solo registro con `get`**
   ```python
   specific_user = User.objects.get(email="example@example.com")
   ```

5. **Manejo de excepciones**
   ```python
   from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

   try:
       user = User.objects.get(email="example@example.com")
   except ObjectDoesNotExist:
       print("User not found!")
   except MultipleObjectsReturned:
       print("Multiple users found!")
   ```

## Vistas

En el archivo `my_app/views.py`, define vistas para manejar datos:
```python
from django.shortcuts import render
from .models import User, Product

def list_users(request):
    users = User.objects.all()
    return render(request, 'list_users.html', {'users': users})

def products_in_stock(request):
    products = Product.objects.filter(stock__gt=0)
    return render(request, 'products.html', {'products': products})
```

## Configuración de URLs

En el archivo `my_project/urls.py`, registra las rutas para las vistas:
```python
from django.contrib import admin
from django.urls import path
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.list_users, name='list_users'),
    path('products/', views.products_in_stock, name='products_in_stock'),
]
```

## Plantillas HTML

**list_users.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>List of Users</title>
</head>
<body>
    <h1>Users</h1>
    <ul>
        {% for user in users %}
            <li>{{ user.first_name }} {{ user.last_name }} - {{ user.email }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

**products.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Products In Stock</title>
</head>
<body>
    <h1>Available Products</h1>
    <ul>
        {% for product in products %}
            <li>{{ product.name }} - ${{ product.price }} (Stock: {{ product.stock }})</li>
        {% endfor %}
    </ul>
</body>
</html>
```

## Carga de información desde el shell de Django

1. **Abrir el shell de Django**
   ```bash
   python manage.py shell
   ```

2. **Cargar datos iniciales**
   ```python
   from my_app.models import User, Product
   from datetime import datetime

   # Crear usuarios
   User.objects.create(first_name="Alice", last_name="Johnson", email="alice@example.com", country_iso="USA", created_at=datetime(2023, 12, 14))
   User.objects.create(first_name="Bob", last_name="Smith", email="bob@example.com", country_iso="CAN", created_at=datetime(2023, 12, 13))
   User.objects.create(first_name="Carlos", last_name="Lopez", email="carlos@example.com", country_iso="MEX", created_at=datetime(2023, 12, 12))

   # Crear productos
   Product.objects.create(name="Laptop", price=1200.00, stock=10, created_at=datetime(2023, 12, 14))
   Product.objects.create(name="Smartphone", price=800.00, stock=25, created_at=datetime(2023, 12, 13))
   Product.objects.create(name="Headphones", price=150.00, stock=0, created_at=datetime(2023, 12, 12))
   ```

3. **Verificar los datos cargados**
   ```python
   for user in User.objects.all():
       print(user)

   for product in Product.objects.all():
       print(product)
   ```

## Ejecutar el servidor

Para iniciar el servidor y probar el proyecto:
```bash
python manage.py runserver
```

Rutas disponibles:
- **Usuarios:** [http://localhost:8000/users/](http://localhost:8000/users/)
- **Productos en stock:** [http://localhost:8000/products/](http://localhost:8000/products/)

## Conclusión

Este proyecto demuestra:
1. Configuración de Django con PostgreSQL.
2. Gestión de migraciones y creación de modelos.
3. Consultas avanzadas utilizando el ORM de Django.
4. Carga inicial de datos mediante el shell interactivo.

Es ideal para comprender los conceptos clave de Django y construir aplicaciones escalables. Si tienes dudas, ¡no dudes en preguntar!

