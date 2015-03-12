#demonstrating local and private variables and subroutines

$var = 4;
print $var;
hello(10, 20);
print $var;

# subroutines
sub hello {
	$y = @_;
     local $var = 10;
     print $var;
     gogo(); # calling subroutine gogo
     print $var;
     while( $a < 20 ){
   print "Value of a: $a\n";
   $a = $a + 1;
   if ($x == 7) {
  print '$x is equal to 7!';
  if($y == 9){
    print $y;
  }
  else
  {
    print "Hello";
  }
}
else{
  if($y == 9){
    print $y;
  }
  else
  {
    print "Hello";
  }
}
}

}
sub gogo {
	my $increment_amount = 2;
    $var += $increment_amount;
    while( $a < 20 ){
   if( $a == 15)
   {
       # skip the iteration.
       $a = $a + 1;
       next;
   }
   print "value of a: $a\n";
   $a = $a + 1;
}
while( $a < 20 ){
   if( $a == 15)
   {
       # terminate the loop.
       $a = $a + 1;
       last;
   }
   print "value of a: $a\n";
   $a = $a + 1;
}
return $y;
}