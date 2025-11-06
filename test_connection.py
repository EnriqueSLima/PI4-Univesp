# test_connection.py
import os
import psycopg2
from urllib.parse import urlparse

print("🔍 Verificando variáveis de ambiente...")
db_url = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL: {db_url}")

if db_url:
    try:
        # Tentar conectar diretamente
        result = urlparse(db_url)
        print(f"Host: {result.hostname}")
        print(f"Database: {result.path[1:]}")
        print(f"User: {result.username}")
        
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        print(f"✅ PostgreSQL version: {cursor.fetchone()}")
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
else:
    print("❌ DATABASE_URL não encontrada")