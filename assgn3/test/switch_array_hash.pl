#!/usr/local/bin/perl

use Switch;

$var = 10;

print $var;


# %hash = ('key1' => 10, 'key2' => 20);

switch($var){
   case (10)           { print "number 100\n"; }
   case (12)          { print "string a"; }
   # case [1..10,42]   { print "number in list" }
   # case (\@array)    { print "number in list" }
   # case (\%hash)     { print "entry in hash" }
   else              { print "previous case not true"; }
}