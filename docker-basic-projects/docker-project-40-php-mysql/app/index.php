<?php

$host = getenv("MYSQL_HOST") ?: "mysql";
$user = getenv("MYSQL_USER") ?: "appuser";
$password = getenv("MYSQL_PASSWORD") ?: "apppassword";
$database = getenv("MYSQL_DATABASE") ?: "appdb";

$conn = new mysqli(
    $host,
    $user,
    $password,
    $database
);

if ($conn->connect_error) {
    http_response_code(500);
    die("MySQL connection failed: " . $conn->connect_error);
}

$conn->query("
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        role VARCHAR(100) NOT NULL
    )
");

if (isset($_GET["add"])) {

    $name = "Docker User";
    $role = "DevOps Engineer";

    $stmt = $conn->prepare(
        "INSERT INTO users (name, role) VALUES (?, ?)"
    );

    $stmt->bind_param("ss", $name, $role);
    $stmt->execute();

    echo "User added successfully!<br><br>";
}

echo "<h1>PHP + MySQL Docker Application</h1>";

$result = $conn->query("SELECT * FROM users");

echo "<h2>Users</h2>";

while ($row = $result->fetch_assoc()) {

    echo "ID: " . $row["id"] .
         " | Name: " . $row["name"] .
         " | Role: " . $row["role"] .
         "<br>";
}

echo "<br>";
echo '<a href="/?add=1">Add User</a>';

$conn->close();

?>
