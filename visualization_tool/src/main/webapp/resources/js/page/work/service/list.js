
$(function () { 
	  $('#startDate').datepicker();
	    $('#startDate').datepicker("option", "maxDate", $("#endDate").val());
	    $('#startDate').datepicker("option", "onClose", function ( selectedDate ) {
	        $("#endDate").datepicker( "option", "minDate", selectedDate );
	    });
	 
	    $('#endDate').datepicker();
	    $('#endDate').datepicker("option", "minDate", $("#startDate").val());
	    $('#endDate').datepicker("option", "onClose", function ( selectedDate ) {
	        $("#startDate").datepicker( "option", "maxDate", selectedDate );
	    });
});


function fn_pageSizeEdit() {
	var pageSize = $("#boardtop01_right").val();
	$("#pageSize").val(pageSize);
	$("#searchForm").submit();
}
