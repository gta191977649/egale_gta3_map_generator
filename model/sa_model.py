# This file deal SA In Game DYMATIC MODEL

SA_MODELS = {}

# Reading all
f = open(r'F:\dev\egale_gta3_map_generator\sa_props\sa_ids.txt', 'r')
lines = f.readlines()

for line in lines:
    id,model = line.strip().split(",")
    SA_MODELS[model.lower()] = id

def getSAModelID(modelname):
    if modelname in SA_MODELS: return SA_MODELS[modelname]
    return False

