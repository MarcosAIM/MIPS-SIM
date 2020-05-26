addi $t2, $s3, 16
addi $t1, $s3, 8
nop
nop
nop
sub $t2, $t2, $t1
nop
nop
nop #need 3 stalls
beq $t2, $t1, -5#jump 5 instructions back from the the next instruction
nop# need one stall
j 11 #jump 11 forward from the the next instruction to or
nop
add $s1, $s3, $t1
add $s1, $s3, $t1
add $s1, $s3, $t1
nop
nop
nop
and $t1, $s1, $t1
nop
nop
nop
or  $t2, $t2, $t1
nop
nop
nop
mul $t5, $t2, $t1