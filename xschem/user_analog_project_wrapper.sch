v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 3240 -470 0 0 {name=p1 lab=vdd
}
C {devices/iopin.sym} 3240 -440 0 0 {name=p2 lab=vss
}
C {devices/ipin.sym} 3260 -410 0 0 {name=p9 lab=wb_clk_i}
C {devices/ipin.sym} 3260 -380 0 0 {name=p10 lab=wb_rst_i}
C {devices/ipin.sym} 3260 -350 0 0 {name=p11 lab=wbs_stb_i}
C {devices/ipin.sym} 3260 -320 0 0 {name=p12 lab=wbs_cyc_i}
C {devices/ipin.sym} 3260 -290 0 0 {name=p13 lab=wbs_we_i}
C {devices/ipin.sym} 3260 -260 0 0 {name=p14 lab=wbs_sel_i[3:0]}
C {devices/ipin.sym} 3260 -230 0 0 {name=p15 lab=wbs_dat_i[31:0]}
C {devices/ipin.sym} 3260 -200 0 0 {name=p16 lab=wbs_adr_i[31:0]}
C {devices/opin.sym} 3240 -170 0 0 {name=p17 lab=wbs_ack_o}
C {devices/opin.sym} 3240 -140 0 0 {name=p18 lab=wbs_dat_o[31:0]}
C {devices/ipin.sym} 3250 -100 0 0 {name=p19 lab=la_data_in[63:0]}
C {devices/opin.sym} 3240 -70 0 0 {name=p20 lab=la_data_out[63:0]}
C {devices/ipin.sym} 3250 10 0 0 {name=p21 lab=io_in[38:0]}
C {devices/ipin.sym} 3250 100 0 0 {name=p23 lab=user_clock2}
C {devices/opin.sym} 3230 40 0 0 {name=p24 lab=io_out[38:0]}
C {devices/opin.sym} 3230 70 0 0 {name=p25 lab=io_oeb[38:0]}
C {devices/opin.sym} 3230 130 0 0 {name=p32 lab=user_irq[2:0]}
C {devices/ipin.sym} 3250 -40 0 0 {name=p28 lab=la_oenb[63:0]}
C {sar_10b/sar/sar.sym} 4150 -30 0 0 {name=xsar
}
C {lab_wire.sym} 3970 -120 3 0 {name=l1 sig_type=std_logic lab=vss
}
C {lab_wire.sym} 3970 -300 3 1 {name=l3 sig_type=std_logic lab=vdd
}
C {lab_wire.sym} 3870 -260 0 0 {name=l5 sig_type=std_logic lab=dac_inp

}
C {lab_wire.sym} 3870 -160 0 0 {name=l6 sig_type=std_logic lab=dac_inm
}
C {lab_wire.sym} 4100 -120 3 0 {name=l7 sig_type=std_logic lab=wb_clk_i
}
C {lab_wire.sym} 4130 -120 3 0 {name=l8 sig_type=std_logic lab=la_data_in[51] 
}
C {lab_wire.sym} 4150 -120 3 0 {name=l9 sig_type=std_logic lab=wb_rst_i
}
C {lab_wire.sym} 4100 -300 3 1 {name=l10 sig_type=std_logic lab=la_data_in[52] 
}
C {lab_wire.sym} 4200 -180 0 1 {name=l11 sig_type=std_logic lab=la_data_out[53]
}
C {lab_wire.sym} 4200 -210 0 1 {name=l12 sig_type=std_logic lab=la_data_out[54:63]
}
C {xschem/symbols/sky130_primitives/cap_mim_m3_2.sym} 3480 -240 0 0 {name=C1[447:0] model=cap_mim_m3_2 W=30 L=30 MF=1 spiceprefix=X
}
C {lab_wire.sym} 3480 -270 3 1 {name=l32 sig_type=std_logic lab=vdd
}
C {lab_wire.sym} 3480 -210 3 0 {name=l33 sig_type=std_logic lab=vss
}
