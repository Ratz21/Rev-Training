"""
ETL for local demo HBO & PARAMOUNT
I have removed csv columns created by trailing commas  where spark names them( due to extra ,,, which it takes them as columns in here c16 to c19 )
columns that are empty have been removed basically

"""
import os, sys, argparse, glob, shutil, traceback, time
from pathlib import Path



# start spark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws

from etl_utils import base_schema, normalize_columns, parse_common_fields




os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk-21"
os.environ["SPARK_HOME"] = "D:\\Revature-Training\\Spark_Project\\spark\\.venv\\Lib\\site-packages\\pyspark"
os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable


def project_paths():
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    HBO_PATH = os.path.join(PROJECT_ROOT, "Dataset", "Hbo-dataset", "titles.csv")
    PARAMOUNT_PATH = os.path.join(PROJECT_ROOT, "Dataset", "Paramount-dataset", "titles.csv")
    data_for_viz = os.path.join(PROJECT_ROOT, "data", "for_viz")
    os.makedirs(data_for_viz, exist_ok=True)

    return PROJECT_ROOT, HBO_PATH, PARAMOUNT_PATH, data_for_viz


def run_etl(source):  # hbo or paramount

    PROJECT_ROOT, HBO_PATH, PARAMOUNT_PATH, data_for_viz = project_paths()

    raw_csv = os.path.join(
        PROJECT_ROOT,
        "Dataset",
        f"{source.capitalize()}-dataset",
        "titles.csv"
    )

    if not os.path.exists(raw_csv):
        raise FileNotFoundError(f"Raw CSV not found: {raw_csv}")

    spark = (
        SparkSession.builder
        .appName(f"{source.upper()}-ETL-LOCAL")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )

    # Read CSV with explicit schema
    schema = base_schema()
    df_raw = spark.read.csv(
        raw_csv,
        header=True,
        schema=schema,
        multiLine=True,
        escape='"',
        mode="DROPMALFORMED"
    )

    # Normalize column names
    df = normalize_columns(df_raw)

    print("[DEBUG] BEFORE parse_common_fields - columns:", df.columns[:15])  # Limit to first 15 columns
    print("[DEBUG] sample raw rows:")
    df.show(10, truncate=50, vertical=False)  # Limit to 10 rows, truncate to 50 chars

    # Parse extra fields
    df = parse_common_fields(df)

    # Select final columns and deduplicate
    # Convert array columns to strings for CSV compatibility (Spark CSV doesn't support ARRAY type)
    df_clean = df.select(
        "content_id", "title", "type", "description", "release_year",
        concat_ws(", ", col("genres_array")).alias("genres_array"),  # Convert array to comma-separated string
        "production_countries", "seasons", "imdb_id",
        "imdb_score", "imdb_votes", "tmdb_popularity", "tmdb_score", "duration_num"
    ).dropDuplicates(["content_id"])

    print(f"[{source}] raw rows: {df_raw.count()} -> cleaned rows: {df_clean.count()}")
    df_clean.show(10, truncate=50, vertical=False)  # Limit to 10 rows, truncate to 50 chars


    # WRITE CLEAN CSV OUTPUT

    tmp_dir = os.path.join(data_for_viz, f"{source}_clean_tmp")
    clean_csv = os.path.join(data_for_viz, f"{source}_clean.csv")

    # Ensure output directory exists
    os.makedirs(data_for_viz, exist_ok=True)

    # Convert for Spark (Windows-safe) - use forward slashes
    tmp_dir_posix = str(Path(tmp_dir).absolute()).replace("\\", "/")

    # Cleanup old temp directory
    if os.path.exists(tmp_dir):
        try:
            shutil.rmtree(tmp_dir)
        except Exception as e:
            print(f"[WARN] Cannot remove tmp dir {tmp_dir}: {e}")

    # Try Spark CSV write first
    spark_write_success = False
    try:
        print(f"[INFO] Spark writing to {tmp_dir_posix}")
        # Use coalesce(1) to write single file, and add options for better CSV compatibility
        df_clean.coalesce(1).write.mode("overwrite").option("header", "true").option("nullValue", "").option("quoteAll", "true").option("escape", "\\").option("quote", "\"").csv(tmp_dir_posix)

        # Wait a moment for file system to sync
        time.sleep(0.5)

        # Find the part file
        if os.path.exists(tmp_dir):
            part_files = [f for f in os.listdir(tmp_dir) if f.startswith("part-") and f.endswith(".csv")]
            if part_files:
                part_file = part_files[0]
                source_path = os.path.join(tmp_dir, part_file)
                shutil.move(source_path, clean_csv)
                # Clean up temp directory
                try:
                    shutil.rmtree(tmp_dir)
                except:
                    pass
                print(f"[SUCCESS] Clean CSV saved → {clean_csv}")
                spark_write_success = True
            else:
                raise RuntimeError(f"No CSV part file found in {tmp_dir}")
        else:
            raise RuntimeError(f"Temp directory {tmp_dir} was not created")

    except Exception as e:
        print(f"[ERROR] Spark CSV write failed: {e}")
        print("[INFO] Falling back to Pandas write method...")
        traceback.print_exc()
        
        # Clean up temp directory if it exists
        if os.path.exists(tmp_dir):
            try:
                shutil.rmtree(tmp_dir)
            except:
                pass

    # Fallback to Pandas if Spark write failed
    if not spark_write_success:
        try:
            pdf = df_clean.toPandas()
            # Write with proper CSV options to handle commas in text fields
            pdf.to_csv(clean_csv, index=False, quoting=1, escapechar='\\', quotechar='"')
            print(f"[FALLBACK] Clean CSV saved via Pandas → {clean_csv}")
        except Exception as e:
            print(f"[ERROR] Pandas fallback also failed: {e}")
            traceback.print_exc()
            raise RuntimeError(f"Failed to write CSV using both Spark and Pandas methods")

    print(f"[SUCCESS] Wrote cleaned CSV → {clean_csv}")

    spark.stop()
    print(f"[{source}] Wrote cleaned CSV: {clean_csv}")

    return clean_csv


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["hbo", "paramount"], required=True, help="catalog source")
    args = p.parse_args()

    run_etl(args.source)
