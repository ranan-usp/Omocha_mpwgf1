# http://opencircuitdesign.com/magic/

# read design
gds read $::env(GDS_FILE)
load $::env(CELL_NAME)

echo 
echo DRC START
# count number of DRC errors
drc euclidean off
drc catchup
drc check
drc count
drc find
drc why
drc list why
echo DRC FINISH!!

# quit
quit
