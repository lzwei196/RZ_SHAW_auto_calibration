import statistics
import math
#takes in two set data where all the data are corresponding, which implies that the len of the two set of the data are same
def nse(ob, sim):
    ob_mean = statistics.mean(ob)
    upper = 0.0
    lower = 0.0
    try:
        for count, val in enumerate(sim):
            if math.isnan(ob[count]):
                continue
            if math.isnan(val):
                val = 0
            upper = (ob[count]-val)**2 + upper
            lower = (ob[count] - ob_mean) ** 2 + lower
    except Exception as e:
        print(e)

    res = 1 - (upper/lower)
    return res

#takes in two set of dict, where data are not corresponding, needs to find the corresponding data from the other dict to calculate the correct nse
def nse_with_dates(ob, sim):
    ob_mean = statistics.mean(ob.values())
    upper = 0.0
    lower = 0.0
    try:
        for val in ob:
            if val in sim:
                ob_val = ob[val]
                if math.isnan(ob_val):
                    continue
                if math.isnan(sim[val]):
                    continue
                upper = (ob_val - sim[val]) ** 2 + upper
                lower = (ob_val - ob_mean) ** 2 + lower
    except Exception as e:
        print(e)
    res = 1 - (upper/lower)
    return res

def rmsd_with_dates(ob, sim):
    n = 0
    upper = 0
    try:
        for val in ob:
            if val in sim:
                ob_val = ob[val]
                if math.isnan(ob_val):
                    continue
                if math.isnan(sim[val]):
                    continue
                dif = (sim[val] - ob[val])**2
                upper = upper + dif
                n = n + 1
    except Exception as e:
        print(e)

    return math.sqrt((upper/n))


