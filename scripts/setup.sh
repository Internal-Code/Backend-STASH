#!/bin/bash
set -e

########################################
# USAGE
########################################
show_help() {
  echo "Usage: sh scripts/setup.sh --env <dev|stg|prod>"
  exit 1
}

########################################
# ARGUMENT PARSING
########################################
if [ "$1" != "--env" ] || [ -z "$2" ]; then
  show_help
fi

ENV="$2"

case "$ENV" in
dev)
  DOMAIN="dev.stash"
  PORT="7000"
  ;;
stg)
  DOMAIN="staging-stash"
  PORT="7100"
  ;;
prod)
  DOMAIN="stash"
  PORT="7200"
  ;;
*)
  show_help
  ;;
esac

########################################
# PATHS
########################################
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

SSL_DIR="/etc/ssl/localcerts"
CERT_FILE="$SSL_DIR/$DOMAIN.pem"
KEY_FILE="$SSL_DIR/$DOMAIN-key.pem"

CONF_BASENAME="$ENV-stash"
CONF_FILE="$CONF_BASENAME.conf"

########################################
# INFO
########################################
echo "======================================"
echo " Setting up STASH environment"
echo "--------------------------------------"
echo " Environment : $ENV"
echo " Domain      : $DOMAIN"
echo " Backend Port: $PORT"
echo "======================================"

########################################
# INSTALL DEPENDENCIES
########################################
sh "$SCRIPT_DIR/install_dependencies.sh"
sh "$SCRIPT_DIR/install_nginx.sh"

########################################
# SSL CREATION
########################################
create_ssl_cert() {
  if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
    echo "SSL already exists for $DOMAIN"
    return
  fi

  echo "Creating SSL certificate for $DOMAIN..."

  sudo mkdir -p "$SSL_DIR"

  sudo openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout "$KEY_FILE" \
    -out "$CERT_FILE" \
    -subj "/C=ID/ST=Jakarta/L=Jakarta/O=STASH/OU=Backend/CN=$DOMAIN"

  sudo chmod 600 "$KEY_FILE"
  sudo chmod 644 "$CERT_FILE"

  echo "SSL created:"
  echo "  - $CERT_FILE"
  echo "  - $KEY_FILE"
}

create_ssl_cert

########################################
# NGINX CONFIG
########################################
echo "Creating Nginx config..."

sudo tee "$NGINX_AVAILABLE/$CONF_FILE" > /dev/null <<EOF
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;

    ssl_certificate     $CERT_FILE;
    ssl_certificate_key $KEY_FILE;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/$CONF_BASENAME.access.log;
    error_log  /var/log/nginx/$CONF_BASENAME.error.log;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
EOF

########################################
# ENABLE SITE
########################################
if [ ! -L "$NGINX_ENABLED/$CONF_FILE" ]; then
  sudo ln -s "$NGINX_AVAILABLE/$CONF_FILE" "$NGINX_ENABLED/$CONF_FILE"
fi

########################################
# TEST & RELOAD
########################################
sudo nginx -t
sudo systemctl reload nginx || sudo nginx -s reload

########################################
# DONE
########################################
echo "======================================"
echo " Setup complete"
echo " URL: https://$DOMAIN"
echo "======================================"
