def analyze_grid(grid):
    grid = np.array(grid)
    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    rows, cols = grid.shape
    bounding_box_area = rows * cols
    return {
        'shape': (rows, cols),
        'unique_colors': unique_colors.tolist(),
        'color_counts': color_counts,
        'bounding_box_area': bounding_box_area
    }

def compare_grids(input_grid, output_grid, predicted_output_grid):
        input_analysis = analyze_grid(input_grid)
        output_analysis = analyze_grid(output_grid)
        predicted_output_analysis = analyze_grid(predicted_output_grid)

        return{
          'input':input_analysis,
          'output':output_analysis,
          'predicted': predicted_output_analysis
        }

# Example usage (assuming the existence of train_input_0, train_output_0, predicted_output_0, etc.)
examples = {}
for i in range(len(task_data['train'])): # Use len(task_data['train']) instead of hardcoding 3
    input_grid = task_data['train'][i]['input']
    output_grid = task_data['train'][i]['output']
    predicted_output_grid = transform(input_grid)
    comparison = compare_grids(input_grid, output_grid, predicted_output_grid)
    examples[f'example_{i}'] = comparison

import json
print(json.dumps(examples, indent=2))
