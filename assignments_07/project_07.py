## Part 2: Mini-Project — World Happiness Agent
## Task 1: Define Your Tools
## Tool 1: load_happiness_data
from pathlib import Path
import pandas as pd
from smolagents import tool
from scipy.stats import pearsonr
from smolagents import CodeAgent, OpenAIServerModel
import os
from dotenv import load_dotenv
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

df = None

DATA_DIR = Path(__file__).parent / "happiness_project"

@tool
def load_happiness_data() -> dict:
    """Load the World Happiness dataset into memory.

    Returns:
        A dictionary containing the DataFrame shape and column names.
    """
    global df

    COLUMN_NAMES = {
        "Country": "country",
        "Regional indicator": "region",
        "Happiness score": "happiness_score",
        "Ladder score": "happiness_score",
        "GDP per capita": "gdp_per_capita",
    }

    frames = []

    for path in sorted(DATA_DIR.glob("world_happiness_*.csv")):
        year_df = pd.read_csv(path, sep=";", decimal=",")
        year_df = year_df.rename(columns=COLUMN_NAMES)

        year_df["year"] = int(path.stem.split("_")[-1])

        frames.append(year_df)

    df = pd.concat(frames, ignore_index=True)

    return {
        "shape": df.shape,
        "columns": df.columns.tolist()
    }
## Tool 2: summarize_column
@tool
def summarize_column(column: str) -> dict:
    """Return descriptive statistics for a single column in the loaded dataset.

    Args:
        column: The name of the column to summarize.

    Returns:
        A dictionary containing descriptive statistics or an error message.
    """
    if df is None:
        return {"error": "Dataset is not loaded. Please load the data first."}

    if column not in df.columns:
        return {"error": f"Column '{column}' not found in the dataset."}

    return df[column].describe().to_dict()

## Tool 3: compute_correlation
@tool
def compute_correlation(col1: str, col2: str) -> dict:
    """Compute the Pearson correlation coefficient and p-value between two numeric columns.

    Args:
        col1: First numeric column.
        col2: Second numeric column.

     Returns:
        A dictionary with the following keys:
        - col1: First column name.
        - col2: Second column name.
        - pearson_r: Pearson correlation coefficient.
        - p_value: Statistical significance p-value.
    """
    if df is None:
        return {"error": "Dataset is not loaded. Please load the data first."}

    if col1 not in df.columns:
        return {"error": f"Column '{col1}' not found."}

    if col2 not in df.columns:
        return {"error": f"Column '{col2}' not found."}

    if not pd.api.types.is_numeric_dtype(df[col1]):
        return {"error": f"Column '{col1}' is not numeric."}

    if not pd.api.types.is_numeric_dtype(df[col2]):
        return {"error": f"Column '{col2}' is not numeric."}

    data = df[[col1, col2]].dropna()

    if len(data) < 2:
        return {"error": "Not enough valid data to calculate correlation."}

    pearson_r, p_value = pearsonr(data[col1], data[col2])

    return {
        "col1": col1,
        "col2": col2,
        "pearson_r": round(pearson_r, 4),
        "p_value": round(p_value, 4)
    }

## Tool 4: get_top_n_countries

@tool
def get_top_n_countries(column: str, year: int, n: int = 5) -> dict:
    """ Return the N countries with the HIGHEST values in a given year.

    Results are sorted in descending order (highest to lowest).

    Args:
        column: Numeric column used for ranking.
        year: Year to filter the dataset.
        n: Number of countries to return.

    Returns:
        A dictionary containing:
        - year: Selected year.
        - column: ranking column.
        - results: List of dictionaries. Each result contains the country name and its value
        for the requested column. Countries with the highest values, sorted in descending order.
    
    Returns an error dictionary if the dataset is not loaded, the
        column or year is invalid, or n is not a positive integer.

    Note:
        This function only returns the highest values


    """
    if df is None:
        return {"error": "Dataset is not loaded. Please load the data first."}

    if column not in df.columns:
        return {"error": f"Column '{column}' not found."}

    if column == "country":
        return {"error": "Please select a numeric column for ranking."}

    if not pd.api.types.is_numeric_dtype(df[column]):
        return {"error": f"Column '{column}' is not numeric."}

    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        return {"error": "n must be a positive integer."}

    if year not in df["year"].values:
        return {"error": f"No data found for year {year}."}

    year_df = df[df["year"] == year]

    top_countries = (
        year_df[["country", column]]
        .dropna(subset=[column])
        .sort_values(by=column, ascending=False)
        .head(n)
    )

    return {
        "year": year,
        "column": column,
        "results": top_countries.to_dict(orient="records")
    }

## Task 2: Build the Agent

model = OpenAIServerModel(api_key=api_key, model_id="gpt-4o-mini")

SYSTEM_PROMPT = """
You are a data analyst assistant for the World Happiness dataset.
Use the available tools for loading data, summarizing columns, computing correlations,
and ranking countries. Write Python code directly only when the tools are not sufficient
(for example, when creating custom plots or computing something the tools don't cover).
Be concise and student-friendly in your responses.
TOOL USAGE:
- First, check whether an available tool is designed to perform the requested task.
- Before calling a tool, verify that its documented behavior matches
  the requested operation, including the direction of sorting or ranking.
- If a suitable tool exists, use that tool instead of writing equivalent Python code.
- Do not use a tool for tasks outside its intended purpose.
- If no suitable tool exists, generate Python code directly.
- Use the existing DataFrame (df) for custom calculations, filtering,
  sorting, and data analysis when no suitable tool is available.
DATA LOADING:
- Call load_happiness_data() to load the dataset.
- The tool returns a summary dictionary with "shape" and "columns".
- Use the returned summary dictionary to report the dataset shape and column names.
- The tool also stores the actual pandas DataFrame in the global variable df.
- Do not assume df is available in the same execution immediately after calling load_happiness_data().
- For subsequent queries, you must use df directly.
- Do not recreate the DataFrame.
- Never treat the summary dictionary as the actual dataset.
- When creating plots, use the non-interactive matplotlib backend 'Agg'.
- Always import matplotlib first and set matplotlib.use('Agg')
  before importing matplotlib.pyplot.
- Never import matplotlib.pyplot before setting the backend.
- Save all plots to outputs/.
- Always use paths beginning with outputs/.
- For example:outputs/happiness_by_year.png.
- Use full relative paths when saving plots.
AGENT EXECUTION:
- Always use valid CodeAgent code formatting.
- After successfully executing a plotting task, immediately
  call final_answer() with a short confirmation message.
- Do not attempt to recreate a plot that has already been saved.
- Do not provide ordinary text instead of a valid final_answer()
  call.
- Do not create or import os to manage output directories.
- The output directory already exists.
- Save plots directly to outputs/ using relative paths.
Never generate synthetic or mock data.
"""

if __name__ == "__main__":

    agent = CodeAgent(
        tools=[load_happiness_data, summarize_column, compute_correlation, get_top_n_countries],
        model=model,
        instructions=SYSTEM_PROMPT,
        additional_authorized_imports=["pandas", "matplotlib.pyplot", "scipy.stats"],
        max_steps=8,
    )

    ## Task 3: Run Guided Queries
    queries = [
        "Load the happiness data and tell me its shape and column names.",
        "Summarize the happiness_score column.",
        "What is the correlation between gdp_per_capita and happiness_score? Is it statistically significant?",
        "Show me the top 5 happiest countries in 2020.",
        "Plot happiness_score over the years as a line chart, with one line per region. Save the plot to outputs/happiness_by_region.png.",
    ]

    for query in queries:
        print(f"\n--- Query: {query} ---")
        response = agent.run(query, reset=False,  additional_args={"df": df})
        print(response)
    plot_path = OUTPUT_DIR / "happiness_by_region.png"

    print("Plot exists:", plot_path.exists())
    print("Plot location:", plot_path.resolve())
    ## Task 4: Your Own Questions
    # My query 1
    my_query_1 = "Which 5 countries had the lowest happiness scores in 2020?"

    response_1 = agent.run(my_query_1, reset=False)
    print("Task 4 query 1",response_1)

    # Comment: This query must not trigger the tool use. 
    # It should trigger code generation. It still calls tool first, but later corrects itself:
    # Which 5 countries had the lowest happiness scores in 2020?            │
    # │                                                                       │
    # ╰─ OpenAIModel - gpt-4o-mini ───────────────────────────────────────────╯
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Step 1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  ─ Executing parsed code: ────────────────────────────────────────────── 
    #   lowest_5_happiness_countries_2020 =                                    
    #   get_top_n_countries(column='happiness_score', year=2020, n=5)          
    #   print(lowest_5_happiness_countries_2020)                               
    #  ─────────────────────────────────────────────────────────────────────── 
    # Execution logs:
    # {'year': 2020, 'column': 'happiness_score', 'results': [{'country': 
    # 'Finland', 'happiness_score': 7.8087}, {'country': 'Denmark', 
    # 'happiness_score': 7.6456}, {'country': 'Switzerland', 'happiness_score':
    # 7.5599}, {'country': 'Iceland', 'happiness_score': 7.5045}, {'country': 
    # 'Norway', 'happiness_score': 7.488}]}

    # Out: None
    # [Step 10: Duration 2.64 seconds| Input tokens: 45,603 | Output tokens: 
    # 1,381]
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Step 2 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  ─ Executing parsed code: ────────────────────────────────────────────── 
    #   lowest_5_happiness_countries_df = df[df['year'] == 2020].nsmallest(5,  
    #   'happiness_score')[['country', 'happiness_score']]                     
    #   print(lowest_5_happiness_countries_df)                                 
    #  ─────────────────────────────────────────────────────────────────────── 
    # Execution logs:
    #                       country  happiness_score
    # 931               Afghanistan           2.5669
    # 930               South Sudan           2.8166
    # 929                  Zimbabwe           3.2992
    # 928                    Rwanda           3.3123
    # 927  Central African Republic           3.47

    # # My query 2
    my_query_2 = "Calculate the average happiness score for each year and create a bar chart showing how global happiness changed over time. Save the chart to outputs/happiness_by_year.png."

    response_2 = agent.run(my_query_2, reset=False)
    print("Task 4 query 2",response_2)

    # Comment: This query triggered code generation.
    # The agent used Python and pandas to calculate yearly averages
    # and matplotlib to create and save the bar chart.

    ## Task 5: Reflection
    # --- Reflection ---
    #
    #  1. The agent reported a positive correlation between GDP per capita
    #    and happiness score, with a Pearson r of 0.6313 and a p-value of
    #    approximately 0. This indicates a moderately strong positive
    #    relationship: countries with higher GDP per capita tend to have
    #    higher happiness scores. The very small p-value indicates that
    #    the correlation is statistically significant.
    #
    # 2. I was surprised by how capable the agent was at generating Python
    #    code to answer questions that were not directly supported by its
    #    tools. For example, when asked to find the five countries with the
    #    lowest happiness scores in 2020, it used pandas to filter and sort
    #    the DataFrame and returned the correct results. However, it initially
    #    selected the wrong tool, which showed me that AI agents do not always
    #    choose the most appropriate tool on the first attempt.
    #
    # 3. An additional tool that would make this agent more useful is a
    #    compare_countries() tool. It would allow users to compare selected
    #    countries across multiple indicators, such as happiness score,
    #    GDP per capita, social support, and healthy life expectancy.
    #    It would help answer questions like: "How do Finland and Denmark
    #    compare in terms of happiness, GDP, and social support?"