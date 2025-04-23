from itertools import combinations
from collections import defaultdict

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

    # Join step
    for L_p, L_q in combinations(prev_itemsets, 2):
        if L_p[:k - 2] != L_q[:k - 2]:
            continue

        if L_p[k-2] < L_q[k-2]:
            sorted_candidate_items = sorted(L_p + (L_q[-1],))
            candidate = tuple(sorted_candidate_items)

            Ck.add(candidate)
    
    # Prune step
    for candidate in Ck:
        for subset in combinations(candidate, k - 1):
            if subset not in L[k - 1]:
                Ck.remove(candidate)

    return Ck


def main():
    # NOTE: Toy example from chatgpt to test the code, delete later
    transactions = [
        ['milk', 'bread', 'butter'],
        ['bread', 'butter'],
        ['milk', 'bread'],
        ['bread', 'butter', 'jam'],
        ['milk', 'butter', 'jam']
    ]
    min_sup = 0.4
    frequent_itemsets = apriori(transactions, min_sup)
    
    for k, itemsets in frequent_itemsets.items():
        print(f"Frequent {k}-itemsets (support >= {min_sup}):")
        for items, count in sorted(itemsets.items()):
            print(f"  {items}: {count}")


if __name__ == "__main__":
    main()