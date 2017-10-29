from atomicplus import AtomicCounter


a = AtomicCounter(0)


def base_test():
    base = AtomicCounter(0)
    assert base.value == 0
    base += 1
    base -= 1
    print base.value
    assert base.value == 0


def counter():
    global a
    print a.value
    a += 1


def thread_test():
    import threading
    tid_list = []

    for i in range(0, 500):
        t = threading.Thread(target=counter)
        t.daemon = True
        tid_list.append(t)

    for t in tid_list:
        t.start()

    for t in tid_list:
        t.join()

    assert a.value == 500
    a.cas(499, 499)
    assert a.value == 500
    a.cas(500, 501)
    assert a.value == 501
    assert a.check(500) is False
    assert a.check(501) is True


base_test()
thread_test()
