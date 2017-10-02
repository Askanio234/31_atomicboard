# Тесты для AtomicBoard

**Задача:** Необходимо протестировать клон Trello - AtomicBoard написанный на Angular, для тестирования используется отдельный
[stage-server](http://atomicboard.devman.org/login/?next=/)

**функционал:** Тест-кейсы unittesta для Selenium в связке с PhantomJS:
- Загрузка страницы
- Проверка наличия тестовых данных
- Создание новой задачи
- Редактирование задачи
- Перенос задачи из одного раздела в другой
- Изменение статуса задачи на "выполнено"

## Приложение использует переменную окружения:
- *path_to_phantom* - Путь к вебдрайверу PhantomJS, [официальный сайт](http://phantomjs.org/)

## Перед запуском необходимо установить зависимости из requirements.txt:
```#!bash
pip install -r requirements.txt
```

## Запускаем тесты:
```#!bash
python run_tests.py
```

## Пример вывода:
```#!bash
test_create_new_ticket (__main__.AtomicBoardTest) ... ok
test_drag_and_drop (__main__.AtomicBoardTest) ... ok
test_edit_ticket (__main__.AtomicBoardTest) ... ok
test_if_page_served (__main__.AtomicBoardTest) ... ok
test_if_tickets_present (__main__.AtomicBoardTest) ... ok
test_mark_ticket_complete (__main__.AtomicBoardTest) ... ok

----------------------------------------------------------------------
Ran 6 tests in 18.959s

OK
```

# Цели проекта

Код написан в образовательных целях. Курс веб-разработки – [DEVMAN.org](https://devman.org)
