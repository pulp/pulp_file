#!/usr/bin/env bash
set -e

echo "Setting environment variables for default hostname/port for the API and the Content app"
export BASE_ADDR=${BASE_ADDR:-http://localhost:24817}

if [ -z "$(pip freeze | grep pulp-cli)" ]; then
  echo "Installing pulp-cli"
  pip install pulp-cli[pygments]
fi

if [ ! -f ~/.config/pulp/settings.toml ]; then
  echo "Configuring pulp-cli"
  mkdir ~/.config/pulp
  cat > ~/.config/pulp/settings.toml << EOF
[cli]
base_url = "$BASE_ADDR"
verify_ssl = false
format = "json"
EOF
fi
