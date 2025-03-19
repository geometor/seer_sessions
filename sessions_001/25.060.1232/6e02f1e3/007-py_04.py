import numpy as np

def get_grid_dimensions(grid_string):
    """Helper function to get dimensions from grid string representation."""
    rows = grid_string.strip().split('\n')
    return len(rows), len(rows[0])

def analyze_results(train_examples):
    results = []
    for i, example in enumerate(train_examples):
        input_grid_str = example['input']
        output_grid_str = example['output']
        input_rows, input_cols = get_grid_dimensions(input_grid_str)
        output_rows, output_cols = get_grid_dimensions(output_grid_str)
        
        #check current function
        input_grid = np.array([[int(pixel) for pixel in row] for row in input_grid_str.split('\n')])
        
        output_grid = transform(input_grid)
        predicted_output_str = '\n'.join([''.join(map(str, row)) for row in output_grid])

        results.append({
            'example_number': i + 1,
            'input_dimensions': f'{input_rows}x{input_cols}',
            'output_dimensions': f'{output_rows}x{output_cols}',
            'success': predicted_output_str == output_grid_str,
            'notes': ''
        })
        if not predicted_output_str == output_grid_str:
          notes = ""
          if input_rows != input_cols:
              notes += "Input grid is not square. "
          results[-1]['notes'] = notes

    return results

train_examples = [
    {'input': '222\n222\n222', 'output': '500\n050\n005'},
    {'input': '1111\n1111\n1111\n1111', 'output': '5000\n0500\n0050\n0005'},
    {'input': '8339\n8329\n8139\n8339', 'output': '5000\n0500\n0050\n0005'},
    {'input': '111\n111', 'output': '500\n050'}
]

analysis = analyze_results(train_examples)

for result in analysis:
    print(result)
