INSERT INTO obstacle_type (obst_type)
VALUES
	('AG EQUIP'),
	('AMUSEMENT PARK'),
	('ANTENNA'),
	('ARCH'),
	('BALLOON'),
	('BLDG'),
	('BLDG-TWR'),
	('BRIDGE'),
	('CATENARY'),
	('COOL TWR'),
	('CRANE'),
	('CTRL TWR'),
	('DAM'),
	('DOME'),
	('ELEC SYS'),
	('ELEVATOR'),
	('FENCE'),
	('GEN UTIL'),
	('GRAIN ELEVATOR'),
	('HANGAR'),
	('HEAT COOL SYSTEM'),
	('LANDFILL'),
	('LGTHOUSE'),
	('MET'),
	('MONUMENT'),
	('NAVAID'),
	('PIPELINE PIPE'),
	('PLANT'),
	('POLE'),
	('POWER PLANT'),
	('REFINERY'),
	('RIG'),
	('SIGN'),
	('SILO'),
	('SOLAR PANELS'),
	('SPIRE'),
	('STACK'),
	('STADIUM'),
	('T-L TWR'),
	('TANK'),
	('TOWER'),
	('TRAMWAY'),
	('UTILITY POLE'),
	('VERTICAL STRUCTURE'),
	('WALL'),
	('WIND INDICATOR'),
	('WINDMILL'),
	('WINDSOCK');
	
INSERT INTO hor_acc
VALUES
	(1, 20, 'ft'),
	(2, 50, 'ft'),
	(3, 100, 'ft'),
	(4, 250, 'ft'),
	(5, 500, 'ft'),
	(6, 1000, 'ft'),
	(7, 0.5, 'NM'),
	(8, 1, 'NM'),
	(9, -1, 'unk');
	
INSERT INTO vert_acc
VALUES
	('A', 3, 'ft'),
	('B', 10, 'ft'),
	('C', 20, 'ft'),
	('D', 50, 'ft'),
	('E', 125, 'ft'),
	('F', 250, 'ft'),
	('G', 500, 'ft'),
	('H', 1000, 'ft'),
	('I', -1, 'unk');

INSERT INTO lighting
VALUES
	('R', 'Red'),
	('D', 'Medium intensity White Strobe & Red'),
	('H', 'Medium Intensity White Strobe'),
	('S', 'High Intensity White Strobe'),
	('F', 'Flood'),
	('C', 'Dual Medium Catenary' ),
	('W', 'Synchronized Red Lighting'),
	('L', 'Lighted (Type Unknown)'), 
	('N', 'None'),
	('U', 'Unknown');
	
INSERT INTO marking
VALUES
	('P', 'Orange or Orange and White Paint'),
	('W', 'White Paint Only'),
	('M', 'Marked'),
	('F', 'Flag Marker'),
	('S', 'Spherical Marker'),
	('N', 'None'),
	('U', 'Unknown');
	
INSERT INTO verif_status
VALUES
	('O', 'Verfified'),
	('U', 'Unverified'),
	('N', 'No data');
