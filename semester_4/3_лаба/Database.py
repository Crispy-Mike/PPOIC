import sqlite3
import hashlib
import random
import string


class Database:
    def __init__(self, db_name="hangman.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT,
                is_verified BOOLEAN DEFAULT 0,
                verification_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ban BOOLEAN DEFAULT 0
            )
        ''')

        # Таблица рекордов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                login TEXT,
                score INTEGER,
                game_mode TEXT,
                word_length INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Таблица статистики игр
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                games_played INTEGER DEFAULT 0,
                games_won INTEGER DEFAULT 0,
                games_lost INTEGER DEFAULT 0,
                total_score INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_verification_code(self):
        return 111111

    def register_user(self, login, email, password):
        try:
            hashed_password = self.hash_password(password)
            verification_code = self.generate_verification_code()

            self.cursor.execute('''
                INSERT INTO users (login, email, password, verification_code)
                VALUES (?, ?, ?, ?)
            ''', (login, email, hashed_password, verification_code))

            self.conn.commit()

            # Создаем статистику для пользователя
            user_id = self.cursor.lastrowid
            self.cursor.execute('''
                INSERT INTO game_stats (user_id) VALUES (?)
            ''', (user_id,))

            self.conn.commit()

            return {"success": True, "user_id": user_id, "code": verification_code}
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: users.login" in str(e):
                return {"success": False, "error": "Логин уже существует"}
            elif "UNIQUE constraint failed: users.email" in str(e):
                return {"success": False, "error": "Email уже зарегистрирован"}
            else:
                return {"success": False, "error": "Ошибка регистрации"}

    def verify_user(self, email, code):
        self.cursor.execute('''
            SELECT id FROM users 
            WHERE email = ? AND verification_code = ? AND is_verified = 0
        ''', (email, code))

        user = self.cursor.fetchone()
        if user:
            self.cursor.execute('''
                UPDATE users SET is_verified = 1, verification_code = NULL
                WHERE id = ?
            ''', (user[0],))
            self.conn.commit()
            return {"success": True}
        return {"success": False, "error": "Неверный код подтверждения"}

    def login_user(self, login, password):
        hashed_password = self.hash_password(password)

        self.cursor.execute('''
            SELECT id, login, email, is_verified, ban FROM users
            WHERE (login = ? OR email = ?) AND password = ?
        ''', (login, login, hashed_password))

        user = self.cursor.fetchone()
        if user:
            if user[4]:  # ban
                return {"success": False, "error": "Пользователь заблокирован"}
            if not user[3]:  # is_verified
                return {"success": False, "error": "Email не подтвержден"}

            return {
                "success": True,
                "user_id": user[0],
                "login": user[1],
                "email": user[2]
            }
        return {"success": False, "error": "Неверный логин или пароль"}

    def save_record(self, user_id, login, score, game_mode, word_length):
        self.cursor.execute('''
            INSERT INTO records (user_id, login, score, game_mode, word_length)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, login, score, game_mode, word_length))

        # Обновляем статистику
        self.cursor.execute('''
            UPDATE game_stats 
            SET games_played = games_played + 1,
                games_won = games_won + ?,
                total_score = total_score + ?
            WHERE user_id = ?
        ''', (1 if score > 0 else 0, score, user_id))

        self.conn.commit()

    def get_top_records(self, limit=10):
        self.cursor.execute('''
            SELECT login, score, game_mode, word_length, date 
            FROM records 
            ORDER BY score DESC, date DESC 
            LIMIT ?
        ''', (limit,))

        return self.cursor.fetchall()

    def get_user_stats(self, user_id):
        self.cursor.execute('''
            SELECT games_played, games_won, games_lost, total_score
            FROM game_stats WHERE user_id = ?
        ''', (user_id,))

        return self.cursor.fetchone()

    def close(self):
        self.conn.close()