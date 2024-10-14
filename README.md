# API – Конвертер валют
## Описание
API-сервер предоставляет высокопроизводительное и масштабируемое решение для конвертации валют, разработанное с учетом требований к production-ready архитектуре. Основу сервера составляет асинхронная архитектура, построенная на принципах инверсии управления (IoC), что обеспечивает легкую расширяемость и поддержку различных компонентов.

### **Технологический стек**

В качестве фундамента был выбран FastAPI, поскольку он сочетает в себе:

1.**Гибкость архитектуры** – позволяет строить решения, опираясь на современные принципы проектирования, такие как DI или, например, CQRS и проч.
2.**Высокую производительность** – благодаря асинхронным возможностям, FastAPI обеспечивает минимальные задержки и высокую пропускную способность.

Для внедрения инверсии управления (IoC) используется библиотека dependency-injector, которая обеспечивает модульное и прозрачное управление зависимостями, делая код чистым и поддерживаемым.

### **Интеграция со сторонними сервисами**

Для взаимодействия с внешними API (например, валютными провайдерами) был выбран aiohttp, так как:

* Он позволяет эффективно управлять асинхронными HTTP-запросами, что особенно важно при необходимости отправки большого количества запросов к сторонним сервисам в режиме реального времени.
* aiohttp обеспечивает низкий уровень задержек при обработке данных, что особенно критично для сервисов конвертации валют, где точность и скорость обработки запросов имеют решающее значение.

### **Контейнеризация и веб-сервер**

Проект использует контейнеризацию через docker-compose, что позволяет легко разворачивать и управлять инфраструктурой. В качестве веб-сервера используется связка **ASGI-сервера Uvicorn** и **Nginx**. Uvicorn, как легковесный и асинхронный ASGI-сервер, отвечает за запуск FastAPI-приложения и обработку запросов с высокой скоростью, поддерживая асинхронные задачи.

Nginx, в свою очередь, используется в качестве **reverse proxy**. Это решение обеспечивает высокую масштабируемость, так что на нем в дальнейшем может быть настроена балансировка нагрузки.

## Архитектура
Архитектура приложения построена на принципе инверсии управления (IoC) с использованием внедрения зависимостей (Dependency Injection), что позволяет гибко управлять компонентами и упрощает их тестирование и масштабирование. Основные компоненты сервера разделены на три ключевые части: **модули**, **сервисы** и **маршруты**, каждая из которых имеет свое четкое назначение и ответственность.

### Модули

Модули представляют собой низкоуровневые компоненты, которые непосредственно взаимодействуют с внешними данными или хранилищами. Это могут быть строки, JSON-схемы, а также прямые запросы к базам данных, кэш-хранилищам или сторонним API. Модули являются обособленными единицами логики и могут быть представлены разными типами в зависимости от их назначения. Например, в текущей реализации существует единственный тип модуля — **адаптер**, который выполняет запросы к внешним API-сервисам. Однако структура поддерживает добавление множества типов модулей.

Для придания строгости и поддержания консистентности кода, каждый тип модуля должен быть предварительно определён через базовый класс. Это гарантирует, что все модули будут следовать единообразному интерфейсу и подходам, что облегчает их замену и расширение. Взаимодействие между модулями и другими компонентами контролируется через механизмы IoC.

### Сервисы

Сервисы — это более высокоуровневые абстракции, которые оперируют данными из модулей и являются “серединным звеном” в потоке данных (Data Flow). Каждый сервис жёстко привязан к одному или нескольким модулям, что обеспечивает изоляцию компонентов и делает архитектуру более модульной и гибкой.

Основная задача сервисов — инкапсулировать логику обработки данных и трансформации их в формы, подходящие для дальнейшего использования в бизнес-логике. Такая структура способствует разделению ответственности, делая каждый компонент более понятным, тестируемым и повторно используемым.

### Маршруты

Маршруты (routes) представляют собой самый верхний уровень архитектуры и отвечают за реализацию конечной бизнес-логики. Они организуют работу с сервисами и обеспечивают взаимодействие между различными частями системы. Один маршрут может вызывать несколько сервисов для выполнения комплексных операций, тем самым представляя собой конечную точку, через которую пользователи или другие системы взаимодействуют с приложением.

Важно отметить, что маршруты не должны напрямую взаимодействовать с модулями. Это требование обеспечивается для поддержания “чистого” Data Flow и разделения ответственности. Вызовы модулей должны происходить исключительно через сервисы, что позволяет минимизировать связанность компонентов и повысить гибкость системы.

## Установка
* Перейдите по ссылке, зарегистрируйтесь и получите бесплатный API-ключ сервиса: [Currency API](https://app.currencyapi.com/login)
* С помощью ```git clone https://github.com/amr0ny/currency-service``` перенесите репозиторий на локальный хост
* Перейдите в корневую директорию проекта```cd ./currency-service```
* Укажите свой API-ключ в ```.env``` файле: ```echo SERVICE_API_KEY=<YOUR_API_KEY> > .env```
* Убедитесь, что у вас установлен Docker с плагином docker-compose, выполните команду запуска проекта: ```docker-compose up -d```
* Перейдите в браузере по ссылке: http://127.0.0.1/docs – там вы можете обнаружить Swagger, в котором будет единственный роут.
* Протестировать работу сервиса вы можете, указав параметры запроса в Swagger, либо перейдя по URL самого запроса http://127.0.0.1/api/rates?from=USD&to=RUB&value=1
