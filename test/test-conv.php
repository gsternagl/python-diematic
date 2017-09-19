<?php

$foo=22.2;
echo "Temp=", $foo, "\n";

$new=min(max(intval(2*$foo)*5,100),300);
echo "Temp conv=", $new, "\n";

$foo=null;
$new=min(max(intval(2*$foo)*5,100),300);
echo "Temp conv=", $new, "\n";


?>
