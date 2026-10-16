# КУДЛАЙН

Первый этап корпоративной платформы ООО «КУДЛАЙН»: Django REST API, PostgreSQL, React + TypeScript и Django Admin.

## Локальный запуск

1. Скопируйте `.env.example` в `.env` и укажите параметры PostgreSQL.
2. Backend:
   ```powershell
   cd backend
   python -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   .venv\Scripts\python manage.py migrate
   .venv\Scripts\python manage.py createsuperuser
   .venv\Scripts\python manage.py runserver
   ```
3. Frontend (в другом терминале):
   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

Для разработки без PostgreSQL можно временно установить `USE_SQLITE=True` в `.env`.

## SPA history fallback

Vite development server автоматически возвращает `index.html` для прямых URL вроде `/about` и `/projects`.
Для production web-сервер должен делать то же самое. Например, для Nginx:

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

Файл `frontend/public/_redirects` содержит эквивалентное правило для совместимых static hosting-платформ.

## Проверки

```powershell
cd backend
python manage.py check
python manage.py test

cd ..\frontend
npm run build
```

## Клиентская база и заказы

Этап 2.1 добавляет внутренний фундамент клиентской базы и заказов, доступный только через Django Admin. Эти данные намеренно не публикуются через REST API. Границы сущностей, политика удаления, будущая модель доступа личного кабинета и принцип snapshot для документов описаны в [docs/CLIENT_DATA_MODEL.md](docs/CLIENT_DATA_MODEL.md).

