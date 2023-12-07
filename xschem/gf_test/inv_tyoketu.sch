v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 840 -280 840 -260 {
lab=vdd}
N 840 -100 840 -80 {
lab=vss}
N 840 -200 840 -160 {
lab=vin}
N 780 -130 800 -130 {
lab=vin}
N 780 -230 780 -130 {
lab=vin}
N 780 -230 800 -230 {
lab=vin}
N 780 -180 840 -180 {
lab=vin}
N 840 -180 980 -180 {
lab=vin}
N 920 -180 920 -160 {
lab=vin}
N 700 -180 780 -180 {
lab=vin}
N 840 -100 920 -100 {
lab=vss}
C {symbols/nfet_06v0.sym} 820 -130 0 0 {name=M2
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
C {symbols/pfet_06v0.sym} 820 -230 0 0 {name=M3
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
C {lab_pin.sym} 840 -280 0 0 {name=l1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 840 -80 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_pin.sym} 700 -180 0 0 {name=l3 sig_type=std_logic lab=vin
}
C {lab_pin.sym} 980 -180 0 1 {name=l4 sig_type=std_logic lab=vout}
C {devices/code_shown.sym} 440 -20 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
"}
C {devices/code_shown.sym} 360 -340 0 0 {name=NGSPICE only_toplevel=true
value="
VDD vdd 6 0
VSS vss 0 0
VIN vin 0 0
.control
save all
tran 1n 10u
.endc
"}
C {capa.sym} 920 -130 0 0 {name=C1
m=1
value=1f
footprint=1206
device="ceramic capacitor"}
