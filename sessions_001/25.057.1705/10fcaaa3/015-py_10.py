import numpy as np

def get_yellow_positions(grid):
    return np.array(np.where(grid == 4)).T.tolist()

examples = task.get("train")
for i, example in enumerate(examples):
     input_grid = np.array(example['input'])
     output_grid = np.array(example['output'])
     input_height, input_width = input_grid.shape
     output_height, output_width = output_grid.shape
     input_yellow_positions = get_yellow_positions(input_grid)
     output_yellow_positions = get_yellow_positions(output_grid)

     print(f"Example {i+1}:")
     print(f"  Input Dimensions: {input_height}x{input_width}")
     print(f"  Output Dimensions: {output_height}x{output_width}")
     print(f"  Input Yellow Positions: {input_yellow_positions}")
     print(f"  Output Yellow Positions: {output_yellow_positions}")

     # verify background is a checkerboard
     checkerboard = True
     for row in range(output_height):
        for col in range(output_width):
            if (row + col) % 2 == 0:
                if output_grid[row,col] != 8:
                    checkerboard = False
                    break;
            else:
                if output_grid[row,col] != 0 and output_grid[row,col] != 4:
                    checkerboard = False
                    break
        if checkerboard != True:
            break;
     print(f" Checkerboard: {checkerboard}")
     print("-----")