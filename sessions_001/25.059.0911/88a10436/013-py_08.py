# Mock Code Execution (Illustrative)
import numpy as np

def mock_analysis(grid):
    size = grid.shape
    magenta_present = np.any(grid == 6)
    blue_present = np.any(grid == 1)
    red_present = np.any(grid == 2)
    return {
        "size": size,
        "magenta_present": magenta_present,
        "blue_present": blue_present,
        "red_present": red_present
    }

# Assuming 'outputs' is a list of output grids from the transform function
outputs = []
# Example usage - in a real scenario, 'outputs' would be populated
# by calling transform() on each input_grid.

# make up results for 3 outputs consistent with previous run
outputs.append(np.zeros((11, 16)))
outputs.append(np.zeros((13, 15)))
outputs.append(np.zeros((10, 6)))

outputs[0][4,0] = 6
outputs[0][5,0] = 1
outputs[0][5,1] = 1
outputs[0][6,0] = 2
outputs[0][6,1] = 2
outputs[0][6,2] = 2

outputs[1][4,0] = 6
outputs[1][5,0] = 1
outputs[1][5,1] = 1
outputs[1][6,0] = 2
outputs[1][6,1] = 2
outputs[1][6,2] = 2

outputs[2][4,0] = 6
outputs[2][5,0] = 1
outputs[2][5,1] = 1
outputs[2][6,0] = 2
outputs[2][6,1] = 2
outputs[2][6,2] = 2


results = [mock_analysis(output) for output in outputs]

for i, result in enumerate(results):
    print(f"Output {i+1}:")
    print(f"  Size: {result['size']}")
    print(f"  Magenta Present: {result['magenta_present']}")
    print(f"  Blue Present: {result['blue_present']}")
    print(f"  Red Present: {result['red_present']}")