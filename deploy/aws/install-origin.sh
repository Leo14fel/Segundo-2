#!/usr/bin/env bash
set -euo pipefail

# Run as root from the unpacked SinapUML AWS deployment bundle on Ubuntu 24.04.
if [[ ${EUID} -ne 0 ]]; then
  echo "Run with sudo: sudo bash ./install-origin.sh" >&2
  exit 1
fi

BUNDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

apt-get update
apt-get install -y openjdk-21-jre-headless nginx

if ! id sinapuml >/dev/null 2>&1; then
  useradd --system --home /opt/sinapuml --shell /usr/sbin/nologin sinapuml
fi

install -d -o sinapuml -g sinapuml /opt/sinapuml/app /opt/sinapuml/data /opt/sinapuml/whisper/models
install -d -o root -g root /var/www/sinapuml /etc/sinapuml

install -o sinapuml -g sinapuml -m 0644 "$BUNDLE_DIR/sinapuml.jar" /opt/sinapuml/app/sinapuml.jar
rm -rf /var/www/sinapuml/*
cp -a "$BUNDLE_DIR/frontend/." /var/www/sinapuml/
chown -R root:root /var/www/sinapuml

if [[ ! -f /etc/nginx/sites-available/sinapuml ]]; then
  install -m 0644 "$BUNDLE_DIR/nginx/sinapuml.conf" /etc/nginx/sites-available/sinapuml
else
  echo "Preserving existing /etc/nginx/sites-available/sinapuml (for example, direct HTTPS/TLS configuration)."
fi
ln -sfn /etc/nginx/sites-available/sinapuml /etc/nginx/sites-enabled/sinapuml
rm -f /etc/nginx/sites-enabled/default

install -m 0644 "$BUNDLE_DIR/systemd/sinapuml.service" /etc/systemd/system/sinapuml.service
install -m 0644 "$BUNDLE_DIR/systemd/sinapuml-whisper.service" /etc/systemd/system/sinapuml-whisper.service

if [[ ! -f /etc/sinapuml/sinapuml.env ]]; then
  install -m 0600 "$BUNDLE_DIR/sinapuml.env.example" /etc/sinapuml/sinapuml.env
  echo "Created /etc/sinapuml/sinapuml.env. Edit CHANGE_ME before starting SinapUML." >&2
else
  chmod 0600 /etc/sinapuml/sinapuml.env
fi

nginx -t
systemctl daemon-reload
systemctl enable nginx sinapuml sinapuml-whisper
systemctl restart nginx

cat <<'MSG'
Origin files installed.

Before starting the application:
  1. Edit /etc/sinapuml/sinapuml.env (JWT secret + exact CloudFront origin when known).
  2. Configure SINAPUML_MONGODB_URI with a MongoDB replica set (for example Atlas).
     Standalone MongoDB is insufficient for project/audit transactions.
  3. Install Whisper reproducibly: sudo bash ./install-whisper.sh
     (or place a known-good whisper-server + ggml-base.bin in /opt/sinapuml/whisper).
  4. Attach the EC2 IAM role that can invoke Bedrock.
  5. Run: systemctl restart sinapuml-whisper sinapuml
  6. Check: systemctl status sinapuml-whisper sinapuml --no-pager
MSG
