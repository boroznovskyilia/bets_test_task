#!/bin/sh
set -e

alembic upgrade head 

uvicorn main:app --host ${APP__HOST} --port ${APP__PORT} --log-level info