<?php
session_start();

header('Content-Type: application/json');

$parameters = array('text' => $_POST['text'], 'language' => $_POST['language']);
// echo json_encode($parameters);

$url = 'localhost:2000/oom';
$content = json_encode($parameters);

$curl = curl_init($url);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HTTPHEADER,
        array("Content-type: application/json"));
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, $content);

$json_response = curl_exec($curl);

$status = curl_getinfo($curl, CURLINFO_HTTP_CODE);

if ( $status != 200 ) {
	$_SESSION['status'] = $status;
	$_SESSION['error'] = $json_response;
	header('Location: error');
	die();
}

curl_close($curl);

$decoded_json = json_decode($json_response, true);
$entities = $decoded_json['entities'];
$zip_uri = $decoded_json['zip-uri'];

$_SESSION['text'] = $_POST['text'];
$_SESSION['language'] = $_POST['language'];
$_SESSION['entities'] = $entities;
$_SESSION['zip-uri'] = $zip_uri;

header('Location: result');
?>