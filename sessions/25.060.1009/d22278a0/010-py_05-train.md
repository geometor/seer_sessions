
## example 1
*input:*
```
1 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
1 0 1 0 1 2 0 2 0 2
0 0 1 0 1 2 0 2 0 0
1 1 1 0 1 2 0 2 2 2
0 0 0 0 1 2 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 3 0 3 0 3
3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 3 0 3 0 3
3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 3 0 3 0 3
3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 3 0 3 0 3
3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 3 0 3 0 3
```
size: True
palette: False
color count: False
pixels off: 75
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 3 0 3 0 3 0 3 0 3 0 3
8 0 0 3 0 3 0 3 0 3 0 0
0 0 0 3 0 3 0 3 0 3 3 3
8 8 8 0 0 3 0 3 0 0 0 0
0 0 0 0 0 3 0 3 3 3 3 3
8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3
8 8 8 8 8 0 8 0 0 0 0 0
0 0 0 0 8 0 8 0 0 3 3 3
8 8 8 0 8 0 8 0 8 0 0 0
0 0 8 0 8 0 8 0 8 0 0 3
8 0 8 0 8 0 8 0 8 0 8 0
```
*transformed output:*
```
3 8 3 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 3 8 3
3 8 3 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 3 8 3
3 8 3 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 3 8 3
3 8 3 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 3 8 3
3 8 3 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 3 8 3
3 8 3 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 3 8 3
```
size: True
palette: True
color count: False
pixels off: 111
**FAILED!**

## example 3
*input:*
```
2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 2 0 2 0 2 0 2 0 2
2 2 2 0 2 0 2 0 2 0 2 0 2
0 0 0 0 2 0 2 0 2 0 2 0 2
2 2 2 2 2 0 2 0 2 0 2 0 2
0 0 0 0 0 0 2 0 2 0 2 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 4 0 4
4 4 4 4 4 0 4 0 4 0 4 0 4
0 0 0 0 4 0 4 0 4 0 4 0 4
4 4 4 0 4 0 4 0 4 0 4 0 4
0 0 4 0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0 4 0 4
```
*transformed output:*
```
3 0 3 0 3 0 3 0 3 0 3 0 3
0 3 0 3 0 3 0 3 0 3 0 3 0
3 0 3 0 3 0 3 0 3 0 3 0 3
0 3 0 3 0 3 0 3 0 3 0 3 0
3 0 3 0 3 0 3 0 3 0 3 0 3
0 3 0 3 0 3 0 3 0 3 0 3 0
3 0 3 0 3 0 3 0 3 0 3 0 3
0 3 0 3 0 3 0 3 0 3 0 3 0
3 0 3 0 3 0 3 0 3 0 3 0 3
0 3 0 3 0 3 0 3 0 3 0 3 0
3 0 3 0 3 0 3 0 3 0 3 0 3
0 3 0 3 0 3 0 3 0 3 0 3 0
3 0 3 0 3 0 3 0 3 0 3 0 3
```
size: True
palette: False
color count: False
pixels off: 121
**FAILED!**

## example 4
*input:*
```
1 0 0 0 0 0 2
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 0 0 0
```
*expected output:*
```
1 0 1 0 2 0 2
0 0 1 0 2 0 0
1 1 1 0 2 2 2
0 0 0 0 0 0 0
8 8 8 0 0 2 2
0 0 8 0 8 0 0
8 0 8 0 8 0 0
```
*transformed output:*
```
3 0 3 0 3 0 3
0 3 0 3 0 3 0
3 0 3 0 3 0 3
0 3 0 3 0 3 0
3 0 3 0 3 0 3
0 3 0 3 0 3 0
3 0 3 0 3 0 3
```
size: True
palette: False
color count: False
pixels off: 33
**FAILED!**
