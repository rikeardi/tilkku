import os

def export_env_variables(request):
    return {
        'ENV_VARIABLES': os.environ,
    }