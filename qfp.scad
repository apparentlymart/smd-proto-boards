
padct = 48;
padsperside = padct / 4;
padwidth = 0.5;
stdpadspacing = 0.8;
padarraywidth = stdpadspacing * (padsperside-1);
rowspacing = 12.23 - (stdpadspacing * 10) + padarraywidth;

function extpadlen(i) = (stdpadspacing / 2) + (padwidth / 2) + padarraywidth + (rowspacing - padarraywidth)/2 - (i + 1) * stdpadspacing;

module pad(length=1.73) {
    square([length, padwidth], center=true);
}

translate([-rowspacing / 2, 0])
for (i = [0:padsperside-1]) {
    translate([0, stdpadspacing * i - padarraywidth/2])
    pad();
} 

rotate(90)
translate([-rowspacing / 2, 0])
for (i = [0:padsperside-1]) {
    translate([0, stdpadspacing * i - padarraywidth/2])
    pad();
} 

translate([rowspacing / 2, 0])
for (i = [0:padsperside-1]) {
    
    translate([0.4-(extpadlen(i)/2), stdpadspacing * i - padarraywidth/2])
    pad(extpadlen(i));
} 

mirror([0, 1])
rotate(-90)
translate([rowspacing / 2, 0])
for (i = [0:padsperside-1]) {
    
    translate([0.4-(extpadlen(i)/2), stdpadspacing * i - padarraywidth/2])
    pad(extpadlen(i));
} 
