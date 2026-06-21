DATABASES = {
    "postgresql": {
        "host": "localhost",
        "database": "streaming_db",
        "user": "postgres",
        "password": "postgres",
        "port": "5432"
    },
    "mysql": {
        "host": "localhost",
        "database": "streaming_db",
        "user": "root",
        "password": "password",
        "port": "3306"
    },
    "mongodb": {
        "host": "localhost",
        "port": 27017,
        "database": "streaming_db"
    }
}

SQL_TEMPLATES = {
    "create_users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL,
            registration_date DATE DEFAULT CURRENT_DATE,
            subscription_type VARCHAR(50) DEFAULT 'basic'
        )
    """,

    "create_genres": """
        CREATE TABLE IF NOT EXISTS genres (
            genre_id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        )
    """,

    "create_videos": """
        CREATE TABLE IF NOT EXISTS videos (
            video_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            duration INTEGER,
            upload_date DATE DEFAULT CURRENT_DATE,
            user_id INTEGER REFERENCES users(user_id)
        )
    """,

    "create_video_genres": """
        CREATE TABLE IF NOT EXISTS video_genres (
            video_id INTEGER REFERENCES videos(video_id),
            genre_id INTEGER REFERENCES genres(genre_id),
            PRIMARY KEY (video_id, genre_id)
        )
    """
}

# MySQL специфичные шаблоны
MYSQL_TEMPLATES = {
    "create_users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL,
            registration_date DATE DEFAULT (CURRENT_DATE),
            subscription_type VARCHAR(50) DEFAULT 'basic'
        )
    """,

    "create_genres": """
        CREATE TABLE IF NOT EXISTS genres (
            genre_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        )
    """,

    "create_videos": """
        CREATE TABLE IF NOT EXISTS videos (
            video_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            duration INTEGER,
            upload_date DATE DEFAULT (CURRENT_DATE),
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """
}
