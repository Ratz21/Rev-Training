"""
Compare HBO vs Paramount cleaned CSVs (produced by the ETL script).
Generates and saves PNG plots:
 - titles_by_year.png
 - top_genres.png
 - top_directors.png for error handling displays nothing
 - duration_distribution.png
 -
"""


import os, ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "for_viz")
OUTPUT_DIR = PROJECT_ROOT  # Save plots to project root
HBO_CSV = os.path.join(DATA_DIR, "hbo_clean.csv")
PARAM_CSV = os.path.join(DATA_DIR, "paramount_clean.csv")


def read_clean_csv(path):
    """Read the Spark-produced CSV and normalize array-columns into Python lists safely."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Clean CSV missing: {path}. Run the Spark ETL first.")
    
    # Read CSV with error handling and encoding options
    # Handle malformed CSV with inconsistent column counts
    try:
        # Try reading with error handling for bad lines
        df = pd.read_csv(
            path, 
            encoding='utf-8', 
            low_memory=False,
            on_bad_lines='skip',  # Skip malformed lines
            quoting=1,  # QUOTE_ALL - treat all fields as quoted
            escapechar='\\',
            quotechar='"',
            skipinitialspace=True
        )
    except Exception as e1:
        try:
            # Fallback: Try with different encoding
            df = pd.read_csv(
                path, 
                encoding='latin-1', 
                low_memory=False,
                on_bad_lines='skip',
                quoting=1,
                escapechar='\\',
                quotechar='"',
                skipinitialspace=True
            )
        except Exception as e2:
            try:
                # Last resort: Use engine='python' which is more lenient
                df = pd.read_csv(
                    path,
                    encoding='utf-8',
                    engine='python',
                    on_bad_lines='skip',
                    quoting=1,
                    quotechar='"',
                    skipinitialspace=True
                )
            except Exception as e3:
                print(f"[ERROR] Failed to read CSV {path}")
                print(f"[ERROR] UTF-8 attempt: {e1}")
                print(f"[ERROR] Latin-1 attempt: {e2}")
                print(f"[ERROR] Python engine attempt: {e3}")
                raise

# genres_array might be stored as "['drama', 'comedy']" or as "drama, comedy" or with nested quotes
    def parse_array_cell(cell):
        if pd.isna(cell):
            return []
        s = str(cell).strip()
        if not s or s == 'nan':
            return []
        
        # Handle nested quotes like [""['comedy'"", ""'drama']""]
        # First, try to clean up double-escaped quotes
        s = s.replace('""', '"').replace("''", "'")
        
        if s.startswith("[") and s.endswith("]"):
            # safe evaluation of Python list literal
            try:
                result = ast.literal_eval(s) # ast means abstract module which handles programmatically abt the current grammar situation
                # Ensure result is a list
                if isinstance(result, list):
                    # Clean up any nested lists or extra quotes
                    cleaned = []
                    for item in result:
                        if isinstance(item, str):
                            cleaned.append(item.strip().strip("'\"[]"))
                        elif isinstance(item, list):
                            cleaned.extend([str(x).strip().strip("'\"") for x in item])
                        else:
                            cleaned.append(str(item).strip())
                    return [x for x in cleaned if x]
                return [str(result).strip()] if result else []
            except Exception:
                # Manual parsing fallback
                content = s.strip("[]")
                items = [x.strip().strip("'\"[]") for x in content.split(",") if x.strip()]
                return [x for x in items if x]
        # if comma-separated string (new format from Spark - genres are now comma-separated)
        if "," in s:
            # Split by comma and clean each item
            items = [x.strip().strip("'\"[]") for x in s.split(",") if x.strip()]
            return [x for x in items if x and x.lower() != 'nan']
        # Single value
        cleaned = s.strip().strip("'\"[]")
        return [cleaned] if cleaned and cleaned.lower() != 'nan' else []

    if "genres_array" in df.columns:
        df["genres_array"] = df["genres_array"].apply(parse_array_cell)
        # Also ensure director field exists (some datasets use different field names)
    if "director" in df.columns:
        df["director"] = df["director"].fillna("").astype(str)
    return df


# read data with error handling
try:
    print(f"[INFO] Reading HBO data from {HBO_CSV}...")
    hbo = read_clean_csv(HBO_CSV)
    print(f"[INFO] HBO data loaded: {len(hbo)} rows, {len(hbo.columns)} columns")
except Exception as e:
    print(f"[ERROR] Failed to load HBO data: {e}")
    raise

try:
    print(f"[INFO] Reading Paramount data from {PARAM_CSV}...")
    param = read_clean_csv(PARAM_CSV)
    print(f"[INFO] Paramount data loaded: {len(param)} rows, {len(param.columns)} columns")
except Exception as e:
    print(f"[ERROR] Failed to load Paramount data: {e}")
    raise


# ---------- Plot 1: Titles by Release Year (top 20 years combined) ----------
def titles_by_year(df):
    if "release_year" not in df.columns:
        return pd.Series(dtype=int)
    return df["release_year"].dropna().astype(int).value_counts().sort_index()

h_years = titles_by_year(hbo)
p_years = titles_by_year(param)
years_df = pd.concat([h_years.rename("HBO"), p_years.rename("Paramount")], axis=1).fillna(0).astype(int)

# Filter out unwanted years (1912, 1913, 1914, 2023)
years_to_remove = [1912, 1913, 1914, 2023]
years_df = years_df[~years_df.index.isin(years_to_remove)]

plt.figure(figsize=(12,6)) #  make a single plot sub plot or single plot change it in bar plot mention axis diff
# plot last 30 years if available
years_to_plot = years_df.index.max() - 30 if pd.notna(years_df.index.max()) else None
years_df.tail(30).plot(kind="bar") # behind the scene it create one axis and on that it has plotted to bar charts instead of me typing axis 1 and all
plt.title("Titles by Release Year — HBO vs Paramount (last 30 years)")
plt.ylabel("Count")
plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, "titles_by_year.png")
plt.savefig(output_path)
print(f"Saved: {output_path}")
plt.show()
plt.close()
#x axis release years (1993 - 2022)
#y axis count of titles released



# ---------- Plot 2: Top Genres (explode and count) ----------
def top_genres(df, top_n=15):
    if "genres_array" not in df.columns:
        return pd.Series(dtype=int) # So basically one row per genre make it easier for count as Movie a title ex
    exploded = df.explode("genres_array") # expands array/list column into multiple rows one per genre
    exploded["genres_array"] = exploded["genres_array"].astype(str).str.strip()
    return exploded["genres_array"].value_counts().head(top_n)

h_gen = top_genres(hbo, top_n=20)
p_gen = top_genres(param, top_n=20)
genres_df = pd.concat([h_gen.rename("HBO"), p_gen.rename("Paramount")], axis=1).fillna(0).astype(int)

plt.figure(figsize=(12,6))
genres_df.head(15).plot(kind="bar")
plt.title("Top Genres — HBO vs Paramount")
plt.ylabel("Count")
plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, "top_genres.png")
plt.savefig(output_path)
print(f"Saved: {output_path}")
plt.show()



# ---------- Plot 3: Top Directors ----------
print("\n[INFO] Checking for director data...")
print(f"[INFO] HBO columns: {list(hbo.columns)}")
print(f"[INFO] Paramount columns: {list(param.columns)}")

def top_directors(df, top_n=10):
    if "director" not in df.columns:
        print(f"[INFO] 'director' column not found in dataset")
        return pd.Series(dtype=int)
    # Check if director column has any non-empty data
    director_data = df["director"].fillna("").astype(str)
    non_empty = director_data[director_data != ""]
    if len(non_empty) == 0:
        print(f"[INFO] 'director' column exists but contains no data")
        return pd.Series(dtype=int)
    # Split directors (comma-separated list), explode and count
    s = director_data.str.split(",").explode().str.strip()
    s = s[s != ""]
    if len(s) == 0:
        return pd.Series(dtype=int)
    return s.value_counts().head(top_n)

h_dir = top_directors(hbo, 10)
p_dir = top_directors(param, 10)
directors_df = pd.concat([h_dir.rename("HBO"), p_dir.rename("Paramount")], axis=1).fillna(0).astype(int)

plt.figure(figsize=(12,6))
if not directors_df.empty and directors_df.sum().sum() > 0:
    directors_df.plot(kind="bar")
    plt.title("Top Directors — HBO vs Paramount (Top 10)")
    plt.ylabel("Count")
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "top_directors.png")
    plt.savefig(output_path)
    print(f"Saved: {output_path}")
    plt.show()
else:
    print("[INFO] Director data not available in titles.csv - skipping directors plot")
    print("[INFO] Note: Director information may be available in credits.csv files, but is not included in the current ETL pipeline")
    # Create a placeholder message plot
    plt.text(0.5, 0.5, 'Director data not available\nin titles.csv dataset', 
             ha='center', va='center', transform=plt.gca().transAxes, 
             fontsize=14, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.title("Top Directors — HBO vs Paramount (Data Not Available)")
    plt.axis('off')
    output_path = os.path.join(OUTPUT_DIR, "top_directors.png")
    plt.savefig(output_path)
    print(f"Saved placeholder: {output_path}")
    plt.show()



# ---------- Plot 4: Duration Distribution (Side-by-Side) ----------
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Duration Distribution (minutes) — HBO vs Paramount", fontsize=14, fontweight='bold')

# Left subplot: HBO
ax1 = axes[0]
if "duration_num" in hbo.columns:
    hbo_durations = hbo["duration_num"].dropna()
    if len(hbo_durations) > 0:
        ax1.hist(hbo_durations, bins=30, alpha=0.7, color='#1f77b4', edgecolor='black')
        ax1.set_title("HBO Duration Distribution", fontweight='bold')
        ax1.set_xlabel("Duration (minutes)")
        ax1.set_ylabel("Count")
        ax1.grid(axis='y', alpha=0.3)
    else:
        ax1.text(0.5, 0.5, 'No duration data available', ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title("HBO Duration Distribution")
else:
    ax1.text(0.5, 0.5, 'No duration data available', ha='center', va='center', transform=ax1.transAxes)
    ax1.set_title("HBO Duration Distribution")

# Right subplot: Paramount
ax2 = axes[1]
if "duration_num" in param.columns:
    param_durations = param["duration_num"].dropna()
    if len(param_durations) > 0:
        ax2.hist(param_durations, bins=30, alpha=0.7, color='#ff7f0e', edgecolor='black')
        ax2.set_title("Paramount Duration Distribution", fontweight='bold')
        ax2.set_xlabel("Duration (minutes)")
        ax2.set_ylabel("Count")
        ax2.grid(axis='y', alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'No duration data available', ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title("Paramount Duration Distribution")
else:
    ax2.text(0.5, 0.5, 'No duration data available', ha='center', va='center', transform=ax2.transAxes)
    ax2.set_title("Paramount Duration Distribution")

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, "duration_distribution.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Saved: {output_path}")
plt.show()

# ---------- Plot 5: Year-by-Year Comparison (Movies Count, Scores, Genres) ----------
print("\n[INFO] Generating comprehensive year-by-year comparison...")

# Filter to common years where both have data
hbo_years = set(hbo["release_year"].dropna().astype(int).unique()) if "release_year" in hbo.columns else set()
param_years = set(param["release_year"].dropna().astype(int).unique()) if "release_year" in param.columns else set()
common_years = sorted(list(hbo_years.intersection(param_years)))

if len(common_years) > 0:
    # Create a comprehensive comparison figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("HBO vs Paramount: Comprehensive Year-by-Year Comparison", fontsize=16, fontweight='bold')
    
    # Subplot 1: Number of titles per year (side-by-side bars)
    ax1 = axes[0, 0]
    hbo_year_counts = hbo[hbo["release_year"].isin(common_years)]["release_year"].value_counts().sort_index()
    param_year_counts = param[param["release_year"].isin(common_years)]["release_year"].value_counts().sort_index()
    
    # Align the series
    all_years = sorted(set(hbo_year_counts.index) | set(param_year_counts.index))
    
    # Limit to last 30 years for better readability, or all years if less than 30
    if len(all_years) > 30:
        all_years = all_years[-30:]  # Show last 30 years
        hbo_year_counts = hbo_year_counts[hbo_year_counts.index.isin(all_years)]
        param_year_counts = param_year_counts[param_year_counts.index.isin(all_years)]
    
    hbo_counts_aligned = [hbo_year_counts.get(year, 0) for year in all_years]
    param_counts_aligned = [param_year_counts.get(year, 0) for year in all_years]
    
    x = range(len(all_years))
    width = 0.35
    ax1.bar([i - width/2 for i in x], hbo_counts_aligned, width, label='HBO', alpha=0.8, color='#1f77b4')
    ax1.bar([i + width/2 for i in x], param_counts_aligned, width, label='Paramount', alpha=0.8, color='#ff7f0e')
    ax1.set_xlabel('Release Year', fontsize=10)
    ax1.set_ylabel('Number of Titles', fontsize=10)
    ax1.set_title('Number of Titles Released per Year', fontweight='bold', fontsize=11)
    ax1.set_xticks(x)
    
    # Show every Nth year label to avoid crowding
    if len(all_years) > 15:
        step = max(1, len(all_years) // 15)  # Show ~15 labels max
        ax1.set_xticks(x[::step])
        ax1.set_xticklabels([int(all_years[i]) for i in range(0, len(all_years), step)], 
                           rotation=45, ha='right', fontsize=8)
    else:
        ax1.set_xticklabels([int(year) for year in all_years], rotation=45, ha='right', fontsize=9)
    
    ax1.legend(fontsize=9)
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Average IMDB Score per year
    ax2 = axes[0, 1]
    if "imdb_score" in hbo.columns and "imdb_score" in param.columns:
        hbo_imdb = hbo[hbo["release_year"].isin(common_years)].groupby("release_year")["imdb_score"].mean()
        param_imdb = param[param["release_year"].isin(common_years)].groupby("release_year")["imdb_score"].mean()
        
        # Align
        hbo_imdb_aligned = [hbo_imdb.get(year, None) for year in all_years]
        param_imdb_aligned = [param_imdb.get(year, None) for year in all_years]
        
        ax2.plot(all_years, hbo_imdb_aligned, marker='o', label='HBO', linewidth=2, markersize=6, color='#1f77b4')
        ax2.plot(all_years, param_imdb_aligned, marker='s', label='Paramount', linewidth=2, markersize=6, color='#ff7f0e')
        ax2.set_xlabel('Release Year')
        ax2.set_ylabel('Average IMDB Score')
        ax2.set_title('Average IMDB Score per Year')
        ax2.legend()
        ax2.grid(alpha=0.3)
        ax2.set_ylim(bottom=0)
    
    # Subplot 3: Average TMDB Score per year
    ax3 = axes[1, 0]
    if "tmdb_score" in hbo.columns and "tmdb_score" in param.columns:
        hbo_tmdb = hbo[hbo["release_year"].isin(common_years)].groupby("release_year")["tmdb_score"].mean()
        param_tmdb = param[param["release_year"].isin(common_years)].groupby("release_year")["tmdb_score"].mean()
        
        # Align
        hbo_tmdb_aligned = [hbo_tmdb.get(year, None) for year in all_years]
        param_tmdb_aligned = [param_tmdb.get(year, None) for year in all_years]
        
        ax3.plot(all_years, hbo_tmdb_aligned, marker='o', label='HBO', linewidth=2, markersize=6, color='#1f77b4')
        ax3.plot(all_years, param_tmdb_aligned, marker='s', label='Paramount', linewidth=2, markersize=6, color='#ff7f0e')
        ax3.set_xlabel('Release Year')
        ax3.set_ylabel('Average TMDB Score')
        ax3.set_title('Average TMDB Score per Year')
        ax3.legend()
        ax3.grid(alpha=0.3)
        ax3.set_ylim(bottom=0)
    
    # Subplot 4: Top genres comparison for a sample year (most recent common year with data)
    ax4 = axes[1, 1]
    sample_year = common_years[-1] if len(common_years) > 0 else None
    if sample_year:
        hbo_year_data = hbo[hbo["release_year"] == sample_year]
        param_year_data = param[param["release_year"] == sample_year]
        
    # Subplot 5 Get top genres for this year
        def get_top_genres_year(df, top_n=5):
            if "genres_array" not in df.columns or len(df) == 0:
                return pd.Series(dtype=int)
            exploded = df.explode("genres_array")
            exploded["genres_array"] = exploded["genres_array"].astype(str).str.strip()
            return exploded["genres_array"].value_counts().head(top_n)
        
        hbo_genres_year = get_top_genres_year(hbo_year_data, 5)
        param_genres_year = get_top_genres_year(param_year_data, 5)
        
        if not hbo_genres_year.empty or not param_genres_year.empty:
            genres_combined = sorted(set(hbo_genres_year.index) | set(param_genres_year.index))
            hbo_genres_aligned = [hbo_genres_year.get(genre, 0) for genre in genres_combined]
            param_genres_aligned = [param_genres_year.get(genre, 0) for genre in genres_combined]
            
            x_genres = range(len(genres_combined)) # add this in subplot 1
            ax4.bar([i - width/2 for i in x_genres], hbo_genres_aligned, width, label='HBO', alpha=0.8, color='#1f77b4')
            ax4.bar([i + width/2 for i in x_genres], param_genres_aligned, width, label='Paramount', alpha=0.8, color='#ff7f0e')
            ax4.set_xlabel('Genre')
            ax4.set_ylabel('Number of Titles')
            ax4.set_title(f'Top Genres in {int(sample_year)}')
            ax4.set_xticks(x_genres)
            ax4.set_xticklabels(genres_combined, rotation=45, ha='right')
            ax4.legend()
            ax4.grid(axis='y', alpha=0.3)
        else:
            ax4.text(0.5, 0.5, f'No genre data available\nfor year {int(sample_year)}', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=12)
            ax4.set_title(f'Top Genres in {int(sample_year)}')
    else:
        ax4.text(0.5, 0.5, 'No common years found', ha='center', va='center', 
                transform=ax4.transAxes, fontsize=12)
        ax4.set_title('Top Genres Comparison')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "year_by_year_comparison.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.show()
else:
    print("[INFO] No common years found between HBO and Paramount datasets - skipping year comparison plot")

# ---------- Plot 6: Production Countries by Type (MOVIE vs SHOW) ----------
print("\n[INFO] Generating production countries comparison by type...")

def get_countries_by_type(df, platform_name):
    """Get production countries count grouped by type (MOVIE vs SHOW)"""
    if "production_countries" not in df.columns or "type" not in df.columns:
        return pd.DataFrame()
    
    # Parse production_countries (might be array or comma-separated string)
    df_copy = df.copy()
    
    # Handle production_countries - might be string representation of array
    def parse_countries(cell):
        if pd.isna(cell):
            return []
        s = str(cell).strip()
        if s.startswith("[") and s.endswith("]"):
            try:
                result = ast.literal_eval(s)
                if isinstance(result, list):
                    return [str(x).strip().strip("'\"[]") for x in result if x]
                return [str(result).strip()]
            except:
                # Manual parsing
                content = s.strip("[]")
                return [x.strip().strip("'\"") for x in content.split(",") if x.strip()]
        # Comma-separated string
        if "," in s:
            return [x.strip().strip("'\"") for x in s.split(",") if x.strip()]
        return [s.strip().strip("'\"")] if s else []
    
    df_copy["countries_list"] = df_copy["production_countries"].apply(parse_countries)
    
    # Explode countries and group by type
    exploded = df_copy.explode("countries_list")
    exploded = exploded[exploded["countries_list"] != ""]
    
    if len(exploded) == 0:
        return pd.DataFrame()
    
    # Group by country and type, count titles
    result = exploded.groupby(["countries_list", "type"]).size().reset_index(name="count")
    result["platform"] = platform_name
    return result

# Get data for both platforms
hbo_countries = get_countries_by_type(hbo, "HBO")
param_countries = get_countries_by_type(param, "Paramount")

if not hbo_countries.empty or not param_countries.empty:
    # Combine data
    all_countries_data = pd.concat([hbo_countries, param_countries], ignore_index=True)
    
    # Get top countries by total count
    top_countries = all_countries_data.groupby("countries_list")["count"].sum().nlargest(15).index.tolist()
    
    # Filter to top countries
    filtered_data = all_countries_data[all_countries_data["countries_list"].isin(top_countries)]
    
    # Create pivot table for easier plotting
    pivot_data = filtered_data.pivot_table(
        index="countries_list",
        columns=["platform", "type"],
        values="count",
        fill_value=0
    )
    
    # Flatten column names
    pivot_data.columns = [f"{platform}_{type}" for platform, type in pivot_data.columns]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Prepare data for grouped bar chart
    countries = pivot_data.index
    x = range(len(countries))
    width = 0.2
    
    # Get all possible combinations
    combinations = [
        ("HBO", "MOVIE"),
        ("HBO", "SHOW"),
        ("Paramount", "MOVIE"),
        ("Paramount", "SHOW")
    ]
    
    colors = {
        ("HBO", "MOVIE"): "#1f77b4",
        ("HBO", "SHOW"): "#aec7e8",
        ("Paramount", "MOVIE"): "#ff7f0e",
        ("Paramount", "SHOW"): "#ffbb78"
    }
    
    positions = [-1.5*width, -0.5*width, 0.5*width, 1.5*width]
    
    for i, (platform, type_val) in enumerate(combinations):
        col_name = f"{platform}_{type_val}"
        if col_name in pivot_data.columns:
            values = pivot_data[col_name].values
            ax.bar([xi + positions[i] for xi in x], values, width, 
                   label=f"{platform} - {type_val}", 
                   color=colors[(platform, type_val)], 
                   alpha=0.8)
        else:
            # If column doesn't exist, plot zeros
            ax.bar([xi + positions[i] for xi in x], [0]*len(countries), width,
                   label=f"{platform} - {type_val}", 
                   color=colors[(platform, type_val)], 
                   alpha=0.8)
    
    ax.set_xlabel("Production Country", fontsize=11, fontweight='bold')
    ax.set_ylabel("Number of Titles", fontsize=11, fontweight='bold')
    ax.set_title("Top Production Countries by Platform and Type (MOVIE vs SHOW)", fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(countries, rotation=45, ha='right', fontsize=9)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "production_countries_by_type.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")
    plt.show()
    plt.close()
else:
    print("[INFO] No production country data available - skipping countries plot")

print("\n" + "="*50)
print("Visualization complete! All plots saved to project root.")
print("="*50)