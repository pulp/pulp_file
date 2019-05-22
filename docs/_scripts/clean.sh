# Stop all pulp services
sudo systemctl stop pulp-content-app pulp-worker@1 pulp-worker@2 pulp-resource-manager pulp-api

# Reset the database (destructive!)
django-admin reset_db --noinput
django-admin migrate
django-admin reset-admin-password --password password

# Restart all pulp services
sudo systemctl restart pulp-content-app pulp-worker@1 pulp-worker@2 pulp-resource-manager pulp-api
