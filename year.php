<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Mathematics</title>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>
    <script src="https://code.jquery.com/jquery-4.0.0.js" integrity="sha256-9fsHeVnKBvqh3FB2HYu7g2xseAZ5MlN6Kz/qnkASV8U=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="index.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
	<div id="selector">
		Mathematics 
		<select id="year">
			<?php
				for ($year = 1980; $year <= 2011; $year++) {
					echo <<<EOF
					<option value="$year">$year</option>
					EOF;
				}
			?>
			<option value="2012-PP">2012-PP</option>
			<option value="2012-CP">2012-CP</option>
			<?php
				for ($year = 2012; $year <= 2025; $year++) {
					echo <<<EOF
					<option value="$year">$year</option>
					EOF;
				}
			?>
		</select>
		<select id="paper">
			<option value="2">Paper 2</option>
		</select>
		<button onclick="loadPaper()">Load</button>
	</div>
	<div id="question-container">

	</div>
	<script src="functions.js"></script>
	<script>
		function loadPaper() {
			let year = $("#year").val()
			let paper = $("#paper").val()
			fetch(`artifact/paper-${paper}/${year}/questions.json`, {method: "GET", type: "json"})
			.then((res) => res.json())
			.then(async (data) => {
				const questionContainer = $("#question-container");
				questionContainer.html("");
				let label = 1;
				let content = "";
				for (const question of data) {
					await appendQuestion(questionContainer, label, null, question);
					label += 1;
				}
				// e.html(content);
				await MathJax.typesetPromise();
			})
		}

		const urlParams = new URLSearchParams(window.location.search);
		const year = urlParams.get('year');
		if (year) {
			document.getElementById("year").value = year;
			loadPaper();
		}
	</script>
</body>
</html>
