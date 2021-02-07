from os import environ


# Configure Test Environment
def get_env(string):
    try:
        return environ[string]
    except KeyError:
        return ""


def env_str(variable, default):
    if variable != "" and variable is not None:
        return variable
    return default


# Configure Test Environment
def env_bool(variable, default):
    value = env_str(variable, default)
    if value is None:
        return default
    if isinstance(value, str):
        return value.upper() == 'TRUE'
    return value


ENV = {
    'remote': {
        'sudo': get_env('SUDO'),
    }
}
