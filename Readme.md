# Hackathon
# https://canteen-recommendation-app.herokuapp.com/
## Technical Aspect
* Python ( programming language )
* Flask ( web development library )
* Postgres SQL on Heroku ( SQL Database )
* Apriori ( Association Rule Mining / Recommendation System )
* Heroku ( Cloud PaaS platform for hosting )
## For Running Canteen Application
```bash
pip install requirements.txt
python app.py
```

## For Hosting
```bash
create a requirements.txt file
create a Procfile file
    * web: gunicorn app:app
push code on github
deploy the github branch on heroku
```

## URL Structure 
```
├── /
│   ├── /admin
|       ├── /menu (shows all the products in database)
|       ├── /add (create a new product)
|       ├── /recommend (shows recommendation based on history)
|       └── /reset-basket (reset basket)
|       
│   ├── /user
|       ├── /menu (shows all the products in database)
|       └── /order (select items and order)
```

## References
### Apriori Implementation 
* https://github.com/ymoch/apyori
* https://github.com/JayMalde/Market_Basket_Analysis