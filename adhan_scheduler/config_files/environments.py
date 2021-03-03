from os import environ


def get_env(string):
    try:
        return environ[string]
    except KeyError:
        return ""


def env_str(variable, default):
    if variable != "" and variable is not None:
        return variable
    return default


def env_int(variable, default):
    try:
        return int(env_str(variable, default))
    except ValueError:
        return default


def env_bool(variable, default):
    value = env_str(variable, default)
    if value is None:
        return default
    if isinstance(value, str):
        return value.upper() == 'TRUE'
    return value


# Configure Environments
ENV = {
    'prayer_times': {
        'school': get_env('SCHOOL'),
        'method': get_env('METHOD'),
        'offset': get_env('OFFSET'),
        'reschedule_isha': get_env('RESCHEDULE_ISHA'),
        'reschedule_fajr': get_env('RESCHEDULE_FAJR'),
        'mins_before_sunrise': get_env('MINS_BEFORE_SUNRISE'),
    }
}
