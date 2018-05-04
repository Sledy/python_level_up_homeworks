def decorator(f):
    def inner():
        result = f()
        print("Za funkcją :(")
    return inner


@decorator
def funkcja():
    print('Pierwszy!')


funkcja()


def jakas_funkcja():
    print('opopo')

cos = jakas_funkcja()