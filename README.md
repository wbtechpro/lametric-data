# data_for_Lametric
Server application for fetching data from finolog.ru and represent it for Lametric in json

##### How to build docker image

```
sudo docker build -t lametric:v1 .
```

##### How to build docker image with env parameters API-key

``` 
docker build \
--build-arg api_key="<finolog_API_key>" \
 -t lametric:v1 . 
```

##### How to run and daemonize container with outer TCP port 8123 

```
sudo docker run -d -p 8123:8080 lametric:v1
```


Приложение работает на сервере wbtech.pro, подключено по адресу wbtech.pro/lametric_data. 
Часы ламетрика посылают запрос на этот адрес, приложение опрашивает сервера финолога и формируют json-ответ для часов "на лету" без хранения данных в файлах. 
На сервере приложение работает по nginx на 8123 порту.

##### Экран finolog

Ссылка:
1. [json finolog](http://172.104.205.95:8123/finolog)

Изменения, внесенные в код этого экрана Ламетрики (в файл `piller.py`), отображаются на сайте сразу.


##### Как отобразить изменения экранов marketing и recruiting

Ссылки:
2. [json marketing](http://172.104.205.95:8123/marketing)
3. [json recruiting](http://172.104.205.95:8123/recruiting)

Эти экраны Ламетрики берут данные через Zapier. Как следствие, изменения в коде этих экранов (в файлах `marketing.py` и `data_base.py`) не отображаются на сайте сразу после заливки кода на сервер.

Для того, чтобы такие изменения отразились в json`е, необходим запуск соответствующих запов - либо автоматический, либо ручной. Сейчас запы автоматически срабатывают утром в субботу.
