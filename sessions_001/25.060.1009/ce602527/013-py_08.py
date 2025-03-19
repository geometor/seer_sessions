# Example 1 (Correctly handled)
print("Example 1:")
input_grid = np.array([[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 4, 0, 0, 0],
                       [0, 0, 0, 4, 0, 0, 0],
                       [0, 4, 4, 4, 4, 4, 0],
                       [0, 0, 0, 4, 0, 0, 0],
                       [0, 0, 0, 4, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0]])
output_grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                        [0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
                        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
objects = find_objects(input_grid)
print(f"  Objects: {objects}")
if 4 in objects:
    for obj in objects[4]:
        h, w = get_plus_extent(obj)
        print(f"  Yellow Plus Extent: h={h}, w={w}")
print(f" input grid size: {input_grid.shape}")
print(f" output grid size: {output_grid.shape}")
#result = transform(input_grid) #we know this works
#print(np.array_equal(result, output_grid))

# Example 2 (Incorrectly handled)
print("\nExample 2:")
input_grid = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                       [8, 8, 8, 8, 8, 8, 8, 8, 8],
                       [8, 8, 8, 8, 8, 8, 8, 8, 8],
                       [8, 8, 8, 1, 8, 8, 8, 8, 8],
                       [8, 8, 8, 8, 8, 8, 8, 8, 8],
                       [8, 8, 8, 8, 8, 8, 8, 8, 8],
                       [8, 8, 8, 8, 8, 8, 8, 8, 8]])
output_grid = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
objects = find_objects(input_grid)
print(f"  Objects: {objects}")
if 1 in objects:
    for obj in objects[1]:
        h, w = get_plus_extent(obj)
        print(f"  Blue Plus Extent: h={h}, w={w}")
print(f" input grid size: {input_grid.shape}")
print(f" output grid size: {output_grid.shape}")
result = transform(input_grid)
print(f"  Correct Result: {np.array_equal(result, output_grid)}")

# Example 3 (Incorrectly handled)
print("\nExample 3:")
input_grid = np.array([[5, 5, 5, 5, 5, 5, 5, 5],
                       [5, 5, 5, 5, 5, 2, 5, 5],
                       [5, 5, 5, 5, 5, 5, 5, 5],
                       [5, 5, 5, 5, 5, 5, 5, 5],
                       [5, 5, 5, 5, 5, 5, 5, 5]])
output_grid = np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                        [5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5],
                        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
objects = find_objects(input_grid)
print(f"  Objects: {objects}")
if 2 in objects:
    for obj in objects[2]:
        h, w = get_plus_extent(obj)
        print(f"  Red Plus Extent: h={h}, w={w}")
print(f" input grid size: {input_grid.shape}")
print(f" output grid size: {output_grid.shape}")
result = transform(input_grid)
print(f"  Correct Result: {np.array_equal(result, output_grid)}")
