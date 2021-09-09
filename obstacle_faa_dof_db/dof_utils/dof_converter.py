""" Convert original Digital Obstacle File (dat format) into CSV, KML, SHP formats. """
from obstacle_faa_dof_db.dof_utils.dof_parser import DOFParser
from obstacle_faa_dof_db.dof_utils.dof_coordinates import longitude_to_dms, latitude_to_dms
import csv
from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsFields,
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsFeature,
    QgsPointXY,
    QgsGeometry
)


class DOFConverter:

    def __init__(self, path_dof_format):
        self.parser = DOFParser(path_dof_format)

    @staticmethod
    def get_coordinates_dd(obstacle_data):
        """ Append coordinates in DD to parsed obstacle data.
        :param obstacle_data: dict
        :return: dict
        """
        try:
            lon_dd = longitude_to_dms(obstacle_data["longitude"])
            lat_dd = latitude_to_dms(obstacle_data["latitude"])
        except Exception as e:
            pass  # TODO: Add logging to DOF import log
        else:
            coordinates = {"lon_dd": lon_dd, "lat_dd": lat_dd}
            return coordinates

    def convert_dof_to_csv(self, dof_path, output_path):
        """ Convert DOF (dat file) into CSV file.
        Notice that data is not validated during conversion it is saved to CSV file as it is in source in dat file.
        param: dof_path: str
        param: output_path: str
        """
        csv_fields = list(self.parser._dof_format.keys())
        csv_fields.extend(["lon_dd", "lat_dd"])

        with open(dof_path, 'r') as input_dof:
            line_nr = 0
            with open(output_path, 'w', newline='') as out_csv:
                writer = csv.DictWriter(out_csv, fieldnames=csv_fields, delimiter=';')
                writer.writeheader()
                for line in input_dof:
                    line_nr += 1
                    if line_nr >= 5:  # Skip DOF header
                        obstacle_data = self.parser.parse_dof_line(line)
                        coordinates_dd = DOFConverter.get_coordinates_dd(obstacle_data)
                        if coordinates_dd:
                            obstacle_data.update(coordinates_dd)
                            writer.writerow(obstacle_data)

    @staticmethod
    def get_fields():
        fields = QgsFields()
        fields.append(QgsField("oas_code", QVariant.String))
        fields.append(QgsField("obstacle_number", QVariant.String))
        fields.append(QgsField("verification_status", QVariant.String))
        fields.append(QgsField("country_identifier", QVariant.String))
        fields.append(QgsField("state_identifier", QVariant.String))
        fields.append(QgsField("city_name", QVariant.String))
        fields.append(QgsField("latitude", QVariant.String))
        fields.append(QgsField("longitude", QVariant.String))
        fields.append(QgsField("obstacle_type", QVariant.String))
        fields.append(QgsField("quantity", QVariant.String))
        fields.append(QgsField("agl_ht", QVariant.String))
        fields.append(QgsField("amsl_ht", QVariant.String))
        fields.append(QgsField("lighting", QVariant.String))
        fields.append(QgsField("horizontal_accuracy", QVariant.String))
        fields.append(QgsField("vertical_accuracy", QVariant.String))
        fields.append(QgsField("mark_indicator", QVariant.String))
        fields.append(QgsField("FAA_study_number", QVariant.String))
        fields.append(QgsField("action", QVariant.String))
        fields.append(QgsField("julian_date", QVariant.String))
        return fields

    @staticmethod
    def get_writer(fields, output_path, extension):
        """
        :param fields: QgsFields
        :param output_path: str
        :param extension: str, shp, kml
        :return writer :QgsVectorFileWriter
        """
        crs = QgsCoordinateReferenceSystem()
        crs.createFromId(4326)
        if extension == "shp":
            writer = QgsVectorFileWriter(output_path, "CP1250", fields, QgsWkbTypes.Point, crs,
                                         "ESRI Shapefile")
        elif extension == "kml":
            writer = QgsVectorFileWriter(output_path, "CP1250", fields, QgsWkbTypes.Point, crs,
                                         "KML")
        return writer

    def convert_dof_to_geographic_formats(self, dof_path, output_path, extension):
        """
        :param dof_path: str
        :param output_path: str
        :param extension: str, shp, kml
        """
        fields = DOFTools.get_fields()
        fnames = fields.names()
        writer = DOFTools.get_writer(fields, output_path, extension)

        feat = QgsFeature()
        with open(dof_path, 'r') as input_dof:
            line_nr = 0
            for line in input_dof:
                line_nr += 1
                if line_nr >= 5:
                    obstacle_data = self.parser.parse_dof_line(line)
                    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(obstacle_data["lon_dd"]),
                                                                        float(obstacle_data["lat_dd"]))))
                    feat.setAttributes([obstacle_data[name] for name in fnames])
                    writer.addFeature(feat)
        del writer
