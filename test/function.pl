$a = 10;
my $i = 1;
sub giveTwenty{
	print $a;
	if ($i>=20) {
		$ret = giveTwenty();
	}
	else{
		$i+=5;
		$a+=1;
		print $a;
		print "\n";
		$ret = $a;
	}
	return $ret;
}


$a = giveTwenty();
print $a;
