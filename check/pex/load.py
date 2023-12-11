path = "saradc.pex.spice"

with open(path,'r') as fr:
    s = fr.read()
lines = s.split('\n')


path2 = "saradc.pex.spice"
with open(path2,'w') as fw:
    for line in lines:
        if '**FLOATING' in line:
            continue
        fw.write(line)
        fw.write('\n')