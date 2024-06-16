# autotrade-admin-api
## Local testing instructions
In order to start the application, follow these steps in the root directory of
your local repository with an active virtual environment:
- Rename ```.env.template``` to ```.env``` in root directory.
- Run the commands:
    ```
    docker-compose up -d db
    ```

    ```
    pip3 install -r requirements.txt
    ```

    ```
    python3 manage.py createadminuser && python3 manage.py migrate && python3 manage.py runserver
    ```


Then the admin interface should be available at http://localhost:8000/admin/ where you can log in with the credentials in the ```.env``` file and create the sales_service user with its API key.
