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
(a) We used NYC Open Data's "Daily Inmates In Custody" dataset. 
<br>
(b) The function `update_csv()`, commented out at the bottom of `main.py`, takes in the original csv file and expands the race and Y/N items. For example, for 'BRADH' column, 
<br>
(c) This dataset is compelling because it can provide insight about not only criminal activity within the city, but also the state of the inmates. The dataset shares with you their age, if they are affiliated with a gang, and if they are under mental observation. We can find patterns to see how all these attributes relate to other attributes, like their top charge, their infractions, and the reason they are being held in custody.

## Project Design
The apriori algorithm is used to generate all frequent itemsets. There are two functions used for this, `apriori` and `apriori_gen`. These are implemented using the pseudocode given in Section 2.1 of the Agrawal and Srikant paper in VLDB 1994. 

The following happens when the `apriori` function is called:
1. Scan the transactions once to build frequent 1-itemsets that meet min_sup. 
2. Repeat for k = 2, 3, … until no new frequent itemsets appear:
    - Join step: take every pair of frequent (k–1)-itemsets that share their first k–2 items and merge them into a sorted k-tuple.
    - Prune step: for each k-tuple candidate, generate all its (k–1)-sized subsets. Delete the candidate if any subset isn’t already in the previous level’s frequent set L<sub>k-1</sub>.
    - Calculate the supports of each valid generated candidate. Discard any candidates that don't meet the min_sup threshold. This filtered set becomes L<sub>k</sub>

The functions `build_k_itemset_rules` and `build_high_conf_rules` are used for rule generation. For each frequent k-itemset, we try moving each element to the RHS and compute:
$$
\mathrm{confidence} \;=\; \frac{\mathrm{support}(LHS)}{\mathrm{support}\bigl(LHS \cup RHS\bigr)}
$$

Finally, we output only the association rules that meet the min_conf threshold.


## Compelling Sample Run
Run this command to see a compelling sample run:
```
python3 main.py daily_inmates.csv 0.01 0.7
```

