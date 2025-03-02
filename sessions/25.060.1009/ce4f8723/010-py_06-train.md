
## example 1
*input:*
```
1 1 0 0
0 1 0 1
0 1 0 0
1 0 1 0
4 4 4 4
2 2 2 2
0 0 2 2
2 2 0 0
0 0 2 2
```
*expected output:*
```
3 3 3 3
0 3 3 3
3 3 0 0
3 0 3 3
```
*transformed output:*
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**

## example 2
*input:*
```
1 1 1 0
0 1 0 1
0 0 1 1
1 1 0 1
4 4 4 4
0 0 0 2
0 0 0 2
2 2 2 2
2 2 0 2
```
*expected output:*
```
3 3 3 3
0 3 0 3
3 3 3 3
3 3 0 3
```
*transformed output:*
```
0 0 0 0
0 0 0 3
0 0 0 3
0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 11
**FAILED!**

## example 3
*input:*
```
1 1 0 0
1 0 1 0
1 1 0 1
1 1 1 1
4 4 4 4
2 2 0 2
0 0 2 0
0 2 0 0
2 0 2 0
```
*expected output:*
```
3 3 0 3
3 0 3 0
3 3 0 3
3 3 3 3
```
*transformed output:*
```
0 0 0 0
0 0 0 0
3 0 0 3
0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 10
**FAILED!**

## example 4
*input:*
```
1 0 1 0
1 1 0 1
1 0 1 1
0 1 0 1
4 4 4 4
2 2 0 0
0 0 2 0
2 2 0 0
0 0 2 0
```
*expected output:*
```
3 3 3 0
3 3 3 3
3 3 3 3
0 3 3 3
```
*transformed output:*
```
0 0 0 0
0 0 0 3
0 0 0 3
0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**
