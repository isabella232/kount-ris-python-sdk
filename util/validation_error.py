#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Kount python sdk project (https://bitbucket.org/panatonkount/sdkpython)
# Copyright (C) 2017 Kount Inc. All Rights Reserved.

__author__ = "Yordanka Spahieva"
__version__ = "1.0.0"
__maintainer__ = "Yordanka Spahieva"
__email__ = "yordanka.spahieva@sirma.bg"
__status__ = "Development"

import unittest

class VALIDATIONERROR:
    """Refund charge back status.
    R - The transaction was a refund.
    C - The transaction was a chargeback.
    """
    REGEX_ERR = 'REGEX'
    LENGTH_ERR = 'LENGTH'
    REQUIRED_ERR = 'REQUIRED'


class ValidationErrorType(Exception, VALIDATIONERROR):
    """ValidationErrorType exception
        Args: value - Value of the error type - REGEX, LENGTH, REQUIRED.
    """
    def __init__(self, message=""):
        if isinstance(message, str) or not message:
            if message not in [VALIDATIONERROR.LENGTH_ERR, VALIDATIONERROR.REGEX_ERR, VALIDATIONERROR.REQUIRED_ERR]:
                message = "Expected value of the error type %s, %s, %s, found [%s]"%(
                    VALIDATIONERROR.LENGTH_ERR, VALIDATIONERROR.REGEX_ERR, VALIDATIONERROR.REQUIRED_ERR, message)
        super(ValidationErrorType, self).__init__(message)


class ValidationError(ValidationErrorType):
    """Get the string representation of the error.
        Keyword arguments:
            field -- the name of the bad field
            mode -- the RIS mode the field is associated with
            value -- field value
            pattern -- the regular expression violated
            length -- the maximum allowable length
        raise  ValidationError
    """
    def __init__(self, field="", mode="", value="", pattern="", length=0):
        validation_error = False
        if int(length) < len(field):
            self.message = "Field [%s] has length [%s] which is longer than the maximum of [%s]"%(
                            field, len(field), length)
            self.error = VALIDATIONERROR.LENGTH_ERR
            validation_error = True
        if pattern:
            self.message = "Field [%s] has value [%s] which which does not match the pattern [%s]"%(
                            field, value, pattern)
            self.error = VALIDATIONERROR.REGEX_ERR
            validation_error = True
        if mode:
            self.message = "Required field [%s] missing for mode [%s]"%(field, mode.upper())
            self.error = VALIDATIONERROR.REQUIRED_ERR
            validation_error = True
        if validation_error:
            super(ValidationError, self).__init__((self.error, self.message))


class TestValidationError(unittest.TestCase):
    def test_max_length(self):
        incorrect = "a"*10
        lengthr = 2
        c = ValidationError(field=incorrect, length=lengthr)
        with self.assertRaises(ValidationError):
            raise c
        self.assertEqual(str(c),
            "('LENGTH', 'Field [%s] has length [%s] which is longer than the maximum of [%s]')"%(
            incorrect, len(incorrect), lengthr))

    def test_mode(self):
        incorrect = "a"*10
        mode = "q"
        c = ValidationError(field=incorrect, mode=mode)
        with self.assertRaises(ValidationError):
            raise c
        self.assertEqual(str(c),
            "('REQUIRED', 'Required field [%s] missing for mode [%s]')"%(
            incorrect, mode.upper()))

    def test_correct_type(self):
        for correct in ["REGEX_ERR", "REQUIRED_ERR", "LENGTH_ERR"]:
            c = ValidationErrorType(correct)
            with self.assertRaises(ValidationErrorType):
                raise c
            self.assertEqual("Expected value of the error type LENGTH, REGEX, REQUIRED, found [%s]"%correct, str(c))

    def test_incorrect_type(self):
        incorrect = "42"
        c = ValidationErrorType(message=incorrect)
        with self.assertRaises(ValidationErrorType):
            raise c
        self.assertEqual(str(c),
            "Expected value of the error type LENGTH, REGEX, REQUIRED, found [%s]"%incorrect)

    def test_empty_field(self):
        incorrect = ""
        c = ValidationErrorType(message=incorrect)
        with self.assertRaises(ValidationErrorType):
            raise c
        self.assertEqual(str(c),
            "Expected value of the error type LENGTH, REGEX, REQUIRED, found [%s]"%incorrect)

    def test_no_field(self):
        incorrect = None
        c = ValidationErrorType(message=incorrect)
        with self.assertRaises(ValidationErrorType):
            raise c
        self.assertEqual(str(c),
            "Expected value of the error type LENGTH, REGEX, REQUIRED, found [%s]"%incorrect)

    def test_none_field(self):
        c = ValidationErrorType()
        with self.assertRaises(ValidationErrorType):
            raise c
        self.assertEqual(str(c),
            "Expected value of the error type LENGTH, REGEX, REQUIRED, found []")

    def test_pattern(self):
        field = 'RFCB'
        value = "42"
        pattern = '^[RC]?$'
        c = ValidationError(field=field, value=value, pattern=pattern)
        with self.assertRaises(ValidationError):
            raise c
        self.assertEqual(str(c),
            "('REGEX', 'Field [%s] has value [%s] which which does not match the pattern [%s]')"%
            (field, value, pattern))


if __name__ == "__main__":
    unittest.main()