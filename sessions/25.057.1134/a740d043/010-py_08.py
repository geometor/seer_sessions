import numpy as np

def find_clusters(grid):
    # Find clusters of adjacent non-blue pixels
    visited = np.zeros_like(grid, dtype=bool)
    clusters = []

    def dfs(r, c, cluster_colors):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] == 1):
            return []

        visited[r, c] = True
        cluster_colors.add(grid[r,c])
        current_cluster = [(r, c, grid[r, c])]

        current_cluster.extend(dfs(r + 1, c, cluster_colors))
        current_cluster.extend(dfs(r - 1, c, cluster_colors))
        current_cluster.extend(dfs(r, c + 1, cluster_colors))
        current_cluster.extend(dfs(r, c - 1, cluster_colors))
        return current_cluster

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 1 and not visited[r, c]:
                cluster_colors = set()
                cluster = dfs(r, c, cluster_colors)
                if cluster:
                    clusters.append(cluster)
    return clusters

def get_cluster_bounds(cluster):
    # find min and max row and col
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for r, c, _ in cluster:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    clusters = find_clusters(input_grid)
    num_clusters = len(clusters)

    cluster_data = []
    for cluster in clusters:
        min_r, min_c, max_r, max_c = get_cluster_bounds(cluster)
        cluster_data.append({
            "min_row": min_r,
            "min_col": min_c,
            "max_row": max_r,
            "max_col": max_c,
            "width": max_c - min_c + 1,
            "height": max_r - min_r + 1,
            "colors": list(set([color for _,_,color in cluster]))
        })

    return {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "num_clusters": num_clusters,
        "clusters": cluster_data,
        "output": output_grid.tolist()  # Include the actual output
    }

task = {
    "train": [
        {
            "input": [[1, 1, 1, 1, 1, 1, 1, 1], [1, 2, 2, 2, 1, 1, 1, 1], [1, 2, 2, 2, 1, 1, 1, 1], [1, 2, 2, 2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 1, 3, 3]],
            "output": [[2, 2, 2], [2, 2, 2], [2, 2, 2], [0, 0, 0], [0, 0, 0], [0, 0, 0], [3, 3, 0], [3, 3, 0], [3, 3, 0]]
        },
        {
            "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1]],
            "output": [[3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 0, 0]]
        },
        {
            "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            "output": [[2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input" : [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2, 2, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 3, 3, 1, 1, 1, 1, 1, 1], [1, 3, 3, 1, 1, 1, 1, 1, 1], [1, 3, 3, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]],
            "output": [[2, 2, 2], [2, 2, 2], [2, 2, 2], [0, 0, 0], [3, 3, 0], [3, 3, 0], [3, 3, 0]]
        }
    ]
}

results = []
for example in task["train"]:
    results.append(analyze_example(example["input"], example["output"]))

print(results)