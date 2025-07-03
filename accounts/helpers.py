from django.utils.timezone import localtime
from django.utils.dateformat import format as dj_format

def mmt(dt):
    if dt is None:
        return None
    return dj_format(localtime(dt),"Y-m-d h:i:s A")