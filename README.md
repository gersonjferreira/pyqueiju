# pyQUEIJU

**pyQUEIJU: QUantum Espresso Interface on JUpyter**

This is a very simple and minimalist interface to use QE from Jupyter instead of running commands and bash scripts.

The idea to aggregate the most of the QE running procedure within a single Jupyter file. This is useful to keep track of what you are running, which parameters are being used, etc. As a bonus, we can plot the results on the same interface.

Of course this can also be done in bash, but it is much easier and clean to run python scripts within Jupyter instead. 

The current version is meant only for simple QE systems that can run in a single node on your personal computer. It is not prepared to run a proper job on a server (to do list).

> **Contributors are welcome!** Please contact me.

## To do list

- create a cool and *cheesy* (pun intended) logo and explain the joke for non-Brazilians.
- improve the overall plot script in graphene.ipynb to extract data automatically from the output files.
- change the run method to allow for running a job on a server (SLURM?) and track its status.

## How to use it

As a reference, I'll use the relaxation call as an example. But on te graphene example file you can see more details.

- To import the module, run

> `from pyqueiju import queiju`

- To create an instance call:

> `relax = queiju(relax_in, qe_path)`

or

> `relax = queiju(relax_in)`

where `relax_in` is the string with the QE input data (see graphene example for details) and `qe_path` is the path to the QE binaries. If the binaries are on $PATH, we can ommit `qe_path=""` as in the second line above. Here we are calling this instance **relax**, but use an appropriate name for the type of calculation you are calling (relax, scf, nscf, bands, ...)

- To run, call the `run` method informing the proper binary:

> `relax.run("pw.x")`

- To see the output, either print to screen or save to an external file as

> `print(relax.out)`

> `relax.saveoutput('relax.out')`

- A list of files created or modified by the QE run is available at

> `print(relax.files)`

