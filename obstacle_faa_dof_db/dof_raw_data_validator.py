from ObstacleDatabase_FAA_DOF.obstacle_faa_dof_db.dof_conversion_errors import *


_lighting_codes = [
    "R", "D", "H", "S", "F", "C", "W", "L", "N", "U"
]

_marking_codes = [
    "P", "W", "M", "F", "S", "N", "U"
]


class DOFRawDataValidator:

    def __init__(self):
        self._err_msg = ""
        self._parsed_data = {
            "agl": None,
            "amsl": None,
            "vert_acc_code": None,
            "hor_acc_code": None,
            "quantity": None,
            "loghting_code": None,
            "marking_code": None,
            "verif_status_code": None
        }

        self._obst_convert_functions = {
            "agl": DOFRawDataValidator.float_value_optional,
            "amsl": DOFRawDataValidator.positive_integer_required,
            "vert_acc_code": None,
            "hor_acc_code": None,
            "quantity": None,
            "loghting_code": DOFRawDataValidator.lighting_code_validation,
            "marking_code": DOFRawDataValidator.marking_code_validation,
            "verif_status_code": None
        }

    def _reset_parsed_data(self):
        for key in self._obstacle_parsed:
            self._obstacle_parsed[key] = None

    @staticmethod
    def float_value_optional(value):
        try:
            if value:
                return float(value)
        except (TypeError, ValueError):
            raise FloatNumberRequired(value)


    @staticmethod
    def positive_integer_required(value):
        try:
            i = int(value)
        except (TypeError, ValueError):
            raise PositiveIntegerNumberRequired(value)
        else:
            if i > 0:
                return i
            else:
                raise PositiveIntegerNumberRequired(value)

    @staticmethod
    def lighting_code_validation(value):
        if value in _lighting_codes:
            return value
        else:
            raise UnknownLightingCode(value)

    @staticmethod
    def marking_code_validation(value):
        if value in _marking_codes:
            return value
        else:
            raise UnknownMarkingCode(value)

    def convert_raw_data(self, raw_data):
        self.reste_obstacle_parsed()

        for attribute, value in raw_data.items():
            try:
                self._obstacle_parsed[attribute] = self._obst_convert_functions[attribute](value)
            except Exception as e:
                if self._err_msg:
                    self._err_msg += "| Attribute {} value error. {} ".format(attribute, e)
                else:
                    self._err_msg += "Attribute {} value error. {} ".format(attribute, e)
