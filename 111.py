f = open("file1","r")
s = f.read()
f.close()

def find_longest(arr, wanted):
    """ Return length and position longest in succession wanted element in arr list """
    tmp_size = 0
    max_size = 0
    tail_pos = -1
    len_arr = len(arr)
    expect_cmp = False

    for indx in range(len_arr):
        if (arr[indx] == wanted):
            if (indx == len_arr - 1):
                expect_cmp = True
                indx += 1
            tmp_size += 1
        else:
            if (indx == 0 and expect_cmp is False):
                continue
            if (arr[indx - 1] == wanted):
                expect_cmp = True
        if (expect_cmp and tmp_size > max_size):
            expect_cmp = False
            max_size = tmp_size
            tail_pos = indx
            tmp_size = 0

    len_pos = []
    len_pos.append(max_size)
    len_pos.append(tail_pos - max_size)

    return len_pos

if __name__=='__main__':
    p1 =(s.replace("\n", " ** ").split(" " ))
    p2=[]
    for i in p1:
        p2.append(int(i))

    print(p2)
    print(find_longest(p2,1))
