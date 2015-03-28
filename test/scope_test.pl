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
$a = <>;
$b = <>;
$ans = add($a, $b);
print chomp($a)." + ".chomp($b)." = ".$ans."\n";
