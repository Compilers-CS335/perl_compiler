sub add {
    my @list = @_;
    $size = @list;
    local $sum;
    for($i=0; $i<$size; $i=$i+1){
        $sum = $sum + $list[$i];
    }
    return $sum;
}

print "Enter the numbers to be added:-\n";
$a = 1;
$b = ();
$ans = add($a, $b);
print $a." + ".$b." = ".$ans."\n";
$a = (1<2);
$ans = ($a == 1);
print $ans."\n";
$a = 'avikalp';
print $a."\n";
$b =1;
$a,$b = (1,2);
print $a." ".$b." \n";
print ($a, $b);
print '-'x80;
print "\n";
print ($a);
