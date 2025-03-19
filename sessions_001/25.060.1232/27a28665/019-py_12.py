import numpy as np

def analyze_results(examples, transform_function):
    results = []
    for example in examples:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform_function(input_grid)
        
        # Basic correctness check
        correct = np.array_equal(predicted_output, expected_output)
        
        # Count Homogeneous 2x2 squares for the whole grid and also for specific colors:
        total_2x2_count = 0
        color_counts = {}
        
        for r in range(input_grid.shape[0] - 1):
           for c in range(input_grid.shape[1] -1):
              subgrid = input_grid[r:r+2, c:c+2]
              if np.all(subgrid == subgrid[0,0]):
                  total_2x2_count += 1
                  color = subgrid[0,0]
                  if color not in color_counts:
                      color_counts[color] = 0
                  color_counts[color] +=1 
        
        results.append({
            'input': input_grid.tolist(),
            'expected_output': expected_output.tolist(),
            'predicted_output': predicted_output.tolist(),
            'correct': correct,
            'total_2x2_count': total_2x2_count,
            'color_counts' : color_counts
        })
    return results

# Provided examples (replace with actual examples from the task)
examples = [
    {'input': [[8, 8, 8], [8, 8, 8], [5, 5, 5]], 'output': [[4]]},  # Example 1
    {'input': [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]], 'output': [[9]]},  # Example 2
    {'input': [[6, 5, 8, 5], [5, 8, 6, 8], [8, 5, 8, 6], [5, 8, 6, 5]], 'output': [[0]]}   # Example 3
]

transform_function = transform  # use the provided transform function

analysis = analyze_results(examples, transform_function)

for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Correct: {result['correct']}")
    print(f"  Total 2x2 count: {result['total_2x2_count']}")
    print(f" Color counts: {result['color_counts']}")
    print(f"  Predicted Output: {result['predicted_output']}")
    print(f"  Expected Output: {result['expected_output']}")
    print("-" * 20)