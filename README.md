# BookAPI

This is a simple API built with fastApi

Due dependencies are in the [Requirement File](https://github.com/HenryAnyiam/BookAPI/blob/master/requirements.txt)

Simply run the following from the base directory to install in your virtual enviroment
```
pip install -r requirements.txt
```

To start up the server, run the following from the base directory

```
fastapi dev server.py
```

It uses sqlite, so there won't be need for an extra database setup before starting
A db would be automatically created in the base directory on successful server startup

You can access the API documentation from the following route once the server is started
```
http://127.0.0.1:8000/docs
```


Tests has been written for the API
To run, this would be done from the base directory
```
python3 -m unittest tests.test
```

All tests can be found in the following [file](https://github.com/HenryAnyiam/BookAPI/blob/master/tests/test.py)
