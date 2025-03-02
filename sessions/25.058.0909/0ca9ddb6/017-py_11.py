import numpy as np

def get_neighbors(grid, row, col):
    """
    returns a list if valid neighbor coordinates
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def analyze_differences(input_grid, expected_output, actual_output):
    """
    Analyzes the differences between the expected and actual outputs.
    """
    differences = []
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            if expected_output[row, col] != actual_output[row, col]:
                neighbors = get_neighbors(input_grid, row, col)
                neighbor_colors = [input_grid[r, c] for r, c in neighbors]
                differences.append({
                    'location': (row, col),
                    'expected': expected_output[row, col],
                    'actual': actual_output[row, col],
                    'input': input_grid[row,col],
                    'neighbors': neighbors,
                    'neighbor_colors': neighbor_colors
                })
    return differences

# Example Data (replace with your actual data)
train = [
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 0, 0, 0, 5, 5, 5],
                           [5, 5, 5, 0, 1, 0, 5, 5, 5],
                           [5, 5, 5, 0, 0, 0, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 7, 7, 7, 5, 5, 5],
                            [5, 5, 5, 7, 1, 7, 5, 5, 5],
                            [5, 5, 5, 7, 7, 7, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5]])
    },
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 0, 5, 5, 5, 5],
                           [5, 5, 5, 0, 0, 0, 5, 5, 5],
                           [5, 5, 5, 0, 1, 0, 5, 5, 5],
                           [5, 5, 5, 0, 0, 0, 5, 5, 5],
                           [5, 5, 5, 5, 2, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 7, 5, 5, 5, 5],
                            [5, 5, 5, 7, 7, 7, 5, 5, 5],
                            [5, 5, 5, 7, 1, 7, 5, 5, 5],
                            [5, 5, 5, 7, 7, 7, 5, 5, 5],
                            [5, 5, 5, 5, 2, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5]])
    },
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5],
                           [5, 5, 5, 0, 0, 1, 0, 0, 5, 5, 5, 5],
                           [5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 7, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 7, 7, 7, 5, 5, 5, 5, 5],
                            [5, 5, 5, 7, 7, 7, 7, 7, 5, 5, 5, 5],
                            [5, 5, 5, 7, 7, 1, 7, 7, 5, 5, 5, 5],
                            [5, 5, 5, 5, 7, 7, 7, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 7, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
    },
    {
        "input": np.array([[6, 6, 6, 5, 5, 5, 5, 5],
                           [6, 6, 6, 5, 0, 5, 5, 5],
                           [6, 6, 6, 5, 0, 5, 5, 5],
                           [5, 5, 5, 0, 0, 0, 5, 5],
                           [5, 5, 5, 0, 1, 0, 5, 5],
                           [5, 5, 5, 0, 0, 0, 5, 5],
                           [5, 5, 5, 5, 2, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[6, 6, 6, 5, 5, 5, 5, 5],
                            [6, 6, 6, 5, 7, 5, 5, 5],
                            [6, 6, 6, 5, 7, 5, 5, 5],
                            [5, 5, 5, 7, 7, 7, 5, 5],
                            [5, 5, 5, 7, 1, 7, 5, 5],
                            [5, 5, 5, 7, 7, 7, 5, 5],
                            [5, 5, 5, 5, 2, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5]])
    },
    {
      "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
      "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }
]

# Create dummy outputs from transform.  Assumes transform is defined elsewhere
outputs = [transform(t["input"]) for t in train]

for i in range(len(train)):
    print(f"Train Example {i+1}:")
    differences = analyze_differences(train[i]["input"], train[i]["output"], outputs[i])
    if differences:
        for diff in differences:
            print(f"  Location: {diff['location']}, Expected: {diff['expected']}, Actual: {diff['actual']}, Input: {diff['input']}, Neighbor Colors: {diff['neighbor_colors']}")
    else:
        print("  No differences found.")
    print("-" * 30)