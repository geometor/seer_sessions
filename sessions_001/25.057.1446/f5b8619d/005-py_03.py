# Example analysis (Conceptual - for illustration)
input_grid = [[...], [...]] #example input
output_grid = [[...], [...]] #example output

input_colors = set(np.array(input_grid).flatten())
output_blocks = {}

for color in input_colors:
    # Find coordinates of the color in the input
    coords = np.where(np.array(input_grid) == color)
    #use first found coordinate
    row, col = coords[0][0], coords[1][0]

    # Extract corresponding 2x2 block from the output
    block = np.array(output_grid)[2*row:2*row+2, 2*col:2*col+2]
    output_blocks[color] = block.tolist()

print(f"Example Analysis:")
print(f"  Input Colors: {input_colors}")
print(f"  Output Blocks: {output_blocks}")
