import unittest
from test.unit.test_system import Test

test_group = unittest.TestLoader().loadTestsFromTestCase(Test)

test_suite = unittest.TestSuite([test_group])

unittest.TextTestRunner(verbosity=2).run(test_suite)

# run "pytest -sv --html report.html" for report