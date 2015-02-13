#!/usr/local/bin/perl

sub TeamNumber{
	print "This is team 24\n";
}

#The Test file is here. Yippie

$number = 99;

if($number == 99){
	print "Ninety Nine\n";
}
elsif($number == 10){
	print "Ten\n";
}
else{
	print "Neither 10 nor 99\n";
}



for($a=10; $a<15; $a +=1){
	printf "Value of a = $a\n";
}


while($a > 10){
	print "Value of a in while loop = $a\n";
	$a = $a -1;
}


do{
	print "Value of a in do-while loop = $a\n";
	$a = $a + 1;
}while($a < 15);


@names = ("Avikalp", "Nikhil", "Deepak");
print "$names[0] is chaapu\n";
print "$names[1] is bakait\n";

TeamNumber();

$a = (-1 + 0 * 1)/10;
$a = 10 % 2;
$a = 10 * 2;
$a = 10 * 2; #End

