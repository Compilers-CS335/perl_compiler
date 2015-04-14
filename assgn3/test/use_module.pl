#!/usr/local/bin/perl

use Switch;

$a = 1;
# print $a;
# if($a==1){
#     print "Equal to hai bhaiya\n";    
# }
switch($a){
    case (1)
    {
        print "You typed 1\n";
    }
    case (2) {
        print "You typed 2\n";
    }
    case (1.0)
    {
        print "You typed 1.0\n";
    }
    else {

        print "Stop typing random things\n";
    }
}
