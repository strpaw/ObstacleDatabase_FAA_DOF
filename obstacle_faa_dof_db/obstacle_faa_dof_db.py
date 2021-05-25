# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ObstacleFAADigitialObstacleFileDB
                                 A QGIS plugin
 PostGIS Digital Obstacle File (DOF) database
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-05-07
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Paweł Strzelewicz
        email                : @
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QWidget, QMessageBox

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .obstacle_faa_dof_db_dialog import ObstacleFAADigitialObstacleFileDBDialog
import os.path
from qgis.core import *
from qgis.gui import *
from .obstacle_database_tools import ObstacleDatabaseTools
from .dof_tools import *


class ObstacleFAADigitialObstacleFileDB:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.conversion_input_path = None
        self.conversion_output_format = None
        self.conversion_output_path = None

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ObstacleFAADigitialObstacleFileDB_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ObstacleFAADigitialObstacleFileDB')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

        self.data_uri = None  # Data source uri for layers from PostGIS database
        self.obstacle_type_map = {}

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ObstacleFAADigitialObstacleFileDB', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/obstacle_faa_dof_db/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'ObstacleFAADigitialObstacleFileDB'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ObstacleFAADigitialObstacleFileDB'),
                action)
            self.iface.removeToolBarIcon(action)

    def set_data_uri(self):
        self.obstacle_layer = QgsProject.instance().mapLayersByName("obstacle")[0]
        provider = self.obstacle_layer.dataProvider()
        self.data_uri = QgsDataSourceUri(provider.dataSourceUri())

    def set_obstacle_type_map(self):
        query = """SELECT
                        obst_type,
                        obst_type_id
                    FROM
                        obstacle_type
                    ORDER BY
                        obst_type;"""
        db_tools = ObstacleDatabaseTools(self.data_uri)
        obst_type_data = db_tools.select_data_from_obstacle_db(query)

        for obst_type, obst_type_id in obst_type_data:
            self.obstacle_type_map[obst_type] = obst_type_id

    def clear_dof_conversion_settings(self):
        self.conversion_input_path = None
        self.conversion_output_format = None
        self.conversion_output_path = None

    def set_conversion_output_format(self):
        selected_format = self.dlg.comboBoxConversionDOFOutputFormat.currentText()
        if selected_format != "[choose format]":
            self.conversion_output_format = selected_format
            self.dlg.mQgsFileWidgetConversionDOFOutput.setFilter('*.{}'.format(self.conversion_output_format))
        else:
            self.conversion_output_format = None
            self.dlg.mQgsFileWidgetConversionDOFOutput.setFilter('')

    def is_conversion_input_valid(self):
        err_msg = ""
        self.conversion_input_path = self.dlg.mQgsFileWidgetConversionDOFInput.filePath()
        self.conversion_output_path = self.dlg.mQgsFileWidgetConversionDOFOutput.filePath()

        if not os.path.isfile(self.conversion_input_path):
            err_msg += "Select input DOF file for conversion!\n"
        if not self.conversion_output_format:
            err_msg += "Select output format!\n"
        if not self.conversion_output_path:
            err_msg += "Select output converted file!\n"

        if err_msg:
            QMessageBox.critical(QWidget(), "Message", err_msg)
        else:
            return True

    def get_converted_layer(self):
        if self.conversion_output_format == "csv":
            uri = 'file:///{}?delimiter=";"&xField=lon_dd&yField=lat_dd'.format(self.conversion_output_path)
            layer = QgsVectorLayer(uri, 'CSVConvertedDOF', 'delimitedtext')
            crs = layer.crs()
            crs.createFromId(4326)
            layer.setCrs(crs)
        else:
            layer = QgsVectorLayer(self.conversion_output_path,
                                   "{}ConvertedDOF".format(self.conversion_output_format.upper()), "ogr")
        return layer

    def convert_dof(self):
        if self.is_conversion_input_valid():
            plugin_dir = os.path.dirname(__file__)
            path_dof_format = os.path.join(plugin_dir, 'dof_format.json')
            dof_tool = DOFTools(path_dof_format)
            if self.conversion_output_format == "csv":
                dof_tool.convert_dof_to_csv(self.conversion_input_path, self.conversion_output_path)
            else:
                dof_tool.convert_dof_to_geographic_formats(self.conversion_input_path,
                                                           self.conversion_output_path,
                                                           self.conversion_output_format)
        if self.dlg.checkBoxAddOutputToMap.isChecked():
            layer = self.get_converted_layer()
            QgsProject.instance().addMapLayer(layer)


    def initialize_plugin_variables(self):
        self.set_data_uri()
        self.set_obstacle_type_map()
        self.clear_dof_conversion_settings()

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ObstacleFAADigitialObstacleFileDBDialog()
            self.dlg.mQgsFileWidgetDigitalObstacleFile.setFilter('*.dat')
            self.dlg.mQgsFileWidgetImportLog.setFilter("*.log")
            self.dlg.mQgsFileWidgetConversionDOFInput.setFilter('*.dat')
            self.dlg.comboBoxConversionDOFOutputFormat.currentIndexChanged.connect(self.set_conversion_output_format)
            self.dlg.pushButtonConvertDOF.clicked.connect(self.convert_dof)
            self.dlg.pushButtonCancel.clicked.connect(self.dlg.close)

        # show the dialog
        self.dlg.show()
        self.dlg.tabWidget.setCurrentIndex(0)
        self.dlg.mQgsFileWidgetDigitalObstacleFile.lineEdit().clear()
        self.dlg.mQgsFileWidgetImportLog.lineEdit().clear()
        self.dlg.pushButtonShowImportLogFile.setEnabled(False)
        self.dlg.mQgsFileWidgetConversionDOFInput.lineEdit().clear()
        self.dlg.comboBoxConversionDOFOutputFormat.setCurrentIndex(0)
        self.dlg.mQgsFileWidgetConversionDOFOutput.lineEdit().clear()
        self.dlg.checkBoxAddOutputToMap.setChecked(False)
        self.initialize_plugin_variables()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
