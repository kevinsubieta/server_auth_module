from unittest import TestCase

from application.validator import validate_password, MIN_PASSWORD_MSG, VALID, MAX_PASSWORD_MSG


class TestValidatePassword(TestCase):
    def test_if_password_len_lower_than_min_len_given_return_min_password_msg(self):
        min_len = 8
        self.assertEqual(validate_password('abc', min_len, 9), MIN_PASSWORD_MSG % min_len)

    def test_if_password_len_is_between_min_max_len_return_valid_msg(self):
        self.assertEqual(validate_password('bc12345678', 8, 10), VALID)

    def test_if_password_len_greater_than_max_len_return_max_password_msg(self):
        max_len = 8
        self.assertEqual(validate_password('abc1234567890', 8, max_len), MAX_PASSWORD_MSG % max_len)
