|bgd|

.. |bgd| image:: https://github.com/pro-well-plan/opensource_apps/raw/master/resources/pwp-bgd.gif


Temperature during Circulating
==============================

.. autofunction:: pwptemp.calc_temp

.. autofunction:: pwptemp.temperature_behavior

Example
-------

.. code-block:: python

    >>> import pwptemp as pt
    >>> import well_profile as wp

    >>> trajectory = wp.load('trajectory1.xlsx', equidistant=True)      # using well_profile to load a trajectory

    >>> casings = [{'od': 12, 'id': 11, 'depth': 1200},       # creating 3 casings with respective parameters
    >>>            {'od': 10, 'id': 9, 'depth': 1500},       # diameter [in] and depth [m]
    >>>            {'od': 8, 'id': 7, 'depth': 2400}]

    >>> well = pt.calc_temp(trajectory,     # calculate the well temperature distribution using pwptemp
    >>>                     casings,
    >>>                     set_inputs={'water_depth': 0,       # water depth [m]
    >>>                                 'temp_inlet': 20,       # inlet fluid temperature [°C]
    >>>                                 'time': 10}             # circulation time [h]
    >>>                     operation='circulating',

    >>> pt.plot_distribution(well).show()

|temp_drill|

|temp_behavior|

.. |temp_drill| image:: /figures/temp_profile_circ.png
                    :scale: 85%

.. |temp_behavior| image:: /figures/temp_behavior_circ.png
                    :scale: 85%

The table below shows the available inputs that can be set when using the parameter *set_inputs*

+------------------+------------------+
|       Name       |      Units       |
+==================+==================+
|        time      | h                |
+------------------+------------------+
|    temp_inlet    | °C               |
+------------------+------------------+
|   temp_surface   | °C               |
+------------------+------------------+
|   water_depth    | in               |
+------------------+------------------+
|     pipe_id      | in               |
+------------------+------------------+
|     pipe_od      | in               |
+------------------+------------------+
|     riser_id     | in               |
+------------------+------------------+
|     riser_od     | in               |
+------------------+------------------+
| fm_diam          | in               |
+------------------+------------------+
| flowrate         | m3/min           |
+------------------+------------------+
| Thermal Conductivities------------- |
+------------------+------------------+
| tc_fluid         |  W / (m °C)      |
+------------------+------------------+
| tc_csg           | W / (m °C)       |
+------------------+------------------+
| tc_cem           | W / (m °C)       |
+------------------+------------------+
| tc_pipe          | W / (m °C)       |
+------------------+------------------+
| tc_fm            | W / (m °C)       |
+------------------+------------------+
| tc_riser         | W / (m °C)       |
+------------------+------------------+
| tc_seawater      | W / (m °C)       |
+------------------+------------------+
| Specific Heat Capacities----------- |
+------------------+------------------+
| shc_fluid        | J / (kg °C)      |
+------------------+------------------+
| shc_csg          | J / (kg °C)      |
+------------------+------------------+
| shc_cem          | J / (kg °C)      |
+------------------+------------------+
| shc_pipe         | J / (kg °C)      |
+------------------+------------------+
| shc_riser        | J / (kg °C)      |
+------------------+------------------+
| shc_seawater     | J / (kg °C)      |
+------------------+------------------+
| shc_fm           | J / (kg °C)      |
+------------------+------------------+
| Densities-------------------------- |
+------------------+------------------+
| rho_fluid        | sg               |
+------------------+------------------+
| rho_pipe         | sg               |
+------------------+------------------+
| rho_csg          | sg               |
+------------------+------------------+
| rho_riser        | sg               |
+------------------+------------------+
| rho_fm           | sg               |
+------------------+------------------+
| rho_seawater     | sg               |
+------------------+------------------+
| rho_cem          | sg               |
+------------------+------------------+
| Others----------------------------- |
+------------------+------------------+
| th_grad_fm       | °C/m             |
+------------------+------------------+
| th_grad_seawater | °C/m             |
+------------------+------------------+
| hole_diam        | m                |
+------------------+------------------+
| rpm              | rev. per min.    |
+------------------+------------------+
| tbit             | kN*m             |
+------------------+------------------+
| wob              | kN               |
+------------------+------------------+
| rop              | m/h              |
+------------------+------------------+
| an               | in^2             |
+------------------+------------------+
| bit_n            | 0 to 1           |
+------------------+------------------+
| dp_e             | 0 to 1           |
+------------------+------------------+
| thao_o           | Pa               |
+------------------+------------------+
| beta             | Pa               |
+------------------+------------------+
| alpha            | 1/°C             |
+------------------+------------------+
| k                | Pa*s^n           |
+------------------+------------------+
| n                | dimensionless    |
+------------------+------------------+
| visc             | cP               |
+------------------+------------------+


Web Application
---------------

There is also the web-app based on pwptemp:

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/op7ZYzlYNn4" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>