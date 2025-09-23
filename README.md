# Prérequis

- Docker Desktop

# Cloner et préparer le dépôt

Clonez le dépôt sur votre machine locale.

Placez-vous à la racine du projet.

# Lancer Docker

Assurez-vous que Docker Desktop est bien lancé.

Démarrez les services avec :

```sh
docker-compose up
```

Une fois que le build est terminé, il est conseillé de faire un CTRL + C pour arrêter les conteneurs et relancer avec :

(-d pour ne pas bloquer un terminal avec docker)

```sh
docker-compose up -d
```

# Effectuer les migrations Django

## Option 1 :

Ouvrez un terminal dans le conteneur backend :

```sh
docker-compose exec -it django_api bash
```

Puis lancez les migrations :

```sh
python manage.py migrate
```

## Option 2 :

Lancez les migrations directement depuis le conteneur (en une ligne) :

```sh
docker-compose run --rm django_api python manage.py migrate
```

# Créer un super utilisateur Django

Ouvrez un terminal dans le conteneur backend :

```sh
docker-compose exec -it django_api bash
```

Puis lancez la commande :

```sh
python manage.py createsuperuser
```

Suivez les instructions (nom, mail, mot de passe)

# Accéder à l'admin

<http://localhost:8000/admin> (se connecter (entrer le juste le nom et le mdp))

# Commandes utiles

```sh
docker-compose up
docker-compose up -d
docker-compose exec -it django_api bash
python manage.py migrate
python manage.py createsuperuser
```