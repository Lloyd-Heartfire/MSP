# Prérequis

- Docker Desktop
- WSL2

# Cloner et préparer le dépôt

Clonez le dépôt sur votre machine locale dans WSL2

Placez-vous à la racine du projet.

# Lancer le Makefile afin d'initier le projet

Assurez-vous que Docker Desktop est bien lancé.

```sh
make init
```
cette commande va :
- Lancer Docker
- Effectuer les migrations Django
- Créer un super utilisateur Django

# Accéder à l'admin

<http://localhost:8000/admin>

# Accéder à la page front

<http://localhost:5173>

# Demarrer le projet

```sh
make start
```

# Commandes utiles

```sh
make init
make start
make stop
docker compose up
docker compose up -d
docker compose exec -it django_api bash
python manage.py migrate
python manage.py createsuperuser
```