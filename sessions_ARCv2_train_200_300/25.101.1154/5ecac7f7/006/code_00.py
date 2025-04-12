import numpy as np
from collections import Counter

def get_col_stats(col_list):
    """Calculates basic statistics for a column (list of ints)."""
    stats = {}
    stats['list'] = col_list
    stats['sum'] = sum(col_list)
    counts = Counter(col_list)
    stats['unique_count'] = len(counts)
    if not counts:
        stats['max_freq'] = 0
        stats['most_freq_color'] = None
    else:
        most_common = counts.most_common(1)[0]
        stats['max_freq'] = most_common[1]
        stats['most_freq_color'] = most_common[0]
    return stats

# --- Example 2 Data ---
inp2 = np.array([
    [7, 7, 1, 8, 8, 6, 7, 7, 7, 7, 7, 6, 4, 7, 7, 7, 7],
    [8, 8, 1, 8, 8, 6, 2, 2, 9, 4, 4, 6, 4, 0, 0, 1, 1],
    [8, 7, 1, 7, 7, 6, 2, 2, 9, 4, 4, 6, 4, 0, 0, 7, 1],
    [8, 8, 7, 7, 7, 6, 7, 7, 7, 7, 4, 6, 7, 0, 0, 1, 1],
    [7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 4, 6, 7, 7, 7, 1, 7]
])
out2 = np.array([
    [7, 7, 7, 7, 7],
    [8, 8, 9, 1, 1],
    [8, 7, 9, 7, 1],
    [8, 8, 7, 1, 1],
    [7, 7, 7, 1, 7]
])

# --- Example 3 Data ---
inp3 = np.array([
    [7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7],
    [7, 9, 3, 1, 7, 6, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 6, 7, 8, 5, 6, 7, 6, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 6, 7, 4, 0, 2, 7],
    [7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7]
])
out3 = np.array([
    [7, 7, 7, 7, 7],
    [7, 9, 7, 7, 7],
    [7, 7, 5, 7, 7],
    [7, 7, 7, 2, 7],
    [7, 7, 7, 7, 7]
])

print("--- Failure Case Analysis ---")

# Example 2, j=3
j = 3
cols_data = [inp2[:, j].tolist(), inp2[:, j+6].tolist(), inp2[:, j+12].tolist()]
stats = [get_col_stats(c) for c in cols_data]
sums = [s['sum'] for s in stats]
max_sum = max(sums)
candidates_indices = [i for i, s in enumerate(sums) if s == max_sum]
chosen_idx = max(candidates_indices) # Apply max index tie-breaker
expected_col = out2[:, j].tolist()
print(f"\nExample 2, Output Column j={j}:")
print(f"  Segment 0 (Col {j}):   Stats={stats[0]}")
print(f"  Segment 1 (Col {j+6}):  Stats={stats[1]}")
print(f"  Segment 2 (Col {j+12}): Stats={stats[2]}")
print(f"  Rule chose Segment: {chosen_idx} (Sum={sums[chosen_idx]})")
print(f"  Expected Column:    {expected_col} (Segment 2, Sum={sums[2]})")
print(f"  Match: {stats[chosen_idx]['list'] == expected_col}")

# Example 2, j=4
j = 4
cols_data = [inp2[:, j].tolist(), inp2[:, j+6].tolist(), inp2[:, j+12].tolist()]
stats = [get_col_stats(c) for c in cols_data]
sums = [s['sum'] for s in stats]
max_sum = max(sums)
candidates_indices = [i for i, s in enumerate(sums) if s == max_sum]
chosen_idx = max(candidates_indices) # Apply max index tie-breaker
expected_col = out2[:, j].tolist()
print(f"\nExample 2, Output Column j={j}:")
print(f"  Segment 0 (Col {j}):   Stats={stats[0]}")
print(f"  Segment 1 (Col {j+6}):  Stats={stats[1]}")
print(f"  Segment 2 (Col {j+12}): Stats={stats[2]}")
print(f"  Rule chose Segment: {chosen_idx} (Sum={sums[chosen_idx]})")
print(f"  Expected Column:    {expected_col} (Segment 2, Sum={sums[2]})")
print(f"  Match: {stats[chosen_idx]['list'] == expected_col}")

# Example 3, j=1 (Identified as failure during re-analysis)
j = 1
cols_data = [inp3[:, j].tolist(), inp3[:, j+6].tolist(), inp3[:, j+12].tolist()]
stats = [get_col_stats(c) for c in cols_data]
sums = [s['sum'] for s in stats]
max_sum = max(sums)
candidates_indices = [i for i, s in enumerate(sums) if s == max_sum]
chosen_idx = max(candidates_indices) # Apply max index tie-breaker
expected_col = out3[:, j].tolist()
print(f"\nExample 3, Output Column j={j}:")
print(f"  Segment 0 (Col {j}):   Stats={stats[0]}")
print(f"  Segment 1 (Col {j+6}):  Stats={stats[1]}")
print(f"  Segment 2 (Col {j+12}): Stats={stats[2]}")
print(f"  Rule chose Segment: {chosen_idx} (Sum={sums[chosen_idx]})")
print(f"  Expected Column:    {expected_col} (Segment 0, Sum={sums[0]})")
print(f"  Match: {stats[chosen_idx]['list'] == expected_col}")

# Example 3, j=3
j = 3
cols_data = [inp3[:, j].tolist(), inp3[:, j+6].tolist(), inp3[:, j+12].tolist()]
stats = [get_col_stats(c) for c in cols_data]
sums = [s['sum'] for s in stats]
max_sum = max(sums)
candidates_indices = [i for i, s in enumerate(sums) if s == max_sum]
chosen_idx = max(candidates_indices) # Apply max index tie-breaker
expected_col = out3[:, j].tolist()
print(f"\nExample 3, Output Column j={j}:")
print(f"  Segment 0 (Col {j}):   Stats={stats[0]}")
print(f"  Segment 1 (Col {j+6}):  Stats={stats[1]}")
print(f"  Segment 2 (Col {j+12}): Stats={stats[2]}")
print(f"  Rule chose Segment: {chosen_idx} (Sum={sums[chosen_idx]})")
print(f"  Expected Column:    {expected_col} (Segment 2, Sum={sums[2]})")
print(f"  Match: {stats[chosen_idx]['list'] == expected_col}")
