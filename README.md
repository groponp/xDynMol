# xDynMol: A toolkit for Macromolecular Modeling and Molecular Dynamics 
<div style="text-align: justify">
This is a suite of useful tools for macromolecule modeling and molecular dynamics, which will allow users to handle different common tasks within these two big fields. The main language is python, and therefore can be easily extended and modified. 

If you have any questions about our tools, ask them in the **issues section** or to ROPÓN-PALACIOS G email: groponp@gmail.com who is the main developer.

## Contributors
Those who contribute to this repo can either place their name here (via a pull request) or ask to be added to the main developer.


## Clone the repository 
```bash
git clone git@github.com:groponp/xDynMol.git
```

## Citations
If you're using any code, please cite our papers: 
1. Ropón-Palacios et al.  (2020) Potential novel inhibitors against emerging zoonotic pathogen Nipah virus: a virtual screening and molecular dynamics approach, Journal of Biomolecular Structure and Dynamics, 38:11, 3225-3234, DOI:10.1080/07391102.2019.1655480
2. Ropón Palacios et al. (2019) Novel multi-epitope protein containing conserved epitopes from different Leishmania species as potential vaccine candidate: Integrated immunoinformatics and molecular dynamics approach, Computational Biology and Chemistry, DOI: https://doi.org/10.1016/j.compbiolchem.2019.107157.
3. Otazu et al. (2020) Targeting Receptor Binding Domain and Cryptic Pocket of Spike glycoprotein from SARS-CoV-2 by biomolecular modeling, ARXIV Quantitative Biology, Biomolecules, DOI: https://doi.org/10.48550/arXiv.2006.06452
4. Ropón-Palacios e tal. (2022) Glycosylation is key for enhancing drug recognition into spike glycoprotein of SARS-CoV-2, Computational Biology and Chemistry, DOI: https://doi.org/10.1016/j.compbiolchem.2022.107668
5. Osorio-Mogollón et al. (2022) Attacking the SARS-CoV-2 Replication Machinery with the Pathogen Box’s Molecules, Letters in Drug Desing & Discovery, DOI: 10.2174/1570180819666220622085659 
6. Atanda et al. (2023). In silico study revealed the inhibitory activity of selected phytomolecules of C. rotundus against VacA implicated in gastric ulcer, Journal of Biomolecular Structure and Dynamics, DOI: https://doi.org/10.1080/07391102.2022.2160814 


## Information of the Tools
 **xCHARMM.py:** This is a tool that allows you to customize the outputs of the CHARMM-GUI Solution Builder module.\
Example: Imagine that you have 2 CHARMM-GUI outputs, called charmm1.tar.gz, charmm2.tar.gz and you want to run a simulation on your local workstation, where each system (i.e. each charmm-gui output), are going to run it triplicate, that is, three independent replicas, you could use the following command, assuming that you want to simulate 300 ns for each replica, a total of 0.9 $\mu s$ per system.
```bash
python xCHARMM.py --xcompress "charmm1.tar.gz,charmm2.tar.gz" --md-time 300 --xrep 3  --machine local 
```
This could generate at the end a bash script called **gmxWorkStation.sh**, which has all the instructions to run with gromacs. Note: Currently this script handles systems that are prepared to run with gromacs. If you need to see other options you can do a **-h** to the script.

## License 
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Disclaimer
Icons in this repo were taken from [flaticon](https://www.flaticon.com/free-icons/programming-language) 
