import unittest
from ObstacleDatabase_FAA_DOF.obstacle_faa_dof_db.dof_raw_data_validator import *


class DOFRawDataValidatorTest(unittest.TestCase):

    def test_float_value_optional_value_convert_to_float(self):
        self.assertEqual(23, DOFRawDataValidator.float_value_optional("0023"))

    def test_float_value_optional_value_do_nothing_for_empty_value(self):
        self.assertIsNone(DOFRawDataValidator.float_value_optional(""))

    def test_float_value_optional_FloatNumberRequired_raised(self):
        self.assertRaises(FloatNumberRequired, DOFRawDataValidator.float_value_optional, "a023")

    def test_positive_integer_required_convert_to_positive_integer(self):
        self.assertEqual(23, DOFRawDataValidator.positive_integer_required("0023"))

    def test_positive_integer_required_PositiveIntegerNumberRequired_raised_when_not_poistive_integer(self):
        self.assertRaises(PositiveIntegerNumberRequired, DOFRawDataValidator.positive_integer_required, "-23")

    def test_positive_integer_required_PositiveIntegerNumberRequired_raised_when_not_integer(self):
        self.assertRaises(PositiveIntegerNumberRequired, DOFRawDataValidator.positive_integer_required, "a23")

    def test_positive_integer_required_PositiveIntegerNumberRequired_raised_when_empty_value(self):
        self.assertRaises(PositiveIntegerNumberRequired, DOFRawDataValidator.positive_integer_required, "")

    def test_lighting_code_validation_ligthing_code_returned_when_valid(self):
        self.assertEqual("R", DOFRawDataValidator.lighting_code_validation("R"))

    def test_lighting_code_validation_UnknownLightingCode_raised_when_not_valid_code(self):
        self.assertRaises(UnknownLightingCode, DOFRawDataValidator.lighting_code_validation, "Z")

    def test_marking_code_validation_ligthing_code_returned_when_valid(self):
        self.assertEqual("F", DOFRawDataValidator.marking_code_validation("F"))

    def test_marking_code_validation_UnknownLightingCode_raised_when_not_valid_code(self):
        self.assertRaises(UnknownMarkingCode, DOFRawDataValidator.marking_code_validation, "Z")

    def test_validate_raw_data_agl_is_none(self):

        raw_data = {
            "agl": "00093a",
            "amsl": "00657",
            "vert_acc_code": "H",
            "hor_acc_code": 8,
            "loghting_code": "N",
            "marking_code": "S",
            "verif_status_code": "O"
        }

        converted_data = {
            "agl": None,
            "amsl": 657,
            "vert_acc_code": "H",
            "hor_acc_code": 8,
            "loghting_code": "N",
            "marking_code": "S",
            "verif_status_code": "O"
        }

        validator = DOFRawDataValidator()
        self.assertEqual(converted_data, validator.validate_raw_data(raw_data))
        self.assertEqual("Attribute agl value error. Float number required. Actual value: 00093a ",
                         validator._err_msg)

    def test_validate_raw_data_amsl_is_none(self):

        raw_data = {
            "agl": "00093",
            "amsl": "00657a",
            "vert_acc_code": "H",
            "hor_acc_code": 8,
            "loghting_code": "N",
            "marking_code": "S",
            "verif_status_code": "O"
        }

        converted_data = {
            "agl": 93.0,
            "amsl": None,
            "vert_acc_code": "H",
            "hor_acc_code": 8,
            "loghting_code": "N",
            "marking_code": "S",
            "verif_status_code": "O"
        }

        validator = DOFRawDataValidator()
        self.assertEqual(converted_data, validator.validate_raw_data(raw_data))
        self.assertEqual("Attribute amsl value error. Positive integer number required. Actual value: 00657a ",
                         validator._err_msg)

    def test_validate_raw_data_vert_acc_is_none(self):

        raw_data = {
            "agl": "00093",
            "amsl": "00657",
            "vert_acc_code": "P",
            "hor_acc_code": 8,
            "loghting_code": "N",
            "marking_code": "S",
            "verif_status_code": "O"
        }

        converted_data = {
            "agl": 93.0,
            "amsl": 657,
            "vert_acc_code": None,
            "hor_acc_code": 8,
            "loghting_code": "N",
            "marking_code": "S",
            "verif_status_code": "O"
        }

        validator = DOFRawDataValidator()
        self.assertEqual(converted_data, validator.validate_raw_data(raw_data))
        self.assertEqual("Attribute vert_acc_code value error. Unknown vertical accuracy code. Actual value: P ",
                         validator._err_msg)

        def test_validate_raw_data_hor_acc_is_none(self):
            raw_data = {
                "agl": "00093",
                "amsl": "00657",
                "vert_acc_code": "B",
                "hor_acc_code": "A",
                "loghting_code": "N",
                "marking_code": "S",
                "verif_status_code": "O"
            }

            converted_data = {
                "agl": 93.0,
                "amsl": 657,
                "vert_acc_code": "B",
                "hor_acc_code": None,
                "loghting_code": "N",
                "marking_code": "S",
                "verif_status_code": "O"
            }

            validator = DOFRawDataValidator()
            self.assertEqual(converted_data, validator.validate_raw_data(raw_data))
            self.assertEqual("Attribute hor_acc_code value error. Unknown horizontal accuracy code. Actual value: B ",
                             validator._err_msg)