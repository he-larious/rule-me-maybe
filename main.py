from itertools import combinations
from collections import defaultdict
import argparse
import os
import pandas as pd

def apriori(transactions, min_sup):
    """
    Apriori algorithm to find all frequent itemsets with support >= min_sup.
    
    Args:
        transactions (List[List[]]): 
            The dataset of transactions.
        min_sup (int): 
            The minimum support threshold as a fraction between 0 and 1.
        
    Returns:
        Dict[int, Dict[Tuple(), float]]: 
            A dictionary mapping k (itemset size) to a dict of frequent k-itemsets and their support.
    """
    L = {}
    total = len(transactions)

    # Count 1-itemsets
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[(item,)] += 1
    
    # Filter to get L1
    L1 = {}
    for itemset, count in item_counts.items():
        support = count / total

        if support >= min_sup:
            L1[itemset] = support

    L[1] = L1
    
    k = 2
    while True:
        prev_L = L[k-1]

        # Generate candidate k-itemsets
        candidates = apriori_gen(list(prev_L.keys()), k, L)

        # Count supports
        c_counts = defaultdict(int)
        for transaction in transactions:
            t_set = set(transaction)

            for candidate in candidates:
                if set(candidate).issubset(t_set):
                    c_counts[candidate] += 1

        # Filter candidates to get Lk
        Lk = {}
        for candidate, count in c_counts.items():
            support = count / total

            if support >= min_sup:
                Lk[candidate] = support

        if len(Lk) == 0:
            break

        L[k] = Lk
        k += 1
        
    return L


def apriori_gen(prev_itemsets, k, L):
    """
    Generate candidate k-itemsets from frequent (k-1)-itemsets using join and prune steps.

    Args:
        prev_itemsets (List[Tuple()]): 
            List of frequent (k-1)-itemsets.
        k (int): 
            Size of candidates to generate.
        L (Dict[int, Dict[Tuple(), float]]): 
            A mapping from itemset size to the dictionary of frequent itemsets of that size.

    Returns:
        Set[Tuple()]: 
            Candidate k-itemsets.
    """
    Ck = set()

    prev_itemsets = sorted(prev_itemsets)

    # Join step
    for L_p, L_q in combinations(prev_itemsets, 2):
        if L_p[:k - 2] != L_q[:k - 2]:
            continue

        if L_p[k-2] < L_q[k-2]:
            sorted_candidate_items = sorted(L_p + (L_q[-1],))
            candidate = tuple(sorted_candidate_items)

            Ck.add(candidate)
    
    # Prune step
    for candidate in list(Ck):
        for subset in combinations(candidate, k - 1):
            if subset not in L[k - 1]:
                Ck.remove(candidate)
                break

    return Ck

def check_csv_file(file_name):
    if not os.path.isfile(file_name):
        raise argparse.ArgumentTypeError("The CSV file must be in the INTEGRATED-DATASET in the directory.")
    return file_name

def check_threshold(t):
    t = float(t)
    if t < 0 or t > 1:
        raise argparse.ArgumentTypeError("Threshold must be between 0 and 1.")
    return t

def validate_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("csv", type=check_csv_file, help="The CSV file containing the INTEGRATED-DATASET")
    parser.add_argument("min_sup", type=check_threshold, help="Minimum support value between 0 and 1.")
    parser.add_argument("min_conf", type=check_threshold, help="Minimum confidence value between 0 and 1.")

    args = parser.parse_args()
    return args

def parse_transactions(csv_file):
    df = pd.read_csv(csv_file)
    df = df.astype(str)
    
    transactions = df.values.tolist()
    return transactions

def build_k_itemset_rules(k, itemsets, frequent_itemsets, min_conf):
    k_itemset_rules = []
    # iterate over each k-itemset
    for itemset, supp in itemsets.items():

        # calc numerator = supp(LHS U RHS)
        numerator = supp

        # for each element in tuple, move it the RHS
        l_itemset = list(itemset)

        for i in range(len(l_itemset)):
            lhs = l_itemset[:i] + l_itemset[i+1:]
            rhs = l_itemset[i]
            denominator = frequent_itemsets[k-1][tuple(lhs)]
            conf = numerator/denominator
            if conf >= min_conf:
                k_itemset_rules.append((lhs, rhs, conf, numerator))
    return k_itemset_rules

def build_high_conf_rules(frequent_itemsets, min_conf):
    high_conf_rules = []

    for k, itemsets in frequent_itemsets.items():

        # skip trivial rules
        if k == 1:
            continue
        
        # build rules for itemsets with k items
        k_itemset_rules = build_k_itemset_rules(k, itemsets, frequent_itemsets, min_conf)

        # add to list
        high_conf_rules = high_conf_rules + k_itemset_rules
        

    return high_conf_rules

    
def main():
    # Parse and validate all user input from args
    args = validate_args()

    transactions = parse_transactions(args.csv)

    frequent_itemsets = apriori(transactions, args.min_sup)
    high_conf_rules = build_high_conf_rules(frequent_itemsets, args.min_conf)

    with open("output.txt", "w") as f:

        # output frequent itemsets
        f.write(f"==Frequent itemsets (min_sup={args.min_sup*100}%)\n")
        for _, itemsets in frequent_itemsets.items():
            for items, count in sorted(itemsets.items()):
                f.write(f"[{','.join(list(items))}], {round(count*100, 4)}%\n")

        # output high conf rules
        f.write(f"==High-confidence association rules (min_conf={args.min_conf*100}%)\n")
        for rule in high_conf_rules:
            f.write(f"[{','.join(rule[0])}] => [{rule[1]}] (Conf: {round(rule[2]*100, 4)}%, Supp: {round(rule[3]*100, 4)}%)\n")

if __name__ == "__main__":
    main()


# update csv
'''
def update_csv(csv_file):
    df = pd.read_csv(csv_file)

    # Replace each Y and N as a unique item name
    df.loc[df["BRADH"] == "Y", "BRADH"] = "Y_BRADH"
    df.loc[df["BRADH"] == "N", "BRADH"] = "N_BRADH"

    df.loc[df["SRG_FLG"] == "Y", "SRG_FLG"] = "Y_SRG_FLG"
    df.loc[df["SRG_FLG"] == "N", "SRG_FLG"] = "N_SRG_FLG"

    df.loc[df["INFRACTION"] == "Y", "INFRACTION"] = "Y_INFRACTION"
    df.loc[df["INFRACTION"] == "N", "INFRACTION"] = "N_INFRACTION"

    # Replace age with age group
    bins = [18, 25, 35, 45, 55, 65, 75, 85, 95]
    labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '66-75', '76-85', '86-95']
    df['AGE_RANGE'] = pd.cut(df['AGE'], bins=bins, labels=labels, include_lowest=True)
    df = df.drop(columns=["AGE"])

    df.to_csv("daily_inmates_2.csv")


'''