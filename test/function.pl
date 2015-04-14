$a = 10;
my $i = 1;
sub giveTwenty{
	print $a;
	if ($i<20) {
		$i+=5;
		$a+=1;
		print $a;
		print "\n";
		return $a;
	}
	else{
		return giveTwenty();
	}
}


$a = giveTwenty();
print $a;
