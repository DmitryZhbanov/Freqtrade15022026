# Структура проекта

Для работы у нас есть три основных файла:

1) `docker-compose.yml` в корне проекта  
2) `/user_data/config.json` — основной конфиг, в котором прописываются все настройки  
3) `/user_data/strategies/CandleFlipFixedDirection.py` — сама стратегия, которая присоединяется через файл `docker-compose.yml` (нужно в yaml указать название стратегии). Её как раз нужно переписать грамотно.

---

# Развёртывание

Нужно будет поставить Docker, развернуть там эту хуйню.

Перед запуском можно проверить стратегии:

```bash
docker compose run --rm freqtrade list-strategies --config /freqtrade/user_data/config.json
```

Перед запуском можно проверить конфиг:

```bash
docker compose run --rm freqtrade show-config --config /freqtrade/user_data/config.json
```

Перед настройкой нужно добавить в конфиг в раздел TG-бота свой chat id. Бота зарядил с сигналов по вуманчи.

---

# Запуск

## Dry-run

```bash
docker compose run --rm freqtrade trade --config /freqtrade/user_data/config.json --strategy CandleFlipFixedDirection --dry-run
```

## Бектест

```bash
docker compose run --rm freqtrade backtesting --config /freqtrade/user_data/config.json --strategy CandleFlipFixedDirection
```

---

# Загрузка данных для бектеста

Для бектеста нужно загружать данные вручную по списку пар из конфига:

```bash
docker compose run --rm freqtrade download-data --config /freqtrade/user_data/config.json --timeframe 15m --timerange 20251115-
```

Загружает данные с `20251115-` до сейчас. Берёт все пары из `pairlists` и фильтрует по `pair_whitelist`. Загруженные данные в `/user_data/data/okx/`.

---

# Интерфейсы управления

Инфо-панель + некоторое управление ордерами по лайф-трейду и dry-run в вебинтерфейсе `http://localhost:8080` и ТГ-боте.

Управление и просмотр данных по бектестам только через CLI.

---

# Логика стратегии

- Таймфрейм: 15 минут.

- На закрытии каждой свечи:
  - Если позиции нет — открываем ордер в заранее заданную сторону (long/short).

- Для каждой сделки выставляются заранее заданные TP и SL:
  - Определить можно в https://colab.research.google.com/drive/1Uw7gvXEvWPYhckA2i95u5bCnKunqpSwb?usp=sharing#scrollTo=J76z1Bwv0P6l по матрице TP + SL.
  - Выставляешь там в начале ячейки параметры (монету, фрейм, плечо).
  - Выполняешь ячейку.
  - Смотришь лучшую ячейку.
  - Копируешь параметры в стратегию.

- Если TP или SL достигнуты внутри свечи — сделка закрывается по ним и ждём следующую свечу.

- Если TP/SL не достигнуты — на закрытии следующей 15m свечи позиция закрывается по рынку.

- Далее цикл повторяется на каждой новой свече.


! Сделки должны быть строго каждую свечу. 1 час - 4 сделки, 4 часа - 16 сделок и т.д. Тестить удобно можно в веб-интерфейсе.
