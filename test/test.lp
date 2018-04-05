\ENCODING=ISO-8859-1
\Problem name: 

Minimize
 obj: - 0.00109 y_0 - 0.00241 y_1 - 0.00423 y_2 - 0.0044 y_3 - 0.00444 y_4
      - 0.00443 y_5
Subject To
 link_total_0:             - y_0 + HH_0_netLoad_0 + HH_1_netLoad_0  = 0
 link_total_1:             - y_1 + HH_0_netLoad_1 + HH_1_netLoad_1  = 0
 link_total_2:             - y_2 + HH_0_netLoad_2 + HH_1_netLoad_2  = 0
 link_total_3:             - y_3 + HH_0_netLoad_3 + HH_1_netLoad_3  = 0
 link_total_4:             - y_4 + HH_0_netLoad_4 + HH_1_netLoad_4  = 0
 link_total_5:             - y_5 + HH_0_netLoad_5 + HH_1_netLoad_5  = 0
 HH_0_link_netLoad_0:      - HH_0_netLoad_0 + HH_0_heat_0_pwr_0
                            = -0.974922000595956
 HH_0_link_netLoad_1:      - HH_0_netLoad_1 + HH_0_heat_0_pwr_1
                            = -1.06702635621054
 HH_0_link_netLoad_2:      - HH_0_netLoad_2 + HH_0_heat_0_pwr_2
                            = -0.849669522472428
 HH_0_link_netLoad_3:      - HH_0_netLoad_3 + HH_0_heat_0_pwr_3
                            = -0.934085554341131
 HH_0_link_netLoad_4:      - HH_0_netLoad_4 + HH_0_heat_0_pwr_4
                            = -0.99290100202548
 HH_0_link_netLoad_5:      - HH_0_netLoad_5 + HH_0_heat_0_pwr_5
                            = -0.983330522706273
 HH_0_heat_0_pwr_th_min_0: - HH_0_heat_0_pwr_0 <= 0
 HH_0_heat_0_pwr_th_min_1: - HH_0_heat_0_pwr_1 <= 0
 HH_0_heat_0_pwr_th_min_2: - HH_0_heat_0_pwr_2 <= 0
 HH_0_heat_0_pwr_th_min_3: - HH_0_heat_0_pwr_3 <= 0
 HH_0_heat_0_pwr_th_min_4: - HH_0_heat_0_pwr_4 <= 0
 HH_0_heat_0_pwr_th_min_5: - HH_0_heat_0_pwr_5 <= 0
 HH_0_heat_0_pwr_th_max_0: HH_0_heat_0_pwr_0 - 10 HH_0_heat_0_on_ind_0 <= 0
 HH_0_heat_0_pwr_th_max_1: HH_0_heat_0_pwr_1 - 10 HH_0_heat_0_on_ind_1 <= 0
 HH_0_heat_0_pwr_th_max_2: HH_0_heat_0_pwr_2 - 10 HH_0_heat_0_on_ind_2 <= 0
 HH_0_heat_0_pwr_th_max_3: HH_0_heat_0_pwr_3 - 10 HH_0_heat_0_on_ind_3 <= 0
 HH_0_heat_0_pwr_th_max_4: HH_0_heat_0_pwr_4 - 10 HH_0_heat_0_on_ind_4 <= 0
 HH_0_heat_0_pwr_th_max_5: HH_0_heat_0_pwr_5 - 10 HH_0_heat_0_on_ind_5 <= 0
 HH_0_heat_0_temp_exch_0:  - 0.333333333333333 HH_0_heat_0_pwr_0
                           + HH_0_heat_0_temp_0  = 18.718410514909
 HH_0_heat_0_temp_exch_1:  - 0.333333333333333 HH_0_heat_0_pwr_1
                           - 0.933333333333333 HH_0_heat_0_temp_0
                           + HH_0_heat_0_temp_1  = -0.0123355597304053
 HH_0_heat_0_temp_exch_2:  - 0.333333333333333 HH_0_heat_0_pwr_2
                           - 0.933333333333333 HH_0_heat_0_temp_1
                           + HH_0_heat_0_temp_2  = -0.00105519973294177
 HH_0_heat_0_temp_exch_3:  - 0.333333333333333 HH_0_heat_0_pwr_3
                           - 0.933333333333333 HH_0_heat_0_temp_2
                           + HH_0_heat_0_temp_3  = -0.030666598265395
 HH_0_heat_0_temp_exch_4:  - 0.333333333333333 HH_0_heat_0_pwr_4
                           - 0.933333333333333 HH_0_heat_0_temp_3
                           + HH_0_heat_0_temp_4  = 0.0279335156395533
 HH_0_heat_0_temp_exch_5:  - 0.333333333333333 HH_0_heat_0_pwr_5
                           - 0.933333333333333 HH_0_heat_0_temp_4
                           + HH_0_heat_0_temp_5  = 0.0517196695834366
 HH_1_link_netLoad_0:      - HH_1_netLoad_0 + HH_1_heat_1_pwr_0
                            = -0.435771557346978
 HH_1_link_netLoad_1:      - HH_1_netLoad_1 + HH_1_heat_1_pwr_1
                            = -0.421160695475579
 HH_1_link_netLoad_2:      - HH_1_netLoad_2 + HH_1_heat_1_pwr_2
                            = -0.429502742265489
 HH_1_link_netLoad_3:      - HH_1_netLoad_3 + HH_1_heat_1_pwr_3
                            = -0.466673282906142
 HH_1_link_netLoad_4:      - HH_1_netLoad_4 + HH_1_heat_1_pwr_4
                            = -0.391061982766354
 HH_1_link_netLoad_5:      - HH_1_netLoad_5 + HH_1_heat_1_pwr_5
                            = -0.408776303556802
 HH_1_heat_1_pwr_th_min_0: - HH_1_heat_1_pwr_0 <= 0
 HH_1_heat_1_pwr_th_min_1: - HH_1_heat_1_pwr_1 <= 0
 HH_1_heat_1_pwr_th_min_2: - HH_1_heat_1_pwr_2 <= 0
 HH_1_heat_1_pwr_th_min_3: - HH_1_heat_1_pwr_3 <= 0
 HH_1_heat_1_pwr_th_min_4: - HH_1_heat_1_pwr_4 <= 0
 HH_1_heat_1_pwr_th_min_5: - HH_1_heat_1_pwr_5 <= 0
 HH_1_heat_1_pwr_th_max_0: HH_1_heat_1_pwr_0 - 10 HH_1_heat_1_on_ind_0 <= 0
 HH_1_heat_1_pwr_th_max_1: HH_1_heat_1_pwr_1 - 10 HH_1_heat_1_on_ind_1 <= 0
 HH_1_heat_1_pwr_th_max_2: HH_1_heat_1_pwr_2 - 10 HH_1_heat_1_on_ind_2 <= 0
 HH_1_heat_1_pwr_th_max_3: HH_1_heat_1_pwr_3 - 10 HH_1_heat_1_on_ind_3 <= 0
 HH_1_heat_1_pwr_th_max_4: HH_1_heat_1_pwr_4 - 10 HH_1_heat_1_on_ind_4 <= 0
 HH_1_heat_1_pwr_th_max_5: HH_1_heat_1_pwr_5 - 10 HH_1_heat_1_on_ind_5 <= 0
 HH_1_heat_1_temp_exch_0:  - 0.333333333333333 HH_1_heat_1_pwr_0
                           + HH_1_heat_1_temp_0  = 18.6758159565388
 HH_1_heat_1_temp_exch_1:  - 0.333333333333333 HH_1_heat_1_pwr_1
                           - 0.933333333333333 HH_1_heat_1_temp_0
                           + HH_1_heat_1_temp_1  = 0.0694333753866848
 HH_1_heat_1_temp_exch_2:  - 0.333333333333333 HH_1_heat_1_pwr_2
                           - 0.933333333333333 HH_1_heat_1_temp_1
                           + HH_1_heat_1_temp_2  = 0.00909289196829795
 HH_1_heat_1_temp_exch_3:  - 0.333333333333333 HH_1_heat_1_pwr_3
                           - 0.933333333333333 HH_1_heat_1_temp_2
                           + HH_1_heat_1_temp_3  = 0.0428683734650406
 HH_1_heat_1_temp_exch_4:  - 0.333333333333333 HH_1_heat_1_pwr_4
                           - 0.933333333333333 HH_1_heat_1_temp_3
                           + HH_1_heat_1_temp_4  = -0.0269756889579014
 HH_1_heat_1_temp_exch_5:  - 0.333333333333333 HH_1_heat_1_pwr_5
                           - 0.933333333333333 HH_1_heat_1_temp_4
                           + HH_1_heat_1_temp_5  = -0.0272122957146189
Bounds
 0 <= y_0 <= 15
 0 <= y_1 <= 15
 0 <= y_2 <= 15
 0 <= y_3 <= 15
 0 <= y_4 <= 15
 0 <= y_5 <= 15
 0 <= HH_0_netLoad_0 <= 10
 0 <= HH_0_netLoad_1 <= 10
 0 <= HH_0_netLoad_2 <= 10
 0 <= HH_0_netLoad_3 <= 10
 0 <= HH_0_netLoad_4 <= 10
 0 <= HH_0_netLoad_5 <= 10
 18 <= HH_0_heat_0_temp_0 <= 22
 18 <= HH_0_heat_0_temp_1 <= 22
 18 <= HH_0_heat_0_temp_2 <= 22
 18 <= HH_0_heat_0_temp_3 <= 22
 18 <= HH_0_heat_0_temp_4 <= 22
 18 <= HH_0_heat_0_temp_5 <= 22
 0 <= HH_0_heat_0_on_ind_0 <= 1
 0 <= HH_0_heat_0_on_ind_1 <= 1
 0 <= HH_0_heat_0_on_ind_2 <= 1
 0 <= HH_0_heat_0_on_ind_3 <= 1
 0 <= HH_0_heat_0_on_ind_4 <= 1
 0 <= HH_0_heat_0_on_ind_5 <= 1
 0 <= HH_1_netLoad_0 <= 10
 0 <= HH_1_netLoad_1 <= 10
 0 <= HH_1_netLoad_2 <= 10
 0 <= HH_1_netLoad_3 <= 10
 0 <= HH_1_netLoad_4 <= 10
 0 <= HH_1_netLoad_5 <= 10
 18 <= HH_1_heat_1_temp_0 <= 22
 18 <= HH_1_heat_1_temp_1 <= 22
 18 <= HH_1_heat_1_temp_2 <= 22
 18 <= HH_1_heat_1_temp_3 <= 22
 18 <= HH_1_heat_1_temp_4 <= 22
 18 <= HH_1_heat_1_temp_5 <= 22
 0 <= HH_1_heat_1_on_ind_0 <= 1
 0 <= HH_1_heat_1_on_ind_1 <= 1
 0 <= HH_1_heat_1_on_ind_2 <= 1
 0 <= HH_1_heat_1_on_ind_3 <= 1
 0 <= HH_1_heat_1_on_ind_4 <= 1
 0 <= HH_1_heat_1_on_ind_5 <= 1
Binaries
 HH_0_heat_0_on_ind_0  HH_0_heat_0_on_ind_1  HH_0_heat_0_on_ind_2 
 HH_0_heat_0_on_ind_3  HH_0_heat_0_on_ind_4  HH_0_heat_0_on_ind_5 
 HH_1_heat_1_on_ind_0  HH_1_heat_1_on_ind_1  HH_1_heat_1_on_ind_2 
 HH_1_heat_1_on_ind_3  HH_1_heat_1_on_ind_4  HH_1_heat_1_on_ind_5 
End
