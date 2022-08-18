# Backup database Vccopr



`cp  .env.example .env`

`pip install -r requirements.txt`

`. venv/bin/activate`

`source .env`

`flask db init --multidb`

`flask db stamp head`

`flask db migrate`

`flask db upgrade`