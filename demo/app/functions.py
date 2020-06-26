def _percentage_change(datastore,cache):
    abs_change = (cache - datastore)
    return str(("%.2f" %(100.0*abs_change/abs(float(datastore))))+"%")