# DER_instances

Instance generator for generating Mixed-Integer Linear Programs that represent the operation of Distributed Energy Resources.

## Requirements

This code is written in `Python 2.7`, and requires the following packages to be installed:
* `pandas`
* `numpy`
* `cplex` (requires that you have CPLEX installed on your machine)

## Use

All models are detailed in: Anjos, Lodi, Tanneau, _A Decentralized Framework for the Optimal Coordination of Distributed Energy Resources_.

### Generating instances

An example is provided in `test/example.ipynb`. Resources' models can be added/modified by updating `src/devices.py`.

### Replicating results

The testbed that was used in [Anjos, Lodi, Tanneau] can be generated using  `test/paper_testbed.ipynb`. More details are given in the notebook.
