init:    ##initialize the project
    @$(MAKE) stop
    @docker compose up -d --build
    @$(MAKE) migrate
    @docker compose exec  api python3 manage.py shell -c "from django.contrib.auth import get_user_model;User = get_user_model();user = User.objects.get(username='admin');user.set_password('admin');user.save()"

start:    ## start back + front
    @docker compose up -d

stop:    ## stop all containers
    @docker compose stop

migrate: ## apply migrations
    @docker compose exec  api python3 manage.py makemigrations
    @docker compose exec  api python3 manage.py migrate