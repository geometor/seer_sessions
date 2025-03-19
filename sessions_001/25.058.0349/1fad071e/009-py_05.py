import numpy as np
from skimage.measure import label, regionprops

def analyze_blue_objects(grid):
    """
    Identifies contiguous blue regions in a grid and returns their properties.
    """
    grid = np.array(grid)
    blue_mask = (grid == 1)
    labeled_mask = label(blue_mask)
    regions = regionprops(labeled_mask)

    object_data = []
    for region in regions:
        object_data.append({
            'area': region.area,
            'bbox': region.bbox,  # (min_row, min_col, max_row, max_col)
        })
    return object_data

# Example usage and gathering of data for all examples
examples = [
    ([[0, 1, 0], [0, 1, 0], [0, 1, 0]], [1, 1, 1]),
    ([[0, 0, 0], [0, 1, 0], [0, 1, 0]], [0, 1, 0]),
    ([[0, 0, 0], [0, 0, 0], [0, 1, 0]], [0, 0, 0]),
    ([[1, 0, 0], [1, 0, 0], [1, 0, 1]], [1, 0, 1]),
    ([[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]], [0,0,1,0,0])
]

results = []
for input_grid, expected_output in examples:
    blue_objects = analyze_blue_objects(input_grid)
    results.append({
        'input': input_grid,
        'expected_output': expected_output,
        'blue_objects': blue_objects
    })

print(results)