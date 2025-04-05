def compare_sequences(seq1_str, seq2_str):
    seq1 = [int(x) for x in seq1_str.split()]
    seq2 = [int(x) for x in seq2_str.split()]
    diff_count = 0
    diff_indices = []
    if len(seq1) != len(seq2):
        return "Length mismatch", [], -1
    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            diff_count += 1
            diff_indices.append(i)
    return diff_count, diff_indices

results = {}
# Train Examples
results["Train 1"] = compare_sequences("0 0 0 4 4 4 4 4 0 0 0 0", "0 0 4 4 4 4 4 0 0 0 0 0")
results["Train 2"] = compare_sequences("0 0 0 0 0 0 9 9 9 9 9 9", "0 0 0 0 0 9 9 9 9 9 9 0")
results["Train 3"] = compare_sequences("0 0 0 0 0 0 1 1 1 0 0 0", "0 0 0 0 0 1 1 1 0 0 0 0")
results["Train 4"] = compare_sequences("0 0 0 0 0 9 9 9 9 9 9 0", "0 0 0 0 9 9 9 9 9 9 0 0")
results["Train 5"] = compare_sequences("0 0 0 0 0 0 0 0 0 2 2 0", "0 0 0 0 0 0 0 0 2 2 0 0")
results["Train 6"] = compare_sequences("0 0 0 0 0 0 5 5 5 5 5 0", "0 0 0 0 0 5 5 5 5 5 0 0")
results["Train 7"] = compare_sequences("0 0 0 0 6 6 6 6 6 6 6 0", "0 0 0 6 6 6 6 6 6 6 0 0")
# Test Example
results["Test 1"] = compare_sequences("0 0 5 5 5 5 0 0 0 0 0 0", "0 5 5 5 5 0 0 0 0 0 0 0")

print(results)
