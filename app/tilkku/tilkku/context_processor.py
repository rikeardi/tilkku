import os


def export_env_variables(request):
    return {
        'environment': {
            'HOME_LAT': os.environ['HOME_LAT'],
            'HOME_LON': os.environ['HOME_LON'],
            'HOME_ZOOM': os.environ['HOME_ZOOM'],
            'GRID_LAT': os.environ['GRID_LAT'],
            'GRID_LON': os.environ['GRID_LON'],
            'GRID_SIZE': os.environ['GRID_SIZE'],
        }
    }
