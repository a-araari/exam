# exercice.net
Online Education Website

# How to run the project locally
#### Assuming python 3.8.1 is installed :

Open your command line and Create a local folder where you will store the project

    $ mkdir project-container && cd project-container

Install & Create & activate & a Virtualenv by typing

    $ pip install virtualenv
    $ virtualenv venv
    $ "venv/scripts/activate"
    
Pull the porject using git (install [git](https://github.com/git-for-windows/git/releases/download/v2.25.1.windows.1/Git-2.25.1-64-bit.exe) if you didn't, or simply download it and extract it)
    
    $ mkdir platform && cd platform
    $ git init
    $ git remote add origin https://github.com/a-araari/devoirs.tn/
    $ git pull origin master

    $ pip install -r requirements.txt

Now everything looks great, let's run the project

    $ py manage.py makemigrations
    $ py manage.py migrate
    $ py manage.py createsuperuser
    $ py manage.py runserver

Now Visit http://127.0.0.1:8000/admin/ and login to be able to CRUD(create/retrieve/update/delete) users / sellers / buyers / messages / companies

Or you can run the scrape command to scrape PDFs

    $ py manage.py scrapedevoiratdata

# Deploy:
Use Nginx instead of Apache (Nginx the fastest)
Use Docker to install and run pdf2htmlEX package and run it like this:
```
import subprocess
subprocess.run(['docker', 'run', '-ti', '--rm', '-v', '[working file directory(dont use 'pwd'!)]:/pdf', 'bwits/pdf2htmlex', 'pdf2htmlEX', '[args]', 'file.pdf'])
```
