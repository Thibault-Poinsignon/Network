#Network


##Create the adequate conda environment

All the necessery package for this project are listed in the file *environment.yml*. A identical environment can be created with the next line in a terminal.

'''

conda env create -f environment.yml --name new_environment
'''


##Open the environment

The new conda environment need to be open. In the terminal, the lines will start with (new_environment) insteed of (base).

'''

conda activate new_environment
'''

##Jupiter Notebook and jupitext

Once the environment is created and opened, the package jupyterlab can be use to open the project *IPY_network.py*.
Jupytext is installed in the environment so jupyter will be able to read the .py file as a notebook.


'''

jupyter notebook
'''

The files *fonctions.py* and *mini_multi_omi.csv* need to be in the same folder than *IPY_network.py*.

