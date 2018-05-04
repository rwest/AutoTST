# Coordinates for CC=C(C)C in Input Orientation (angstroms):
#   C    0.8403   -0.5907    0.0120
#   C   -0.4070   -0.1537   -0.0784
#   C    2.0984    0.1898    0.2802
#   C   -1.5430   -1.1100   -0.3571
#   C   -0.8434    1.2832    0.0761
#   H    1.0027   -1.6494   -0.1215
#   H    2.5913   -0.1804    1.1759
#   H    1.9270    1.2496    0.4127
#   H    2.8027    0.0683   -0.5393
#   H   -2.2773   -1.0841    0.4452
#   H   -1.1954   -2.1310   -0.4622
#   H   -2.0658   -0.8354   -1.2707
#   H   -1.3479    1.6236   -0.8254
#   H   -0.0265    1.9622    0.2752
#   H   -1.5593    1.3750    0.8897
conformer(
    label = 'CC=C(C)C',
    E0 = (3546.66, 'kJ/mol'),
    modes = [
        IdealGasTranslation(mass=(70.0782, 'amu')),
        NonlinearRotor(
            inertia = ([62.5929, 143.621, 196.994], 'amu*angstrom^2'),
            symmetry = 1,
        ),
        HarmonicOscillator(
            frequencies = ([117.231, 134.704, 189.224, 278.553, 313.164, 403.088, 485.653, 549.797, 803.349, 902.596, 1017.95, 1032.88, 1098.3, 1139.51, 1155.72, 1194.66, 1205.24, 1318.16, 1476.87, 1538.13, 1541.56, 1551.02, 1589.96, 1601.1, 1601.23, 1609.84, 1615.09, 1615.76, 1881.78, 3127.87, 3135.15, 3138.61, 3169.45, 3175.38, 3176.31, 3218.89, 3231.29, 3253.11, 3261.32], 'cm^-1'),
        ),
    ],
    spinMultiplicity = 1,
    opticalIsomers = 1,
)

# Coordinates for [O]O in Input Orientation (angstroms):
#   O    0.9924   -0.1641    0.0000
#   O   -0.1727    0.4322    0.0000
#   H   -0.8197   -0.2681    0.0000
conformer(
    label = '[O]O',
    E0 = (1936.47, 'kJ/mol'),
    modes = [
        IdealGasTranslation(mass=(32.9977, 'amu')),
        NonlinearRotor(
            inertia = ([0.775043, 14.5598, 15.3349], 'amu*angstrom^2'),
            symmetry = 1,
        ),
        HarmonicOscillator(frequencies=([1228.4, 1593.69, 3942.52], 'cm^-1')),
    ],
    spinMultiplicity = 2,
    opticalIsomers = 1,
)

# Coordinates for [CH2]C=C(C)C in Input Orientation (angstroms):
#   C    2.2607    0.0356   -0.4606
#   C    1.0049    0.0307    0.1374
#   C   -0.2129   -0.3493   -0.4299
#   C   -1.4841   -0.2885    0.3764
#   C   -0.3667   -0.8370   -1.8463
#   H    2.4256   -0.2703   -1.4763
#   H    3.1232    0.3548    0.0946
#   H    0.9670    0.3603    1.1638
#   H   -1.9507   -1.2695    0.4464
#   H   -1.3086    0.0692    1.3846
#   H   -2.2127    0.3719   -0.0904
#   H    0.5675   -0.8658   -2.3903
#   H   -1.0522   -0.1978   -2.3993
#   H   -0.7901   -1.8394   -1.8624
conformer(
    label = '[CH2]C=C(C)C',
    E0 = (3569.16, 'kJ/mol'),
    modes = [
        IdealGasTranslation(mass=(69.0704, 'amu')),
        NonlinearRotor(
            inertia = ([62.0095, 134.418, 190.276], 'amu*angstrom^2'),
            symmetry = 1,
        ),
        HarmonicOscillator(
            frequencies = ([55.824, 137.413, 224.402, 309.649, 342.943, 391.034, 550.411, 556.615, 757.306, 775.912, 969.647, 1034.34, 1052.27, 1064.51, 1130.49, 1141.67, 1235.38, 1321.61, 1442.84, 1531.95, 1540.44, 1562.4, 1589.42, 1598.56, 1605.33, 1620.98, 1630.08, 3118.91, 3128.18, 3157.94, 3164.69, 3212.74, 3242.66, 3259.8, 3282.43, 3365.89], 'cm^-1'),
        ),
    ],
    spinMultiplicity = 2,
    opticalIsomers = 1,
)

# Coordinates for OO in Input Orientation (angstroms):
#   O    0.5715   -0.3877    0.2666
#   O   -0.5726    0.4120    0.2246
#   H    1.1867    0.1185   -0.2495
#   H   -1.1856   -0.1428   -0.2417
conformer(
    label = 'OO',
    E0 = (1930.97, 'kJ/mol'),
    modes = [
        IdealGasTranslation(mass=(34.0055, 'amu')),
        NonlinearRotor(
            inertia = ([1.58184, 17.8015, 18.4661], 'amu*angstrom^2'),
            symmetry = 1,
        ),
        HarmonicOscillator(
            frequencies = ([391.396, 1129.99, 1466.15, 1605.09, 4017.01, 4018.89], 'cm^-1'),
        ),
    ],
    spinMultiplicity = 1,
    opticalIsomers = 1,
)

# Coordinates for TS in Input Orientation (angstroms):
#   O   -3.1136    0.1359   -0.7352
#   O   -3.9485    1.1890   -0.4758
#   C    0.2252    0.4037   -1.0803
#   C    0.9200   -0.1405   -0.0472
#   C   -0.8861    1.3423   -0.9967
#   C    0.6616    0.1623    1.4065
#   C    2.0348   -1.1228   -0.3038
#   H   -4.3466    1.3724   -1.3188
#   H    0.4836    0.0769   -2.0744
#   H   -2.0014    0.6634   -0.8902
#   H   -1.0690    1.9093   -1.8985
#   H   -0.9562    1.9563   -0.1125
#   H    1.5454    0.5965    1.8687
#   H   -0.1669    0.8389    1.5619
#   H    0.4415   -0.7554    1.9463
#   H    2.1848   -1.2988   -1.3625
#   H    2.9721   -0.7629    0.1147
#   H    1.8242   -2.0787    0.1707
conformer(
    label = 'TS',
    E0 = (5624.22, 'kJ/mol'),
    modes = [
        IdealGasTranslation(mass=(103.076, 'amu')),
        NonlinearRotor(
            inertia = ([102.297, 548.163, 575.177], 'amu*angstrom^2'),
            symmetry = 1,
        ),
        HarmonicOscillator(
            frequencies = ([18.1757, 53.4283, 61.8371, 97.9974, 164.373, 191.497, 290.477, 309.356, 370.558, 403.245, 450.994, 524.332, 576.341, 581.091, 792.729, 909.448, 1031.48, 1051.52, 1071.96, 1125, 1136.56, 1160.99, 1168.5, 1206.05, 1296.97, 1332.98, 1463.51, 1517, 1538.16, 1544.07, 1546.49, 1586, 1590.38, 1595.83, 1606.18, 1610.66, 1655.66, 3128.23, 3136.79, 3171.33, 3178.27, 3216.62, 3220.05, 3250.53, 3270.18, 3298.12, 3993.19], 'cm^-1'),
        ),
    ],
    spinMultiplicity = 2,
    opticalIsomers = 1,
    frequency = (-3357.9, 'cm^-1'),
)

#   ======= =========== =========== =========== ===============
#   Temp.   k (TST)     Tunneling   k (TST+T)   Units
#   ======= =========== =========== =========== ===============
#     300 K   1.190e-14 3.06875e+09   3.651e-05 cm^3/(mol*s)
#     400 K   2.680e-08      112090   3.004e-03 cm^3/(mol*s)
#     500 K   2.073e-04     688.181   1.427e-01 cm^3/(mol*s)
#     600 K   9.216e-02     51.9716   4.790e+00 cm^3/(mol*s)
#     800 K   2.384e+02     6.48258   1.546e+03 cm^3/(mol*s)
#    1000 K   3.253e+04     3.05179   9.928e+04 cm^3/(mol*s)
#    1500 K   3.449e+07     1.61246   5.562e+07 cm^3/(mol*s)
#    2000 K   1.523e+09     1.31236   1.999e+09 cm^3/(mol*s)
#   ======= =========== =========== =========== ===============


#   ======= ============ =========== ============ ============= =========
#   Temp.    Kc (eq)        Units     krev (TST)   krev (TST+T)   Units
#   ======= ============ =========== ============ ============= =========
#     300 K   3.273e-03              3.635e-12     1.116e-02      cm^3/(mol*s)
#     400 K   2.046e-02              1.310e-06     1.468e-01      cm^3/(mol*s)
#     500 K   6.482e-02              3.199e-03     2.201e+00      cm^3/(mol*s)
#     600 K   1.448e-01              6.365e-01     3.308e+01      cm^3/(mol*s)
#     800 K   4.176e-01              5.710e+02     3.702e+03      cm^3/(mol*s)
#    1000 K   8.158e-01              3.988e+04     1.217e+05      cm^3/(mol*s)
#    1500 K   2.070e+00              1.667e+07     2.687e+07      cm^3/(mol*s)
#    2000 K   3.331e+00              4.573e+08     6.001e+08      cm^3/(mol*s)
#   ======= ============ =========== ============ ============= =========


# krev (TST) = Arrhenius(A=(18.6381,'cm^3/(mol*s)'), n=3.16929, Ea=(118.026,'kJ/mol'), T0=(1,'K'), Tmin=(300,'K'), Tmax=(2000,'K'), comment="""Fitted to 8 data points; dA = *|/ 1.59487, dn = +|- 0.0609539, dEa = +|- 0.34183 kJ/mol""") 
# krev (TST+T) = Arrhenius(A=(2.04028e-41,'cm^3/(mol*s)'), n=15.0141, Ea=(-7.54206,'kJ/mol'), T0=(1,'K'), Tmin=(300,'K'), Tmax=(2000,'K'), comment="""Fitted to 8 data points; dA = *|/ 98365.9, dn = +|- 1.50122, dEa = +|- 8.41884 kJ/mol""") 

kinetics(
    label = 'CC=C(C)C+[O]O_[CH2]C=C(C)C+OO',
    kinetics = Arrhenius(
        A = (4.24535e-41, 'cm^3/(mol*s)'),
        n = 15.2205,
        Ea = (12.3176, 'kJ/mol'),
        T0 = (1, 'K'),
        Tmin = (303.03, 'K'),
        Tmax = (2500, 'K'),
        comment = 'Fitted to 59 data points; dA = *|/ 53.2679, dn = +|- 0.521727, dEa = +|- 2.87002 kJ/mol',
    ),
)
