%nprocshared=20
%mem=5GB
#p hf/6-31g* opt=(verytight,gdiis) freq IOP(2/16=3) 

Gaussian input prepared by ASE

0 2
C                 2.1797000000        0.3125000000       -0.5781000000
C                 0.9307000000       -0.2492000000        0.0127000000
C                -0.2498000000       -0.0146000000       -0.5772000000
C                -1.4258305639       -0.0658591351        0.3527483770
C                -0.4492396278       -0.7357154546       -1.8781229785
H                 2.7824000000       -0.4991000000       -1.0572000000
H                 2.8065000000        0.6546000000        0.2846000000
H                 1.0056000000       -0.8579000000        0.9188000000
H                -1.4460150462       -1.1240669874        0.7187476637
H                -1.3289416290        0.6232018724        1.2015797632
H                -2.3735907831        0.0784542792       -0.1896137763
H                 0.5217970690       -0.9162460023       -2.3961391797
H                -1.0970680062       -0.1744772947       -2.5738492322
H                -0.8852075439       -1.7268306224       -1.5912418180



