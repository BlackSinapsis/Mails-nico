# Owner y repo privado vacío

Type: task
Modo: HITL
Status: humano
Blocked by: 
Fase: 1 · Integridad
Tamaño: S
Archivos:
- (ninguno)

## Decisión cerrada

La org [OrderByte01](https://github.com/OrderByte01) ya existe. Los dos figuran en People. El producto se llama Aldia, sin tilde. El siguiente paso es confirmar la etiqueta Owner en los dos y crear [OrderByte01/aldia](https://github.com/OrderByte01/aldia), privado, vacío y sin ser un fork. No se pushea. No se toca `Juanrocod/Mails-nico`. No se renombra el código de la app.

## Resultado

Julián confirma Owner y crea el repo vacío. Juan confirma que su fila dice Owner. El código sigue donde está.

## Criterios de aceptación

- En People, Julián y Juanrocod tienen la etiqueta Owner. Owner es el admin. GitHub no tiene rol Admin. Ninguno queda como Member.
- Los dos entran con su cuenta personal.
- El repo es `aldia`, Private, sin README, sin .gitignore y sin license. La URL es https://github.com/OrderByte01/aldia. No es un fork. No se importa `Juanrocod/Mails-nico` ni `BlackSinapsis/Mails-nico`.
- No hay push.
- Los deploys de Render y Cloudflare siguen apuntando a `Juanrocod/Mails-nico`.
- Un agente no lo toma. Los clics están en la lista.

## Pregunta

¿La org tiene a los dos como Owner, y existe https://github.com/OrderByte01/aldia vacío, sin código y sin ser un fork?
