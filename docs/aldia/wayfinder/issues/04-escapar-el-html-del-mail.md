# Escapar el HTML del mail

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: S
Archivos:
- `backend/app/services/email_generator.py`
- `backend/app/templates/mail_cobro.html`
- `backend/tests/test_email_generator.py`

## Decisión cerrada

El nombre del Excel no puede inyectar HTML en el mail. Entra ahora, en la capa 1.

## Resultado

Nombre, localidad y clave salen como texto. El mail manda el header de baja en un clic, sin aplicar la baja en el GET.

## Criterios de aceptación

- Jinja usa `autoescape=True`. `|safe` queda solo para el cuerpo cuyas variables ya se escaparon.
- `color_primario` cumple `^#[0-9A-Fa-f]{6}$`. `logo_url` solo `https`.
- Un test con `</p><a href=...>` en el nombre no deja el tag en el HTML enviado.
- El mail incluye `List-Unsubscribe` y `List-Unsubscribe-Post: List-Unsubscribe=One-Click`. La página y el POST que aplican la baja son Baja por POST. Este ticket no edita el router.
- No se loguea el token.

## Pregunta

¿Cómo se impide que un nombre del Excel inyecte HTML en el mail?
