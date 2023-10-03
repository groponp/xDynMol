# -*- coding: utf-8 -*-
#! xcharmm: A tiny script to custom CHARMM-GUI Inputs 
#! Only for gromacs inputs
#! author: Ropón-Palacios G. 
#! date: Sun 1 Oct 16:21 , 2023 

import os 
import sys
import optparse
from datetime import datetime

#################################### END ######################################################################################
class CharmmFiles:
    def __init__(self, tarfile, NVTns="5", MDns="300", systemType="solution"):
        self.tarfile  = tarfile     # tar.gz file of charmm-gui "charm0.tar.gz, charmm1.tar.gz"
        self.NVTns = NVTns          # tiempo en nanosegundos NVT
        self.MDns = MDns           # tiempo en nanosegundos MD 
        self.systemType = systemType  # tipo de sistema a simular, membrana o solución

    def message(self, string, typeM):
        if typeM == "INFO":
            print("[INFO     ] %s" % (string))
        elif typeM == "WARNING":
            print("[WARNING  ] %s" % (string)) 
        elif typeM == "ERROR":
            print("[ERROR    ] %s" % (string)) 
    
    def xmdp(self, mdpFile, typparm):
        nvtFile = mdpFile   # nombre del archivo en gromacs, too para namd 
        f = open(nvtFile, "r")
        lines = f.readlines()
        newlines = []
        ###########################################################
        if typparm == "nvt":
            nsteps = int(5000000)
            savesteps = int(10000)
            for line in lines:
                if line.startswith("nsteps"):
                    #! run 5 ns at 1 fs 
                    xline = line.replace("nsteps                  = 125000", f"nsteps                = {nsteps} ; 5 ns")
                    newlines.append(xline)

                elif line.startswith("nstxtcout"):
                    #! save each 10 ps  at 1 fs 
                    xline = line.replace("nstxtcout               = 5000", f"nstxtcout               = {savesteps} ; 10 ps")
                    newlines.append(xline)
                elif line.startswith("nstvout"):
                    #! save each 10 ps  at 1 fs 
                    xline = line.replace("nstvout                 = 5000", f"nstvout                 = {savesteps} ; 10 ps")
                    newlines.append(xline)
                elif line.startswith("nstfout"):
                    #! save each 10 ps  at 1 fs 
                    xline = line.replace("nstfout                 = 5000", f"nstfout                 = {savesteps}; 10 ps")
                    newlines.append(xline)
                else:
                    newlines.append(line)
        else: 
            nsteps = int((self.MDns*1000)/0.002)
            savesteps = int(5000)
            for line in lines:
                if line.startswith("nsteps"):
                    #! run 5 ns at 1 fs 
                    xline = line.replace("nsteps                  = 500000", f"nsteps                = {nsteps}; {nsteps}")
                    newlines.append(xline)
                elif line.startswith("nstxtcout"):
                    #! save each 10 ps  at 1 fs 
                    xline = line.replace("nstxtcout               = 50000", f"nstxtcout               = {savesteps} ; 10 ps")
                    newlines.append(xline)
                elif line.startswith("nstvout"):
                    #! save each 10 ps  at 1 fs 
                    xline = line.replace("nstvout                 = 50000", f"nstvout                 = {savesteps}; 10 ps")
                    newlines.append(xline)
                elif line.startswith("nstfout"):
                    #! save each 10 ps  at 1 fs 
                    xline = line.replace("nstfout                 = 5000", f"nstfout                 = {savesteps}; 10 ps")
                    newlines.append(xline)
                else:
                    newlines.append(line)
        f.close()
        ###########################################################
        #!Write file
        os.system(f"rm -rf {mdpFile}")
        fo = open(f"{mdpFile}", "w")
        now = datetime.now()
        datex =  now.strftime("%d/%m/%Y %H:%M:%S")
        fo.write("; Modified with xCHARMM %s by ROPON-PALACIOS G.\n"% (datex))
        for l in newlines:
            fo.write(l)
            
        fo.close()

    def extract(self, xrep=1):
        systems = self.tarfile.split(",")  # genera una lista 
        basename = None
        for idx, k in enumerate(systems):
            self.message(f"Descomprimiendo el archivo {k}", typeM="INFO")
            os.system(f"tar -xvzf {k} > targz{idx}.log")
            f = open(f"targz{idx}.log", "r")
            lines = f.readlines()
            tmo = lines[-1]
            f.close()
            bs1 = tmo.split("/")[0]  # para obtener el nombre de la carpeta
            if "x" in bs1 : basename = bs1.split()[1] # esto porque hay un valor de x y solo se quiere charmm-gui-
            else: basename = bs1
            if os.path.exists(f"sys{idx}/"):
                pass
        
            else:
                os.mkdir(f"sys{idx}")
                os.mkdir(f"sys{idx}/gmx")

            #self.message(f"Copiando gromacs para sys{idx}/gmx_r", typeM="INFO")
            self.message(f"Copiando de {basename}/gromacs para sys{idx}", typeM="INFO")
            os.system(f"cp -r {basename}/gromacs/* sys{idx}/gmx/")
            os.chdir(f"sys{idx}/gmx/")
            self.xmdp(mdpFile="step4.1_equilibration.mdp", typparm="nvt")
            self.xmdp(mdpFile="step5_production.mdp", typparm="md")
            os.chdir("../../")
            for j in range(xrep):
                os.system(f"cp -r sys{idx}/gmx/ sys{idx}/gmx_rep{j}")
        
        os.system(f"rm -rf {basename}")


    def writeBASHscript(self, machine="local"):
        if machine == "local":
            f = open("gmxWorkStation.sh", "w")
            now = datetime.now()
            datex =  now.strftime("%d/%m/%Y %H:%M:%S")
            f.write("# Write with xCHARMM %s by ROPON-PALACIOS G.\n"% (datex))
            xxG = """\
for file in sys*; do 
    echo "Entrando a la carpeta $file ..."
    sleep 5
    cd $file 
    for rep in gmx_rep*; do 
        cd $rep
        echo "Entrando a la repeticion $rep ..."
        sleep 5
        gmx grompp -f step4.0_minimization.mdp -o em.tpr -c step3_input.gro -r step3_input.gro -p topol.top -n index.ndx -maxwarn 10
        gmx mdrun -v -deffnm em 

        gmx grompp -f step4.1_equilibration.mdp -o nvt.tpr -c em.gro -r em.gro -p topol.top -n index.ndx -maxwarn 10
        gmx mdrun -v -deffnm nvt -nb gpu -pme gpu 

        gmx grompp -f step5_production.mdp -o md.tpr -c nvt.gro -p topol.top -n index.ndx -maxwarn 10 
        gmx mdrun -v -deffnm md -nb gpu -pme gpu
        cd ../
    done; 
    cd ../
done
"""
            f.write(xxG)
            f.close()

        else:
            f = open("gmxHPCTemplate.sh", "w")
            now = datetime.now()
            datex =  now.strftime("%d/%m/%Y %H:%M:%S")
            f.write("# Write with xCHARMM %s by ROPON-PALACIOS G.\n"% (datex))
            xxf = """\
#!/bin/bash
#SBATCH --account=def-nike-ab
#SBATCH --mail-user=groponp@gmail.com
#SBATCH --mail-type=ALL
#SBATCH --time=7-00:00:00           #! time limit (D-HH:MM)
#SBATCH --nodes=1
##SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=5
#SBATCH --gpus-per-node=v100:4
#SBATCH --mem=0                  #! request all available memory on the node
#SBATCH --job-name="changeMe"

#! Os paquetes que sao necesarios para usar gromacs.
module purge
module load StdEnv/2020 gcc/9.3.0 cuda/11.4 openmpi/4.0.3 gromacs/2022.3
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"

cd sys0
cd gmx_rep0
gmx grompp -f step4.0_minimization.mdp -o em.tpr -c step3_input.gro -r step3_input.gro -p topol.top -n index.ndx -maxwarn 10
srun --cpus-per-task=$OMP_NUM_THREADS gmx_mpi mdrun -v -deffnm em 

gmx grompp -f step4.1_equilibration.mdp -o nvt.tpr -c em.gro -r em.gro -p topol.top -n index.ndx -maxwarn 10
srun --cpus-per-task=$OMP_NUM_THREADS gmx_mpi mdrun -v -deffnm nvt 

gmx grompp -f step5_production.mdp -o md.tpr -c nvt.gro -p topol.top -n index.ndx -maxwarn 10 
srun --cpus-per-task=$OMP_NUM_THREADS gmx_mpi mdrun -v -deffnm md 
"""
            f.write(xxf)
            f.close()

#################################### END ######################################################################################



parser = optparse.OptionParser() 
#! INPUTS options
parser.add_option("--xcompress", help="Compress File \"charmm1.tar.gz, charmm2.tar.gz\"", type=str)
parser.add_option("--md-time", help="Time to perform md in nanoseconds", dest="mdns", type=int)
parser.add_option("--xrep", help="Number of independent replicates by system, defaut 1", type=int)
parser.add_option("--machine", help="machine to use, hpc, local", type=str)
options, args = parser.parse_args() 

#! call class 
xcharmm = CharmmFiles(tarfile=options.xcompress, MDns=options.mdns)
xcharmm.extract(xrep=options.xrep)

if options.machine == "local":
    xcharmm.writeBASHscript(machine="local")

else:
    xcharmm.writeBASHscript(machine="hpc")
