from obstacle_faa_dof_db.dof_utils.dof_conversion_errors import LongitudeConversionError, LatitudeConversionError


def check_hemisphere(hem, coord_type):
    """
    param: hem: string, hemisphere character
    param: coord_type: string, coordinate type: LATITUDE or LONGITUDE
    return: bool
    """
    if coord_type == "LATITUDE":
        if hem in ['N', 'S']:
            return True
    elif coord_type == "LONGITUDE":
        if hem in ['E', 'W']:
            return True


def dmsh_to_dd(src_coord, coord_type):
    """ Converts DMS format of longitude, latitude from DOF data into DD format.
    param: src_coord: string, latitude or longitude in degrees, minutes, seconds format
    return: dd: float, latitude or longitude in decimal degrees format
    """
    h = src_coord[-1]
    if check_hemisphere(h, coord_type):
        coord_parts = src_coord.split(' ')
        d = float(coord_parts[0])
        m = float(coord_parts[1])
        s = float(coord_parts[2][:-1])

        dd = d + m / 60 + s / 3600

        if h in ['W', 'S']:
            dd = - dd
        return dd


def longitude_to_dms(lon_src):
    """
    :param lon_src: str
    :return: float
    """
    try:
        dd = dmsh_to_dd(lon_src, "LONGITUDE")
    except (ValueError, TypeError):
        raise LongitudeConversionError(lon_src)
    else:
        if dd is None:
            raise LongitudeConversionError(lon_src)
        else:
            return dd


def latitude_to_dms(lat_src):
    """
    :param lat_src: str
    :return: float
    """
    try:
        dd = dmsh_to_dd(lat_src, "LATITUDE")
    except (ValueError, TypeError):
        raise LongitudeConversionError(lat_src)
    else:
        if dd is None:
            raise LatitudeConversionError(lat_src)
        else:
            return dd
