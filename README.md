# herokuvania

An API: 
- created using FastAPI 
- that scrapes free udemy coupons from [this site](https://coursevania.com/) using selenium, requests and BeautifulSoup modules 
- and serves them in a neat and organized manner
- deployed [here](https://udemy-coupons-api.herokuapp.com/) on heroku

## API endpoints
- [/](https://udemy-coupons-api.herokuapp.com) : homepage
- [/json/{course_num}](https://udemy-coupons-api.herokuapp.com/json/3) : fetch n courses and return in json format
- [/table/{course_num}](https://udemy-coupons-api.herokuapp.com/table/3) : fetch n courses and return in tabular format
- [/docs](https://udemy-coupons-api.herokuapp.com/docs) : API documentation automatically created by FastAPI using [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [/redoc](https://udemy-coupons-api.herokuapp.com/redoc) : API documentation automatically created by FastAPI using [redoc](https://github.com/Redocly/redoc)

## Screenshots

### Homepage
![homepage](https://github.com/Prajwalsrinvas/herokuvania/blob/main/screenshots/home.png)


### JSON response
![JSON Response](https://github.com/Prajwalsrinvas/herokuvania/blob/main/screenshots/json_response.png)


### Tabular response
![Tabular Response](https://github.com/Prajwalsrinvas/herokuvania/blob/main/screenshots/tabular_response.png)


### Documentation
![docs](https://github.com/Prajwalsrinvas/herokuvania/blob/main/screenshots/docs.png)

## Note
- Initially the API would take some time to load, as it is not running 24/7 and has to "wake up", but once the first request is made, it should be faster.
- Internal Server Error might occur sometimes due to invalid session id, so try again some time later.
