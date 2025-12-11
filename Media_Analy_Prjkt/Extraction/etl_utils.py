"""

- base_schema(): returns the CSV schema
- normalize_columns(df): column name normalization
- parse_common_fields(df): parse dates, arrays, duration, and create content_id

"""

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

from pyspark.sql.functions import( col, split, regexp_extract, lit, concat_ws ,coalesce, sha2, expr)


def base_schema():
    return StructType([

        StructField("id", StringType(), True), #defines a column in Spark’s schema:
        StructField("title", StringType(), True),
        StructField("type", StringType(), True),
        StructField("description", StringType(), True),
        StructField("release_year", StringType(),True),
        StructField("age_certification", StringType(), True),
        StructField("runtime",StringType(), True),
        StructField("genres",StringType(),True),
        StructField("production_countries", StringType(), True),
        StructField("seasons", StringType(), True),
        StructField("imdb_id", StringType(), True),
        StructField("imdb_score" , StringType(), True),
        StructField("imdb_votes", StringType(), True),
        StructField("tmdb_popularity", StringType(), True),
        StructField("tmdb_score", StringType(),True),

    ])


""" Normalize column names to snake_case and lowercase.
    Example: "Release Year" -> "release_year"""

def normalize_columns(df): #A new DataFrame where all column names have been cleaned up into a predictable, machine-friendly format.
    for c in df.columns:
        df = df.withColumnRenamed(c,c.strip().lower().replace(" ", "_")) #strip -> removes whitespaces #lower converted to lower "" spaces replaces with underscore
    return df


""" convert release_year to int
    - parse date-like fields if present (not required for these datasets)
    - split genres string into an array (comma-separated)
    - extract numeric runtime/duration
    - create a stable content_id (sha2 of title+release_year)"""


def parse_common_fields(df):
    if df is None:
        raise ValueError("parse_common_fields received None for df")

        # DEBUG: show columns (remove later)
    print("[DEBUG parse_common_fields] incoming columns:", df.columns[:60])

    # 1) release_year -> integer if present
    if "release_year" in df.columns:
        df = df.withColumn("release_year", col("release_year").cast(IntegerType()))

    # 2) genres_array: support multiple possible source columns
    genres_src = next((c for c in ("genres_array", "listed_in", "genres") if c in df.columns), None)
    if genres_src:
        df = df.withColumn("genres_array", split(col(genres_src).cast(StringType()), r",\s*"))
    else:
        # create a true empty array using SQL expression (safe across Spark versions)
        df = df.withColumn("genres_array", expr("array()"))

    # 3) duration_num: try runtime or duration (extract numbers)
    runtime_src = next((c for c in ("runtime", "duration") if c in df.columns), None)
    if runtime_src:
        df = df.withColumn("duration_num",
                           regexp_extract(col(runtime_src).cast(StringType()), r"(\d+)", 1).cast(IntegerType()))
    else:
        df = df.withColumn("duration_num", lit(None).cast(IntegerType()))

    # 4) cast/actors -> standardized cast_list
    # Handle potential conflicts with SQL 'cast' function by using df[column] syntax
    cast_col = None
    for col_name in df.columns:
        if col_name.lower() == "cast":
            cast_col = col_name
            break
    
    if cast_col:
        # Use df[column] syntax to avoid conflict with SQL cast function
        df = df.withColumn("cast_list", split(df[cast_col].cast(StringType()), r",\s*"))
    elif "actors" in df.columns:
        df = df.withColumn("cast_list", split(col("actors").cast(StringType()), r",\s*"))
    else:
        # safe empty array fallback
        df = df.withColumn("cast_list", expr("array()"))

    # 5) stable key and content_id (title+year preferred)
    if "title" in df.columns:
        df = df.withColumn("content_key",
                           concat_ws("_", col("title").cast(StringType()),
                                     coalesce(col("release_year").cast(StringType()), lit(""))))
    elif "id" in df.columns:
        df = df.withColumn("content_key", col("id").cast(StringType()))
    else:
        df = df.withColumn("content_key", lit("unknown"))

    df = df.withColumn("content_id", sha2(col("content_key"), 256))

    # final
    if df is None:
        raise RuntimeError("parse_common_fields failed: resulting df is None")

    return df










