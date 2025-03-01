import numpy as np

def find_clusters(grid):
    """Finds clusters of non-zero pixels in a grid."""
    visited = set()
    clusters = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_cluster):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_cluster.append((r, c))
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            dfs(nr, nc, current_cluster)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def bounding_box(cluster):
    """Calculates the bounding box of a cluster."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in cluster:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def extract_rows_cols(grid, clusters):
    """Extracts rows and columns of interest based on the first cluster."""
    rows_of_interest = []
    cols_of_interest = []

    if clusters:  # Check if there are any clusters
        first_cluster = clusters[0]
        min_r, min_c, max_r, max_c = bounding_box(first_cluster)

        #Use dimensions from bounding box
        for r in range(min_r, max_r + 1):
            rows_of_interest.append(r)
        for c in range(min_c, max_c + 1):
            cols_of_interest.append(c)

    return rows_of_interest, cols_of_interest

def transform(input_grid):
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Clusters
    clusters = find_clusters(input_grid)

    # 2. & 3. Bounding Box and Sample based on the first cluster
    rows_of_interest, cols_of_interest = extract_rows_cols(input_grid, clusters)

    # 4. Assemble Output - create a grid with the selected rows and columns
    if rows_of_interest and cols_of_interest:
      subgrid = input_grid[np.ix_(rows_of_interest, cols_of_interest)]
      return subgrid.tolist()
    else:
       return []
    
def analyze_example(example):
    input_grid = np.array(example['input'])
    expected_output = np.array(example['output'])
    generated_output = np.array(transform(example['input']))

    input_clusters = find_clusters(input_grid)
    output_clusters = find_clusters(expected_output)

    print("Input Clusters:", len(input_clusters))
    for i, cluster in enumerate(input_clusters):
        min_r, min_c, max_r, max_c = bounding_box(cluster)
        print(f"  Cluster {i+1}: Bounding Box - ({min_r}, {min_c}) to ({max_r}, {max_c})")

    print("Output Clusters:", len(output_clusters))
    for i, cluster in enumerate(output_clusters):
        min_r, min_c, max_r, max_c = bounding_box(cluster)
        print(f"  Cluster {i+1}: Bounding Box - ({min_r}, {min_c}) to ({max_r}, {max_c})")
        
    print("Expected Output Dimensions:", expected_output.shape)
    if generated_output.size > 0:
        print("Generated Output Dimensions:", generated_output.shape)
        print("Pixel-wise Comparison (True = match, False = mismatch):")
        comparison = generated_output == expected_output
        #resize comparison grid to match expected
        resized_comparison = np.zeros_like(expected_output, dtype=bool)
        h, w = comparison.shape
        resized_comparison[:h,:w] = comparison
        print(resized_comparison)
    else:
        print("Generated output is empty")

    print("-" * 20)

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[8, 8, 8], [8, 8, 8], [8, 8, 8]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 7, 7, 7], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 7, 7, 7], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 7, 7, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[1, 1, 1, 7, 7, 7], [1, 1, 1, 7, 7, 7], [1, 1, 1, 7, 7, 7]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[6, 6, 6, 2, 2], [6, 6, 6, 2, 2], [6, 6, 6, 2, 2]]
        }
    ]
}

for i, example in enumerate(task['train']):
    print(f"Example {i+1}:")
    analyze_example(example)