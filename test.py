import main
import doctest

fail, test = doctest.testmod(main)

exit(fail)
