<?php
    $data = json_decode(trim(file_get_contents("php://input")), true);

    if (!isset($data['year']) || !$data['year'] || !isset($data['q']))
        die(0);

    $year = $data['year'];
    $q = $data['q'];
    $topic = $data['topic'];

    $file = "artifact/paper-2/$year/topics.json";
    $content = json_decode(file_get_contents($file));
    $content[$q] = $topic;
    file_put_contents($file, json_encode($content));

    var_dump("Success");