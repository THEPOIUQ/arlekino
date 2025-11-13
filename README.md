# arlekino

Shadow C2 — исследовательский проект по созданию модульного и безопасного C2-инструментария. Этот репозиторий содержит демонстрационные сценарии, документацию и материалы для локального запуска.

## Основные возможности
- демонстрационные скрипты для быстрого развёртывания среды;
- материалы по настройке split-архитектуры и VPN-доступа;
- набор вспомогательных инструментов для операционной безопасности.

## Development Workflow
Ниже приведён фактический рабочий процесс, который следует использовать при разработке. Он отражает раздел «Development Workflow» из `agents.md`, но содержит проверенные команды и ссылки на актуальные скрипты.

1. **Подготовьте окружение**
   ```bash
   git clone https://github.com/your-username/shadow-c2.git
   cd shadow-c2
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements_minimal.txt
   ```
2. **Создайте рабочую ветку**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Выполните проверки качества**
   - статический анализ (проверка синтаксиса):
     ```bash
     python3 scripts/run_static_checks.py
     ```
   - модульные тесты:
     ```bash
     python3 test_suite.py
     ```
4. **Подготовьте коммит и отправьте изменения**
   ```bash
   git add <изменённые файлы>
   git commit -m "feat: краткое описание изменений"
   git push origin feature/your-feature-name
   ```
5. **Создайте Pull Request**, используя шаблон из `.github/pull_request_template.md`.

## Коммиты и Pull Request’ы
- Рекомендуемый шаблон сообщения коммита и инструкции по его применению описаны в `docs/COMMIT_AND_PR_GUIDELINES.md`.
- Pull Request’ы автоматически используют шаблон из `.github/pull_request_template.md`. Перед отправкой убедитесь, что в разделе «Quality checks» отмечены актуальные команды.

## Тесты и статический анализ
- `test_suite.py` запускает `unittest`-совместимые тесты из каталога `tests/`.
- `scripts/run_static_checks.py` проверяет синтаксис всех Python-файлов с помощью стандартного модуля `py_compile`.

Эти команды используются в CI/локальной проверке и должны выполняться перед отправкой изменений.
