# FastAPI 3Commas Trading Bot 

## Overview
This project implements a **trading bot** using **FastAPI**, **3Commas API**, **PostgreSQL**, and **Celery** for automation. The .env.templates you need is included on .env-template for the project to work for you and don't
forget to install the requirements.txt files after you are done cloning the project.

## Features
- 🛠 **FastAPI Backend**
- 📈 **DCA Trading Strategy**
- 🔄 **Automated Trading with Celery**
- 💾 **PostgreSQL for Data Storage**: Additional features for record purposes
- 🚀 **Deployment with Render/DigitalOcean**

## Installation
```bash
git clone https://github.com/blaise-93/trading-bot.git
cd trading-bot
pip install -r requirements.txt

```

## To start up the server in development:
In development environment, you can start up the server on your local machine by running:
```bash
uvicorn main:app --reload
celery -A celery_worker worker -l info
```
You can use already generated swaggarUI docs - localhost:8000/docs/default to make some API calls
and test the program locally or even on the production server too, https://trading-bot.blaisemart.com/docs/

For database migrations and migrate, we are using alembic library to achieve that.
```bash

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head # will commit the migrate to db.
```

This **project is served live** on https://trading-bot.blaisemart.com/docs/