import piexif
from PIL import Image
import os

def decimal_to_dms(decimal):
    """
    Converts decimal degrees to degrees, minutes, seconds for EXIF.
    Returns ((d, 1), (m, 1), (s*100, 100))
    """
    degrees = int(decimal)
    temp = (decimal - degrees) * 60
    minutes = int(temp)
    seconds = round((temp - minutes) * 60, 2)
    return ((degrees, 1), (minutes, 1), (int(seconds * 100), 100))

def embed_gps_to_image(image_path, lat, lon):
    """
    Embeds GPS coordinates into JPEG EXIF using piexif.
    """
    try:
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info.get('exif', b''))
        
        lat_dms = decimal_to_dms(abs(lat))
        lon_dms = decimal_to_dms(abs(lon))
        
        gps_ifd = {
            piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
            piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
            piexif.GPSIFD.GPSLatitude: lat_dms,
            piexif.GPSIFD.GPSLongitudeRef: 'E' if lon >= 0 else 'W',
            piexif.GPSIFD.GPSLongitude: lon_dms,
        }
        
        exif_dict['GPS'] = gps_ifd
        exif_bytes = piexif.dump(exif_dict)
        img.save(image_path, exif=exif_bytes)
        return True
    except Exception as e:
        print(f"Error embedding GPS: {e}")
        return False

def read_gps_from_image(image_path):
    """
    Reads GPS coordinates from JPEG EXIF.
    Returns (lat, lon) or None.
    """
    try:
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info.get('exif', b''))
        gps = exif_dict.get('GPS')
        
        if not gps:
            return None
            
        def convert_to_degrees(value):
            d = value[0][0] / value[0][1]
            m = value[1][0] / value[1][1]
            s = value[2][0] / value[2][1]
            return d + (m / 60.0) + (s / 3600.0)

        lat = convert_to_degrees(gps[piexif.GPSIFD.GPSLatitude])
        if gps[piexif.GPSIFD.GPSLatitudeRef] == b'S':
            lat = -lat
            
        lon = convert_to_degrees(gps[piexif.GPSIFD.GPSLongitude])
        if gps[piexif.GPSIFD.GPSLongitudeRef] == b'W':
            lon = -lon
            
        return lat, lon
    except Exception:
        return None
