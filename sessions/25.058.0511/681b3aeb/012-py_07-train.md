
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 7 7
```
*expected output:*
```
3 3 7
3 7 7
3 7 7
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: tuple index out of range

## example 2
*input:*
```
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 4
0 0 0 6 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
6 6 6
4 6 6
4 4 6
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: tuple index out of range

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
```
*expected output:*
```
1 1 1
1 3 1
3 3 3
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: tuple index out of range
