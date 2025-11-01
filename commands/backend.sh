#!/bin/bash

alembic upgrade head
exec python bot.py
