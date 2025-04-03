
## train_1

**input:**
```
0 0 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 0 0 0 0 8 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 8 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 8 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 3 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 3 0 0 3 0 0 0 3 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The input grid consists of a background color (`white` - 0) and foreground elements primarily of one color (`azure` - 8 in the first two examples, `green` - 3 in the third). In the input, there is one large, contiguous rectangular object composed of the foreground color, along with several isolated pixels of the same foreground color scattered around it.

The output grid retains the background color and the large rectangular object from the input. However, all the isolated foreground pixels present in the input have been removed (replaced with the background color).

The transformation appears to isolate the single largest contiguous object of the non-background color present in the input and removes all other pixels of that same color.

**Facts:**


```yaml
Task: Keep the largest contiguous object of the dominant non-background color.
Elements:
  - Background:
      Color: white (0)
      Role: Fills the grid initially and replaces removed pixels.
  - Foreground Pixels:
      Color: Varies per example (azure - 8 or green - 3)
      Role: Form objects within the grid.
  - Objects:
      Definition: Contiguous areas of the same non-background color.
      Input State: Multiple objects exist - one significantly larger than others, and several small (often single-pixel) objects.
      Output State: Only the single largest object from the input remains.
Properties:
  - Connectivity: Used to define objects (pixels are connected if adjacent horizontally or vertically).
  - Size: Measured by the number of pixels in a contiguous object. Crucial for identifying the object to keep.
Actions:
  - Identify: Locate all distinct contiguous objects of the non-background color.
  - Compare: Determine the size (pixel count) of each identified object.
  - Select: Choose the object with the largest size.
  - Filter/Remove: Eliminate all foreground pixels that are not part of the selected largest object.
  - Replace: Change the color of the removed pixels to the background color (white - 0).
Relationships:
  - Largest Object vs Others: The core distinction is based on size. The transformation preserves the largest object while discarding others of the same color.
```


**Natural Language Program:**

1.  Identify the background color (which is consistently `white`, 0).
2.  Identify all pixels that are not the background color. Note the color of these foreground pixels.
3.  Find all distinct contiguous groups (objects) formed by these foreground pixels. Use 4-connectivity (up, down, left, right neighbours).
4.  Calculate the size (number of pixels) for each distinct foreground object.
5.  Identify the object with the largest size. If there's a tie for the largest size, the examples suggest only one large object exists, so assume there is a unique largest object.
6.  Create a new output grid of the same dimensions as the input grid, filled entirely with the background color (`white`, 0).
7.  Iterate through the pixels of the identified largest object from step 5. For each pixel in this largest object, set the corresponding pixel in the output grid to the foreground color identified in step 2.
8.  Return the modified output grid.
