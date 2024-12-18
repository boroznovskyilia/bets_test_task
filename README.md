# тз
 Вам предстоит разработать небольшую систему, принимающую пользовательские
 ставки на определённые события (например, спортивные).
 Система должна состоять из двух независимых сервисов:
 ● сервис line-provider — провайдер информации о событиях,
 ● сервис bet-maker, принимающий ставки на эти события от пользователя

Описание сервиса line-provider
 Сервис должен выдавать информацию о событиях, на которые можно совершать ставки.
 Наша система будет максимально упрощённой, поэтому мы будем принимать ставки
 только на выигрыш первой команды
 Таким образом, информация о событии должна содержать как минимум:
 ● уникальный идентификатор события — строка или число,
 ● коэффициент ставки на выигрыш — строго положительное число с двумя
 знаками после запятой,
 ● дедлайн для ставок — таймстемп, до которого на событие принимаются ставки,
● текущий статус события.
 В нашей простой системе событие может иметь один из трёх статусов:
 ● незавершённое,
 ● завершено выигрышем первой команды,
 ● завершено выигрышем второй команды и, соответственно, поражением первой
 (ничьих в наших событиях не бывает)

 Описание сервиса bet-maker
 Сервис bet-maker отвечает за постановку ставок на события пользователями.
 Информация о событиях должна получаться из сервиса line-provider. В частности,
 сервису bet-maker необходимо узнавать об изменении статуса событий (переход в
 статус завершено с выигрышем или поражением), чтобы понять выиграла ставка или
 проиграла.
 Взаимодействие между сервисами может быть реализовано, к примеру, запросами в
 сервис line-provider, вызовом callback-урла bet-maker при изменении статуса события
 на стороне line-provider или обменом сообщений между сервисами через очередь
## что сделано
- реализована логика двух сервисов:
  - line_provider:
    - служит для управления сущностью event, так же реализована логика отправки сообщений через rabbitmq при обновлении статуса event-a
  - bet_market:
    - служит для управления сущность bet, реализован comsumer для прослушки сообщений от line_provider, для обновления данных по событиям,
    - так же реализованно кеширование events на сторене bet_market для оптимизации взаимодействия между сервисами, кэш также обносляется при получении события об оновлении или добавлении нового события
    - взаимодействие с line_provider происходит черезе асинхронный запросы
- применены некоторые паттерны проектирования(Например паттерн репозиторй) + зазделил сервисы на слои
- заложил архитектуру для дальнейшего масштабтрования системы: использовал rabbitmq для взаимодействия между сервисами, redis для кеширования
- покрыл часть системы Unit тестами
## как улучшить
  - на основе существующей архитектуры можно было отказаться от прямых запросов между сервисами и перейти полснотью на взаимодействие через очереь для повышения надежности взаимодействия между сервисами
  - и улучшения масштабирования сисетмы
  - увеличить степень покрытия unit тестами + добавить интеграционные тесты
  - уточнить больше требований о том что именно ожидается от работы сервисов, заложить больше архитектуры для дальнейшего расширения функционала и масштабирования

# установска и запуск
1) git clone https://github.com/boroznovskyilia/bets_test_task.git
2) cd bet_market -> docker compose up --build
3) cd line_provider -> docker compsoe up --build



