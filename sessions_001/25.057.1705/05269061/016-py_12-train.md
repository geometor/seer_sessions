
## example 1
*input:*
```
2 8 3 0 0 0 0
8 3 0 0 0 0 0
3 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
*expected output:*
```
2 8 3 2 8 3 2
8 3 2 8 3 2 8
3 2 8 3 2 8 3
2 8 3 2 8 3 2
8 3 2 8 3 2 8
3 2 8 3 2 8 3
2 8 3 2 8 3 2
```
*transformed output:*
```
2 8 3 8 3 3 2
8 3 8 3 3 2 8
3 8 3 3 2 8 3
8 3 3 2 8 3 8
3 3 2 8 3 8 3
3 2 8 3 8 3 3
2 8 3 8 3 3 2
```
size: True
palette: True
color count: False
pixels off: 16
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 1
0 0 0 0 0 1 2
0 0 0 0 1 2 4
0 0 0 1 2 4 0
0 0 1 2 4 0 0
```
*expected output:*
```
2 4 1 2 4 1 2
4 1 2 4 1 2 4
1 2 4 1 2 4 1
2 4 1 2 4 1 2
4 1 2 4 1 2 4
1 2 4 1 2 4 1
2 4 1 2 4 1 2
```
*transformed output:*
```
1 1 2 1 2 4 1 2 4 1 2 4
1 1 2 1 2 4 1 2 4 1 2 4
1 1 2 1 2 4 1 2 4 1 2 4
1 1 2 1 2 4 1 2 4 1 2 4
1 1 2 1 2 4 1 2 4 1 2 4
1 1 2 1 2 4 1 2 4 1 2 4
1 1 2 1 2 4 1 2 4 1 2 4
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 0 0 8 3 0
0 0 0 8 3 0 0
0 0 8 3 0 0 0
0 8 3 0 0 0 4
8 3 0 0 0 4 0
3 0 0 0 4 0 0
0 0 0 4 0 0 0
```
*expected output:*
```
4 8 3 4 8 3 4
8 3 4 8 3 4 8
3 4 8 3 4 8 3
4 8 3 4 8 3 4
8 3 4 8 3 4 8
3 4 8 3 4 8 3
4 8 3 4 8 3 4
```
*transformed output:*
```
8 3 8 3 8 3 8
3 8 3 8 3 8 3
8 3 8 3 8 3 4
3 8 3 8 3 4 8
8 3 8 3 4 8 3
3 8 3 4 8 3 4
8 3 4 8 3 4 3
```
size: True
palette: True
color count: False
pixels off: 38
**FAILED!**
