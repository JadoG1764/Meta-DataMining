# Meta-DataMining

Data Mining Final Project repo
This repo will datamine from the following datasets: https://ai.meta.com/ai-for-good/datasets/social-connectedness-index/, https://ai.meta.com/ai-for-good/datasets/travel-patterns/

We want to mine for relationships between social connectedness and physical travel patterns between geographic areas. 
In particular, to determine whether areas that have stronger social connections also tend to have more travel between them, using techniques such as clustering, correlation analysis, and possibly association or graph-based mining.
This could reveal groups of locations or travel connections that follow similar patterns.

## Database setup

The database is built locally at `data/meta.duckdb` from the Meta CSV files. The `data/` folder is gitignored, so each person builds their own copy.

1. Create a Python 3.14 virtual environment and install dependencies:
   ```
   py -3.14 -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Download the data from the [Social Connectedness Index page](https://ai.meta.com/ai-for-good/datasets/social-connectedness-index/) and put this file in a `data` folder in the project:
   - `data/gadm1.csv`: the GADM level-1 file
3. Build the database:
   ```
   python load_data.py --local
   ```

## Using the database

```python
import duckdb

con = duckdb.connect("data/meta.duckdb")
con.sql("SELECT * FROM sci_gadm1 LIMIT 10").show()
```

Tables:
- `sci_gadm1`: Social Connectedness Index between GADM level-1 regions
