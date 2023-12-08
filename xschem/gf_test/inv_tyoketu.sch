v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 620 -230 620 -210 {
lab=vdd}
N 620 -50 620 -30 {
lab=vss}
N 620 -150 620 -110 {
lab=vout}
N 560 -80 580 -80 {
lab=vin}
N 560 -180 560 -80 {
lab=vin}
N 560 -180 580 -180 {
lab=vin}
N 620 -130 760 -130 {
lab=vout}
N 700 -130 700 -110 {
lab=vout}
N 480 -130 560 -130 {
lab=vin}
N 620 -50 700 -50 {
lab=vss}
N 90 -100 90 -60 {lab=GND}
N -50 -100 -50 -60 {lab=GND}
N 190 -80 190 -40 {lab=GND}
N 190 -190 190 -140 { lab=vin}
N 480 170 560 170 {
lab=vin2}
N 650 90 680 90 {
lab=vout2}
N 680 90 680 250 {
lab=vout2}
N 650 250 680 250 {
lab=vout2}
N 620 90 620 110 {
lab=vdd}
N 620 230 620 250 {
lab=vss}
N 560 90 590 90 {
lab=vin2}
N 560 90 560 250 {
lab=vin2}
N 560 250 580 250 {
lab=vin2}
N 580 250 590 250 {
lab=vin2}
N 680 170 820 170 {
lab=vout2}
N 760 170 760 190 {
lab=vout2}
N 760 250 760 290 {
lab=vss}
N 620 30 620 50 {
lab=vss}
N 620 290 620 310 {
lab=vdd}
N 130 140 130 180 {lab=GND}
N 130 30 130 80 { lab=vin2}
C {symbols/nfet_06v0.sym} 600 -80 0 0 {name=M2
L=0.70u
W=1u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_06v0
spiceprefix=X
}
C {symbols/pfet_06v0.sym} 600 -180 0 0 {name=M3
L=0.55u
W=1u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_06v0
spiceprefix=X
}
C {lab_pin.sym} 620 -230 0 0 {name=l1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 620 -30 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_pin.sym} 480 -130 0 0 {name=l3 sig_type=std_logic lab=vin
}
C {lab_pin.sym} 760 -130 0 1 {name=l4 sig_type=std_logic lab=vout}
C {devices/code_shown.sym} 360 -460 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
"}
C {devices/code_shown.sym} 360 -340 0 0 {name=NGSPICE only_toplevel=true
value="
.control
save all
tran 1n 30u
.endc
"}
C {capa.sym} 700 -80 0 0 {name=C1
m=1
value=1f
footprint=1206
device="ceramic capacitor"}
C {devices/vsource.sym} 90 -130 0 0 {name=VSS value=0
}
C {devices/gnd.sym} 90 -60 0 0 {name=l18 lab=GND}
C {devices/vsource.sym} -50 -130 0 0 {name=VDD value=6
}
C {devices/gnd.sym} -50 -60 0 0 {name=l20 lab=GND}
C {devices/vsource.sym} 190 -110 0 0 {name=VIN value="PULSE(0 6 10e-6 1e-9 1e-9 0.5e-6 1e-6)"
}
C {devices/gnd.sym} 190 -40 0 0 {name=l32 lab=GND}
C {lab_pin.sym} -50 -160 0 0 {name=l5 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 90 -160 0 0 {name=l6 sig_type=std_logic lab=vss}
C {lab_pin.sym} 190 -170 0 0 {name=l7 sig_type=std_logic lab=vin
}
C {symbols/nfet_06v0.sym} 620 270 3 0 {name=M1
L=0.70u
W=1u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_06v0
spiceprefix=X
}
C {symbols/pfet_06v0.sym} 620 70 1 0 {name=M4
L=0.55u
W=1u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_06v0
spiceprefix=X
}
C {lab_pin.sym} 480 170 0 0 {name=l10 sig_type=std_logic lab=vin2
}
C {lab_pin.sym} 620 110 2 0 {name=l12 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 620 230 2 0 {name=l13 sig_type=std_logic lab=vss}
C {lab_pin.sym} 820 170 0 1 {name=l14 sig_type=std_logic lab=vout2}
C {capa.sym} 760 220 0 0 {name=C3
m=1
value=1f
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 760 290 0 0 {name=l8 sig_type=std_logic lab=vss}
C {lab_pin.sym} 620 310 0 0 {name=l9 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 620 30 0 0 {name=l11 sig_type=std_logic lab=vss}
C {devices/vsource.sym} 130 110 0 0 {name=VIN1 value="PULSE(0 6 10e-6 1e-9 1e-9 0.5e-6 1e-6)"
}
C {devices/gnd.sym} 130 180 0 0 {name=l15 lab=GND}
C {lab_pin.sym} 130 50 0 0 {name=l16 sig_type=std_logic lab=vin2
}
