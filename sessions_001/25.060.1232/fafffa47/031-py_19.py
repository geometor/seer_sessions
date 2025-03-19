import numpy as np

def analyze_section(input_grid):
    """
    Analyzes 2x1 sections of the input grid and reports their contents.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    section_data = []

    for i in range(0, height, 2):
        for j in range(width):
            section = input_grid[i:i+2, j:j+1]
            section_data.append({
                'row_start': i,
                'col': j,
                'contents': section.tolist(),
                'has_maroon': 9 in section,
                'top_value' : section[0][0]
            })

    return section_data

def test_transform_with_analysis(task, transform_function):
    """
    Tests the transform function on each example and provides section analysis.
    """
    results = []
    for example in task['train']:
        input_grid = example['input']
        expected_output_grid = example['output']
        predicted_output_grid = transform_function(input_grid)
        is_correct = predicted_output_grid == expected_output_grid

        section_analysis = analyze_section(input_grid)

        results.append({
            'input': input_grid,
            'expected_output': expected_output_grid,
            'predicted_output': predicted_output_grid,
            'is_correct': is_correct,
            'section_analysis': section_analysis
        })
    return results
# Dummy task for demonstration. Replace with the actual task data when available.

dummy_task = {
    'train': [
        {'input': [[1, 9], [9, 1]], 'output': [[1, 2]]},
        {'input': [[0, 4], [5, 6]], 'output': [[0, 4]]},
        {'input': [[9, 1, 9], [2, 3, 2]], 'output': [[2, 1, 2]]}
    ]
}
import json
print(json.dumps(test_transform_with_analysis(dummy_task, transform), indent=2))
