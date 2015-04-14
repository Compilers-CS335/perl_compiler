#demonstrating local and private variables and subroutines

$var = 4;
print $var;
hello();
print $var;

# subroutines
sub hello {
     local $var = 10;
     print $var;
     gogo(10, 20); # calling subroutine gogo
     print $var;
}
sub gogo {
	my $increment_amount = 2;
    $var += $increment_amount;
}
