# ecommerce-bi-pipeline

#### Учебный проект по продуктовой и торговой аналитике интернет-магазина.

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


Перейдите по адресу: http://localhost:8088
