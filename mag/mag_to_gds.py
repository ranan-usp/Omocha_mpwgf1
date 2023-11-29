import subprocess
import os



def exe_magic_file(path = None):

    # pex
    cp = subprocess.run(["magic","-noconsole","-dnull",path])
    print("returncode:", cp.returncode)


if __name__ == '__main__':

    path = "/home/oe23ranan/gf_analog/mag/inv"

    folderfile = os.listdir(path)

    export_file = 'mag_to_gds.tcl'
    
    for file_name in folderfile:
        cell_name = file_name.split('.')[0]
        

        with open('template.tcl','r') as fr:
            s = fr.read()
        lines = s.split('\n')
        
        with open(export_file,'w') as fw:
            for line in lines:

                line = line.replace('temp',cell_name)
                fw.write(line+'\n')

        exe_magic_file(path = export_file)



