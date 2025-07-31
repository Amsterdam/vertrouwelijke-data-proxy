# Vertrouwelijke Data Proxy

Proxy service and token-based authorization for bulk data downloads with a confidential nature.
At the moment we only export data that is accessible to all employees of the City of Amsterdam,
and this scope level is hardcoded.

## Installation

Requirements:

* Python >= 3.12
* Recommended: Docker/Docker Compose (or pyenv for local installs)

### Using Docker Compose

Run docker compose:
```shell
docker compose up
```

Navigate to `localhost:8098`.

### Using Local Python

Create a virtualenv:

```shell
python3 -m venv venv
source venv/bin/activate
```

Install all packages in it:
```shell
pip install -U wheel pip
cd src/
make install  # installs src/requirements_dev.txt
```

Set the required environment variables and start the Django application:
```shell
export PUB_JWKS="$(cat jwks_test.json)"
export DJANGO_DEBUG=true
export AZURE_SEARCH_BASE_URL={AZURE_SEARCH_API_KEY}
export AZURE_SEARCH_API_KEY={AZURE_SEARCH_API_KEY}
export DSO_API_BASE_URL={DSO_API_BASE_URL}

./manage.py runserver localhost:8000
```

## Environment Settings

The following environment variables are useful for configuring a local development environment:

* `DJANGO_DEBUG` to enable debugging (true/false).
* `LOG_LEVEL` log level for application code (default is `DEBUG` for debug, `INFO` otherwise).
* `AUDIT_LOG_LEVEL` log level for audit messages (default is `INFO`).
* `DJANGO_LOG_LEVEL` log level for Django internals (default is `INFO`).

Connections:

* `AZURE_STORAGE_CONTAINER_ENDPOINT` endpoint for the Azure Search Service.

Deployment:

* `ALLOWED_HOSTS` will limit which domain names can connect.
* `CLOUD_ENV=azure` will enable Azure-specific telemetry.

Hardening deployment:

* `SESSION_COOKIE_SECURE` is already true in production.
* `CSRF_COOKIE_SECURE` is already true in production.
* `SECRET_KEY` is used for various encryption code.
* `CORS_ALLOW_ALL_ORIGINS` can be true/false to allow all websites to connect.
* `CORS_ALLOWED_ORIGINS` allows a list of origin URLs to use.
* `CORS_ALLOWED_ORIGIN_REGEXES` supports a list of regex patterns fow allowed origins.

## Developer Notes

Run `make` in the `src` folder to have a help-overview of all common developer tasks.

## Package Management

The packages are managed with *pip-compile*.

To add a package, update the `requirements.in` file and run `make requirements`.
This will update the "lockfile" aka `requirements.txt` that's used for pip installs.

To upgrade all packages, run `make upgrade`, followed by `make install` and `make test`.
Or at once if you feel lucky: `make upgrade install test`.

## Environment Settings

Consider using *direnv* for automatic activation of environment variables.
It automatically sources an ``.envrc`` file when you enter the directory.
This file should contain all lines in the `export VAR=value` format.

In a similar way, *pyenv* helps to install the exact Python version,
and will automatically activate the virtualenv when a `.python-version` file is found:

```shell
pyenv install 3.12.4
pyenv virtualenv 3.12.4 vertrouwelijke-data-proxy
echo vertrouwelijke-data-proxy > .python-version
```
