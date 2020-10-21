$(function () {
	$('[data-toggle="tooltip"]').tooltip();
	setTimeout(function () {
		$(".flash-msg").remove();
	}, 2000);
});
