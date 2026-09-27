import sqlite3
import os

  # Ensure the uploads folder exists for images
if not os.path.exists("uploads"):
      os.makedirs("uploads")

def get_connection():
      """Returns a connection to the SQLite database."""
      return sqlite3.connect("store_data.db", check_same_thread=False)

def init_db():
      """Initializes the database and handles schema migrations."""
      conn = get_connection()
      cursor = conn.cursor()

      # 1. Create tables if they don't exist
      cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT UNIQUE,
                          password TEXT,
                          tier TEXT DEFAULT 'Free',
                          account_type TEXT DEFAULT 'Business')''')

      cursor.execute('''CREATE TABLE IF NOT EXISTS stores (
                          user_id INTEGER PRIMARY KEY,
                          store_name TEXT,
                          logo_path TEXT,
                          brand_color TEXT DEFAULT '#FFFFFF',
                          layout TEXT DEFAULT 'Grid',
                          animation_style TEXT DEFAULT 'Fade',
                          FOREIGN KEY(user_id) REFERENCES users(id))''')

      cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER,
                          name TEXT,
                          description TEXT,
                          price REAL,
                          link TEXT,
                          image_path TEXT,
                          FOREIGN KEY(user_id) REFERENCES users(id))''')

      cursor.execute('''CREATE TABLE IF NOT EXISTS personal_profiles (
                          user_id INTEGER PRIMARY KEY,
                          bio TEXT,
                          skills TEXT,
                          experience TEXT,
                          profile_image TEXT,
                          theme_color TEXT DEFAULT '#FFFFFF',
                          FOREIGN KEY(user_id) REFERENCES users(id))''')

      # 2. ROBUST MIGRATION: Fix for "table users has no column named account_type"
      # This checks the actual database file to see if the column is missing
      cursor.execute("PRAGMA table_info(users)")
      columns = [column[1] for column in cursor.fetchall()]

      if 'account_type' not in columns:
          try:
              cursor.execute("ALTER TABLE users ADD COLUMN account_type TEXT DEFAULT 'Business'")
              print("Migration: Added account_type column to users table.")
          except sqlite3.OperationalError as e:
              print(f"Migration failed: {e}")

      conn.commit()
      conn.close()

  # Call init_db immediately so the tables are ready as soon as the app starts
init_db()

def add_user(username, password, account_type='Business'):
      """Adds a new user to the database."""
      try:
          conn = get_connection()
          cursor = conn.cursor()
          cursor.execute("INSERT INTO users (username, password, account_type) VALUES (?, ?, ?)",
                         (username, password, account_type))
          conn.commit()
          conn.close()
          return True
      except sqlite3.IntegrityError:
          # This happens if the username already exists (UNIQUE constraint)
          return False

def verify_user(username, password):
      """Verifies user credentials and returns the user ID."""
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
      user = cursor.fetchone()
      conn.close()
      return user[0] if user else None

def update_store(user_id, name, color, layout, logo_path=None, animation='Fade'):
      """Updates or creates store details for a user."""
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("INSERT OR REPLACE INTO stores (user_id, store_name, brand_color, layout, logo_path, animation_style) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, name, color, layout, logo_path, animation))
      conn.commit()
      conn.close()

def update_profile(user_id, bio, skills, exp, color):
      """Updates or creates a personal profile for a user."""
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("INSERT OR REPLACE INTO personal_profiles (user_id, bio, skills, experience, theme_color) VALUES (?, ?, ?, ?, ?)",
                    (user_id, bio, skills, exp, color))
      conn.commit()
      conn.close()

def get_store_details(user_id):
      """Retrieves store configuration for a specific user."""
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM stores WHERE user_id = ?", (user_id,))
      data = cursor.fetchone()
      conn.close()
      return data

def add_product(user_id, name, desc, price, link, image_path):
      """Adds a product to a user's store."""
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("INSERT INTO products (user_id, name, description, price, link, image_path) VALUES (?, ?, ?, ?, ?, ?)",
                     (user_id, name, desc, price, link, image_path))
      conn.commit()
      conn.close()

def get_products(user_id):
      """Retrieves all products belonging to a user's store."""
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM products WHERE user_id = ?", (user_id,))
      rows = cursor.fetchall()
      conn.close()
      return rows

def get_all_premium_stores():
      """Retrieves stores belonging to users with 'Premium' tier."""
      conn = get_connection()
      cursor = conn.cursor()
      # Joins stores and users tables to filter by user tier
      cursor.execute("""
          SELECT stores.store_name, stores.logo_path, users.username
          FROM stores
          JOIN users ON stores.user_id = users.id
          WHERE users.tier = 'Premium'
      """)
      rows = cursor.fetchall()
      conn.close()
      return rows

def update_user_tier(user_id, tier):
      """Updates the subscription tier (e.g., 'Free' to 'Premium')."""
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("UPDATE users SET tier = ? WHERE id = ?", (tier, user_id))
      conn.commit()
      conn.close()