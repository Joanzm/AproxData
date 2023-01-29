import numpy as np

def my_func(a):
    factor = (a[3] - a[1]) / (a[2] - a[0])
    offset = a[1] - factor * a[0]
    return np.array([factor, offset], dtype=np.float32)

class A():

    def __init__(self, key: str) -> None:
        super().__init__()
        self._key = key
    
    @property
    def key(self) -> str:
        return self._key
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return self._key == __o
        else:
            return self._key == __o.key

if __name__ == "__main__":

    l = [A("t"), A("b"), A("c")]

    print("x" in l)

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
    print(gCalc)

    select = np.array([[0, 33, 66, 100],[1,34,67,101]], np.int64)
    print(select)
    print(select[:, [2,3]])
    print(np.unique(select[:, [2,3]]))
    eleCounts = select[1:select.shape[0]] - select[0:select.shape[0] - 1]
    #print(eleCounts)
    a = np.array([[0, 1, 7, 3, 4],[5, 6, 2, 8, 9]], np.float32)
    print(np.max(a[:, -1], axis=0))

    x = np.array([[[2.8168, 2.7963, 2.7666, 2.823], [0.00, 0.00, 0.00, 0.00]],
                [[3.0028, 2.9916, 2.9644, 3.0078], [0.01, 0.01, 0.009, 0.01]],
                [[3.1163, 3.1088, 3.0915, 3.1194], [0.02, 0.02, 0.019, 0.02]]])

    a = 2.9
    calcValues = np.array([[2.8, 0], [2.8, 0], [3.0, 0.01], [3.1, 0.02]])
    print(calcValues[:,0] < 2.9)

    b = np.array([1,1,0])
    print(len(x.shape))
    print(len(b.shape))
    print((x[:,0]) * b[:,None])

    y = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]).reshape(5,4)
    print(y)

    z = np.array([1, 1, 1, 1, 1])
    print(y - np.vstack(z))
    print(y - np.vstack(z))
    
    p = np.poly1d(np.polyfit(np.array([0, 1, 2]), np.array([2.3, 4.3, 2.1]), 5))
    print(p(y))"""
    


