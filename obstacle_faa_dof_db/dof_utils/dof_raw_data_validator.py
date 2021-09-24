""" Raw data from Digital Obstacle File validator/converter. """
from obstacle_faa_dof_db.dof_utils.dof_conversion_errors import *
from obstacle_faa_dof_db.dof_utils.dof_coordinates import longitude_to_dms, latitude_to_dms


_vert_acc_codes = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I"
]

_hor_acc_codes = [
    1, 2, 3, 4, 5, 6, 7, 8, 9
]

_lighting_codes = [
    "R", "D", "H", "M", "S", "F", "C", "W", "L", "N", "U"
]

_marking_codes = [
    "P", "W", "M", "F", "S", "N", "U"
]

_verif_status = [
    "O", "U", "N"
]


class DOFRawDataValidator:

    def __init__(self):
        self._err_msg = ""
        self._obst_convert_functions = {
            "agl": DOFRawDataValidator.float_value_optional,
            "amsl": DOFRawDataValidator.positive_integer_required,
            "vert_acc_code": DOFRawDataValidator.vert_acc_code_validation,
            "hor_acc_code": DOFRawDataValidator.hor_acc_code_validation,
            "lighting_code": DOFRawDataValidator.lighting_code_validation,
            "marking_code": DOFRawDataValidator.marking_code_validation,
            "verif_status_code": DOFRawDataValidator.verif_status_validation
        }

        self.attributes_to_check = self._obst_convert_functions.keys()

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
            i = float(value)
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

    @staticmethod
    def vert_acc_code_validation(value):
        if value in _vert_acc_codes:
            return value
        else:
            raise UnknownVertAccCode(value)

    @staticmethod
    def hor_acc_code_validation(value):
        if int(value) in _hor_acc_codes:
            return int(value)
        else:
            raise UnknownHorAccCode(value)

    @staticmethod
    def verif_status_validation(value):
        if value in _verif_status:
            return value
        else:
            raise UnknownVerifStatus(value)

    def validate_raw_data(self, raw_data):
        self._err_msg = ""
        parsed_data = {}

        for attribute, value in raw_data.items():
            if attribute in self.attributes_to_check:
                try:
                    parsed_data[attribute] = self._obst_convert_functions[attribute](value)
                except Exception as e:
                    parsed_data[attribute] = None
                    if self._err_msg:
                        self._err_msg += "| Attribute {} value error. {} ".format(attribute, e)
                    else:
                        self._err_msg += "Attribute {} value error. {} ".format(attribute, e)

        try:
            parsed_data["lon_dd"] = longitude_to_dms(raw_data["lon_src"])
        except Exception as e:
            self._err_msg += "| Attribute lon_src value error. {} ".format(e)

        try:
            parsed_data["lat_dd"] = latitude_to_dms(raw_data["lat_src"])
        except Exception as e:
            self._err_msg += "| Attribute lat_src value error. {} ".format(e)

        parsed_data["obst_ident"] = raw_data["oas_code"] + '-' + raw_data["obstacle_number"]
        parsed_data["obst_type_id"] = 1
        parsed_data["state_id"] = int(raw_data["oas_code"])
        parsed_data["city_name"] = raw_data["city_name"]
        parsed_data["lon_src"] = raw_data["lon_src"]
        parsed_data["lat_src"] = raw_data["lat_src"]

        return parsed_data
