# Leroux Consultancy

Sitio estático de lerouxconsultancy.com en español, inglés y sueco.

- Los textos están en `content.json`.
- Para regenerar las páginas (`index.html`, `en/`, `sv/`) después de cambiar textos: `python3 build.py`
- Estilos en `assets/styles.css`.

## Instalar en un servidor propio (Clouding.io u otro con Ubuntu)

Como root en un servidor Ubuntu 24.04 nuevo:

```bash
curl -fsSL https://raw.githubusercontent.com/reival69/lerouxconsultancy/main/deploy/clouding-setup.sh | EMAIL=tu@correo.com bash
```

El script instala Nginx, descarga la página, la actualiza desde GitHub cada 10 minutos
y activa HTTPS cuando el dominio ya apunta al servidor (si no, muestra qué registros DNS
cambiar; después se vuelve a ejecutar). No toca los registros MX del correo.
