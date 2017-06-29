<?php
session_start();

$extension = null;

if ($_SESSION['language'] == 'java') {
	$extension = '.java';
}
else {
	$extension = '.cs';
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<title>Object Oriented Modeling</title>

	<link href="css/bootstrap.min.css" rel="stylesheet">
	<link href="css/bootstrap-theme.min.css" rel="stylesheet">
	<link href="css/oomodeling.css" rel="stylesheet">
</head>

<body>
	<header>
		<div class="container">
			<div class="row row-header">
				<div class="col-xs-12 col-sm-12">
					<h1 align="center"><a href="/oomodeling">Object Oriented Modeling</a></h1>
					<div class="col-xs-12 col-sm-8 col-sm-offset-2">
						<p align="center">A smart application which transforms your text into object-oriented models. Try it out!</p>
					</div>
				</div>
			</div>
		</div>
	</header>

	<div class="container">
		<div class="row row-content">
			<div class="col-xs-12 col-sm-2">
				<p align="right"><strong>Your text:</strong></p>
			</div>

			<div class="col-xs-12 col-sm-10">
				<p>
					<?php
					echo $_SESSION['text'];
					?>
				</p>
			</div>
		</div>

		<div class="row row-content code-container">
			<div class="col-xs-12 col-sm-12">
				<!-- result code goes here -->
				<div>
					<ul id="tabslist" class="nav nav-tabs" role="tablist">
						<?php
						$first = true;

						foreach ($_SESSION['entities'] as $key => $elem) {
							if ($first == true) {
								echo '<li id="'.$key.'Tab" role="presentation" class="active"><a href="#'.$key.'" role="tab" data-toggle="tab">'.$key.$extension.'</a></li>';
								$first = false;
							}
							else {
								echo '<li id="'.$key.'Tab" role="presentation"><a href="#'.$key.'" role="tab" data-toggle="tab">'.$key.$extension.'</a></li>';
							}
						}
						?>
					</ul>

					<div id="tabscontent" class="tab-content">
						<?php
						$first = true;

						foreach ($_SESSION['entities'] as $key => $elem) {
							if ($first == true) {
								echo '<div role="tabpanel" class="tab-pane fade in active" id="'.$key.'">';
								$first = false;
							}
							else {
								echo '<div role="tabpanel" class="tab-pane fade" id="'.$key.'">';
							}
							echo '<pre class="prettyprint" style="font-size: 13pt;">'.$elem.'</pre></div>';
						}
						?>
					</div>
				</div>
			</div>
		</div>

		<div class="row row-content">
			<div class="col-xs-12">
				<a href="<?php echo $_SESSION['zip-uri'];?>" class="btn pull-right" id="downloadBtn">Download files</a>
			</div>
		</div>
	</div>

	<footer class="row-footer">
        <div class="container">
            <div class="row">
                <div class="col-xs-12">
                    <p align=center>Ștefan Gordîn, 2017</p>
                    <p align=center>Application for the "Object Oriented Modeling" Bachelor Thesis, Faculty of Computer Science Iași</p>
                </div>
            </div>
        </div>
    </footer>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
	<script src="js/oomodeling.js"></script>

</body>

</html>