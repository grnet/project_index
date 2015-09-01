
$( document ).ready(function () {
	$("#txt1, #btnSelect").click(function() {
	    Select();
	});


	function Select() {
	    $("#txt2").val($("#txt1").html()).show();
	    $("#txt1").hide();

	    $("#txt2").focus()[0].select();
	}

	function Deselect() {
	    $("#txt1").html($("#txt2").val()).show();
	    $("#txt2").hide();
	}
	$("#txt2").blur(function() {
	    Deselect();
	});

	$("#btnDeselect").click(function() {
	    Deselect();
	});
});