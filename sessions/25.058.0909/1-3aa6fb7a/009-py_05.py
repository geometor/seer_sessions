import numpy as np

def analyze_regions(grid):
    """
    Analyzes contiguous regions of azure (8) pixels, calculating metrics.
    """
    def find_contiguous_regions(grid, color):
        visited = np.zeros_like(grid, dtype=bool)
        regions = []

        def dfs(row, col):
            if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                    visited[row, col] or grid[row, col] != color):
                return []

            visited[row, col] = True
            region = [(row, col)]

            region.extend(dfs(row + 1, col))
            region.extend(dfs(row - 1, col))
            region.extend(dfs(row, col + 1))
            region.extend(dfs(row, col - 1))
            return region

        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if grid[row, col] == color and not visited[row, col]:
                    regions.append(dfs(row, col))

        return regions
    
    azure_regions = find_contiguous_regions(grid, 8)
    analysis = []
    for region in azure_regions:
        rows, cols = zip(*region)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        size = len(region)
        analysis.append({
            'min_row': min_row,
            'max_row': max_row,
            'min_col': min_col,
            'max_col': max_col,
            'width': width,
            'height': height,
            'size': size,
            'shape': 'rectangle' if size == width * height else 'irregular',
        })
    return analysis

# Load the example grids (replace with actual grid data)
task_id = '272f91fa'
train_example = __examples__[task_id]['train'][0]
train_input_0 = np.array(train_example['input'])
train_output_0 = np.array(train_example['output'])
train_result_0 = transform(train_input_0)
train_example = __examples__[task_id]['train'][1]
train_input_1 = np.array(train_example['input'])
train_output_1 = np.array(train_example['output'])
train_result_1 = transform(train_input_1)
train_example = __examples__[task_id]['train'][2]
train_input_2 = np.array(train_example['input'])
train_output_2 = np.array(train_example['output'])
train_result_2 = transform(train_input_2)


analysis_input_0 = analyze_regions(train_input_0)
analysis_output_0 = analyze_regions(train_output_0)
analysis_result_0 = analyze_regions(train_result_0)
analysis_input_1 = analyze_regions(train_input_1)
analysis_output_1 = analyze_regions(train_output_1)
analysis_result_1 = analyze_regions(train_result_1)
analysis_input_2 = analyze_regions(train_input_2)
analysis_output_2 = analyze_regions(train_output_2)
analysis_result_2 = analyze_regions(train_result_2)

print(f"{analysis_input_0=}")
print(f"{analysis_output_0=}")
print(f"{analysis_result_0=}")
print(f"{analysis_input_1=}")
print(f"{analysis_output_1=}")
print(f"{analysis_result_1=}")
print(f"{analysis_input_2=}")
print(f"{analysis_output_2=}")
print(f"{analysis_result_2=}")


def compare_grids(grid1, grid2):
    """Compares two grids and returns the differences."""
    if grid1.shape != grid2.shape:
        return "Different shapes"
    diff = grid1 != grid2
    return np.argwhere(diff)

diff_0 = compare_grids(train_output_0, train_result_0)
diff_1 = compare_grids(train_output_1, train_result_1)
diff_2 = compare_grids(train_output_2, train_result_2)

print(f"{diff_0=}")
print(f"{diff_1=}")
print(f"{diff_2=}")