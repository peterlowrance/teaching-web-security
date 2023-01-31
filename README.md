# DjangoReactStarter
### Backend

Setup python for dependencies:

Make virtual environment

`python3 -m venv venv`

`source venv/bin/activate` (do this every time you have a new terminal)

Install deps

`pip install -r requirements.txt`

Run server (for each application)

```
cd attacking-website
python manage.py runserver 8080
```

```
cd vulnverable-website
python manage.py migrate
python manage.py runserver 80801
```


### Frontend for attacking-website
In website/react-website, run:

`cd attacking-website/website/react-website`

`npm install` to setup once

Run `npm run dev` to build for dev (live builds when code changes)

Or run `npm run build` to build once for production
