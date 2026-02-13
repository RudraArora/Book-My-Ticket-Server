# RA-BookMyShow-BE

 - Backend for the **BookMyShow Clone** project — a Django-based REST API for movie ticket booking.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/jtg-inductions-fe/RA-BookMyShow-BE
cd RA-BookMyShow-BE
```

### 2. Set up the Python environment

 - You can use either Pipenv or venv.

#### Option A: Using Pipenv (recommended)

```bash
pip install pipenv # Install pipenv if not already installed
pipenv shell # Activate virtual environment
pipenv install # Install dependencies from Pipfile
```

#### Option B: Using venv

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install pipenv # Optional, if you want to use pipenv inside venv
```

### 3. Setup PostgreSQL

 - Switch to postgres user:

```bash
sudo -i -u postgres
psql

Create a database and user (replace with your preferred names):
```

```bash
CREATE DATABASE book_my_show_db;
CREATE USER user_name WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE book_my_show_db TO user_name;

 - Exit psql:
 ```

```bash
\q
exit
```

### 4. Configure .env

 - Create a .env file at the root of the project:

```bash
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=db_name
DB_USER=user_name
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=port_number

 - You can use .env.template as a reference and rename it to .env.
```

### 5. Select Python interpreter in VS Code (if using VS Code)

 - Press Ctrl + Shift + P

 - Search for Python: Select Interpreter

 - Choose the interpreter from your virtual environment (e.g., ./.venv/bin/python or ./myenv/bin/python)


### 6. Run database migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```
