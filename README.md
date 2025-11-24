Pepestore (mini e-commerce)

https://fintoc-ecomerce-app.onrender.com

Pequeña Pepestore creada como ejercicio de integración con Fintoc Payments (modo sandbox).

Características

- Catálogo de productos (snacks/bebidas).
- Carrito de compras básico.
- Checkout que inicia un pago (integración pensada para Fintoc Payments sandbox).
- Deploy previsto en Render (configurable con Gunicorn).

Requisitos

- Python 3.12.x
- Dependencias en `requirements.txt` (Flask, Flask-Login, Flask-SQLAlchemy, google-auth, gunicorn, etc.)

Instalación local

1. Clona el repositorio:

```bash
git clone https://github.com/AlbertoZuiga/fintoc-ecomerce-test
cd fintoc-ecomerce-test
```

2. Crea y activa un virtualenv (macOS/zsh):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Variables de entorno (recomendado: crear un `.env` con los valores):

- `DATABASE_URI` o las variables `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME`.
- `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` (para login con Google).
- `SECRET_KEY` (cadena larga y secreta — necesaria para persistencia de sesión).
- `URL` (opcional, usado para callbacks de OAuth).

Ejemplo `.env` mínimo para desarrollo:

```
DATABASE_URI=mysql+pymysql://user:pass@localhost/fintoc_ecomerce_db
SECRET_KEY=una_clave_larga_y_secreta
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
URL=http://localhost:5050
```

4. Crear la base de datos y poblar seed (opcional si ya existen migraciones):

```bash
python -m app.db.drop && python -m app.db.setup
```

5. Ejecutar la app en desarrollo:

```bash
python run.py
# o con gunicorn localmente
gunicorn run:app
```

Uso

- Accede a `/products` para ver el catálogo.
- En la página de producto pulsa "Agregar al carrito" para añadir items.
- Visita `/cart` para ver el carrito y `/orders` para ver compras pasadas.

Deploy en Render

- Comando de inicio recomendado en Render: `gunicorn run:app` (el módulo `run` exporta `app`).
- Variables de entorno importantes en Render:
  - `DATABASE_URI` (o las variables separadas de DB).
  - `SECRET_KEY` (obligatorio para cookies persistentes y `remember` de Flask-Login).
  - `RUN_CREATE_ALL` = `true` si quieres que la app cree tablas automáticamente durante deploy (no recomendado en producción).

Notas sobre seguridad y producción

- No guardes `SECRET_KEY` en el repositorio. Usa las Environment Variables del servicio (Render, Heroku, etc.).
- En producción usa migraciones en lugar de `create_all()` para cambios en el esquema.

Fintoc Payments

- El proyecto está preparado para integrar Fintoc Payments (sandbox). Lee `INSTRUCCIONS.md` para el objetivo de la prueba.
- Añade las credenciales y sigue la documentación de Fintoc para crear sesiones de pago desde el servidor.

Mejoras posibles

- Asociar `Order` a `User` para soportar carritos por usuario.
- Mostrar y actualizar el contador del carrito en la navbar.
- Añadir endpoints para editar cantidades / eliminar items del carrito.

Contacto

- Si necesitas que haga el deploy o ajuste variables en tu servicio, dime y te guío o aplico los cambios.
