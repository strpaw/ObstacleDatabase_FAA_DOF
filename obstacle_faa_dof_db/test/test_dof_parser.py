import unittest
from ObstacleDatabase_FAA_DOF.obstacle_faa_dof_db.dof_parser import *


class DOFRawDataValidatorTest(unittest.TestCase):

    def test_set_dof_format(self):
        dof_format = {
            "oas_code": [0, 2],
            "obstacle_number": [3, 9],
            "verif_status_code": [10],
            "country_identifier": [12, 14],
            "state_identifier": [15, 17],
            "city_name": [18, 34],
            "latitude": [35, 47],
            "longitude": [48, 61],
            "obstacle_type": [62, 80],
            "quantity": [81],
            "agl": [83, 88],
            "amsl": [89, 94],
            "lighting_code": [95],
            "hor_acc_code": [97],
            "vert_acc_code": [99],
            "marking_code": [101],
            "FAA_study_number": [103, 117],
            "action": [118],
            "julian_date": [120, 127]
        }
        parser = DOFParser(path_dof_format=r"./test_data/dof_format.json")
        self.assertEqual(dof_format, parser._dof_format)

    def test_parse_dof_line(self):
        raw_line = "99-987654 O X1 1X TEST             01 02 18.12N 006 42 20.36W TOWER              1 00065 00657 R 8 I P 2011TEST123456 A 2011350"

        expected_data = {
            "oas_code": "99",
            "obstacle_number": "987654",
            "verif_status_code": "O",
            "country_identifier": "X1",
            "state_identifier": "1X",
            "city_name": "TEST",
            "latitude": "01 02 18.12N",
            "longitude": "006 42 20.36W",
            "obstacle_type": "TOWER",
            "quantity": "1",
            "agl": "00065",
            "amsl": "00657",
            "lighting_code": "R",
            "hor_acc_code": "8",
            "vert_acc_code": "I",
            "marking_code": "P",
            "FAA_study_number": "2011TEST123456",
            "action": "A",
            "julian_date": "2011350"
        }

        parser = DOFParser(path_dof_format=r"./test_data/dof_format.json")
        parsed_data = parser.parse_dof_line(raw_line)

        self.assertEqual(expected_data, parsed_data)
