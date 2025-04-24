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
            The dataset of transactions (each transaction is a list of items).
        min_sup (int): 
            The minimum support threshold as a fraction between 0 and 1..
        
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
            List of frequent (k-1)-itemsets (tuples sorted lexically).
        k (int): 
            Size of candidates to generate.
        L (Dict[int, Dict[Tuple(), float]]): 
            A mapping from itemset size to the dictionary of frequent itemsets of that size

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
    
    transactions = df.values.tolist()
    return transactions

def main():
    # Parse and validate all user input from args
    args = validate_args()

    transactions = parse_transactions(args.csv)

    # NOTE: Toy example from class, delete later
    # transactions = [
    #     ['pen', 'ink', 'diary', 'soap'],
    #     ['pen', 'ink', 'diary'],
    #     ['pen', 'diary'],
    #     ['pen', 'ink', 'soap']
    # ]
    # min_sup = 0.7
    frequent_itemsets = apriori(transactions, args.min_sup)
    
    for k, itemsets in frequent_itemsets.items():
        print(f"Frequent {k}-itemsets (support >= {args.min_sup}):")
        for items, count in sorted(itemsets.items()):
            print(f"  {items}: {count}")


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