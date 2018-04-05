# Data format
Price, demand and production data are given for the Ontario province
* `date`: Day of the year, in the format `DD/MM/YYYY`
* `hour`: hour of the day. Hour `0` corresponds to `0am-1am`, and hour `24` corresponds to `23pm-24pm`.

Only the first day of year 2016 is included in sample files. Full hourly data can be obtained here: http://www.ieso.ca/en/power-data/data-directory.

## load.csv

* `OntDemand`: Hourly electricity demand of Ontario, in `MW.h`.

## price.csv
Prices are indicated in `$/kW.h`. Please note that market prices are typically given in `$/MW.h` on the IESO website.

* `HOEP`: Hourly Ontario Energy Price
* `TOU`: Hourly Time-of-Use rates (winter)

## prod.csv

All outputs are in `MW.h`. Since these are hourly energy productions, the values also correspond to average power output over the hour.

* `NUCLEAR`: Nuclear power plants
* `GAS`: Gas-fired power plants
* `HYDRO`: Hydroelectric power plants
* `WIND`: Wind power plants
* `SOLAR`: Solar photovoltaic power plants
* `BIOFUEL`: Biofuel power plants
