import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    height, width = input_grid.shape

    # Find potential separators (vertical lines of the same color)
    separators = []
    for x in range(width):
        first_color = input_grid[0, x]
        is_separator = True
        for y in range(1, height):
            if input_grid[y, x] != first_color:
                is_separator = False
                break
        if is_separator:
            separators.append((x, first_color))

    # Find repeating unit size.
    repeating_unit_width = 0
    if separators:
      separator_x = separators[0][0]
      repeating_unit_width = separator_x

    return {
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape,
        'separators': separators,
        'repeating_unit_width': repeating_unit_width,
        'exact_match': np.array_equal(input_grid, output_grid)
    }

def show_grid(grid) :
    print(np.array(grid))

# Placeholder for the actual grids from the task
train_examples = task['train']
test_examples = task['test']

example_data = []
for i, example in enumerate(train_examples):
  input_grid = example['input']
  output_grid = example['output']
  show_grid(input_grid)
  print("---")
  show_grid(output_grid)
  analysis = analyze_example(input_grid, output_grid)
  example_data.append({
        'example_number': i + 1,
        'analysis': analysis
  })
  print(analysis)

print("\n--- Summary ---")
for data in example_data:
    print(f"Example {data['example_number']}:")
    print(f"  Input Shape: {data['analysis']['input_shape']}")
    print(f"  Output Shape: {data['analysis']['output_shape']}")
    print(f"  Separators: {data['analysis']['separators']}")
    print(f"  Repeating Unit Width: {data['analysis']['repeating_unit_width']}")
    print(f"  Exact Match: {data['analysis']['exact_match']}")
