
# How to run
```shell
poetry shell # only if the virtual environment is not active
poetry run debt_calculator/main.py
```
# How to run tests
```shell
poetry shell # only if the virtual environment is not active 
poetry run pytest
```

# Planned features roadmap
- 🟢 Collect debt data from user (item name, Amount to pay, # of installments and start date)
- 🟢 Validate that debt data are valid 
- 🟢 Store debt in a json file
- 🟢 Calculate remaining debt amount from the moment of entry
- 🟢 Calculate remaining installments from the moment of entry
- 🟠 containerise the whole project 
- 🟠 Expand README with how to run 
- 🟠 Activate CI
- 🔵 deprecate json file storage and migrate into a database storage with consistent storage
- 🔵 Graph for total debt amount with each contributor based on how much is remaining
- 🔵 Bar/Line chart for projected 6 month of payments 
- 🔵 Add tests

#### Legend
🟢 - Done  
🟠 - In progress  
🔵 - Planned