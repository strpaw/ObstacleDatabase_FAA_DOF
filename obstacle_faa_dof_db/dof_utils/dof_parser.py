""" Digital Obstacle File parser """
import json


class DOFParser:

    def __init__(self, path_dof_format):
        self._path_dof_format = path_dof_format
        self._dof_format = {}
        self._set_dof_format()

    def _get_dof_format(self):
        """ Load Digital Obstacle File format data from json file. """
        with open(self._path_dof_format, 'r') as f:
            return json.load(f)

    def _set_dof_format(self):
        """ Assign Digital Obstacle File format - begin/end columns to obstacle attributes/fields. """
        dof_format = self._get_dof_format()
        for field in dof_format['fields']:
            field_name = field["field_name"]
            column_from = field["column_from"]
            column_to = field["column_to"]
            if column_from == column_to:
                self._dof_format[field_name] = [column_from - 1]
            else:
                self._dof_format[field_name] = [column_from - 1, column_to]

    def parse_dof_line(self, line):
        """ Extract data from Digital Obstacle File line according to given DOF format.
        param: line: str, line of Digital Obstacle File
        return: dict
        """
        obstacle_data = {}
        for field_name, columns in self._dof_format.items():
            if len(columns) == 1:
                obstacle_data[field_name] = line[columns[0]]
            elif len(columns) == 2:
                obstacle_data[field_name] = line[columns[0]:columns[1]].strip()
        return obstacle_data
