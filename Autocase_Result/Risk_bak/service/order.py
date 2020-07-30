def f(ord):
    class order:
        orderinfos = []
        def __init__(self, ord):
            order.orderinfos.append(ord)
    if not hasattr(f, 'info'):
        f.info = []
    if not hasattr(f, 'getorder'):
        f.getorder = order

    f.getorder(ord)
    f.info.append(ord)
