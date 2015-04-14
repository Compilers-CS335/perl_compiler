$a = 10;
my $i = 1;
sub giveTwenty{
	print $a;
	if ($i<=20) {
		$i+=5;
		$ret = giveTwenty();
	}
	else{
		$a+=1;
		print $a;
		print "\n";
		$ret = "aavik";
	}
	
	return $ret;
}


$b= giveTwenty();
print $b;
