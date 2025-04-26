# rule-me-maybe
COMS 6111 Project 3

## Group
Helena He (hh3090) <br>
Kristine Pham (klp2157)

## Files
- main.py
- daily_inmates_2.csv
- requirements.txt
- example-run.txt
- README.md

## To Run the Program
To install all packages needed to run the program, use this command:
```
pip3 install -r requirements.txt
```

To run the program, use this command:
```
python3 main.py daily_inmates.csv <min_sup> <min_conf>
```

## Dataset Description
(a) We used NYC Open Data's "Daily Inmates In Custody" dataset
(b) The function `update_csv()`, commented out at the bottom of `main.py`, takes in the original csv file and expands the race and Y/N items. For example, for 'BRADH' column, 
(c) This dataset is compelling because it can provide insight about not only criminal activity within the city, but also the state of the inmates. The dataset shares with you their age, if they are affiliated with a gang, and if they are under mental observation. We can find patterns to see how all these attributes relate to other attributes, like their top charge, their infractions, and the reason they are being held in custody.

## Project Design

## Compelling Sample Run