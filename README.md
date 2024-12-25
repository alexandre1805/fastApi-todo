
# Todo API

Une API permettant d'apprendre à utiliser le framework FastAPI. Cette API comporte une intégration avec `Keycloak` et une base de données relationnelle de type `SQL`.


## Installation

Le projet necessite la version python 3.10 ou plus.

```bash
  pip install -r requirements.txt
```


## Démarrer en local

Cloner le projet :

```bash
  git clone git@github.com:alexandre1805/fastApi-todo.git
```

Aller dans le dossier du projet :

```bash
  cd fastApi-todo
```

Créer un environnement virtuel :
```bash
  python -m venv venv
  source ./venv/bin/activate
```

Installer les dépendances :

```bash
  pip install -r requirements.txt
```

Ajouter les variables d'environnement :
```bash
  cp .env.example .env
```

Démarrer le serveur :

```bash
  fastapi dev app/main.py
```
La documentation se trouve à l'adresse suivante : http://localhost:8000/docs
