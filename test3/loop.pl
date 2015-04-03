#!/usr/local/bin/perl
 
$a = 11;

# while loop execution
# while( $a < 20 ){
#    print "Value of a: $a\n";
#    $a = $a + 1;
#    if ($x == 7) {
#   print '$x is equal to 7!';
#   if($y == 9){
#     print $y;
#   }
#   else
#   {
#     print "Hello";
#   }
# }
# else{
#   if($y == 9){
#     print $y;
#   }
#   else
#   {
#     print "Hello";
#   }
# }
# }

















#dowhile loop
# do
# {
#   print "Value of a: $a\n";
#   $a = $a + 1;  
# } while($a>11);





# until loop execution
# until( $a > 10 ){
#   print "Value of a: $a\n";
#   $a = $a + 1;
# }

# for loop execution
# for( $a = 10;  $a<12 ; $a = $a + 1 ){
#     print ("value of a: $a\n");
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

$b=<>;
while( $a < 20 ){
   
       # skip the iteration.
       
      
   
   print "value of a: $a\n";
   $a = $a + "1";
   last;
   
}

# #demonstrating last
# while( $a < 20 ){
#    if( $a == 15)
#    {
#        # terminate the loop.
#        $a +=1;
#        last;
#    }
#    print "value of a: $a\n";
#    $a = $a + 1;
# }
