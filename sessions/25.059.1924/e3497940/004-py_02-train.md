
## example 1
*input:*
```
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 4 5 0 0 0 0
0 0 0 4 5 4 4 0 0
0 0 3 3 5 0 0 0 0
0 0 0 3 5 0 0 0 0
0 0 0 3 5 3 3 3 0
0 0 0 3 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
```
*expected output:*
```
0 0 0 0
0 0 0 0
0 0 0 4
0 0 4 4
0 0 3 3
0 0 0 3
0 3 3 3
0 0 0 3
0 0 0 0
0 0 0 0
```
*transformed output:*
```
0 0
0 0
4 0
4 4
3 0
3 0
3 3
3 0
0 0
0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 0 5 0 0 0 0
0 0 0 2 5 0 0 0 0
0 0 0 2 5 2 6 0 0
0 0 0 2 5 0 0 0 0
0 0 0 2 5 2 2 2 0
0 0 6 6 5 6 0 0 0
0 0 0 2 5 0 0 0 0
0 2 2 0 5 2 0 0 0
0 0 0 2 5 0 0 0 0
0 0 0 0 5 0 0 0 0
```
*expected output:*
```
0 0 0 0
0 0 0 2
0 0 6 2
0 0 0 2
0 2 2 2
0 0 6 6
0 0 0 2
0 2 2 2
0 0 0 2
0 0 0 0
```
*transformed output:*
```
0 0
2 0
2 2
2 0
2 2
6 6
2 0
0 2
2 0
0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 0 0 5 0 0 0 0
0 0 0 0 5 7 0 0 0
0 0 0 8 5 0 0 0 0
0 0 0 8 5 0 0 0 0
0 7 8 8 5 0 0 0 0
0 0 0 0 5 8 8 0 0
0 0 0 8 5 0 0 0 0
0 0 0 8 5 0 0 0 0
0 0 0 0 5 8 7 0 0
0 0 0 0 5 0 0 0 0
```
*expected output:*
```
0 0 0 0
0 0 0 7
0 0 0 8
0 0 0 8
0 7 8 8
0 0 8 8
0 0 0 8
0 0 0 8
0 0 7 8
0 0 0 0
```
*transformed output:*
```
0 0
0 7
8 0
8 0
8 0
0 8
8 0
8 0
0 8
0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
