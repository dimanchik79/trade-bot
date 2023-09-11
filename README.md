# travel-bot

Здравствуте! Этот телеграмм-бот - моя дипломная работа на курсе SkillBox по языку Python

Он предназначен для вывода, по запросу пользователя, цен на билеты и направления поездов в РФ.

1. API:
Бот использует API tutu.ru https://suggest.travelpayouts.com/search (токен не нужно).

Запрос
Get https://suggest.travelpayouts.com/search?service=tutu_trains&term=2000000&term2=2064130&callback=n

Параметры запроса
Параметр	Тип	    Описание
term	    int	    Код станции отправления
term2	    int	    Код станции прибытия
callback	string	Параметр для колбек функции
Код станции можно получить здесь https://support.travelpayouts.com/hc/ru/articles/115001440551

Пример ответа
{
  "trips": [
    {
      "name": "Двухэтажный",
      "departureStation": "2000003",
      "arrivalStation": "2064130",
      "runDepartureStation": "2000003",
      "runArrivalStation": "2064150",
      "departureTime": "10:52:00",
      "arrivalTime": "10:14:00",
      "trainNumber": "104В",
      "categories": [
        {
          "type": "coupe",
          "price": 4307
        },
        {
          "type": "lux",
          "price": 14465
        }
      ],
      "travelTimeInSeconds": "84120",
      "firm": true,
      "numberForUrl": "MTA00JI="
    }
  ]
  "url": "/poezda/rasp_d.php?nnst1=2000000&nnst2=2064130"
}

Поля ответа
name                — название поезда:
plazcard            — плацкарт;
coupe               — купе;
sedentary           — сидячий;
lux                 — люкс;
soft                — мягкий.
departureStation    — станция отправления;
arrivalStation      — станция назначения;
runDepartureStation — начальная станция данного поезда;
runArrivalStation   — конечная станция данного поезда;
departureTime       — время отправления (московское);
arrivalTime         — время прибытия (московское);
trainNumber         — номер поезда;
categories          — категории вагонов в составе поезда:
type                — тип;
price               — цена в рублях.
travelTimeInSeconds — время в пути (в секундах);
firm                — является ли поезд фирменным;
url                 — ссылка на расписание данного поезда на сайте Туту.ру.

2. Функционал бота.

Справка по командам бота:
/start      - регистрирует нового пользователя
/help       - справка по командам бота
/low        - выводит самую низкую цену билета по заданному направлению
/mid        - выводит бюджетный вариант билета
/high       - выводит самую высокую цену билета
/direct     - выводит в файл возможные направления из пункта отправки
/cancel     - отменить ввод станций
/history    - выводит последние 10 команд пользователя
/exit       - покинуть бот

Бот также ведет регистрацию пользователей. Использует GUI в качестве админ-панели.
Ведет запись команд пользователя. И можно вывести все направления из конкретной
станции отправления в текстовый файл.
