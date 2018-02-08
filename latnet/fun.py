def set_default(obj):
    '''for saving set objects using json'''
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

