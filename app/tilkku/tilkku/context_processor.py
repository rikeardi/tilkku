import os

def export_env_variables(request):
    return {
        'HOME_LAT': os.environ['HOME_LAT'],
    }