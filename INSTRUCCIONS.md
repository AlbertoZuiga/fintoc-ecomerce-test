# Pepestore – Fintoc Hackathon

Leer el enunciado y responder preguntas: 10 minutos

Desarrollar: 2 horas

Demos: 30 minutos (2 minutos por persona)

> Puedes usar IA para el desarrollo de tu app
> 
- Revisar la documentación de Fintoc con anticipación
- Traer computador con un ambiente para programar listo

## Problema

<aside>
💡

En Fintoc compramos ~~monsters~~ snacks y bebidas con la [*Pepestore*](https://pepestore.fintoc.com/), nuestra propia tienda interna que usa nuestro producto de pagos.

Para esta prueba, queremos que **tú diseñes y construyas tu propia versión de una Pepestore**, partiendo desde cero: catálogo de productos, carrito y flujo de pago con cuenta bancaria usando Fintoc Payments.

</aside>

El “problema” que queremos resolver con este ejercicio es:

- Ver cómo modelas y construyes rápidamente un mini e-commerce que use **Fintoc Payments** en modo sandbox.
- Entender cómo diseñas el flujo completo de la aplicación: desde la experiencia de compra hasta la integración con la API de Fintoc y el deploy.
- Tener un ejemplo tuyo, aunque sea simple, que podría vivir como una Pepestore alternativa para explicar el producto y jugar con él.

La idea no es replicar pixel-perfect la Pepestore actual, sino que **propongas y construyas tu propia versión**, tomando la Pepestore real solo como inspiración.

---

## Objetivo

<aside>
🎯

Construir una **Pepestore**: un mini e-commerce donde las personas puedan “comprar” snacks y bebidas pagando con su cuenta bancaria, usando **Fintoc Payments en sandbox**, y que esté deployeado en una URL pública.

</aside>

En el contexto de esta prueba técnica:

- Tienes **2 horas** para:
    - Diseñar la solución técnica que creas más razonable.
    - Implementar una versión funcional del flujo principal.
    - Deployearlo en algún servicio.

---

## Métricas de Éxito

<aside>
🎖️

Para esta prueba, las métricas son más cualitativas que cuantitativas, pero igual queremos que pienses en “éxito” de forma concreta.

</aside>

- Al menos **1 flujo de compra completo** (seleccionar producto → iniciar pago con Fintoc → ver resultado).
- Tu tienda **debe estar disponible en una URL pública** al final de la prueba.
- El flujo de usuario es entendible sin explicaciones externas (qué estoy comprando, cuánto pago, qué pasó con mi pago).

---

## Solución

<aside>
⭐

Queremos construir una **Pepestore** simple: un catálogo de productos (snacks/bebidas), un carrito y un checkout que use **Fintoc Payments** para cobrar.

</aside>

A nivel conceptual, la solución debería incluir:

- Una **tienda web** donde:
    - Se vea un listado de productos (nombre, precio, etc.).
    - Se puedan agregar productos a un carrito.
    - Se pueda ir a una pantalla de checkout y “pagar con Fintoc”.
- Una **capa de lógica de negocio e integración con Fintoc** que:
    - Modele los productos y las órdenes.
    - Se integre con **Fintoc Payment Initiation** para iniciar el pago (por ejemplo, usando los recursos/documentación de Checkout Sessions u otros que estimes razonables).
    - Exponga las operaciones necesarias para que la tienda pueda:
        - Obtener productos.
        - Crear/iniciar un pago a partir del carrito.
        - (Opcional) Consultar o simular el estado de una orden o pago.
- Un **deploy mínimo**:
    - La Pepestore debe estar disponible en una **URL pública.**

### Alcance de esta prueba

- Puedes usar el **stack que quieras.**
- Debes usar **Fintoc Payments en modo test** siguiendo la [documentación de Payment Initiation](https://docs.fintoc.com/docs/overview-payment-initiation#/).
- La forma en que estructures tu código, nombres tus rutas/operaciones y organices el proyecto es decisión tuya, siempre que:
    - El flujo Pepestore → carrito → pago con Fintoc → resultado sea entendible.
    - Dejes en el `README` una breve descripción de cómo está armada tu solución.

---

## Key Features: Widget / UX de pago

<aside>
📄

Esta sección describe la experiencia de pago desde el punto de vista del usuario final.

</aside>

Desde la mirada de quien compra en la Pepestore:

- **Botón de “Pagar con Fintoc”**
    - En la pantalla de checkout debe haber una acción clara para pagar usando cuenta bancaria.
    - Al hacer click, se debe iniciar el flujo de pago usando Fintoc Payments (por ejemplo, un widget o una redirección, según decidas con la doc).
- **Flujo de pago**
    - El usuario debe ver una experiencia que le permita seleccionar su banco, autenticarse y autorizar el pago.
    - Este flujo se apoya completamente en **Fintoc Payment Initiation**, como está documentado.
- **Estados de resultado**
    - Si el pago se completa exitosamente, el usuario debería ver un feedback claro (ej. “Pago recibido 🎉”).
    - Si el pago se cancela o falla, el usuario debería ver un mensaje coherente (ej. “El pago fue cancelado o falló 😢”).
    - Cómo conectas estos estados (callbacks, redirecciones, etc.) queda a tu criterio, mientras se base en la documentación de Fintoc.

---

## Scope

<aside>
🙅

Es igual de importante decir qué NO vamos a construir.

</aside>

Fuera del alcance de esta prueba (no lo esperamos en 2 horas):

- Sistema de autenticación de usuarios (login, roles, etc.).
- Dashboard de administración completo (dashboard interno) para gestionar productos o órdenes. Puedes asumir un set de productos finito.
- Flujos complejos de reintentos de pago, devoluciones (refunds), conciliación contable, etc.

Puedes implementar nuevos features si alcanzas, pero como **bonus**. Debes dejar documentado en el readme los extras y por qué los hiciste.

---

## Core UX Flows

<aside>
🖋️

Aquí describimos los flujos mínimos que debería soportar la Pepestore.

</aside>

### Flujo 1: Navegar catálogo y armar carrito

1. El usuario entra a la Pepestore (URL pública).
2. Ve un listado de productos (ej. snacks y bebidas con sus precios).
3. Puede agregar uno o varios productos a un carrito.
4. Puede ver el resumen del carrito (productos, cantidad, total).

### Flujo 2: Checkout y pago con Fintoc

1. Desde el carrito, el usuario va a una pantalla de checkout.
2. Revisa el detalle de su compra (productos + total a pagar).
3. Hace click en “Pagar con Fintoc” (o similar).
4. Se abre el flujo de pago de Fintoc (widget o redirect).
5. El usuario termina el flujo de Fintoc:
    - Si es exitoso, vuelve a tu app o recibe feedback de éxito.
    - Si cancela o falla, vuelve a tu app o recibe feedback de error/cancelación.
6. Tu app muestra el estado final de la compra (ej. pantalla de “gracias” o “hubo un problema”).

---

## Riesgos

<aside>
🚨

Qué podría salir mal y qué harías si pasa, incluso en este contexto de prueba rápida.

</aside>

Algunos riesgos obvios en este ejercicio:

- **Tiempo limitado (2 horas)**
    - Podrías quedarte a medias entre “solución perfecta” y “solución funcional”.
    - Mitigación: prioriza el flujo principal (catálogo → carrito → pago → feedback) y deja comentarios o TODOs para mejoras.
- **Dudas con la doc de Fintoc o con el flujo de Payment Initiation**
    - Mitigación: elige un camino sencillo dentro de la doc y apégate a él; documenta en el README las decisiones que tomaste.
- **Problemas con el deploy / plataforma elegida**
    - Mitigación: elige herramientas que conozcas o que sean muy simples; si se cae el deploy, deja instrucciones claras para correrlo localmente.

---

## Shipping it

<aside>
🚢

Para efectos de esta prueba, “lanzar” la Pepestore significa tener algo que podamos abrir y usar.

</aside>

Lo que esperamos al final de las 2 horas:

- Una **URL pública** donde podamos:
    - Ver el catálogo.
    - Armar un carrito.
    - Pagar con Fintoc en el sandbox.
- Un **repositorio (GitHub, etc.)** con:
    - El código de tu app
    - Un `README` con:
        - Cómo correr el proyecto localmente.
        - Qué stack usaste.
        - Dónde configurar las variables de entorno de Fintoc.