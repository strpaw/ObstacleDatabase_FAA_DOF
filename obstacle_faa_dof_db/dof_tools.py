import json
import csv


class DOFTools:

    def __init__(self, path_dof_format):
        self.path_dof_format = path_dof_format
        self.dof_format = {}
        self.set_dof_format()

    @staticmethod
    def coordinate_to_dd(src_coord):
        """ Converts DMS format of longitude, latitude from DOF data into DD format.
        param: src_coord: string, latitude or longitude in degrees, minutes, seconds format
        return: dd: float, latitude or longitude in decimal degrees format
        """
        h = src_coord[-1]
        coord_parts = src_coord.split(' ')
        d = float(coord_parts[0])
        m = float(coord_parts[1])
        s = float(coord_parts[2][:-1])

        dd = d + m / 60 + s / 3600
        if h in ['W', 'S']:
            dd = - dd
        return dd

    def get_json(self):
        with open(self.path_dof_format, 'r') as format_file:
            return json.load(format_file)

    def set_dof_format(self):
        json_data = self.get_json()
        for field in json_data['fields']:
            field_name = field["field_name"]
            column_from = field["column_from"]
            column_to = field["column_to"]
            if column_from == column_to:
                self.dof_format[field_name] = [column_from - 1]
            else:
                self.dof_format[field_name] = [column_from - 1, column_to]

    @staticmethod
    def parse_dof_line(parser_format, line):
        obstacle_data = {}
        for field_name, columns in parser_format.items():
            if len(columns) == 1:
                obstacle_data[field_name] = line[columns[0]]
            elif len(columns) == 2:
                obstacle_data[field_name] = line[columns[0]:columns[1]].strip()
        obstacle_data["lon_dd"] = DOFTools.coordinate_to_dd(obstacle_data["longitude"])
        obstacle_data["lat_dd"] = DOFTools.coordinate_to_dd(obstacle_data["latitude"])
        return obstacle_data

    def convert_dof_to_csv(self, dof_path, output_path):
        csv_fields = list(self.dof_format.keys())
        csv_fields.extend(["lon_dd", "lat_dd"])

        with open(dof_path, 'r') as input_dof:
            line_nr = 0
            with open(output_path, 'w', newline='') as out_csv:
                writer = csv.DictWriter(out_csv, fieldnames=csv_fields, delimiter=';')
                writer.writeheader()
                for line in input_dof:
                    line_nr += 1
                    if line_nr >= 5:
                        obstacle_data = DOFTools.parse_dof_line(self.dof_format, line)
                        writer.writerow(obstacle_data)
