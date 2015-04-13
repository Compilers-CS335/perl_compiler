#!/usr/local/bin/perl

use Switch;

$name = "Sarah";
$x = 5;

# IF/ELSE STATEMENTS
if ($x > 10) {
	print '$x is greater than 10!';
} else {
	print "$x is not greater than 10!";
	print "";
}
$a = 10;
while( $a < 20 )
{
   print "Value of a: $a\\n";
   next;
   $a = $a + 1;
}
$a=10;
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

$var = 10;
switch($var){
   case (10)           { print "number 100\n"; }
   case (12)          { print "string a"; }
   else              { print "previous case not true"; }
}
