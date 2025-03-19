import numpy as np

def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    print(f"Input shape: {input_grid.shape}")
    print(f"Output shape: {output_grid.shape}")
    print(f"Input unique colors: {np.unique(input_grid)}")
    print(f"Output unique colors: {np.unique(output_grid)}")
    # Check differences using current code generated output
    current_code_output = transform(input_grid)
    print(f"Current code output shape: {current_code_output.shape}")    
    print(f"Difference between expected and current code: {np.sum(output_grid != current_code_output)}")

# Assuming 'task' is a dictionary loaded with ARC data for the current task.
for i, example in enumerate(task['train']):
    print(f"--- Example {i} ---")
    analyze_example(example)
