import numpy as np

def get_pixel_positions(grid, color):
    return np.array(np.where(grid == color)).T.tolist()

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        green_positions = get_pixel_positions(input_grid, 3)
        gray_positions = get_pixel_positions(input_grid, 5)
        changed_pixels = np.where(input_grid != output_grid)
        changed_to_green = []

        for x,y in zip(changed_pixels[0], changed_pixels[1]):
            if output_grid[x,y] == 3:
                changed_to_green.append([x,y])


        results.append({
            'example': i + 1,
            'green_positions': green_positions,
            'gray_positions': gray_positions,
            'changed_to_green': changed_to_green
        })
    return results

# Assuming 'task' is your dictionary containing the training examples
examples = task['train']

analysis = analyze_examples(examples)

for item in analysis:
    print(item)