addi $t2, $s3, 16
addi $t1, $s3, 8
sub $t2, $t2, $t1
beq $t2, $t1, -2
j 4
add $s1, $s3, $t1
add $s1, $s3, $t1
add $s1, $s3, $t1
and $t1, $s1, $t1
or  $t2, $t2, $t1
mul $t5, $t2, $t1