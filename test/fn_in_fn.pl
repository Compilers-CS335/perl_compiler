sub parent{
    my $a = 10;
    sub child {
        $a = $a+1;
        return $a;
    }
    print "\ninside and before:= ";
    print $a;
    $a = $a+$tmp;
    print "\n inside and after:= ";
    print $a;
    $b = child();
    $b = 10*$b;
    return $b;
}

sub child2{
    $a = $a+1;
    return $a;
}

$tmp = 12;
$ret = parent();
$tmp = 25;
$ret = parent();
$ret2 = child();
$ret3 = child2();
print "\$tmp wala = ";
print $ret;
print "\n and \$a wala =";
print $ret2;
print " and ";
print $ret3;
print "\n";

