def analyze_results(input_grid, expected_output, actual_output):
    """
    Analyzes the results of the transformation and returns relevant metrics.
    """
    correct = np.all(expected_output == actual_output)
    diff = expected_output != actual_output
    diff_count = np.sum(diff)
    

    metrics = {
        'correct': correct,
        'diff_count': diff_count,
        'input_shape': input_grid.shape,
        'output_shape': expected_output.shape,
      
    }
    
    if not correct:
        #where are the differences
        diff_coords = np.where(diff)
        
        
        metrics['diff_coords']=diff_coords
        metrics['input_vals_diff']= input_grid[diff_coords]
        metrics['expected_vals_diff']= expected_output[diff_coords]
        metrics['actual_vals_diff'] = actual_output[diff_coords]
    

    return metrics

# Hypothetical example data (replace with actual data from the task)
examples = [
    {
        'input': np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        'output': np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    },
        {
        'input': np.array([[0, 1, 0, 1, 0],[0, 1, 0, 0, 0]]),
        'output': np.array([[0, 2, 0, 2, 0],[0, 2, 0, 0, 0]]),
    },
    {
        'input': np.array([[1, 0, 1], [0, 1, 0], [0, 0, 0]]),
        'output': np.array([[2, 0, 2], [0, 0, 0], [0, 0, 0]]),
    },
    
    {
        'input': np.array([[1, 1, 0, 1, 1], [0, 0, 1, 0, 0]]),
        'output': np.array([[2, 2, 0, 2, 2], [0, 0, 0, 0, 0]]),
    },

    {
        'input': np.array([[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1,1,1,1,1]]),
        'output': np.array([[0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [2,2,2,2,2]]),
    },
]

for i, example in enumerate(examples):
  actual_output = transform(example['input'])
  analysis = analyze_results(example['input'], example['output'], actual_output)
  print(f"Example {i+1}:")
  print(analysis)
