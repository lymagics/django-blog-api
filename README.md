# Blog API
Lightweight blogging API written in Python and Django.

## Resources:
 - Users
 - Posts
 - Tokens
 - Follows

## Deploy methods:
### Docker-compose development:
1. Create .env file
2. Fill in this file with variables from .env.example
3. Run command:
```
    docker-compose up -d
```
4. Apply database migrations:
```
    docker-compose exec web python manage.py migrate
```

### Docker-compose production:
1. Set up your environments variables
2. Run command:
```
    docker-compose -f docker-compose-prod.yml up -d
```
3. Apply database migrations:
```
    docker-compose exec web python manage.py migrate
```
