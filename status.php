<head>
    <meta charset="UTF-8">
    <title>DSE Mathematics Compulsory Part Practice Paper</title>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>
    <script src="https://code.jquery.com/jquery-4.0.0.js" integrity="sha256-9fsHeVnKBvqh3FB2HYu7g2xseAZ5MlN6Kz/qnkASV8U=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="index.css">
    <link rel="stylesheet" href="style.css">
</head>

<?php
    $actions = ["Raw", "Parse", "Translate", "Statement", "Figure", "Proofread", "Topic"];

    function query($year, $action) {
        if ($action == "Raw") {
            return file_exists("raw/paper-2/$year.pdf");
        }
        if ($action == "Parse") {
            return file_exists("artifact/paper-2/$year/merged.txt");
        }
        if ($action == "Translate") {
            return file_exists("artifact/paper-2/$year/questions.html");
        }
        if ($action == "Statement") {
            return file_exists("artifact/paper-2/$year/questions.json");
        }
        if ($action == "Figure") {
            return file_exists("artifact/paper-2/$year/figures.json");
        }
        if ($action == "Proofread") {
            $json = json_decode(file_get_contents("./proofread.json"));
            return in_array($year, $json);
	}
	if ($action == "Topic") {
	    return file_exists("artifact/paper-2/$year/topics.json");
	}
        return 1;
    }
?>

<style>

.status-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    width: 640px;
}

.status-grid > span {
    padding: 3px 0;
    display: flex;
    justify-content: center;
    align-items: center;
    border: solid 1px var(--text-color);
}

.status-cell-done {
    background-color: #00FF0060;
}

.status-cell-not-done {
    background-color: #FF000060;
}
</style>

<div class="status-grid">
    <span>Paper 2</span>
    <?php
        foreach ($actions as $action) {
            echo "<span>$action</span>";
        }

        $years = array_merge(range(1980, 2011), ["2012-PP", "2012-CP"], range(2012, 2025));

        foreach ($years as $year) {
            echo "<span>$year</span>";
            foreach ($actions as $action) {
                $is_done = query($year, $action);
                echo '<span class="' . ($is_done ? "status-cell-done" : "status-cell-not-done") . '">' . ($is_done ? 1 : 0) . '</span>';
            }
        }
    ?>
</div>
