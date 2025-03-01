import numpy as np

# Define the examples (as provided previously)
input_grid1 = np.array([[8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5]])
expected_output1 = np.array([[8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5],
                       [8,5,8,5,8,5,8,5]])
input_grid2 = np.array([[8, 5, 5, 8, 5, 5, 8, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5],
                       [8, 5, 5, 8, 5, 5, 8, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5],
                       [8, 5, 5, 8, 5, 5, 8, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5]])
expected_output2 = np.array([[8, 5, 5, 8, 5, 5, 8, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5],
                       [8, 5, 5, 8, 5, 5, 8, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5],
                       [8, 5, 5, 8, 5, 5, 8, 5],
                       [5, 8, 8, 5, 8, 8, 5, 5],
                       [8, 5, 8, 5, 8, 8, 5, 5]])
input_grid3 = np.array([[8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 8, 8]])
expected_output3 = np.array([[8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 5, 5, 8],
                       [8, 5, 8, 5, 8, 8, 5, 8]])

def analyze_changes(input_grid, expected_output):
    changes = []
    diff = np.where(input_grid != expected_output)
    for row, col in zip(diff[0], diff[1]):
        changes.append({
            'row': int(row),
            'col': int(col),
            'from': int(input_grid[row, col]),
            'to': int(expected_output[row, col])
        })
    return changes

changes1 = analyze_changes(input_grid1, expected_output1)
changes2 = analyze_changes(input_grid2, expected_output2)
changes3 = analyze_changes(input_grid3, expected_output3)

print("Changes in Example 1:")
print(changes1)
print("\nChanges in Example 2:")
print(changes2)
print("\nChanges in Example 3:")
print(changes3)