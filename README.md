# Count For You
## _Сборщик и обработчик информации о валютной паре USDT-RUB_

## Основные функции

- Сбор информации с ряда ресурсов
- Анализ наиболее выгодного предложения в режиме реального времени
- Уведомления о наступлении события
- Email-уведомления 

Приложение собирает информацию с ряда ресурсов, в реальном времени отслеживает самое выгодное предложение на покупку/продажу. Доступна конфигурация частоты запросов, логирования, системы уведомлений, пользовательского интерфейса. Также реализована система email-уведомлений, которая осуществляет рассылку при наступлении заданного пользователем события.

## Стек
- Python
- Asyncio 
- Aiohttp
- PyQt5
- Sqlalchemy
- win10toast
- Smtplib
- Email

## Пользовательский интерфейс

Пользователю доступно на выбор 4 вида оформления. За базу стилей были взяты [готовые шаблоны](https://github.com/GTRONICK/QSS).

Aqua:

[![2022-06-29-180138304.png](https://i.postimg.cc/pXSWLY42/2022-06-29-180138304.png)](https://postimg.cc/RNc5Pfv8)

Dark:

[![2022-06-29-180222510.png](https://i.postimg.cc/XJ1hkxwq/2022-06-29-180222510.png)](https://postimg.cc/62RY9rbx)

MacOs:

[![2022-06-29-180314467.png](https://i.postimg.cc/HkTqHJsp/2022-06-29-180314467.png)](https://postimg.cc/2VXc7SZJ)

Forbidden:

[![2022-06-29-180505290.png](https://i.postimg.cc/ydhhVNNH/2022-06-29-180505290.png)](https://postimg.cc/DJZ46nsj)

Пример построения графика:

[![2022-06-29-180552742.png](https://i.postimg.cc/gjTxd93p/2022-06-29-180552742.png)](https://postimg.cc/xNLfy4sp)

## Запуск проекта

```sh
python run.py
```

### Идеи на будущее

- Оптимизировать работу приложения, на данный момент есть недостаток в том, что пользователь может заметить, когда приложение делает запрос к ресурсам.
- Сделать более современный интерфейс, возможно, потребуется привлечь дизайнера.
- Расширить пул собираемых обменных пар и возможность их конфигурации.
- Настроить собственный SMTP-сервер.
- Расширить возможность выбора типов уведомлений, можно добавить рассылку в telegram.
