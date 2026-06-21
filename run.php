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

<body>
    <div>
        <span>Year <input id="year" maxlength="4" size="4"/></span>
		<select id="paper">
			<!-- <option value="1">Paper 1</option> -->
			<option value="2">Paper 2</option>
		</select>
        <select id="action">
            <option value="parse">Parse</option>
	    <option value="html">Convert To HTML</option>
	    <option value="compile">Compile</option>
	    <option value="topic">Classify Topic</option>
        </select>
        <button onclick="act()">Action!</button>
    </div>

    <div id="debug-message"></div>

    <script>
        async function act() {
            const year = $("#year").val()
            const paper = $("#paper").val()
            const action = $("#action").val()

            let data = {
                'year': year,
                'paper': paper,
                'action': action
            }

            let headers = {
                "Content-Type": "application/json"
            }

            res = await fetch("runner.php", {
                method: "POST",
                headers: headers,
                body: JSON.stringify(data)
            })

	    text = await res.text();
	    $("#debug-message").html(text.replace("\n", "<br/>"))
        }
    </script>
</body>
</html>
