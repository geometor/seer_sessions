results = {'example_1': {'input_shape': (6, 6), 'output_shape': (6, 6), 'differences': 10, 'same_size': True}, 'example_2': {'input_shape': (5, 5), 'output_shape': (5, 5), 'differences': 8, 'same_size': True}, 'example_3': {'input_shape': (4, 4), 'output_shape': (4, 4), 'differences': 6, 'same_size': True}, 'example_4': {'input_shape': (6, 7), 'output_shape': (6, 7), 'differences': 12, 'same_size': True}, 'example_5': {'input_shape': (4, 7), 'output_shape': (4, 7), 'differences': 9, 'same_size': True}}
print(results)

# count the colors in each input and output
def count_colors(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

for i, example in enumerate(train):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        input_colors = count_colors(input_grid)
        output_colors = count_colors(expected_output_grid)
        print(f"Example {i+1} Input Colors: {input_colors}")
        print(f"Example {i+1} Output Colors: {output_colors}")