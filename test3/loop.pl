#!/usr/local/bin/perl
 
$a = 10;

# while loop execution
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

# until loop execution
#until( $a > 10 ){
#   printf "Value of a: $a\n";
#   $a = $a + 1;
#}

# for loop execution
# for( $a = 10; ; $a = $a + 1 ){
#     print ("value of a: $a\n";
# }

# $a = 0;
# $b = 0;

# outer while loop
# while($a < 3){
#    $b = 0;
#    # inner while loop
#    while( $b < 3 ){
#       print "value of a = $a, b = $b\n";
#       $b = $b + 1;
#    }
#    $a = $a + 1;
#    print "Value of a = $a\n\n";
# }

#demostrating next
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

# #demonstrating last
while( $a < 20 ){
   if( $a == 15)
   {
       # terminate the loop.
       $a +=1;
       last;
   }
   print "value of a: $a\n";
   $a = $a + 1;
}