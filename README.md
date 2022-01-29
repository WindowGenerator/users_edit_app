# Приложение редактирования пользователей

## Установка зависимостей

### Для Backend`а:
```bash
make -f backend/Makefile create-venv
```
### Для Frontend`а:
```bash
cd frontend && npm i
```


## Запуск

### Без докера

- Запуск backend`а:
```bash
source ./backend/.venv/bin/activate && make -f backend/Makefile start-dev
```
- Запуск postgres`а:
```bash
postgres -D /usr/local/pgsql/data >logfile 2>&1 &
sudo -iu postgres
psql -c 'CREATE DATABASE users_db' 
```
- Запуск frontend`а:
```bash
cd frontend && npm run dev
```

### С докером

```bash
docker-compose down -v && docker-compose build && docker-compose up -d
```
