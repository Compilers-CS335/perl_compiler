sub add {
    print $b." ".$c."\n";
    $a = $b + $c;
    return $a;
}

sub Lin {
    sub Sub{
        $a = $b-$c;
        return $a;
    }
    local $b,local $c;
    $b = 10;
    $c = 2;
    $d = add();
    print $d."\n";
    $d = Sub();
    print $d."\n";
}

Lin();
