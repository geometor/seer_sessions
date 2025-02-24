import numpy as np

def grid_characteristics(grid):
    grid = np.array(grid)
    unique_colors = np.unique(grid)
    num_unique_colors = len(unique_colors)
    height, width = grid.shape
    color_counts = {color: np.sum(grid == color) for color in unique_colors}

    objects = {}
    object_count = 0
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color):
        if (row < 0 or row >= height or col < 0 or col >= width or
            visited[row, col] or grid[row, col] != color):
            return []
        visited[row, col] = True
        region = [(row, col)]
        region.extend(dfs(row + 1, col, color))
        region.extend(dfs(row - 1, col, color))
        region.extend(dfs(row, col + 1, color))
        region.extend(dfs(row, col - 1, color))
        return region

    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                color = grid[r, c]
                region = dfs(r, c, color)
                if region:
                    object_count += 1
                    objects[f'object_{object_count}'] = {
                        'color': int(color),
                        'pixels': len(region),
                        'coordinates': region,
                    }
    
    return {
        'height': height,
        'width': width,
        'unique_colors': unique_colors.tolist(),
        'num_unique_colors': num_unique_colors,
        'color_counts': color_counts,
        'objects': objects,
        'object_count': object_count,
    }
def report_examples(examples):
    report = {}
    for example_id, example in examples.items():
        report[example_id] = {
            'input': grid_characteristics(example['input']),
            'output': grid_characteristics(example['output'])
        }
    return report

example_report = report_examples(examples)
print(example_report)
