import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid."""
    return {
        'shape': grid.shape,
        'unique_values': np.unique(grid).tolist(),
    }
def find_object(grid, value):
    # find the coordinates of cell with specified value
    for i, row in enumerate(grid):
        for j, cell_value in enumerate(row):
            if cell_value == value:
                return (i, j)
    return None

def code_execution(input_grid, output_grid, predicted_grid):
   
    input_desc = describe_grid(input_grid)
    output_desc = describe_grid(output_grid)
    predicted_desc = describe_grid(predicted_grid)
    green_input = find_object(input_grid, 3)
    green_output = find_object(output_grid, 3)
    match = np.array_equal(output_grid, predicted_grid)
    
    return{
      'input': input_desc,
      'output': output_desc,
      'predicted' : predicted_desc,      
      'green_input_location': green_input,
      'green_output_location': green_output,
      'match' : match
    }

# Example Data (replace with your actual data)
examples = [
    {
        'input': np.array([[4, 0, 0], [0, 3, 0], [0, 0, 0]]),
        'output': np.array([[4, 0, 0], [0, 0, 3], [0, 0, 0]]),
    },
    {
        'input': np.array([[0, 0, 0, 0], [0, 0, 3, 0], [0, 0, 0, 0]]),
        'output': np.array([[0, 0, 0, 0], [0, 0, 0, 3], [0, 0, 0, 0]]),
    },
        {
        'input': np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 3, 0, 0]]),
        'output': np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 3, 0]]),
    },
            {
        'input': np.array([[0, 0, 0, 0, 3]]),
        'output': np.array([[0, 0, 0, 0, 3]]),
    },
]
results = []
for example in examples:
    predicted_output = transform(example['input'])
    results.append(code_execution(example['input'], example['output'], predicted_output))

for i,r in enumerate(results):
    print(f"Example {i+1}:")
    print(r)
