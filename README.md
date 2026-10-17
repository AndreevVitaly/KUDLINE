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

## Рабочее место менеджера

Защищённый интерфейс находится по адресу `http://127.0.0.1:5173/workspace/`. Он использует Django session authentication и CSRF, а внутренний API расположен под `/api/internal/`.

Первую административную учётную запись создайте интерактивно, не сохраняя пароль в Git:

```powershell
cd backend
$env:USE_SQLITE='True'
python manage.py createsuperuser
```

Для обычных сотрудников включите `is_staff` и назначьте группу `Менеджер` или `Руководитель` через Django Admin. Группы и модельные разрешения синхронизируются после `migrate`. Администратор-суперпользователь имеет полный доступ; руководитель получает обзор и рабочие операции в рамках выданных разрешений; менеджер работает с заявками, клиентами, объектами и заказами. Проверки выполняются backend-разрешениями, а не только интерфейсом.

Основные защищённые endpoints: `dashboard/`, `inquiries/`, `clients/`, `objects/`, `orders/`, `audit/`, `users/`. Реестры поддерживают пагинацию, поиск и фильтрацию. Изменения статусов заказов, ответственных и значимых данных фиксируются в журнале. Вложения заявок выдаются только через авторизованный endpoint; прямые URL `/media/inquiries/` заблокированы.

Будущие модули производства, сотрудников, финансов и документов обозначены в меню как планируемые и должны развиваться отдельными Django-приложениями со связью на `Order` по UUID.

