<?php
    $_POST = json_decode(file_get_contents('php://input'), true);
    $message = $_POST["message"];
    $crash = $_POST["crash"];
    $myYear = date("d.m.Y");
    $myHour = date("H:i");
    $myFile = "canteen.txt";
    $fh = fopen($myFile, 'a') or die("can't open file");
    fwrite($fh, $myYear . " " .  $myHour);
    fwrite($fh, "\t");
    fwrite($fh, $message);
    fwrite($fh, "\t");
    fwrite($fh, $crash);
    fwrite($fh, "\n");    
    fclose($fh);
?>