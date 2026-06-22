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

			let promises = []
			promises.push(loadQuestionJson(paper, year))
			promises.push(loadAnswerJson(paper, year))
			Promise.all(promises).then(async function() {
				const container = $("#question-container");
				container.html("");
				let label = 1;
				for (const qid in questions[year]) {
					const statement = questions[year][qid]
					const answer = answers[year][qid]
					await appendQuestion(container, label, null, statement, answer);
					label += 1;
				}
				$(".question-label").on('click', function(e) {
					toggleAnswer($(e.currentTarget))
				})
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
