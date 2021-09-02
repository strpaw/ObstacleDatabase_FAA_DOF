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
