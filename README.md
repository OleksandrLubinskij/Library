Щоб встановити і запустити проєкт слід виконати цей список команд:

git clone https://github.com/OleksandrLubinskij/Library
cd Library/library_app
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
New-Item .env -ItemType File

За допомогою осьанньої команди було створено файл .env
Відкрийте його і вствате це:

SECRET_KEY=fjwfrhiofwriofwrhio
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Значення SECRET_KEY варто замінити на те, яке вам захочеться

Після цього виконайте наступні команди:

alembic upgrade head
uvicorn main:app --reload --port 8080

Перед запуском останньої команди, переконайтеся що на вашому комп'ютері нічого не запущено за портом 8080
Якщо запуск пройшов успішно, то у терміналі ви побачите це:
INFO: Application startup complete.

Після цього перейдіть у браузері за адресою
http://127.0.0.1:8080/login

Також є можливість переглянути інтерактивну документацію API за цією адресою:
http://127.0.0.1:8080/docs#/
