"""
Instance generator for residential Demand Response problems.

This module contains functions to import numerical data and generate instances
    of residential DR problems, formulated as Mixed-Integer Linear Programs.

Functions:
    load_data: import price, load, output and temperature data
    build_model: build the CPLEX MIP instance
        Modify this function to include other aggregator constraints
    generate_instance: wrapper for the above two functions

For detailed models, see [Anjos, Lodi and Tanneau, A Decentralized Framework
    for the optimal coordination of Distributed Energy Resources]

Contact info: mathieu.tanneau@polymtl.ca
"""

import numpy as np
import pandas as pd

import cplex

import devices


def main():
    0


def load_data(
    time_window
):
    """
    Load input data.

    Load and output data are normalized, i.e., each time series is divided by
        its maximum.

    Args:
        time_window: time range, under the form [t1, ..., tn]

    Returns:
        load_norm: normalized Ontario load
        price_mkt: market price of electricity (HOEP)
        price_tou: Time-of-Use rates
        pv_norm: normalized PV output
        temp: temperature
        wind_norm: normalized wind output
    """
    # Price data (normalized)
    ont_price = pd.read_csv('../data/price2016.csv')
    price_mkt = np.array(ont_price['HOEP'])[time_window]  # market prices
    price_tou = np.array(ont_price['TOU'])[time_window]  # Time-of-Use prices

    # Production data (normalized)
    ont_output = pd.read_csv('../data/prod2016.csv')
    wind_norm = np.array(
        (ont_output['WIND']/np.mean(ont_output['WIND']))
    )[time_window]
    pv_norm = np.array(
        (ont_output['SOLAR']/np.mean(ont_output['SOLAR']))
    )[time_window]

    # Load data
    ont_load = pd.read_csv('../data/load2016.csv')
    load_norm = np.array(
        ont_load['OntDemand']/np.mean(ont_load['OntDemand'])
    )[time_window]

    # Temperature data
    temperature = pd.read_csv('../data/temperature2016.csv')
    temperature = np.array(temperature['Temperature'])[time_window]

    return load_norm, price_mkt, price_tou, pv_norm, wind_norm, temperature


def generate_instance(
    n_hh,
    t_begin,
    t_horizon,
    own_rates,
    delta_t=1,
    seed=0
):
    """
    Generate an instance.

    Args:
        n_hh: number of households
        t_begin: beginning of the time horizon
        t_horizon: length of the time horizon
        own_rates: ownership rates of the considered devices
        seed: random seed

    Returns:
        m: CPLEX instance (MIP)

    Raises:
    """
    # load Ontario data
    time_window = range(t_begin, t_begin+t_horizon)
    load_norm, price_mkt, price_tou, pv_norm, wind_norm, temperature =\
        load_data(time_window)

    # re-adjsut the time-window
    time_window = range(t_horizon)

    # generate devices
    dev = devices.generate_devices(
        n_hh=n_hh,
        time_window=time_window,
        load_norm=load_norm,
        pv_norm=pv_norm,
        temperature=temperature,
        own_rates=own_rates,
        seed=seed
    )

    # minimum and maximum aggregated load
    total_load_min = np.zeros(t_horizon)
    total_load_max = 180. * n_hh * np.ones(t_horizon) / 24.

    # build CPLEX model
    m = build_model(
        dev,
        time_window,
        delta_t,
        price_mkt,
        total_load_min,
        total_load_max
    )

    return m


def build_model(
    dev=[],
    time_window=[],
    delta_t=1,
    price_mkt=[],
    total_load_min=[],
    total_load_max=[]
):
    """
    Build CPLEX model.

    Args:
        dev: list of devices
        time_window: list of time indices, has the form [0, ..., T-1]
        delta_t: duration of each time step (in hours)
        price_mkt: market price of electricity
        total_load_min: minimum total load for each time step
        total_load_max: maximum total load for each time step

    Returns:
        m: a centralized MILP formulation of the DR problem

    Raises:
    """
    m = cplex.Cplex()

    v2idx = {}
    c2idx = {}

    # I.
    # Create linking variables

    # total load
    totalLoad_obj = delta_t*price_mkt
    v_idx = m.variables.add(
        names=['totalLoad_'+str(t) for t in time_window],
        obj=totalLoad_obj,
        lb=total_load_min,
        ub=total_load_max
    )
    v2idx.update(dict(zip(
        ['totalLoad'+str(t) for t in time_window],
        v_idx
    )))

    # II.
    # Create linking constraints
    c_idx = m.linear_constraints.add(
        names=['link_total_'+str(t) for t in time_window],
        lin_expr=[
            cplex.SparsePair(
                ind=[v2idx['totalLoad'+str(t)]],
                val=[-1]
            )
            for t in time_window
        ]
    )
    c2idx.update(dict(zip(
        ['totalLoad_link'+str(t) for t in time_window],
        c_idx
    )))

    # III.
    # Add resources to the model
    for i_r, r_devices in enumerate(dev):
        r_label = 'HH_'+str(i_r)
        # create net load variable
        v_idx = m.variables.add(
            names=[r_label+'_'+'netLoad_'+str(t) for t in time_window],
            columns=[
                cplex.SparsePair(
                    ind=[c2idx['totalLoad_link'+str(t)]],
                    val=[1]
                )
                for t in time_window
            ],
            ub=[10 for _ in time_window]
        )
        v2idx.update(dict(zip(
            [r_label+'_'+'netLoad_'+str(t) for t in time_window],
            v_idx
        )))

        # create linking net load for household
        c_idx = m.linear_constraints.add(
            senses=['E' for t in time_window],
            names=[r_label+'_'+'link_netLoad_'+str(t) for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[v2idx[r_label+'_'+'netLoad_'+str(t)]],
                    val=[-1]
                )
                for t in time_window
            ]
        )
        c2idx.update(dict(zip(
            [r_label+'_'+'link_netLoad_'+str(t) for t in time_window],
            c_idx
        )))

        # update with device models
        for d in r_devices:
            d.update_model(
                m,
                var2idx=v2idx,
                ctr2idx=c2idx,
                time_window=time_window,
                delta_t=delta_t,
                r_label=r_label+'_'
            )

    return m


if __name__ == '__main__':
    main()
