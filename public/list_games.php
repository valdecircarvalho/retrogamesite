<!DOCTYPE html>
<html>
<head>
    <title>Jogos Atari 2600</title>
    <style>
        .game-container {
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        .game-img {
            max-width: 100px;
            max-height: 100px;
            border: 1px solid #ccc;
            margin-right: 20px;
        }
        .game-info {
            display: flex;
            flex-direction: column;
        }
        .game-info h3 {
            margin: 0;
        }
    </style>
</head>
<body>

<?php
$host = "10.170.0.179";
$user = "root";
$password = "root_mysql_retrogamesite";
$dbname = "teste_db";

$conn = new mysqli($host, $user, $password, $dbname);

if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}

$sql = "SELECT * FROM games";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "<div class='game-container'>";
        echo "<img src='" . $row["gameScreenshot1"] . "' alt='" . $row["gameNome"] . "' class='game-img'>";
        echo "<div class='game-info'>";
        echo "<h3>" . $row["gameNome"] . "</h3>";
        echo "</div>";
        echo "</div>";
    }
} else {
    echo "0 resultados encontrados";
}

$conn->close();
?>

</body>
</html>
