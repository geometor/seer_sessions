import numpy as np

def compare_grids(predicted, expected):
    """
    Compares two grids and returns the coordinates where they differ.
    """
    diff_coords = []
    for r in range(predicted.shape[0]):
        for c in range(predicted.shape[1]):
            if predicted[r, c] != expected[r, c]:
                diff_coords.append((r, c, predicted[r,c], expected[r,c]))
    return diff_coords

# Example usage (assuming 'transform' function and train_pairs are available)
# Reload train_pairs from the json
import json
with open('data/training/6fa7a44f.json', 'r') as f:
    task_data = json.load(f)
train_pairs = task_data['train']
    
for i, pair in enumerate(train_pairs):
    input_grid = np.array(pair['input'])
    expected_output = np.array(pair['output'])
    predicted_output = transform(input_grid)
    diffs = compare_grids(predicted_output, expected_output)
    print(f"Example {i+1} Differences:")
    if diffs:
        for r, c, pred_val, exp_val in diffs:
            print(f"  Row: {r}, Col: {c}, Predicted: {pred_val}, Expected: {exp_val}")
    else:
        print("  No differences found.")
    print("---")
