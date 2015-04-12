#demonstrating local and private variables and subroutines

$var = 4;
print $var;

print $var;
sub gogo {
	my $increment_amount = 2;
    $var += $increment_amount;
}
# subroutines
sub hello {
     local $var = 10;
     print $var;
     gogo(); # calling subroutine gogo
     print $var;
}

hello();