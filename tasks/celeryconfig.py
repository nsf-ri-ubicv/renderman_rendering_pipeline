
BROKER_BACKEND="mongodb"
BROKER_HOST="honeybadger.rowland.org"
BROKER_PORT=22334
BROKER_USER=""
BORKER_PASSWORD=""
BROKER_VHOST="celery_broker"

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "honeybadger.rowland.org",
    "port": 22334,
    "database": "celery_broker",
    "taskmeta_collection": "taskmeta_collection",
}

CELERY_IMPORTS = ("celerender", )
