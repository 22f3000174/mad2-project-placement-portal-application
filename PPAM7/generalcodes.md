#is already installed globally
npm install -g @vue/cli


vue create frontend

cd frontend
npm run serve

PS J:\MAD3 TEST\mad3 test\frontend> npm install bootstrap
PS J:\MAD3 TEST\mad3 test\frontend> npm install vue-router

PS J:\MAD3 TEST\mad3 test> pip install flask flask-sqlalchemy flask-cors
PS J:\MAD3 TEST\mad3 test\backend> pip install flask-cors
# inside backend folder
python -m venv venv

# Redis Celery code
# run inside backend
pip install redis
pip install celery flask-mail

# open inside a new backend terminal -- Terminal 1 — Celery worker: 
python -m celery -A celery_app:celery worker --loglevel=info --pool=solo
# open inside a new backend terminal -- Terminal 2 — Celery Beat:
python -m celery -A celery_app:celery beat --loglevel=info