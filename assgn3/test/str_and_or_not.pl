$a= 10;
$b = 12;
$c = 10;

if (($a==$b) or ($b==$c)) {
	print "Two consecutive are same\n";
}
else {
	if ($a==$b and $b==$c) {
		print "All three are same\n";
	}
	else {
		unless  (not $a == $c) {
			print "Two are same, but ";
		}
		print "no 2 consecutive are same\n";
	}
}