import numpy as np

def get_grid_info(grid):
    """Provides detailed information about a given grid."""
    height, width = grid.shape
    unique_colors = np.unique(grid)
    num_unique_colors = len(unique_colors)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    
    info = {
        "height": height,
        "width": width,
        "unique_colors": unique_colors.tolist(),
        "num_unique_colors": num_unique_colors,
        "color_counts": color_counts,
    }
    return info

# Example grids (replace with actual data)
train_pairs = [
    {
        "input": np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        "output": np.array([[1, 1, 2, 2, 3, 3], [1, 1, 2, 2, 3, 3], [4, 4, 5, 5, 6, 6], [4, 4, 5, 5, 6, 6], [7, 7, 8, 8, 9, 9], [7, 7, 8, 8, 9, 9]])
    },
    {
        "input": np.array([[0, 1, 2], [3, 4, 5]]),
        "output": np.array([[0, 0, 1, 1, 2, 2], [0, 0, 1, 1, 2, 2], [3, 3, 4, 4, 5, 5], [3, 3, 4, 4, 5, 5]])
    },
    {
        "input": np.array([[5, 6], [7, 8]]),
        "output": np.array([[5, 5, 6, 6], [5, 5, 6, 6], [7, 7, 8, 8], [7, 7, 8, 8]])
    },
     {
        "input": np.array([[1]]),
        "output": np.array([[1,1],[1,1]])
    },
    {
        "input": np.array([[1,2],[3,4]]),
        "output": np.array([[1,1,2,2],[1,1,2,2],[3,3,4,4],[3,3,4,4]])
    }   
]

for i, pair in enumerate(train_pairs):
    print(f"Train Pair {i+1}:")
    print("Input Info:")
    print(get_grid_info(pair['input']))
    print("Output Info:")
    print(get_grid_info(pair['output']))
    print("-" * 20)