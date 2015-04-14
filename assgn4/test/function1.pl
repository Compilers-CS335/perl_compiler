$a = 10;
my $i = 1;
sub giveTwenty{
	print $a;
	if ($i<=20) {
		$i+=1;
		return giveTwenty();
	}
	else{
		$a+=1;
		print $a;
		print "\n";
		return $a;
	}
	
	# return $ret;
}


$b= giveTwenty();
print $b;