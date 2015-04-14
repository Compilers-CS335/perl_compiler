#!/usr/local/bin/perl
 
$a = 10;

# while loop execution
while( $a < 20 )
{
  
   
   print "temp";
   #next;
   $a = $a + 1;
}

# # until loop execution
# until( $a > 10 ){
#    print "Value of a: $a\n";
#    $a = $a + 1;
# }

# # # for loop execution
# for( $a = 10; $a < 20; $a = $a + 1 ){
#     print "value of a: $a\n";
# }

# $a = 0;
# $b = 0;

# # # outer while loop
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

# # #demostrating next
# while( $a < 20 ){
#    if( $a == 15)
#    {
#        # skip the iteration.
#        $a = $a + 1;
#        next;
#    }
#    print "value of a: $a\n";
#    $a = $a + 1;
# }

# # #demonstrating last
# 	while( $a < 20 ){
# 	   if( $a == 15)
# 	   {
# 	       # terminate the loop.
# 	       $a = $a + 1;
# 	       last;
# 	   }
# 	   print "value of a: $a\n";
# 	   $a = $a + 1;
# 	}