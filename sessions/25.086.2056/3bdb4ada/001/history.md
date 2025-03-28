
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 7 0 7 0 7 0 7 0 7 0 7 0 0
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
```

*   **Perception:** The input grids contain one or more solid rectangular blocks of a single non-white color, set against a white background. In the provided examples, there are always two such blocks. The key transformation observed is that for certain blocks, their middle horizontal row is modified into an alternating pattern.
*   **Analysis:** By comparing the input and output grids, I notice that only blocks that are exactly 3 rows high are affected. The top and bottom rows of these 3-row-high blocks remain unchanged. The middle row of these blocks is altered: starting from the leftmost pixel of the block in that row, the pixels alternate between the original block color and white (color 0). Pixels outside these specific blocks (the background and any blocks not 3 rows high) are unchanged.


```yaml
facts:
  - task_type: object_modification
  - input_features:
      - background_color: white (0)
      - objects:
          - type: solid rectangular blocks
          - properties:
              - single non-white color
              - height varies
              - width varies
  - output_features:
      - background_color: unchanged (white)
      - modified_objects:
          - condition: blocks with height == 3 rows
          - modification:
              - target: middle row (row index 1 within the 3-row block)
              - pattern: alternate between original block color and white (0)
              - start: original block color at the leftmost column of the block
          - unchanged_parts: top and bottom rows of the 3-row block
      - unmodified_objects: blocks with height != 3 rows remain unchanged
```



```plaintext
natural_language_program:
1.  Identify all distinct, contiguous, solid rectangular blocks of non-white color in the input grid.
2.  For each identified block, check if its height is exactly 3 rows.
3.  If a block's height is 3 rows:
    a.  Locate the middle row of this block.
    b.  Keep track of the block's original color.
    c.  Iterate through the columns occupied by the block in this middle row.
    d.  Starting with the first column of the block in this row, set the pixel color to the block's original color.
    e.  For the next column, set the pixel color to white (0).
    f.  Continue alternating between the original color and white for all columns within the block's width in that middle row.
4.  If a block's height is not 3 rows, leave it unchanged.
5.  Leave all background (white) pixels unchanged.
6.  The resulting grid is the output.
```
