# Example usage (assuming 'task' is loaded as described in previous turns):

def grid_to_string(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

def print_example(task, example_index, io_type):
  if io_type == "input":
    print(grid_to_string(task['train'][example_index]['input']))
  if io_type == "output":
    print(grid_to_string(task['train'][example_index]['output']))
  if io_type == "predicted":
    print(grid_to_string(transform(np.array(task['train'][example_index]['input']))))

def get_color_counts(grid, color):
    return np.sum(grid == color)

# Example: Get the number of azure pixels in the first example's input
print(f"Number of azure pixels in input 0: {get_color_counts(task['train'][0]['input'], 8)}")
print(f"Number of azure pixels in output 0: {get_color_counts(task['train'][0]['output'], 8)}")
print(f"Number of azure pixels in prediction 0: {get_color_counts(transform(np.array(task['train'][0]['input'])), 8)}")

print (f"Input 0")
print_example(task, 0, 'input')
print (f"Output 0")
print_example(task, 0, 'output')
print (f"Prediction 0")
print_example(task, 0, 'predicted')

print(f"Number of azure pixels in input 1: {get_color_counts(task['train'][1]['input'], 8)}")
print(f"Number of azure pixels in output 1: {get_color_counts(task['train'][1]['output'], 8)}")
print(f"Number of azure pixels in prediction 1: {get_color_counts(transform(np.array(task['train'][1]['input'])), 8)}")

print (f"Input 1")
print_example(task, 1, 'input')
print (f"Output 1")
print_example(task, 1, 'output')
print (f"Prediction 1")
print_example(task, 1, 'predicted')

print(f"Number of azure pixels in input 2: {get_color_counts(task['train'][2]['input'], 8)}")
print(f"Number of azure pixels in output 2: {get_color_counts(task['train'][2]['output'], 8)}")
print(f"Number of azure pixels in prediction 2: {get_color_counts(transform(np.array(task['train'][2]['input'])), 8)}")

print (f"Input 2")
print_example(task, 2, 'input')
print (f"Output 2")
print_example(task, 2, 'output')
print (f"Prediction 2")
print_example(task, 2, 'predicted')