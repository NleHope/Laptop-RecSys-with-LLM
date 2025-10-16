# %%
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("PostgresJupyterTest")
    .master("local[*]")  # use all cores on your machine
    .config("spark.executor.memory", "2g")
    .config("spark.jars", "/home/nghia/Downloads/postgresql-42.2.29.jre7.jar")
    .getOrCreate()
)

spark


# %%
df = spark.read.csv("/media/nghia/G3 Plus/Work/Chatbot for selling product/chatbot-system/laptop_specs.csv", header=True, inferSchema=True)

# %%
from pyspark.sql.functions import col

rename_map = {
    "Loại card đồ họa": "gpu_type",
    "Dung lượng RAM": "ram_capacity",
    "Loại RAM": "ram_type",
    "Số khe ram": "ram_slots",
    "Ổ cứng": "storage",
    "Kích thước màn hình": "screen_size",
    "Công nghệ màn hình": "screen_tech",
    "Pin": "battery",
    "Hệ điều hành": "os",
    "Độ phân giải màn hình": "screen_resolution",
    "Loại CPU": "cpu_type",
    "Cổng giao tiếp": "ports",
    "Tần số quét": "refresh_rate",
    "Chất liệu tấm nền": "panel_material",
    "Công nghệ âm thanh": "audio_tech",
    "Tính năng đặc biệt": "special_features",
    "Loại đèn bàn phím": "keyboard_light",
    "Bảo mật": "security",
    "Webcam": "webcam",
    "Kích thước": "dimensions",
    "Trọng lượng": "weight",
    "Wi-Fi": "wifi",
    "Bluetooth": "bluetooth",
    "Khe đọc thẻ nhớ": "card_reader",
    "Chất liệu": "material",
    "Chất liệu vỏ trên": "upper_case_material",
    "Chất liệu vỏ dưới": "lower_case_material",
    "Chất liệu vỏ màn hình": "screen_case_material",
    "Loại màn hình": "screen_type",
    "Hãng sản xuất": "brand",
    "Nguồn": "power",
    "Chip AI": "ai_chip"
}

for old, new in rename_map.items():
    df = df.withColumnRenamed(old, new)


# %%
from pyspark.sql.functions import regexp_extract, regexp_replace, trim, when, length


def safe_cast(column, data_type):
    """Cast a column to the given type, returning NULL for empty strings."""
    return when(column.isNull() | (length(column) == 0), None).otherwise(column.cast(data_type))


# Price: "25.990.000₫" → 25990000
price_clean = regexp_replace(col("price"), "[^0-9]", "")
df = df.withColumn("price", safe_cast(price_clean, "long"))

# RAM capacity: "16 GB" → 16
ram_capacity_clean = regexp_extract(col("ram_capacity"), r"(\d+)", 1)
df = df.withColumn("ram_capacity", safe_cast(ram_capacity_clean, "int"))

# Screen size: "15.6 inch" → 15.6
screen_size_clean = regexp_extract(col("screen_size"), r"(\d+\.?\d*)", 1)
df = df.withColumn("screen_size", safe_cast(screen_size_clean, "double"))

# Weight: "1.6 kg" → 1.6
weight_clean = regexp_extract(col("weight"), r"(\d+\.?\d*)", 1)
df = df.withColumn("weight", safe_cast(weight_clean, "double"))

# Refresh rate: "144Hz" → 144
refresh_rate_clean = regexp_extract(col("refresh_rate"), r"(\d+)", 1)
df = df.withColumn("refresh_rate", safe_cast(refresh_rate_clean, "int"))


# %%
from pyspark.sql.functions import regexp_extract, lower, col

df.show(5, truncate=False)
df= df.drop("ram_type")
df.show(5, truncate=False)

storage_size_clean = regexp_extract(lower(col("storage")), r"(\d+)\s*gb", 1)
df = df.withColumn("storage_size_gb", safe_cast(storage_size_clean, "int"))
df = df.withColumn(
    "panel_material",
    regexp_extract(lower(col("panel_material")), r"(ips|sva|va|tn|oled|pl|wva)", 1)
)



# %%

numerical_cols = [
    "laptop_id", "price", "ram_capacity",
    "screen_size", "refresh_rate", "weight",
    "storage_size_gb", "brand", "ai_chip",
    "screen_resolution", "gpu_type", "cpu_type", "panel_material"
]

textual_cols = [
    "laptop_id", "product_name", "link", "screen_tech", "ram_slots",
    "battery", "os", "ports", "audio_tech", "special_features",
    "keyboard_light", "security", "webcam", "dimensions",
    "wifi", "bluetooth", "card_reader", "material",
    "upper_case_material", "lower_case_material",
    "screen_case_material", "screen_type", "power"
]

df_numeric = df.select(*numerical_cols)
df_textual = df.select(*textual_cols)
df_numeric.show(5, truncate=False)
df_textual.show(5, truncate=False)

# %%
pdf_textual = df_textual.toPandas()


# %%
# Add this cell at the end of your notebook to write df_numeric to PostgreSQL

from pyspark.sql import DataFrameWriter

# PostgreSQL connection properties
pg_url = "jdbc:postgresql://localhost:5432/laptop_db"  # Change to your DB name
pg_properties = {
    "user": "nghia",      # Change to your username
    "password": "nghia123",  # Change to your password
    "driver": "org.postgresql.Driver"
}

# Write df_numeric to PostgreSQL table 'laptop_numeric'
df_numeric.write.jdbc(
    url=pg_url,
    table="laptop_numeric",
    mode="overwrite",  # or "append"
    properties=pg_properties
)

# Write the full cleaned dataset to PostgreSQL table 'laptop_specs'
df.write.jdbc(
    url=pg_url,
    table="laptop_specs",
    mode="overwrite",
    properties=pg_properties
)



# %%
