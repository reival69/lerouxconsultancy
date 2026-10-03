#!/usr/bin/env bash
# Instala lerouxconsultancy.com en un servidor Ubuntu nuevo (por ejemplo, en Clouding.io).
#
# Uso, como root en el servidor:
#   curl -fsSL https://raw.githubusercontent.com/reival69/lerouxconsultancy/main/deploy/clouding-setup.sh | bash
#
# Se puede volver a ejecutar sin problema: actualiza lo que ya existe.
# Opcional: EMAIL=tu@correo.com para recibir avisos de Let's Encrypt.
set -euo pipefail

DOMAIN="lerouxconsultancy.com"
REPO="https://github.com/reival69/lerouxconsultancy.git"
WEBROOT="/var/www/lerouxconsultancy"
SITE="/etc/nginx/sites-available/lerouxconsultancy"

if [ "$(id -u)" -ne 0 ]; then
  echo "Ejecuta este script como root (o con sudo)." >&2
  exit 1
fi

echo "==> Instalando paquetes"
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get upgrade -yq
apt-get install -yq nginx git certbot python3-certbot-nginx ufw dnsutils curl

echo "==> Firewall (SSH, HTTP y HTTPS)"
ufw allow OpenSSH >/dev/null
ufw allow 'Nginx Full' >/dev/null
ufw --force enable >/dev/null

echo "==> Descargando la página desde GitHub"
if [ -d "$WEBROOT/.git" ]; then
  git -C "$WEBROOT" pull -q
else
  git clone -q "$REPO" "$WEBROOT"
fi

echo "==> Configurando Nginx"
if [ ! -f "$SITE" ] || ! grep -q "listen 443" "$SITE"; then
  cat > "$SITE" <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;
    root $WEBROOT;
    index index.html;

    location / { try_files \$uri \$uri/ \$uri.html =404; }
    location ~ /\.git { deny all; }
    location ^~ /deploy/ { deny all; }
    location ~ \.(py|json|md|sh)\$ { deny all; }
    location ~* \.(css|js|svg|png|jpg|jpeg|webp|woff2?)\$ { expires 7d; }
}
NGINX
fi
ln -sf "$SITE" /etc/nginx/sites-enabled/lerouxconsultancy
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "==> Actualización automática desde GitHub cada 10 minutos"
CRON="*/10 * * * * cd $WEBROOT && git pull -q"
( crontab -l 2>/dev/null | grep -vF "$WEBROOT" || true; echo "$CRON" ) | crontab -

echo "==> HTTPS"
SERVER_IP="$(curl -4 -fsS https://ifconfig.me || true)"
DOMAIN_IPS="$(dig +short A "$DOMAIN"; dig +short A "www.$DOMAIN")"
if [ -n "$SERVER_IP" ] && [ "$(echo "$DOMAIN_IPS" | sort -u | grep -v '^$')" = "$SERVER_IP" ]; then
  if [ -n "${EMAIL:-}" ]; then
    certbot --nginx -n --agree-tos -m "$EMAIL" --redirect -d "$DOMAIN" -d "www.$DOMAIN"
  else
    certbot --nginx -n --agree-tos --register-unsafely-without-email --redirect -d "$DOMAIN" -d "www.$DOMAIN"
  fi
  echo "Listo: https://$DOMAIN"
else
  echo "El dominio todavía no apunta solo a este servidor ($SERVER_IP)."
  echo "Ahora apunta a: $(echo "$DOMAIN_IPS" | sort -u | tr '\n' ' ')"
  echo "En tu DNS pon: A @ -> $SERVER_IP y A www -> $SERVER_IP (borra los A viejos, no toques los MX)."
  echo "Cuando cambie, vuelve a ejecutar este script para activar HTTPS."
  echo "Mientras tanto la página se ve en: http://$SERVER_IP"
fi
