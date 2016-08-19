import main
import doctest

fail, test = doctest.testmod(main)

print("%d outta %d ain't bad" % (test-fail, test))

exit(fail)
