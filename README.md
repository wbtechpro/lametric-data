# data_for_Lametric
Server application for fetching data from Finolog.ru and represent it for Lametric in json

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


The application runs on the wbtech.pro server, connected at wbtech.pro/lametric_data.
The Lametric clock sends a request to this address, the application polls Finolog server and generates a json response for the clock on the fly without storing data in files. On the server, the application runs on nginx on port 8123.

##### Finolog screen

Link:
1. [json finolog](http://172.104.205.95:8123/finolog)

Changes made to the code for this Lametrics screen (in the `puller.py` file) are displayed on the site immediately.


##### How to display marketing and recruiting screen changes

Links:
2. [json marketing](http://172.104.205.95:8123/marketing)
3. [json recruiting](http://172.104.205.95:8123/recruiting)

These Lametrics screens take data through Zapier. As a result, changes in the code of these screens (in the `marketing.py` and `data_base.py` files) are not displayed on the site immediately after uploading the code to the server.

In order for such changes to be reflected in json, it is necessary to launch the corresponding commands - either automatic or manual. Currently, the zaps are automatically triggered on Saturday mornings.