"""
Models for devices.

For more details on models and terminology, see
    [Anjos, Lodi and Tanneau, A Decentralized Framework the optimal
    coordination of Distributed Energy Resources]

Classes:
    Device: abstract class
    FixedLoad: models fixed load devices
    Battery: models battery energy storage systems
    ThermalLoad: models thermal load, such as space heating
    DeferrableLoad: models deferrable loads, such as electric vehicles
    ShiftableLoad: models uninterruptible loads, e.g. dishwashers
    CurtailableLoad: models curtailable loads, e.g. solar PV

You can add device models by adding the corresponding class, or simply changing
    numerical parameters of existing classes.

Contact info: mathieu.tanneau@polymtl.ca
"""


import numpy as np
import cplex


class Device:
    """Energy device."""

    def __init__(
        self,
        label='',
    ):
        """Class constructor."""
        self.label = label
        return

    def update_model(
        self,
        m,
        var2idx={},
        ctr2idx={},
        time_window=[],
        delta_t=1,
        r_label='',
        binaries=True
    ):
        """
        Add self to household model.

        This function must be implemented in all child classes.

        Args:
            m: existing CPLEX instance, to which that device's model is added
            var2idx: a dictionnary that maps the name of the variables in `m`
                to their index number. Indexing by number speeds-up the
                building of the model.
                This dictionnary must be updated accordingly.
            ctr2idx: a dictionnary that maps the name of the constraints in `m`
                to their index number. Same as var2idx.
            time_window: a list of the time indices [0, ..., T-1]
            delta_t: duration of each time-step, in hours
            r_label: label of the resource owning that device.
                Example: r_label==`HH0` mean this device is part of household
                    `HH0`
            binaries: boolean that indicates whether binary requirements are to
                be enforced or not. Setting this parameter to `False` will
                relax binary requirements for that device's model.

            Returns:
                nothing, but `m`, `var2idx` and `ctr2idx` are modified in-place

            Raises:
        """

        return


class FixedLoad(Device):
    """
    Fixed load

    """

    def __init__(
        self,
        label='',
        fixed_load=[]
    ):
        """
        Class constructor.

        """

        Device.__init__(self, label=label)
        self.load = fixed_load

        return

    def update_model(
        self,
        m,
        var2idx={},
        ctr2idx={},
        time_window=[],
        delta_t=1,
        r_label='',
        binaries=True
    ):
        """
        Add self to household model.

        """

        # Since load is fixed, simply change the right-hand side
        # Recall link constraint writes as:
        # - <HH_net_load> + \sum_{D} <D_net_load> = 0
        # so the negative load is added to the rhs:
        # - <HH_net_load> + \sum_{D} <D_net_load> = - <fixed_load>

        # get right-hand side of linking constraints for net load
        rhs = np.array(m.linear_constraints.get_rhs(
            [ctr2idx[r_label+'link_netLoad_'+str(t)] for t in time_window]
        ))
        rhs -= self.load
        m.linear_constraints.set_rhs(
            [
                (
                    ctr2idx[r_label+'link_netLoad_'+str(t)],
                    rhs[t]
                )
                for t in time_window
            ]
        )

        return


class Battery(Device):
    """
    Battery.

    """

    def __init__(
        self,
        label='',
        pwr_chg_min=0,
        pwr_chg_max=6,
        pwr_dis_min=0,
        pwr_dis_max=6,
        soc_min=0,
        soc_max=10,
        soc_init=0,
        eff_chg=0.9,
        eff_dis=0.9,
        half_life=50000
    ):
        """
        Constructor.

        Parameters
        ----------
        time_window : array

        pwr_chg_min : float
            minimum charging power
        pwr_chg_max : float
            maximum charging power
        pwr_dis_min : float
            minimum duscharging power
        pwr_dis_max : float
            maximum discharging power
        soc_min : float
            minimum state of charge
        soc_max : float
            maximum state of charge
        soc_init : float
            initial state of charge
        eff_chg : float in [0,1]
            charging efficiency
        eff_dis : float in [0,1]
            discharging efficiency
        half_life : float
            Number of hours it would take the battery to loose half its
            energy, by self-discharge only.
            1 percent loss per month <=> <half_life> ~ 50000 hours
        """

        Device.__init__(self, label=label)

        self.pwr_chg_min = pwr_chg_min
        self.pwr_chg_max = pwr_chg_max
        self.pwr_dis_min = pwr_dis_min
        self.pwr_dis_max = pwr_dis_max
        self.soc_min = soc_min
        self.soc_max = soc_max
        self.soc_init = soc_init
        self.eff_chg = eff_chg
        self.eff_dis = eff_dis
        self.half_life = half_life

        return

    def update_model(
        self,
        m,
        var2idx={},
        ctr2idx={},
        time_window=[],
        delta_t=1,
        r_label='',
        binaries=True
    ):
        """
        Add self to model

        Parameters
        ----------

        """

        # I.
        # Add variables

        # battery charging power
        # bounds are tackle by the on-off indicator
        v_idx = m.variables.add(
            names=[r_label+self.label+'_pwr_chg_'+str(t) for t in time_window],
            columns=[
                cplex.SparsePair(
                    ind=[ctr2idx[r_label+'link_netLoad_'+str(t)]],
                    val=[1]
                )
                for t in time_window
            ]
        )
        var2idx.update(dict(zip(
            [r_label+self.label+'_pwr_chg_'+str(t) for t in time_window],
            v_idx
        )))

        # battery discharging power
        # bounds are tackle by the on-off indicator
        v_idx = m.variables.add(
            names=[r_label+self.label+'_pwr_dis_'+str(t) for t in time_window],
            columns=[
                cplex.SparsePair(
                    ind=[ctr2idx[r_label+'link_netLoad_'+str(t)]],
                    val=[-1]
                )
                for t in time_window
            ]
        )
        var2idx.update(dict(zip(
            [r_label+self.label+'_pwr_dis_'+str(t) for t in time_window],
            v_idx
        )))

        # state-of-charge
        v_idx = m.variables.add(
            names=[r_label+self.label+'_soc_'+str(t) for t in time_window],
            lb=[self.soc_min for t in time_window],
            ub=[self.soc_max for t in time_window]
        )
        var2idx.update(dict(zip(
            [r_label+self.label+'_soc_'+str(t) for t in time_window],
            v_idx
        )))

        # battery charging indicator
        if binaries:
            v_idx = m.variables.add(
                names=[
                    r_label+self.label+'_chg_ind_'+str(t)
                    for t in time_window
                ],
                types=['B' for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_chg_ind_'+str(t) for t in time_window],
                v_idx
            )))

            # battery discharging indicator
            v_idx = m.variables.add(
                names=[
                    r_label+self.label+'_dis_ind_'+str(t)
                    for t in time_window
                ],
                types=['B' for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_dis_ind_'+str(t) for t in time_window],
                v_idx
            )))
        else:
            v_idx = m.variables.add(
                names=[
                    r_label+self.label+'_chg_ind_'+str(t)
                    for t in time_window
                ],
                lb=[0 for t in time_window],
                ub=[1 for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_chg_ind_'+str(t) for t in time_window],
                v_idx
            )))

            # battery discharging indicator
            v_idx = m.variables.add(
                names=[
                    r_label+self.label+'_dis_ind_'+str(t)
                    for t in time_window
                ],
                lb=[0 for t in time_window],
                ub=[1 for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_dis_ind_'+str(t) for t in time_window],
                v_idx
            )))

        # II.
        # Add constraints
        eta = np.exp(-np.log(2) * delta_t / self.half_life)

        # Conservation of energy at time t=0
        # <soc_0> =
        #           <soc_init> * <eta>
        #           + <delta_t> * <eff_chg> * <pwr_chg_t>
        #           - <delta_t> * 1/<eff_dis> * <pwr_dis_t>
        c_idx = m.linear_constraints.add(
            names=[r_label+self.label+'_ener_cons_0'],
            senses=['E'],
            rhs=[eta * self.soc_init],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_soc_0'],
                        var2idx[r_label+self.label+'_pwr_chg_0'],
                        var2idx[r_label+self.label+'_pwr_dis_0']
                    ],
                    val=[
                        1,
                        - delta_t * self.eff_chg,
                        + delta_t / self.eff_dis
                    ]
                )
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_ener_cons_0'],
            c_idx
        )))
        # Conservation of energy at time t>0
        # <soc_t> =
        #           <soc_{t-1}> * <eta>
        #           + <delta_t> * <eff_chg> * <pwr_chg_t>
        #           - <delta_t> * 1/<eff_dis> * <pwr_dis_t>
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_ener_cons_'+str(t)
                for t in time_window[1:]
            ],
            senses=['E' for t in time_window[1:]],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_soc_'+str(t)],
                        var2idx[r_label+self.label+'_soc_'+str(t-1)],
                        var2idx[r_label+self.label+'_pwr_chg_'+str(t)],
                        var2idx[r_label+self.label+'_pwr_dis_'+str(t)]
                    ],
                    val=[
                        1,
                        - eta,
                        - delta_t * self.eff_chg,
                        + delta_t / self.eff_dis
                    ]
                )
                for t in time_window[1:]
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_ener_cons_'+str(t) for t in time_window[1:]],
            c_idx
        )))

        # Charging bounds
        # u_chg[t] * pwr_chg_min <= pwr_chg <= u_chg[t] * p_chg_max
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_pwr_chg_min_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_chg_'+str(t)],
                        var2idx[r_label+self.label+'_chg_ind_'+str(t)]
                    ],
                    val=[
                        -1,
                        1 * self.pwr_chg_min
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_pwr_chg_min_'+str(t) for t in time_window],
            c_idx
        )))
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_pwr_chg_max_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_chg_'+str(t)],
                        var2idx[r_label+self.label+'_chg_ind_'+str(t)]
                    ],
                    val=[
                        1,
                        -1 * self.pwr_chg_max
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_pwr_chg_max_'+str(t) for t in time_window],
            c_idx
        )))

        # Discharging bounds
        # u_dis[t] * pwr_dis_min <= pwr_dis <= u_dis[t] * p_dis_max
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_pwr_dis_min_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_dis_'+str(t)],
                        var2idx[r_label+self.label+'_dis_ind_'+str(t)]
                    ],
                    val=[
                        -1,
                        1 * self.pwr_dis_min
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_pwr_dis_min_'+str(t) for t in time_window],
            c_idx
        )))
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_pwr_dis_max_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_dis_'+str(t)],
                        var2idx[r_label+self.label+'_dis_ind_'+str(t)]
                    ],
                    val=[
                        1,
                        -1 * self.pwr_dis_max
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_pwr_dis_max_'+str(t) for t in time_window],
            c_idx
        )))

        # Charge/discharge binary constraint
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_cstr_bin_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            rhs=[1 for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_chg_ind_'+str(t)],
                        var2idx[r_label+self.label+'_dis_ind_'+str(t)]
                    ],
                    val=[
                        1,
                        1
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_cstr_bin_'+str(t) for t in time_window],
            c_idx
        )))

        # Done

        return


class ThermalLoad(Device):
    """
    Thermal load.

    """

    def __init__(
        self,
        label='',
        temp_min=[],
        temp_max=[],
        temp_ext=[],
        temp_init=20.,
        pwr_th_min=0,
        pwr_th_max=1.,
        heat_cpty=1.,
        th_eff=1.,
        cond_coeff=1.
    ):
        """
        Class constructor.

        Parameters
        ----------
        temp_min : float array
            minimum temperature (in C)
        temp_max : float array
            maximum temperature (in C)
        temp_ext : float array
            outside temperature (in C)
        pwr_th_min : float
            minimum thermal power
        pwr_th_max : float
            maximum thermal power
        heat_cpty : float
            heat capacity of the house
        th_eff : float
            power efficienvy of the heating unit
        cond_coeff : float
            conduction coefficient of the house

        """
        Device.__init__(self, label=label)

        self.temp_min = temp_min
        self.temp_max = temp_max
        self.temp_ext = temp_ext
        self.temp_init = temp_init
        self.pwr_th_min = pwr_th_min
        self.pwr_th_max = pwr_th_max
        self.heat_cpty = heat_cpty
        self.th_eff = th_eff
        self.cond_coeff = cond_coeff

        return

    def update_model(
        self,
        m,
        var2idx,
        ctr2idx,
        time_window,
        delta_t,
        r_label='',
        binaries=True
    ):
        """
        Add self to model

        """

        # I
        # Add variables.

        # thermal power
        v_idx = m.variables.add(
            names=[r_label+self.label+'_pwr_'+str(t) for t in time_window],
            columns=[
                cplex.SparsePair(
                    ind=[ctr2idx[r_label+'link_netLoad_'+str(t)]],
                    val=[1]
                )
                for t in time_window
            ]
        )
        var2idx.update(dict(zip(
            [r_label+self.label+'_pwr_'+str(t) for t in time_window],
            v_idx
        )))

        # temperature
        v_idx = m.variables.add(
            names=[r_label+self.label+'_temp_'+str(t) for t in time_window],
            lb=self.temp_min,
            ub=self.temp_max
        )
        var2idx.update(dict(zip(
            [r_label+self.label+'_temp_'+str(t) for t in time_window],
            v_idx
        )))

        # on-off coefficient
        if binaries:
            # on-off is binary variable
            v_idx = m.variables.add(
                names=[
                    r_label+self.label+'_on_ind_'+str(t) for t in time_window
                ],
                types=['B' for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_on_ind_'+str(t) for t in time_window],
                v_idx
            )))
        else:
            # binary condition is relaxed
            v_idx = m.variables.add(
                names=[
                    r_label+self.label+'_on_ind_'+str(t) for t in time_window
                ],
                lb=[0 for t in time_window],
                ub=[1 for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_on_ind_'+str(t) for t in time_window],
                v_idx
            )))

        # II.
        # Add constraints

        # bounds on thermal power
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_pwr_th_min_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_'+str(t)],
                        var2idx[r_label+self.label+'_on_ind_'+str(t)]
                    ],
                    val=[
                        -1,
                        1 * self.pwr_th_min
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_pwr_th_min_'+str(t) for t in time_window],
            c_idx
        )))
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_pwr_th_max_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_'+str(t)],
                        var2idx[r_label+self.label+'_on_ind_'+str(t)]
                    ],
                    val=[
                        1,
                        -1 * self.pwr_th_max
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_pwr_th_max_'+str(t) for t in time_window],
            c_idx
        )))

        # Temperature exchange for t=0
        c_idx = m.linear_constraints.add(
            names=[r_label+self.label+'_temp_exch_0'],
            senses=['E'],
            rhs=[
                self.temp_init
                + delta_t * (self.cond_coeff / self.heat_cpty)
                * (self.temp_ext[0] - self.temp_init)
            ],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_temp_0'],
                        var2idx[r_label+self.label+'_pwr_0']
                    ],
                    val=[
                        1,
                        - delta_t * (self.th_eff / self.heat_cpty),
                    ]
                )
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_temp_exch_0'],
            c_idx
        )))

        # Temperature exchange for t>0
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_temp_exch_'+str(t)
                for t in time_window[1:]
            ],
            senses=['E' for t in time_window[1:]],
            rhs=[
                (
                    delta_t * (self.cond_coeff / self.heat_cpty)
                    * self.temp_ext[t]
                )
                for t in time_window[1:]
            ],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_temp_'+str(t)],
                        var2idx[r_label+self.label+'_temp_'+str(t-1)],
                        var2idx[r_label+self.label+'_pwr_'+str(t)]
                    ],
                    val=[
                        1,
                        - (
                            1.
                            - delta_t * (self.cond_coeff / self.heat_cpty)
                        ),
                        - delta_t * (self.th_eff / self.heat_cpty),
                    ]
                )
                for t in time_window[1:]
            ]
        )
        ctr2idx.update(dict(zip(
            [
                r_label+self.label+'_temp_exch_'+str(t)
                for t in time_window[1:]
            ],
            c_idx
        )))

        return


class DeferrableLoad(Device):
    """
    Deferrable load.

    """

    def __init__(
        self,
        label='',
        energy_min=0,
        energy_max=0,
        pwr_min=0,
        pwr_max=0
    ):
        """
        Class constructor.

        """

        Device.__init__(self, label=label)

        self.pwr_min = pwr_min
        self.pwr_max = pwr_max
        self.energy_min = energy_min
        self.energy_max = energy_max

        return

    def update_model(
        self,
        m,
        var2idx={},
        ctr2idx={},
        time_window=[],
        delta_t=1,
        r_label='',
        binaries=True
    ):
        """
        Add self to household model.

        """

        # I.
        # Add variables

        # power
        v_idx = m.variables.add(
            names=[r_label+self.label+'_pwr_'+str(t) for t in time_window],
            columns=[
                cplex.SparsePair(
                    ind=[ctr2idx[r_label+'link_netLoad_'+str(t)]],
                    val=[1]
                )
                for t in time_window
            ]
        )
        var2idx.update(dict(zip(
            [r_label+self.label+'_pwr_'+str(t) for t in time_window],
            v_idx
        )))

        # on-off
        if binaries:
            v_idx = m.variables.add(
                names=[r_label+self.label+'_u_'+str(t) for t in time_window],
                types=['B' for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_u_'+str(t) for t in time_window],
                v_idx
            )))
        else:
            v_idx = m.variables.add(
                names=[r_label+self.label+'_u_'+str(t) for t in time_window],
                lb=[0 for t in time_window],
                ub=[1 for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_u_'+str(t) for t in time_window],
                v_idx
            )))

        # II.
        # Add constraints

        # total energy requirement
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_E_tot_min',
                r_label+self.label+'_E_tot_max'
            ],
            senses=['G', 'L'],
            rhs=[self.energy_min, self.energy_max],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_'+str(t)]
                        for t in time_window
                    ],
                    val=[
                        delta_t
                        for t in time_window
                    ]
                ),
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_'+str(t)]
                        for t in time_window
                    ],
                    val=[
                        delta_t
                        for t in time_window
                    ]
                )
            ]
        )
        ctr2idx.update(dict(zip(
            [
                r_label+self.label+'_E_tot_min',
                r_label+self.label+'_E_tot_max'
            ],
            c_idx
        )))

        # on-off
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_pwr_min_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_'+str(t)],
                        var2idx[r_label+self.label+'_u_'+str(t)]
                    ],
                    val=[
                        -1,
                        1 * self.pwr_min[t]
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_pwr_min_'+str(t) for t in time_window],
            c_idx
        )))
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_pwr_max_'+str(t)
                for t in time_window
            ],
            senses=['L' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_'+str(t)],
                        var2idx[r_label+self.label+'_u_'+str(t)]
                    ],
                    val=[
                        1,
                        -1 * self.pwr_max[t]
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [r_label+self.label+'_pwr_max_'+str(t) for t in time_window],
            c_idx
        )))

        # Done

        return


class ShiftableLoad(Device):
    """
    Uninterruptible load.

    """

    def __init__(
        self,
        label='',
        t_start_min=[],
        t_start_max=[],
        cycles=[[]]
    ):
        """
        Class constructor

        Parameters
        ----------
        label : string
            Device label
        t_start_min : array of int
            minimum start time for each cycle
        t_start_max : array of int
            maximum start time for each cycle
        cycles : list of (float array)
            List of load profile for each cycle
            cycles[k] is the load profile for the k-th cycle
        """

        Device.__init__(self, label=label)

        self.t_start_min = t_start_min
        self.t_start_max = t_start_max
        self.cycles = cycles
        # number of cycles
        self.n_cycles = len(cycles)
        # duration of each cycle
        self.durations = [len(c) for c in cycles]

    def update_model(
        self,
        m,
        var2idx={},
        ctr2idx={},
        time_window=[],
        delta_t=1,
        r_label='',
        binaries=True
    ):
        """
        Add self to household model.

        It is assumed that:
            * There exists at least one feasible schedule.
            * Min/Max starting times are so that each cycle is guaranteed to
                terminate before the end of the time horizon, ie:
                t_max[k] + L_k <= T

        """

        # I.
        # Add variables.

        # power
        v_idx = m.variables.add(
            names=[r_label+self.label+'_pwr_'+str(t) for t in time_window],
            columns=[
                cplex.SparsePair(
                    ind=[ctr2idx[r_label+'link_netLoad_'+str(t)]],
                    val=[1]
                )
                for t in time_window
            ]
        )
        var2idx.update(dict(zip(
            [r_label+self.label+'_pwr_'+str(t) for t in time_window],
            v_idx
        )))

        # start_up for each cycle
        # for k in range(self.n_cycles):
        if binaries:
            v_idx = m.variables.add(
                names=[
                    r_label+self.label+'_u_'+str(k)+'_'+str(t)
                    for k in range(self.n_cycles)
                    for t in range(
                        self.t_start_min[k],
                        self.t_start_max[k]+1
                    )
                ],
                types=[
                    'B'
                    for k in range(self.n_cycles)
                    for t in range(
                        self.t_start_min[k],
                        self.t_start_max[k]+1
                    )
                ]
            )
            var2idx.update(dict(zip(
                [
                    r_label+self.label+'_u_'+str(k)+'_'+str(t)
                    for k in range(self.n_cycles)
                    for t in range(
                        self.t_start_min[k],
                        self.t_start_max[k]+1
                    )
                ],
                v_idx
            )))
        else:
            v_idx = m.variables.add(
                names=[
                    r_label+self.label+'_u_'+str(k)+'_'+str(t)
                    for k in range(self.n_cycles)
                    for t in range(
                        self.t_start_min[k],
                        self.t_start_max[k]+1
                    )
                ],
                lb=[
                    0
                    for k in range(self.n_cycles)
                    for t in range(
                        self.t_start_min[k],
                        self.t_start_max[k]+1
                    )
                ],
                ub=[
                    1
                    for k in range(self.n_cycles)
                    for t in range(
                        self.t_start_min[k],
                        self.t_start_max[k]+1
                    )
                ]
            )
            var2idx.update(dict(zip(
                [
                    r_label+self.label+'_u_'+str(k)+'_'+str(t)
                    for k in range(self.n_cycles)
                    for t in range(
                        self.t_start_min[k],
                        self.t_start_max[k]+1
                    )
                ],
                v_idx
            )))

        # II.
        # Add constraints.

        # exactly one start_up for each cycle
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_start_up_'+str(k)
                for k in range(self.n_cycles)
            ],
            senses=['E' for k in range(self.n_cycles)],
            rhs=[1 for k in range(self.n_cycles)],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_u_'+str(k)+'_'+str(t)]
                        for t in range(
                            self.t_start_min[k],
                            self.t_start_max[k]+1
                        )
                    ],
                    val=[
                        1
                        for t in range(
                            self.t_start_min[k],
                            self.t_start_max[k]+1
                        )
                    ]
                )
                for k in range(self.n_cycles)
            ]
        )
        ctr2idx.update(dict(zip(
            [
                r_label+self.label+'_start_up_'+str(k)
                for k in range(self.n_cycles)
            ],
            c_idx
        )))

        # net power
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_net_power_'+str(t)
                for t in time_window
            ],
            lin_expr=[
                cplex.SparsePair(
                    ind=[var2idx[r_label+self.label+'_pwr_'+str(t)]] + [
                        var2idx[r_label+self.label+'_u_'+str(k)+'_'+str(t-d)]
                        for k, c in enumerate(self.cycles)
                        for d in range(self.durations[k])
                        if (
                            (t-d >= self.t_start_min[k])
                            and (t-d <= self.t_start_max[k])
                        )

                    ],
                    val=[1] + [
                        - c[d]
                        for k, c in enumerate(self.cycles)
                        for d in range(self.durations[k])
                        if (
                            (t-d >= self.t_start_min[k])
                            and (t-d <= self.t_start_max[k])
                        )
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [
                r_label+self.label+'_net_power_'+str(t)
                for t in time_window
            ],
            c_idx
        )))

        # cycle k+1 cannot start before end of cycle k
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_cycle_start_'+str(k)
                for k in range(1, self.n_cycles)
            ],
            senses=[
                'G'
                for k in range(1, self.n_cycles)
            ],
            rhs=[
                self.durations[k-1]
                for k in range(1, self.n_cycles)
            ],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_u_'+str(k-1)+'_'+str(t)]
                        for t in range(
                            self.t_start_min[k-1],
                            self.t_start_max[k-1]+1
                        )
                    ] + [
                        var2idx[r_label+self.label+'_u_'+str(k)+'_'+str(t)]
                        for t in range(
                            self.t_start_min[k],
                            self.t_start_max[k]+1
                        )
                    ],
                    val=[
                        - t
                        for t in range(
                            self.t_start_min[k-1],
                            self.t_start_max[k-1]+1
                        )
                    ] + [
                        t
                        for t in range(
                            self.t_start_min[k],
                            self.t_start_max[k]+1
                        )
                    ]
                )
                for k in range(1, self.n_cycles)
            ]
        )
        ctr2idx.update(dict(zip(
            [
                r_label+self.label+'_cycle_start_'+str(k)
                for k in range(1, self.n_cycles)
            ],
            c_idx
        )))

        # Done.

        return


class CurtailableLoad(Device):
    """
    Curtailable Load.

    """

    def __init__(
        self,
        label='',
        load=[],
        binary=True
    ):
        """
        Class constructor.

        """

        Device.__init__(self, label=label)

        #
        self.load = load
        self.binary = binary

    def update_model(
        self,
        m,
        var2idx={},
        ctr2idx={},
        time_window={},
        delta_t=1,
        r_label='',
        binaries=True
    ):
        """
        Add self to household model.

        """

        # I.
        # Add variables.
        # Load can be negative (ie generation), so a lower bound is specified
        v_idx = m.variables.add(
            names=[r_label+self.label+'_pwr_'+str(t) for t in time_window],
            lb=[-cplex.infinity for t in time_window],
            columns=[
                cplex.SparsePair(
                    ind=[ctr2idx[r_label+'link_netLoad_'+str(t)]],
                    val=[1]
                )
                for t in time_window
            ]
        )
        var2idx.update(dict(zip(
            [r_label+self.label+'_pwr_'+str(t) for t in time_window],
            v_idx
        )))

        # on-off
        if self.binary and binaries:
            # binary control
            v_idx = m.variables.add(
                names=[r_label+self.label+'_u_'+str(t) for t in time_window],
                types=['B' for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_u_'+str(t) for t in time_window],
                v_idx
            )))
        else:
            # continuous control
            v_idx = m.variables.add(
                names=[r_label+self.label+'_u_'+str(t) for t in time_window],
                lb=[0 for t in time_window],
                ub=[1 for t in time_window]
            )
            var2idx.update(dict(zip(
                [r_label+self.label+'_u_'+str(t) for t in time_window],
                v_idx
            )))

        # II.
        # Add constraints

        # curtailment constraint
        c_idx = m.linear_constraints.add(
            names=[
                r_label+self.label+'_curtail_'+str(t)
                for t in time_window
            ],
            senses=['E' for t in time_window],
            lin_expr=[
                cplex.SparsePair(
                    ind=[
                        var2idx[r_label+self.label+'_pwr_'+str(t)],
                        var2idx[r_label+self.label+'_u_'+str(t)]
                    ],
                    val=[
                        1,
                        -1 * self.load[t]
                    ]
                )
                for t in time_window
            ]
        )
        ctr2idx.update(dict(zip(
            [self.label+'_curtail_'+str(t) for t in time_window],
            c_idx
        )))


def generate_devices(
    n_hh,
    time_window,
    load_norm,
    pv_norm,
    temperature,
    own_rates,
    d_param=None,
    seed=None
):
    """
    Generate a set of devices for each household.

    Parameters
    ----------
    n_hh : integer
        Number of households: n_hh sets of devices will be generated
    time_window : int array
        Time indices, assumed to be [0, 1, ..., T-1] with T the length
        of the time-horizon
    native_load : float array
        Native load for each household
        native_load[i] is a T-dimensional array,
    native_pv_load : float array
        Same as native_load, except it gives the PV production for each house.
        A PV profile is given for each house, even though all may not have PV.
    native_price : float array
        Native price (eg TOU rates) for each house.
        native_price[i] is the price vector for house number i
    temperature : float array
        Outside temperature for each house.
    own_rates : dictionnary of ownership rates for devices.

    """
    # set random seed
    if seed is not None:
        np.random.seed(seed)

    # list of devices
    # devices[h] is the set of devices for household h
    devices = []
    # length of the time-horizon
    T = len(time_window)
    # number of (full) days in the time-horizon
    n_day = int(T / 24)

    # device parameters, default values
    if d_param is None:
        d_param = {
            'dw_cycle_length': 2,
            'dw_cycle': np.array([1, 1]),
            'cw_cycle_length': 2,
            'cw_cycle': np.array([1, 1]),
            'cd_cycle_length': 3,
            'cd_cycle': np.array([1, 1, 1]),
            'ev_pwr_min': 1.1,
            'ev_pwr_max': 7.7,
            'ev_energy_min': 10.,
            'ev_energy_max': 10.,
            'heat_pwr_min': 0.,
            'heat_pwr_max': 10.,
            'heat_eta': 1.,
            'heat_c': 3.,
            'heat_mu': 0.2,
            'heat_temp_init': 20.,
            'heat_temp_min': 18.,
            'heat_temp_max': 22.,
            'bat_soc_min': 0.,
            'bat_soc_max': 13.5,
            'bat_soc_init': 0.,
            'bat_pwr_min': 0.,
            'bat_pwr_max': 5.,
            'bat_effcy': 0.95,
            'bat_half_life': 693149
        }

    #####################################
    #   I. Households parameters
    #####################################
    hh_seeds = np.random.randint(
        low=0,
        high=2**16,
        size=n_hh
    )

    for i_hh in range(n_hh):

        # set numpy random seed
        np.random.seed(hh_seeds[i_hh])

        # Household sclaing factor
        # between 0.5 and 1.5
        hh_scale = np.random.uniform(
            low=0.5,
            high=1.5
        )

        # list of that household's devices
        dev = []

        #####################################
        #   II. Generate devices
        #####################################
        renew = (np.random.rand() < own_rates['pv'])

        # II.1 - Native loads
        # All uncontrollable loads are aggregated into one 'native' load
        eps = np.random.randn(T)  # white noise
        native_load = np.maximum(
            0,
            hh_scale*(load_norm + 0.05*eps)
        )
        d = FixedLoad(
            label='load_'+str(i_hh),
            fixed_load=native_load
        )
        dev.append(d)

        # II.2 - Curtailable loads
        # Curtailable PV generation
        if renew:
            eps = np.random.rand(T)
            pv_prod = hh_scale * pv_norm * eps

            d = CurtailableLoad(
                label='PV_'+str(i_hh),
                load=-pv_prod,
                binary=True
            )
            dev.append(d)

        # II.3 - Uninterruptible loads
        # One cycle per day
        # Dishwasher
        if np.random.rand() < own_rates['dishwasher']:
            cycle_length = 2
            cycle = np.ones(cycle_length)
            for day in range(n_day):
                d = ShiftableLoad(
                    label='shift_dw_'+str(i_hh)+'_'+str(day),
                    t_start_min=[0+24*day],
                    t_start_max=[0+24*(day+1)-1-cycle_length],
                    cycles=[cycle]
                )
                dev.append(d)
        # Clothes washer
        clothes_washer = False
        if np.random.rand() < own_rates['clothes_washer']:
            clothes_washer = True
            cycle_length = 2
            cycle = np.ones(cycle_length)
            for day in range(n_day):
                d = ShiftableLoad(
                    label='shift_cw_'+str(i_hh)+'_'+str(day),
                    t_start_min=[0+24*day],
                    t_start_max=[0+24*(day+1)-1-cycle_length],
                    cycles=[cycle]
                )
                dev.append(d)
        # Clothes dryer
        # only households with clothes washer have a clothes dryer
        if own_rates['clothes_washer'] > 0:
            p_cd = own_rates['clothes_dryer']/own_rates['clothes_washer']
        else:
            p_cd = 0
        if (
            clothes_washer
            and np.random.rand() < p_cd
        ):
            cycle_length = 3
            cycle = np.ones(cycle_length)
            for day in range(n_day):
                d = ShiftableLoad(
                    label='shift_cd_'+str(i_hh)+'_'+str(day),
                    t_start_min=[0+24*day],
                    t_start_max=[0+24*(day+1)-1-cycle_length],
                    cycles=[cycle]
                )
                dev.append(d)

        # II.4 - Deferrrable loads
        # Electric vehicle
        if renew:

            # charging and discharging rates are for Tesla
            # with NEMA 14-50 charger
            # minimum charging power is set at ~40% of max charging power
            # enery requirements are 10kW.h for each day
            # charging hours are 8pm-5am
            ev_pwr_min = np.zeros(T)
            ev_pwr_max = np.zeros(T)
            # here we assume that the time horizon starts at 5am
            ev_pwr_min[
                [
                    t
                    for t in time_window
                    if ((t % 24 < 24) and (t % 24 >= 14))
                ]
            ] = d_param['ev_pwr_min']
            ev_pwr_max[
                [
                    t
                    for t in time_window
                    if ((t % 24 < 24) and (t % 24 >= 14))
                ]
            ] = d_param['ev_pwr_max']

            d = DeferrableLoad(
                label='EV_'+str(i_hh),
                pwr_min=ev_pwr_min,
                pwr_max=ev_pwr_max,
                energy_min=d_param['ev_energy_min'],
                energy_max=d_param['ev_energy_max']
            )
            dev.append(d)

        # II.5 - Thermal loads
        # Thermostat
        if np.random.rand() < own_rates['heating']:

            eps = np.random.randn(T)
            d = ThermalLoad(
                label='heat_'+str(i_hh),
                temp_min=d_param['heat_temp_min']*np.ones(T),
                temp_max=d_param['heat_temp_max']*np.ones(T),
                temp_ext=temperature+0.5*eps,
                temp_init=d_param['heat_temp_init'],
                pwr_th_min=d_param['heat_pwr_min'],
                pwr_th_max=d_param['heat_pwr_max'],
                heat_cpty=d_param['heat_c'],
                th_eff=d_param['heat_eta'],
                cond_coeff=d_param['heat_mu']
            )
            dev.append(d)

        # II.6 - Energy storage
        # Home battery
        if renew:
            d = Battery(
                label='bat_'+str(i_hh),
                pwr_chg_min=d_param['bat_pwr_min'],
                pwr_dis_min=d_param['bat_pwr_min'],
                pwr_chg_max=d_param['bat_pwr_max'],
                pwr_dis_max=d_param['bat_pwr_max'],
                soc_min=d_param['bat_soc_min'],
                soc_max=d_param['bat_soc_max'],
                soc_init=d_param['bat_soc_init'],
                eff_chg=d_param['bat_effcy'],
                eff_dis=d_param['bat_effcy'],
                half_life=d_param['bat_half_life']
            )
            dev.append(d)

        devices.append(dev)

    return devices


if __name__ == '__main__':
    0
