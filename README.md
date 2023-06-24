# python_api
Learning python api development 

# Creting a virutal env

```
python3 -m venv venv 
```

# Activating virtual env 
```
source venv/bin/activate
```

# Generating requiremet.txt
```
pip3 install pipreqs
pip3 freeze > requirements.txt 
```

# Starting the application 
```
uvicorn app.main:app --reload
```

# Buildin documentation for API

```
\redoc
\docs
```


```
pip3 install fastapi[all]
pip3 install psycopg2-binary
pip3 install sqlalchemy==1.4.46 --ignore-installed

```