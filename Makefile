init:    ##initialize the project
	@$(MAKE) stop
	@docker compose up -d --build
	@$(MAKE) migrate
	@docker compose exec -e DJANGO_SUPERUSER_PASSWORD=admin django_api python manage.py createsuperuser --noinput --email admin@admin.com --username admin
start:    ## start back + front
	@docker compose up -d

stop:    ## stop all containers
	@docker compose stop

migrate: ## apply migrations
	@docker compose exec -it django_api python manage.py makemigrations
	@docker compose exec -it django_api python manage.py migrate