import psycopg2

# Connection details
conn = psycopg2.connect(
    host="localhost",       # or IP of your PostgreSQL server
    database="laptop_db", # name of your database
    user="nghia",
    password="12345",   # your PostgreSQL user
    port=5432               # default PostgreSQL port
)

# Create a cursor
cur = conn.cursor()

# Example: Create a table
cur.execute("""
    CREATE TABLE IF NOT EXISTS laptops (
        id SERIAL PRIMARY KEY,
        brand VARCHAR(50),
        model VARCHAR(50),
        ram_gb INT,
        price DECIMAL
    )
""")

# Example: Insert a row
cur.execute(
    "INSERT INTO laptops (brand, model, ram_gb, price) VALUES (%s, %s, %s, %s)",
    ("Lenovo", "ThinkPad X1", 16, 1299.99)
)

# Commit changes
conn.commit()

# Query
cur.execute("SELECT * FROM laptops;")
rows = cur.fetchall()
for row in rows:
    print(row)

# Close
cur.close()
conn.close()
