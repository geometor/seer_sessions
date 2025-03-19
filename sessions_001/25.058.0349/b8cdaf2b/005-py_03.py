def get_grid_differences(grid1, grid2):
    """
    Compares two grids and returns the coordinates and values of differing pixels.
    """
    differences = []
    rows = len(grid1)
    cols = len(grid1[0])  # Assumes grids are same shape
    for i in range(rows):
        for j in range(cols):
            if grid1[i][j] != grid2[i][j]:
                differences.append({
                    'row': i,
                    'col': j,
                    'grid1_value': grid1[i][j],
                    'grid2_value': grid2[i][j]
                })
    return differences

def analyze_results(task_data):
    results = {}
    for example_idx, example in enumerate(task_data['train']):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)
        differences = get_grid_differences(expected_output_grid, predicted_output_grid)
        
        results[f'example_{example_idx}'] = {
            'success': len(differences) == 0,
            'differences': differences
        }
    return results


#this is a dummy task, replace with a real task in a real run
task_data = {
 'train': [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [5, 0, 0, 5, 0, 0, 5, 0, 0, 9],
               [5, 0, 0, 5, 0, 0, 5, 0, 0, 9],
               [5, 0, 0, 5, 0, 0, 5, 0, 0, 9],
               [5, 0, 0, 5, 0, 0, 5, 0, 0, 9],
               [5, 0, 0, 5, 0, 0, 5, 0, 0, 0]],
     'output': [[5, 0, 0, 5, 0, 0, 5, 0, 0, 9],
                [5, 0, 0, 5, 0, 0, 5, 0, 0, 9],
                [5, 0, 0, 5, 0, 0, 5, 0, 0, 9],
                [5, 0, 0, 5, 0, 0, 5, 0, 0, 9],
                [5, 0, 0, 5, 0, 0, 5, 0, 0, 0],
                [5, 0, 0, 5, 0, 0, 5, 0, 0, 0]]},

    {'input': [[6, 6, 6, 6, 6, 6, 6, 6, 0, 6],
               [6, 6, 6, 6, 6, 6, 6, 6, 0, 6],
               [6, 6, 6, 6, 6, 6, 6, 6, 0, 6],
               [6, 6, 6, 6, 6, 6, 6, 6, 0, 6],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
     'output': [[6, 6, 6, 6, 6, 6, 6, 6, 0, 6],
                [6, 6, 6, 6, 6, 6, 6, 6, 0, 6],
                [6, 6, 6, 6, 6, 6, 6, 6, 0, 6],
                [6, 6, 6, 6, 6, 6, 6, 6, 0, 6],
                [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]]},
               
    {'input': [[1, 0, 8, 3, 8, 0, 1, 8, 0, 0],
               [0, 7, 0, 4, 0, 0, 6, 0, 0, 5],
               [1, 8, 0, 5, 1, 0, 0, 8, 0, 7],
               [0, 0, 2, 0, 0, 7, 8, 0, 0, 0],
               [0, 4, 0, 0, 8, 0, 0, 5, 0, 0]],
     'output': [[1, 7, 8, 3, 8, 7, 1, 8, 0, 5],
                [0, 7, 2, 4, 1, 7, 6, 0, 0, 5],
                [1, 8, 2, 5, 1, 7, 0, 8, 0, 7],
                [0, 0, 2, 0, 0, 7, 8, 0, 0, 0],
                [0, 4, 0, 0, 8, 0, 0, 5, 0, 0]]}
 ]
}

analysis_results = analyze_results(task_data)
print(analysis_results)
