addi $t2, $s3, 64
addi $t1, $s3, 4
nop
nop
addi $s0, $t2, 21
addi $s1, $t1, 6
nop
nop
addi $s2, $s0, 21
addi $s3, $s4, 6

sw $s0, 0($t2)
sw $s1, 4($t2)
sw $s2, -8($t2)
sw $s2, 8($t2)
sw $s3, 12($t2)

lw $a0, 0($t2)
lw $a1, 4($t2)
lw $a2, 8($t2)
lw $a3, 12($t2)
nop
lw $t1, 12($t2)