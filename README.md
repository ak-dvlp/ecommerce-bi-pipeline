# ecommerce-bi-pipeline

#### Инженерный проект по проектированию и настройке инфраструктуры сбора, преобразования и визуализации данных для интернет-магазина. 

Основная цель проекта — построение полноценного конвейера данных (Data Pipeline) по классической Enterprise-архитектуре, обеспечивающего разделение операционной (OLTP) и аналитической (OLAP) нагрузки.

#### 🗺️ Конвейер данных:

#### Сырые CSV ➡️ Python Pandas (ETL) ➡️ PostgreSQL (OLTP) ➡️ ClickHouse (OLAP) ➡️ Apache Superset (Визуализация данных).

## Развёртывание и настройка

#### Клонирование репозитория и переход в директорию проекта

```bash
git clone https://github.com/ak-dvlp/ecommerce-bi-pipeline.git
cd ecommerce-bi-pipeline
```

#### Создание виртуального окружения для работы скриптов папки `scripts`

Для успешного выполнения дальнейших шагов в вашей системе должен быть установлен `Poetry`. После установки `Poetry`, выполните установку пакетов командой:

```bash
poetry install
```

Если вы работаете в `VS Code`, нажмите комбинацию клавиш `Ctrl + Shift + P`, наберите в поисковом поле `Python: Select Interpreter` и выберите пункт, содержащий имя виртуального окружения вашего проекта.

Примерный вид корректного пункта:

```bash
Python 3.x.x ('.venv': Poetry) ./.venv/bin/python
```

#### Запуск службы Docker и настройка прав группы

Перед запуском контейнеров убедитесь, что сама служба `Docker` запущена в вашей системе. Без этого команды управления контейнерами будут выдавать ошибку подключения к сокету.

Проверка статуса службы:

```bash
sudo systemctl status docker
```

В строке `Active:` должно быть указано `active (running)` зелёным цветом.

Запуск службы (если она остановлена):

```bash
sudo systemctl start docker
```

Если вы как пользователь не являетесь членом группы `docker`, то будете вынуждены использовать `sudo` в большинстве команд. Для того чтобы упростить себе работу, выполните команды в раскрывающемся списке ниже.

<details>
<summary>Пошаговая настройка прав (без перезагрузки)</summary>

Создание группы:

```bash
sudo groupadd docker
```

Добавление себя в группу:

```bash
sudo usermod -aG docker $USER
```

Обновление конфигурации групп текущей сессии (необходимо, если не хотите перезагружать компьютер)

```bash
newgrp docker
```

Проверка вашего членства в группе `docker`:

```bash
id $USER
```

Примерный вывод (где вместо `aleks` будет ваше имя пользователя):

```text
uid=1001(aleks) gid=1001(aleks) groups=1001(aleks),10(wheel),999(docker)
```

</details>

#### Развёртывание и запуск контейнеров

```bash
docker compose up -d
```

Дождитесь окончания создания изолированных хранилищ данных, создания виртуальной сети и запуска всех контейнеров:

```bash
✔ Volume ecommerce-bi-pipeline_chdata        Created                                                                                                       0.0s
 ✔ Network ecommerce-bi-pipeline_default      Created                                                                                                       0.0s
 ✔ Volume ecommerce-bi-pipeline_superset_home Created                                                                                                       0.0s
 ✔ Volume ecommerce-bi-pipeline_pgdata        Created                                                                                                       0.0s
 ✔ Container superset                         Started                                                                                                       0.2s
 ✔ Container ecommerce_clickhouse             Started                                                                                                       0.3s
 ✔ Container ecommerce_postgres               Started
```

Выполните команду для вывода сообщений журнала в реальном времени:

```bash
docker compose logs superset -f
```

Дождитесь следующих сообщений журнала:

```bash
superset  | ⏳ Запуск Superset...
superset  | [2026-08-20 11:46:40 +0000] [114] [INFO] Starting gunicorn 23.0.0
superset  | [2026-08-20 11:46:40 +0000] [114] [INFO] Listening at: http://0.0.0.0:8088 (114)
superset  | [2026-08-20 11:46:40 +0000] [114] [INFO] Using worker: gthread
superset  | [2026-08-20 11:46:40 +0000] [115] [INFO] Booting worker with pid: 115
```

Выйдите из режима вывода сообщений журнала при помощи комбинации горячих клавиш `Ctrl + C`.

#### Инициализация БД, извлечение, преобразование и загрузка данных в PostgreSQL и ClickHouse

Выполните команду запуска скрипта инициализации БД. При появлении запроса на подтверждение введите букву `y` (утвердительный ответ) и нажмите клавишу `Enter`:

```bash
poetry run python scripts/init_db.py
```

Выполните команду запуска ETL-скрипта для `PostgreSQL`:

```bash
poetry run python scripts/etl_postgres.py
```

Выполните команду запуска ETL-скрипта для `ClickHouse`:

```bash
poetry run python scripts/etl_to_clickhouse.py
```

#### Настройка Apache Superset в веб клиенте

Перейдите по адресу: [http://localhost:8088](http://localhost:8088)
Введите имя пользователя `admin` и пароль `admin`

<img width="897" height="500" alt="image" src="https://github.com/user-attachments/assets/bfeb68db-bc71-46ed-8036-d66f33b99f60" />

Откройте выпадающее меню нажав в правой части навигационного меню на иконку `+`. Затем нажмите: `Data` => `Connect Database`.

<img width="756" height="500" alt="image" src="https://github.com/user-attachments/assets/0167034d-25a5-43f6-899a-b76e6811bae3" height="350" />

Шаг 1. В выпадающем меню поля выбора `Supported databases` выберите `ClickHouse`. Отсутствие данного пункта может означает неудачную установку драйверов базы данных.

<img width="300" height="500" alt="image" src="https://github.com/user-attachments/assets/78d23ac0-167c-461e-9a9f-d0e742bf2e74" />

Шаг 2. Заполните форму:  
Host: `127.0.0.1`  
Port: `8123`  
UserName: `bi_user`  
Password: `bi_password`

Нажмите кнопку `Connect`.

<img width="300" height="500" alt="image" src="https://github.com/user-attachments/assets/abc4687e-e72a-4bab-99c6-aa301767d91e" height="350" />

Шаг 3. Нажмите кнопку `Finish`

<img width="300" height="500" alt="image" src="https://github.com/user-attachments/assets/0daada9b-b28e-4f9a-9da5-b78dcb92d99b" height="350" />

#### Проверка наличия денормализованной таблицы

В левой части навигационного меню нажмите на `SQL`. В выпадающем меню выберите пункт `SQL Lab`.

<img width="1154" height="632" alt="image" src="https://github.com/user-attachments/assets/a652ee7b-0474-4e94-a18e-f92db2bee9ed" />

Нажмите на вкладку `Add a new tab`

<img width="1111" height="317" alt="image" src="https://github.com/user-attachments/assets/e031fe97-8e46-4507-98a2-23e6d4b04a96" />

Выполните запрос:

```sql
SELECT * FROM ecommerce_olap.f_sales;
```

Нажмите на кнопку `Run selection`

<img width="2559" height="1411" alt="image" src="https://github.com/user-attachments/assets/2b99ccae-f919-44ff-9f93-3331c7259634" />  
<img width="2559" height="1411" alt="image" src="https://github.com/user-attachments/assets/8a4270e2-d67d-482d-b5b8-71442592b4e8" />  
<img width="2559" height="1411" alt="image" src="https://github.com/user-attachments/assets/1fe5b142-0463-4f5e-9973-d05f5fe41886" />



#### Работа с данными через ClickHouse

Перейдите по адресу: [http://localhost:8123/play](http://localhost:8123/play)

<img width="2551" height="1398" alt="image" src="https://github.com/user-attachments/assets/417d0034-b9ee-49de-a9bb-ffa1a53c0d51" />

Заполните поля `user` и `password` значениями `bi_user` и `bi_password` соответственно (если поля скрыты, нажмите на иконку ключ).

Выполните какой-либо запрос, например:

```sql
SELECT
    event_time,
    query_duration_ms,
    read_rows,
    result_rows,
    projections,
    substring(query, 1, 150) AS sql_preview
FROM system.query_log
WHERE user = 'bi_user'
  AND type = 'QueryFinish'
  AND query LIKE 'SELECT%'
ORDER BY query_duration_ms DESC
LIMIT 10;
```

Нажмите на кнопку `Run`.

<img width="2556" height="1403" alt="image" src="https://github.com/user-attachments/assets/595cf66c-103a-4504-9d66-5caac90127e6" />


## Заключение

Инфраструктура готова к созданию графиков и витрин интерактивной аналитики в `Apache Superset`.

<img width="2555" height="1319" alt="image" src="https://github.com/user-attachments/assets/6dbdd795-d3cc-47cc-be63-01d634715dfd" />






