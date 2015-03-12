#demonstrating local and private variables and subroutines

$var = 4;
print $var, "\n";
&hello;
print $var, "\n";

# subroutines
sub hello {
     local $var = 10;
     print $var, "\n";
     &gogo; # calling subroutine gogo
     print $var, "\n";
}
sub gogo {
	my $increment_amount = 2;
    $var += $increment_amount;
}