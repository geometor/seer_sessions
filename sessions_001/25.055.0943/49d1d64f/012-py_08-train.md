
## example 1
*input:*
```
1 2
3 8
```
*expected output:*
```
0 1 2 0
1 1 2 2
3 3 8 8
0 3 8 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 4 is out of bounds for axis 0 with size 4

## example 2
*input:*
```
1 8 4
8 3 8
```
*expected output:*
```
0 1 8 4 0
1 1 8 4 4
8 8 3 8 8
0 8 3 8 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 4 is out of bounds for axis 0 with size 4

## example 3
*input:*
```
2 1 4
8 0 2
3 2 8
```
*expected output:*
```
0 2 1 4 0
2 2 1 4 4
8 8 0 2 2
3 3 2 8 8
0 3 2 8 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 5 is out of bounds for axis 0 with size 5
