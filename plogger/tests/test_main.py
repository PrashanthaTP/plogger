import logging
import unittest
from plogger.main import get_global_logger, set_verbosity, get_logger

"""
References:

    Testing logging
    - https://pythonin1minute.com/how-to-test-logging-in-python/
    - https://stackoverflow.com/questions/899067/how-should-i-verify-a-log-message-when-testing-python-code-under-nose
    Mocking print
    - https://realpython.com/lessons/mocking-print-unit-tests/
    - https://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python/17981937
"""


logger = get_global_logger()
class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_verbosity(self):
        set_verbosity(logging.DEBUG)
        with self.assertLogs(logger=logger.name, level="DEBUG") as captured:
            logs = ["Inside test_verbosity"]
            for log in logs:
                logger.info(log)
                logger.debug(log)
            self.assertEqual(len(captured.records), len(logs)*2)

    def test_global_logger(self):
        set_verbosity(logging.INFO)
        with self.assertLogs(logger=logger.name, level="INFO") as captured:
            logs = ["Inside test_global_logger"]
            for log in logs:
                logger.info(log)
                logger.debug(log)  # should not log
                logger.warning(log)
            len_captured_records = len(captured.records)
            expected_len_captured_records = len(logs)*2
            self.assertEqual(len_captured_records,
                             expected_len_captured_records)

    def test_get_logger(self):
        mLogger = get_logger(__name__, level=logging.WARNING)
        with self.assertLogs(logger=mLogger.name, level=mLogger.level) as captured:
            logs = ["Inside test_get_logger"]
            for log in logs:
                mLogger.debug(log)
                mLogger.info(log)
                mLogger.warning(log)

            len_captured_records = len(captured.records)
            expected_len_captured_records = len(logs)
            self.assertEqual(len_captured_records,
                             expected_len_captured_records)


if __name__ == "__main__":
    unittest.main()
