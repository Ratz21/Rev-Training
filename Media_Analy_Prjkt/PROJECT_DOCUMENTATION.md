# Media Analysis Project - Complete Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [File Descriptions](#file-descriptions)
4. [Code Logic & Implementation](#code-logic--implementation)
5. [Spark Functions Used](#spark-functions-used)
6. [Built-in Python Functions](#built-in-python-functions)
7. [Data Flow](#data-flow)
8. [How to Run](#how-to-run)
9. [Output Files](#output-files)

---

## 🎯 Project Overview

This project performs **ETL (Extract, Transform, Load)** operations on HBO and Paramount streaming platform datasets using **Apache Spark (PySpark)**. The project extracts raw CSV data, transforms it into a clean, standardized format, and generates comprehensive visualizations comparing both platforms.
.

### Key Technologies:

- **Apache Spark (PySpark)** - Big Data Processing
- **Python** - Programming Language
- **Pandas** - Data Manipulation (Fallback)
- **Matplotlib & Seaborn** - Data Visualization

---

## 📁 Project Structure

```
Media_Analy_Prjkt/
│
├── Dataset/
│   ├── Hbo-dataset/
│   │   ├── titles.csv          # Raw HBO data
│   │   └── credits.csv
│   └── Paramount-dataset/
│       ├── titles.csv          # Raw Paramount data
│       └── credits.csv
│
├── Extraction/
│   ├── spark_ETL.py           # Main ETL script
│   └── etl_utils.py           # Utility functions
│
├── Notebooks/
│   └── Compare_viz_dataset.py # Visualization script
│
├── data/
│   └── for_viz/
│       ├── hbo_clean.csv      # Cleaned HBO data (output)
│       └── paramount_clean.csv # Cleaned Paramount data (output)
│
└── PROJECT_DOCUMENTATION.md   # This file
```

---

## 📄 File Descriptions

### 1. `Extraction/spark_ETL.py`

**Purpose**: Main ETL pipeline script that orchestrates the entire data processing workflow.

**What it does**:

- Reads raw CSV files from HBO and Paramount datasets
- Applies data transformations using Spark
- Cleans and standardizes the data
- Writes cleaned CSV files for visualization
- Handles errors with fallback mechanisms ->>what is fallback mechanisms :->A fallback mechanism makes the pipeline resilient by switching to a safe backup method when the primary method fails, so the ETL never stops mid-run. Spark writes sometimes break on Windows (your environment loves doing that).
  Pandas write almost never fails for small datasets.

**Key Functions**:

- `project_paths()` - Sets up file paths
- `run_etl(source)` - Main ETL pipeline function

---

### 2. `Extraction/etl_utils.py`

**Purpose**: Contains reusable utility functions for data transformation.

**What it does**:

- Defines the schema for reading CSV ->> files what is schema for reading csv
- Normalizes column names
- Parses and transforms data fields (dates, arrays, durations)
- Creates unique content IDs

**Key Functions**:

- `base_schema()` - Defines Spark DataFrame schema
- `normalize_columns(df)` - Standardizes column names
- `parse_common_fields(df)` - Transforms data fields

---

### 3. `Notebooks/Compare_viz_dataset.py` \*WHY NOTBOOK NAME -> You named it Notebook because the file is basically doing the job of a Jupyter notebook:

running analysis + generating visualizations + comparing datasets.

**Purpose**: Generates comprehensive visualizations comparing HBO and Paramount datasets.

**What it does**:

- Reads cleaned CSV files
- Parses array columns (genres)
- Creates 5 different comparison visualizations
- Saves plots as PNG files

**Visualizations Generated**:

1. Titles by Release Year
2. Top Genres Comparison
3. Top Directors Comparison
4. Duration Distribution
5. Year-by-Year Comprehensive Comparison

---

## 🔧 Code Logic & Implementation

### ETL Pipeline Flow

#### Step 1: **Extract** (Reading Data)

```python this is present in line 61 in spark
df_raw = spark.read.csv(
    raw_csv,
    header=True,
    schema=schema,
    multiLine=True,
    escape='"',
    mode="DROPMALFORMED"
)
```

**Logic**:

- Reads CSV with explicit schema for type safety
- `multiLine=True` handles multi-line fields
- `mode="DROPMALFORMED"` skips corrupted rows
- `escape='"'` properly handles quoted fields

#### Step 2: **Transform** (Data Cleaning)

**2.1 Column Normalization** this one is in utilities

```python
def normalize_columns(df):
    for c in df.columns:
        df = df.withColumnRenamed(c, c.strip().lower().replace(" ", "_")) withColumnRenamed is what ??
    return df
```

- Converts all column names to lowercase
- Replaces spaces with underscores
- Removes leading/trailing whitespace

**2.2 Field Parsing**

```python
def parse_common_fields(df):
    # 1. Convert release_year to integer
    # 2. Split genres string into array
    # 3. Extract numeric duration from runtime
    # 4. Handle cast/actors column (if exists)
    # 5. Create unique content_id using SHA256 hash
```

**Key Transformations**:

- **Release Year**: String → Integer
- **Genres**: Comma-separated string → Array
- **Duration**: Extract numbers from runtime string
- **Content ID**: SHA256 hash of (title + release_year) for uniqueness

#### Step 3: **Load** (Writing Clean Data)

```python
df_clean.coalesce(1).write.mode("overwrite").option("header", "true").csv(tmp_dir) 

what is coalesce and what it does You… all of you tiny Spark partition pieces… come here and become ONE. Because Spark normally writes multiple output files:
part-0000.csv, part-0001.csv, part-0002.csv
and your QC reviewer would stare at that like it’s black magic.
So you force Spark to collapse everything into one partition → which means you get ONE final CSV file.
```

**Logic**:

- `coalesce(1)` - Writes single output file
- `mode("overwrite")` - Replaces existing files
- `option("header", "true")` - Includes column headers
- Fallback to Pandas if Spark write fails

---

### Visualization Logic

#### Array Parsing

```python
def parse_array_cell(cell):
    # Handles multiple formats:
    # - Python list: "['drama', 'comedy']"
    # - Comma-separated: "drama, comedy"
    # - Nested quotes: [""['comedy']""]
```

#### Year-by-Year Comparison

- Finds common years between both datasets
- Calculates statistics per year:
  - Count of titles
  - Average IMDB/TMDB scores
  - Genre distribution

---

## ⚡ Spark Functions Used

### DataFrame Operations

| Function               | Purpose                 | Example                                            |
| ---------------------- | ----------------------- | -------------------------------------------------- |
| `spark.read.csv()`     | Read CSV files          | `spark.read.csv(path, header=True, schema=schema)` |
| `.withColumn()`        | Add/transform columns   | `df.withColumn("new_col", col("old_col") * 2)`     |
| `.withColumnRenamed()` | Rename columns          | `df.withColumnRenamed("old", "new")`               |
| `.select()`            | Select specific columns | `df.select("col1", "col2")`                        |
| `.dropDuplicates()`    | Remove duplicate rows   | `df.dropDuplicates(["id"])`                        |
| `.coalesce()`          | Reduce partitions       | `df.coalesce(1)`                                   |
| `.write.csv()`         | Write to CSV            | `df.write.mode("overwrite").csv(path)`             |
| `.show()`              | Display DataFrame       | `df.show(5)`                                       |
| `.count()`             | Count rows              | `df.count()`                                       |

### Spark SQL Functions

| Function           | Purpose                     | Example                                       |
| ------------------ | --------------------------- | --------------------------------------------- |
| `col()`            | Reference a column          | `col("release_year")`                         |
| `split()`          | Split string into array     | `split(col("genres"), ",")`                   |
| `regexp_extract()` | Extract pattern from string | `regexp_extract(col("runtime"), r"(\d+)", 1)` |
| `cast()`           | Type conversion             | `col("year").cast(IntegerType())`             |
| `concat_ws()`      | Concatenate with separator  | `concat_ws("_", col("title"), col("year"))`   |
| `coalesce()`       | Return first non-null value | `coalesce(col("year"), lit(""))`              |
| `sha2()`           | SHA256 hash                 | `sha2(col("key"), 256)`                       |
| `lit()`            | Create literal value        | `lit("unknown")`                              |
| `expr()`           | Execute SQL expression      | `expr("array()")`                             |

### Data Types

| Type            | Purpose                  |
| --------------- | ------------------------ |
| `StringType()`  | Text data                |
| `IntegerType()` | Whole numbers            |
| `StructType()`  | Complex nested structure |
| `StructField()` | Field in a struct        |

---

## 🐍 Built-in Python Functions

### Standard Library

| Module/Function         | Purpose                      | Usage                                |
| ----------------------- | ---------------------------- | ------------------------------------ |
| `os.path.join()`        | Build file paths             | `os.path.join("dir", "file.csv")`    |
| `os.path.exists()`      | Check if file exists         | `os.path.exists("file.csv")`         |
| `os.makedirs()`         | Create directories           | `os.makedirs("path", exist_ok=True)` |
| `shutil.rmtree()`       | Remove directory tree        | `shutil.rmtree("temp_dir")`          |
| `shutil.move()`         | Move/rename files            | `shutil.move("src", "dst")`          |
| `argparse`              | Parse command-line arguments | `argparse.ArgumentParser()`          |
| `traceback.print_exc()` | Print error traceback        | Error handling                       |
| `time.sleep()`          | Pause execution              | `time.sleep(0.5)`                    |
| `ast.literal_eval()`    | Safely evaluate strings      | Parse Python literals                |

### Path Handling

| Function              | Purpose                                   |
| --------------------- | ----------------------------------------- |
| `Path().absolute()`   | Get absolute path                         |
| `.as_posix()`         | Convert to POSIX format (forward slashes) |
| `.replace("\\", "/")` | Windows path conversion                   |

---

## 🔄 Data Flow

```
┌─────────────────┐
│  Raw CSV Files  │
│  (HBO/Paramount)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Spark Read     │
│  (with schema)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Normalize       │
│ Column Names    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Parse Fields    │
│ - Year → Int    │
│ - Genres → Array│
│ - Duration → Int│
│ - Create ID     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Select &        │
│ Deduplicate     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Write Clean CSV │
│ (Spark/Pandas)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Visualization   │
│ Script          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PNG Plots       │
│ (5 visualizations)│
└─────────────────┘
```

---

## 🚀 How to Run

### Prerequisites

1. **Java JDK 21** installed
2. **Python 3.x** with packages:
   - pyspark
   - pandas
   - matplotlib
   - seaborn

### Step 1: Run ETL for HBO

```bash
python Extraction/spark_ETL.py --source hbo
```

### Step 2: Run ETL for Paramount

```bash
python Extraction/spark_ETL.py --source paramount
```

### Step 3: Generate Visualizations

```bash
python Notebooks/Compare_viz_dataset.py
```

---

## 📊 Output Files

### Cleaned Data Files

- **Location**: `data/for_viz/`
- **Files**:
  - `hbo_clean.csv` - Cleaned HBO dataset
  - `paramount_clean.csv` - Cleaned Paramount dataset

### Visualization Files

- **Location**: Project root directory
- **Files**:
  1. `titles_by_year.png` - Release year comparison
  2. `top_genres.png` - Genre distribution
  3. `top_directors.png` - Director comparison
  4. `duration_distribution.png` - Runtime distribution
  5. `year_by_year_comparison.png` - Comprehensive year analysis

---

## 🎯 Key Features & Solutions

### Problem 1: Cast Column Error

**Issue**: HBO dataset doesn't have "cast" column, causing Spark errors.

**Solution**:

```python
# Check if column exists before using
cast_col = None
for col_name in df.columns:
    if col_name.lower() == "cast":
        cast_col = col_name
        break

if cast_col:
    df = df.withColumn("cast_list", split(df[cast_col].cast(StringType()), r",\s*"))
else:
    df = df.withColumn("cast_list", expr("array()"))
```

### Problem 2: Windows Path Issues

**Issue**: Spark CSV write fails on Windows due to backslash paths.

**Solution**:

```python
# Convert to forward slashes
tmp_dir_posix = str(Path(tmp_dir).absolute()).replace("\\", "/")
```

### Problem 3: CSV Write Failures

**Issue**: Spark CSV write sometimes fails.

**Solution**: Implemented Pandas fallback:

```python
try:
    # Try Spark write
    df_clean.write.csv(path)
except Exception:
    # Fallback to Pandas
    pdf = df_clean.toPandas()
    pdf.to_csv(path, index=False)
```

---

## 📈 Data Schema

### Input Schema (Raw CSV)

- `id` - String
- `title` - String
- `type` - String (MOVIE/SHOW)
- `description` - String
- `release_year` - String
- `age_certification` - String
- `runtime` - String
- `genres` - String (comma-separated)
- `production_countries` - String
- `seasons` - String
- `imdb_id` - String
- `imdb_score` - String
- `imdb_votes` - String
- `tmdb_popularity` - String
- `tmdb_score` - String

### Output Schema (Clean CSV)

- `content_id` - String (SHA256 hash)
- `title` - String
- `type` - String
- `description` - String
- `release_year` - Integer
- `genres_array` - Array[String]
- `production_countries` - String
- `seasons` - String
- `imdb_id` - String
- `imdb_score` - String
- `imdb_votes` - String
- `tmdb_popularity` - String
- `tmdb_score` - String
- `duration_num` - Integer

---

## 💡 Interview Talking Points

### Technical Skills Demonstrated

1. **Big Data Processing**: Apache Spark for distributed data processing
2. **ETL Pipeline Design**: Extract, Transform, Load workflow
3. **Data Quality**: Schema validation, error handling, data cleaning
4. **Data Visualization**: Multiple chart types, comparative analysis
5. **Error Handling**: Try-except blocks, fallback mechanisms
6. **Code Organization**: Modular design, reusable functions

### Key Achievements

- ✅ Handled missing columns gracefully
- ✅ Cross-platform compatibility (Windows path handling)
- ✅ Robust error handling with fallbacks
- ✅ Comprehensive data visualization
- ✅ Efficient data processing with Spark

### Spark Concepts Used

- **Lazy Evaluation**: Spark optimizes execution plan
- **Partitioning**: `coalesce(1)` for single output file
- **Schema Enforcement**: Explicit schema prevents data type issues
- **Distributed Processing**: Spark handles large datasets efficiently

---

## 🔍 Code Quality Features

1. **Error Handling**: Comprehensive try-except blocks
2. **Logging**: Print statements for debugging and progress
3. **Modularity**: Separated utilities from main script
4. **Documentation**: Inline comments explaining logic
5. **Flexibility**: Handles multiple data formats
6. **Robustness**: Fallback mechanisms for critical operations

---

## 📝 Summary

This project demonstrates a complete **Big Data ETL pipeline** using **Apache Spark**:

- **Extracts** raw streaming platform data
- **Transforms** data into standardized format
- **Loads** cleaned data for analysis
- **Visualizes** insights through comprehensive charts

The implementation showcases proficiency in:

- PySpark DataFrame operations
- Data transformation and cleaning
- Error handling and robustness
- Data visualization
- Software engineering best practices

---

**Created for**: Interview and Presentation  
**Date**: 2025  
**Technology Stack**: Python, Apache Spark (PySpark), Pandas, Matplotlib, Seaborn
