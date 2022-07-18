import os


def export_env_variables(request):
    return {
        'environment': {
            'HOME_LAT': os.environ['HOME_LAT'],
        }
    }
