$a = 10;
my $i = 1;
sub giveTwenty{
	sub take{
		# return 3;
		print "HELLO";
	}
	print $a;
	if ($i<=20) {
		$i+=5;
		# $ret = take();
		print "qwerty";
	}
	else{
		$a+=1;
		print $a;
		print "\n";

		$ret = 2;
	}
	
	# return $ret;
}


giveTwenty();
print $b;
