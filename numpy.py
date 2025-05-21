class ndarray(list):
    def __init__(self, data):
        if isinstance(data, int):
            data = [0.0] * data
        else:
            data = list(data)
        super().__init__(data)
        self._shape = (len(data),)

    @property
    def shape(self):
        return self._shape


def array(obj):
    return ndarray(obj)


def zeros_like(arr):
    if isinstance(arr, ndarray):
        return ndarray(len(arr))
    else:
        return ndarray([0.0 for _ in range(len(arr))])
