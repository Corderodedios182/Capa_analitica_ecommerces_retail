# Makefile — Atajos para el entorno de desarrollo
# Uso: make <comando>
# Requiere: Docker Desktop instalado y corriendo

.PHONY: build up down shell dbt-run dbt-test dbt-docs clean help

## Construir la imagen Docker (solo necesario la primera vez)
build:
	docker compose build

## Levantar el entorno (Jupyter Lab en http://localhost:8888)
up:
	docker compose up

## Levantar en segundo plano
up-detached:
	docker compose up -d

## Abrir una terminal bash dentro del contenedor
shell:
	docker compose exec workspace bash

## Ejecutar todos los modelos dbt
dbt-run:
	docker compose exec workspace bash -c "cd /workspace/dbt_project && dbt run"

## Ejecutar tests dbt
dbt-test:
	docker compose exec workspace bash -c "cd /workspace/dbt_project && dbt test"

## Generar y servir documentación dbt (http://localhost:8080)
dbt-docs:
	docker compose exec workspace bash -c \
		"cd /workspace/dbt_project && dbt docs generate && dbt docs serve --port 8080"

## Apagar el entorno
down:
	docker compose down

## Apagar y eliminar la imagen (libera espacio en disco)
clean:
	docker compose down --rmi all --volumes

## Mostrar este mensaje de ayuda
help:
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make build       → Construir la imagen (primera vez)"
	@echo "  make up          → Levantar Jupyter Lab"
	@echo "  make up-detached → Levantar en segundo plano"
	@echo "  make shell       → Abrir terminal en el contenedor"
	@echo "  make dbt-run     → Ejecutar modelos dbt"
	@echo "  make dbt-test    → Ejecutar tests dbt"
	@echo "  make dbt-docs    → Generar y servir docs dbt"
	@echo "  make down        → Apagar el entorno"
	@echo "  make clean       → Apagar y limpiar imagen"
	@echo ""
