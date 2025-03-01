
## example 1
*input:*
```
3 3 3
0 2 2
1 1 0
```
*expected output:*
```
3 3 3 3 3 3
0 2 2 2 2 0
1 1 0 0 1 1
1 1 0 0 1 1
0 2 2 2 2 0
3 3 3 3 3 3
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: could not broadcast input array from shape (1,3) into shape (1,4)

## example 2
*input:*
```
3 3 1
1 3 0
0 2 2
```
*expected output:*
```
3 3 1 1 3 3
1 3 0 0 3 1
0 2 2 2 2 0
0 2 2 2 2 0
1 3 0 0 3 1
3 3 1 1 3 3
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: could not broadcast input array from shape (1,3) into shape (1,4)

## example 3
*input:*
```
2 1 0
0 2 3
0 3 0
```
*expected output:*
```
2 1 0 0 1 2
0 2 3 3 2 0
0 3 0 0 3 0
0 3 0 0 3 0
0 2 3 3 2 0
2 1 0 0 1 2
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: could not broadcast input array from shape (1,3) into shape (1,4)
