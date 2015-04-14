#!/usr/local/bin/perl
 
$a = 10;

# while loop execution
while( $a < 20 )
{
    print "\nValue of a: ";
   print $a;
   #next;
   $a = $a + 1;
}

# # until loop execution
until( $a > 10 ){
   print "\nValue of a: ";
   print $a;
   $a = $a + 1;
}

# # # for loop execution
for( $a = 10; $a > -10; $a -= 1 ){
    # print "value of a: $a\n";
    print $a;
}
for( $a = 10; $a < 20; $a = $a + 1 ){
    # print "\nValue of a: ";
   print $a;
}

$a = 0;
$b = 0;

# # outer while loop
while($a < 3){
   $b = 0;
   # inner while loop
   while( $b < 3 ){
   print "\nValue of a: ";
   print $a;
    print "\nValue of b: ";
   print $b;
      $b = $b + 1;
   }
   $a = $a + 1;
    print "\nValue of a: ";
   print $a;
}

# #demostrating next
while( $a < 20 ){
   if( $a == 15)
   {
       # skip the iteration.
       $a = $a + 1;
       next;
   }
    print "\nValue of a: ";
   print $a;
   $a = $a + 1;
}

# #demonstrating last
	while( $a < 20 ){
	   if( $a == 15)
	   {
	       # terminate the loop.
	       $a = $a + 1;
	       last;
	   }
	    print "\nValue of a: ";
   print $a;
	   $a = $a + 1;
	}
