import numpy as np

def describe_grid(grid):
    return f"Grid: {grid.tolist()}, Shape: {grid.shape}"

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        # Previous transform function
        transformed_grid = np.copy(input_grid)
        if transformed_grid.shape[0] >=2 and transformed_grid.shape[1] >=2: #ensure grid is big enough
            transformed_grid[1][0] = input_grid[0][0]
            transformed_grid[1][1] = input_grid[1][0]
            transformed_grid[0][1] = input_grid[1][1]
            transformed_grid[0][0] = input_grid[0][1]


        match = np.array_equal(transformed_grid, output_grid)
        
        results.append({
            'example_index': i,
            'input_description': describe_grid(input_grid),
            'output_description': describe_grid(output_grid),
            'transformation_match': match
        })
    return results
# Mock examples (replace with actual data from the task)
examples = [
    {'input': [[1, 2], [3, 4], [5,6]], 'output': [[2, 4], [1, 3], [5,6]]},
    {'input': [[6, 7, 9], [8, 5, 4],[3,1,2]], 'output': [[7, 5, 9], [6, 8, 4],[3,1,2]]},
    {'input': [[9, 1], [2, 4],[3,8],[7,5]], 'output': [[1, 4], [9, 2],[3,8],[7,5]]},
    {'input': [[4, 5, 6, 1], [7, 2, 9, 3],[1,2,3,8]], 'output': [[5, 2, 6, 1], [4, 7, 9, 3],[1,2,3,8]]}

]

analysis_results = analyze_examples(examples)

for result in analysis_results:
    print(result)