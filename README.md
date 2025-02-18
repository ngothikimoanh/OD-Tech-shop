## Information about project

| Website Language | Program Language | Framework | Database      | Build     |
| ---------------- | ---------------- | --------- | ------------- | --------- |
| Vietnamese       | Python 3.12      | Django 5  | Postgresql 17 | Docker 27 |

<br>

## Prepair for project

> Step 1: Change directory to docker folder

```bash
cd docker
```

> Step 2: Copy `.env.example` in `docker` folder to `.env` file

```bash
cp .env.example .env
```

> Step 3: Create docker network

```bash
docker network create od-tech-shop_network
```

<br>

## Start project

> Run this command

```bash
cd docker && docker-compose up --build -d && cd ..
```

<br>

## Shutdown project

> Run this command

```bash
cd docker && docker-compose down && cd ..
```

<br>

## Note

> - The Django server loads the `.env` file from the `root` directory.
> - If not found, it loads from the `docker` directory.
> - If the file is not found in either location, a `FileNotFoundError` exception is raised, and the server **terminates**.

<br>

> - To make migrations. Run this command
>   ```bash
>   cd docker && docker-compose exec django bash -c "cd src && python manage.py makemigrations" && cd ..
>   ```

<br>

> - To migrate. Run this command
>   ```bash
>   cd docker && docker-compose exec django bash -c "cd src && python manage.py migrate" && cd ..
>   ```
