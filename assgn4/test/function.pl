$a = 10;
my $i = 1;
sub giveTwenty{
	sub take{
		print "HELLO";
	}
	print $a;
	if ($i<=20) {
		$i+=5;
		print "qwerty";
	}
	else{
		$a+=1;
		print $a;
		print "\n";

		$ret = 2;
	}
}

giveTwenty();
