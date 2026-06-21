<?php
    $data = json_decode(trim(file_get_contents("php://input")), true);

    $year = $data['year'];
    $paper = $data['paper'];
    $action = $data['action'];

    $paperID = "paper-$paper/$year";
    if ($action == 'parse') {
        $pdf_path = "raw/paper-$paper/$year.pdf";
        $output_path = "artifact/$paperID";
	$res = system("./parse $paperID 1>&2 &");
	$res .= "Work in progress...";
    } else if ($action == 'compile') {
        $res = system("./compile $year 2>&1 &");
    } else if ($action == 'diagram') {
        
    } else if ($action == 'html') {
	$res = system("python3 ask_gemini.py $paperID statement");
    } else if ($action == 'topic') {
        $res = system("python3 ask_gemini.py $paperID topic");
    }
    
    echo "<pre>$res</pre>";
