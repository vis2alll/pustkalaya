def go():
    b()
def a():
    if 1:
        go()
    def b():
        print "bye"
    print "hello"
    