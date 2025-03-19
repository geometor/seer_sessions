import numpy as np
from scipy.ndimage import label, center_of_mass

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        # Background color
        values, counts = np.unique(input_grid, return_counts=True)
        background_color = values[np.argmax(counts)]

        # Identify objects
        non_background_mask = input_grid != background_color
        labeled_array, num_features = label(non_background_mask)

        if num_features > 0:
            # Find the center of mass
            center = center_of_mass(non_background_mask)
            center_row, center_col = int(round(center[0])), int(round(center[1]))
            
            #extract 3x3
            rows, cols = input_grid.shape
            start_row = max(0, center_row - 1)
            end_row = min(rows, center_row + 2)
            start_col = max(0, center_col - 1)
            end_col = min(cols, center_col + 2)
            
            extracted_grid = input_grid[start_row:end_row, start_col:end_col]

            if extracted_grid.shape != (3,3):
                # Pad with background
                padded_grid = np.full((3, 3), background_color)
                
                pr_start_row = max(0, 1 - center_row)
                pr_end_row = min(3, rows + (2-center_row))
                
                pc_start_col = max(0, 1 - center_col)
                pc_end_col = min(3, cols + (2 - center_col))

                padded_grid[pr_start_row:pr_end_row, pc_start_col:pc_end_col] = extracted_grid
                extracted_grid = padded_grid

            comparison = np.array_equal(extracted_grid, output_grid)

        else:
            extracted_grid = np.zeros((3,3)).tolist()
            comparison = False

        results.append({
            'background_color': int(background_color),
            'num_features': num_features,
            'center': (center_row, center_col) if num_features > 0 else None,
            'extracted_grid_shape': extracted_grid.shape if num_features>0 else (0,0),
            'comparison': comparison
        })

    return results

# Assume 'task' variable is loaded with the task data (as in the notebook environment)
# The following line is replaced by the actual task loading in the notebook
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 8, 3, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0], [1, 8, 3], [0, 1, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0], [0, 3, 0], [3, 3, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 2, 0], [2, 2, 2], [0, 2, 0]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 4, 4, 4, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5]],
            "output": [[5, 4, 5], [4, 4, 4], [5, 4, 5]]
        }
    ]
}

results = analyze_examples(task)
for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Background Color: {result['background_color']}")
    print(f"  Number of Objects: {result['num_features']}")
    print(f"  Center: {result['center']}")
    print(f" Extracted grid shape: {result['extracted_grid_shape']}")
    print(f"  Correct Output: {result['comparison']}")