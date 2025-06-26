import pandas as pd

test = pd.to_datetime("Jun. 26, 2025", errors="coerce")
print(test)

#Ran this test to make sure pandas parse date now correctly
