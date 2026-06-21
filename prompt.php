<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DSE Mathematics Compulsory Part Practice Paper</title>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>
    <script src="https://code.jquery.com/jquery-4.0.0.js" integrity="sha256-9fsHeVnKBvqh3FB2HYu7g2xseAZ5MlN6Kz/qnkASV8U=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="index.css">
    <link rel="stylesheet" href="style.css">
</head>

<?php
    $paper = $_GET['paper'];
    $year = $_GET['year'];
    $content = file_get_contents("artifact/paper-$paper/$year/merged.txt");
    $prompt = file_get_contents("prompt.txt");

    echo "<pre>";
    echo htmlspecialchars($prompt);
    echo htmlspecialchars($content);
    echo "</pre>";