# Etiquetas, foco y estado visible

Type: task
Modo: AFK
Status: open
Blocked by: 
Fase: 1 · Integridad
Tamaño: M
Archivos:
- `frontend/src/pages/LoginPage.tsx`
- `frontend/index.html`
- `frontend/src/lib/estado.ts`
- `frontend/src/components/layout/Sidebar.tsx`
- `frontend/package.json`
- `frontend/package-lock.json`

## Decisión cerrada

Entran ahora las etiquetas, el foco visible y el estado con punto y texto. El login es el primer formulario con reglas: Zod y React Hook Form, los dos MIT. El modo oscuro y el shell nuevo son Rediseño visual y modo oscuro.

## Resultado

El login tiene etiquetas, se puede pegar la clave, y un estado no se entiende solo por el color.

## Criterios de aceptación

- Usuario y contraseña tienen `<label>` visible, `autocomplete="username"` y `autocomplete="current-password"`. El error usa `role="alert"` y no dice cuál de los dos falló.
- Después de entrar se llega al dashboard.
- `lang="es-AR"` y el título visible dice Aldia, sin tilde. Hoy la barra dice «Mails Nico»; este ticket lo cambia cuando se tome. No se renombra el repo de la app ni se pushea.
- El estado es punto más texto, con el diccionario de `lib/estado.ts`.
- El anillo de foco no queda debajo de la barra. En 390 px de ancho el foco de la barra se puede ver.
- Zod valida el login en el cliente. El servidor sigue siendo la autoridad. No se migran el resto de los formularios.
- `package.json` es de este ticket hasta que cierre. Sentry y la tabla densa esperan.

## Pregunta

¿Qué tiene que poder hacer el operador con teclado, sin adivinar un estado por el color?
