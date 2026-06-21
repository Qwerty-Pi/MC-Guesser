<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DSE Mathematics Compulsory Part Practice Paper</title>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>
    <link rel="stylesheet" href="index.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
	<div id="selector">
		DSE Mathematics 
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
			<!-- <option value="1">Paper 1</option> -->
			<option value="2">Paper 2</option>
		</select>
		<button onclick="loadPaper()">Load</button>
	</div>
	<div></div>
	<div id="content">

	</div>
	<script>
		function sleep(ms) {
			return new Promise(resolve => setTimeout(resolve, ms));
		}

		function loadPaper() {
			let year = document.getElementById("year").value
			let paper = document.getElementById("paper").value
			fetch(`artifact/paper-${paper}/${year}/questions.json`, {method: "GET", type: "json"})
			.then((res) => res.json())
			.then(async (data) => {
				const e = document.getElementById("content");
				e.innerHTML = "";
				let question = 1;
				for (const datum of data) {
					e.innerHTML += "<div>" + question + ". " + datum + "</div>";
					question += 1;
				}
				await MathJax.typesetPromise();
			})
		}

		const urlParams = new URLSearchParams(window.location.search);
		const year = urlParams.get('year');
		if (year) {
			document.getElementById("year").value = year;
			loadPaper();
		}
		// too slow...
		// document.getElementById("year").addEventListener('change', function() {
		// 	loadPaper();
		// })
		// document.getElementById("paper").addEventListener('change', function() {
		// 	loadPaper();
		// })
		// loadPaper();
	</script>
</body>
</html>
