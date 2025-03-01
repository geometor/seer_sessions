import numpy as np

def code_execution(input_grid, expected_output, transformed_output):

    print(f"Input Grid:\n{input_grid}\n")
    print(f"Expected Output:\n{expected_output}\n")
    print(f"Transformed Output:\n{transformed_output}\n")
    print(f"Transformed Correctly: {np.array_equal(expected_output, transformed_output)}\n")

    magenta_input_count = np.sum(input_grid == 6)
    yellow_input_count = np.sum(input_grid == 4)
    magenta_expected_count = np.sum(expected_output == 6)
    yellow_expected_count = np.sum(expected_output == 4)
    magenta_transformed_count = np.sum(transformed_output == 6)
    yellow_transformed_count = np.sum(transformed_output == 4)
        
    print(f"Input: Magenta={magenta_input_count}, Yellow={yellow_input_count}")
    print(f"Expected: Magenta={magenta_expected_count}, Yellow={yellow_expected_count}")
    print(f"Transformed: Magenta={magenta_transformed_count}, Yellow={yellow_transformed_count}")
    print("-" * 20)
    

#Example grids for testing
example_grids = [
    (np.array([[6, 0, 0, 0, 6, 0],
               [0, 6, 0, 6, 0, 0],
               [0, 0, 6, 0, 0, 0],
               [0, 6, 0, 6, 0, 0],
               [6, 0, 0, 0, 6, 0]]),
     np.array([[6, 0, 0, 0, 6, 0],
               [0, 6, 0, 6, 0, 0],
               [0, 0, 6, 0, 0, 0],
               [0, 6, 0, 6, 0, 0],
               [4, 0, 0, 0, 4, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 6, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 0, 6],
               [0, 0, 0, 0, 0, 0, 6, 0],
               [0, 0, 0, 0, 0, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 6, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 0, 6],
               [0, 0, 0, 0, 0, 0, 6, 0],
               [0, 0, 0, 0, 0, 6, 0, 0],
               [0, 4, 0, 0, 0, 4, 0, 4]])),
    (np.array([[0, 0, 0, 0, 0, 0],
              [0, 6, 6, 6, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0],
               [0, 6, 6, 6, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 4, 4, 4, 0, 0]])),
     (np.array([[0, 0, 0, 0, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 0, 0]]),
     np.array([[0, 0, 0, 0, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 4, 0, 0]]))
]

# Previous transform function
def find_clusters(grid, color):
    clusters = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_cluster):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        current_cluster.append((r, c))
        dfs(r + 1, c, current_cluster)
        dfs(r - 1, c, current_cluster)
        dfs(r, c + 1, current_cluster)
        dfs(r, c - 1, current_cluster)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def find_rightmost_pixel(cluster):
    rightmost_pixel = cluster[0]
    for pixel in cluster:
        if pixel[1] > rightmost_pixel[1]:
            rightmost_pixel = pixel
    return rightmost_pixel

def filter_clusters_by_row(clusters, rows_to_check):
    filtered_clusters = []
    for cluster in clusters:
        for pixel in cluster:
            if pixel[0] in rows_to_check:
                filtered_clusters.append(cluster)
                break  # Move to the next cluster once a pixel is found in the specified rows
    return filtered_clusters

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify Magenta Clusters
    magenta_clusters = find_clusters(output_grid, 6)

    # Filter Clusters by rows 0 and 1
    filtered_clusters = filter_clusters_by_row(magenta_clusters, [0, 1])

    # Find Rightmost Magenta Pixels in the filtered clusters
    rightmost_pixels = []
    for cluster in filtered_clusters:
        rightmost_pixels.append(find_rightmost_pixel(cluster))

    # Place Yellow Pixels
    for pixel in rightmost_pixels:
        output_grid[rows - 1, pixel[1]] = 4

    return output_grid


for i, (input_grid, expected_output) in enumerate(example_grids):
    transformed_output = transform(input_grid)
    print(f"Example {i+1}:")
    code_execution(input_grid, expected_output, transformed_output)