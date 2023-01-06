import numpy as np

def my_func(a):
    factor = (a[3] - a[1]) / (a[2] - a[0])
    offset = a[1] - factor * a[0]
    return np.array([factor, offset], dtype=np.float32)

if __name__ == "__main__":
    """ a = np.arange(202, dtype=np.float32).reshape(101, 2)
    print(a)
    b = np.round(np.linspace(0, 100, 7, dtype=np.int64), 0)
    print(b)
    print(np.take(a, b, axis=0))

    x = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
    print(x)
    print(x.mean(axis=2))

    g = np.arange(2 * 10 * 3).reshape((10, 2, 3))
    print(g)
    print(g.mean(axis=2))
    gMean = np.mean(g, axis=2)
    gRepeat = np.repeat(gMean, 2, axis=0)
    gRed = gRepeat[1:gRepeat.shape[0] - 1]
    gResize = gRed.reshape((int(gRed.shape[0] / 2), 4))
    gCalc = np.apply_along_axis(my_func, 1, gResize)
    print(gCalc) """
    select = np.array([[0, 33, 66, 100],[1,34,67,101]], np.int64)
    print(select)
    print(select[:, [2,3]])
    print(np.unique(select[:, [2,3]]))
    eleCounts = select[1:select.shape[0]] - select[0:select.shape[0] - 1]
    #print(eleCounts)
    a = np.array([[0, 1, 7, 3, 4],[5, 6, 2, 8, 9]], np.float32)
    print(np.max(a[:, -1], axis=0))
