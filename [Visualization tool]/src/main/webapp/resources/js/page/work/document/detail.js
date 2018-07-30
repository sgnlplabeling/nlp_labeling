var webFontURLs;
var dispatcher1;
var dispatcher2;

$(function () { 
	bindbratInit(); 
	fn_bratView();

	var recordSeq = $("#lastRecordSeq").val();
	
	if (recordSeq != '' && typeof recordSeq !='undefined') {
		fn_LastBratView(recordSeq);
	}
	
	var $divs = $('#brat_viewer1_scroll, #brat_viewer2_scroll');
	var sync = function(e){
	    var $other = $divs.not(this).off('scroll'), other = $other.get(0);
	    var percentage = this.scrollTop / (this.scrollHeight - this.offsetHeight);
	    other.scrollTop = percentage * (other.scrollHeight - other.offsetHeight);
	   // setTimeout( function(){ $other.on('scroll', sync ); },0);
	}
	$divs.on('scroll', sync);

});

function bindbratInit() {
	var bratLocation = '/resources/lib/brat';
	dispatcher1 = new Dispatcher();
	dispatcher2 = new Dispatcher();
	webFontURLs = [];
}

function fn_LastBratView(recordSeq) {

	var colId = $("#colId").val();
	var docId = $("#docId").val();
	var groupName = $("#groupName").val();
	
	$("#brat-loading2").show();
	$("#lastRecordSeq").val(recordSeq);

	var regDate = $("#history_"+recordSeq).text();
	$("#lastBratRegDate").text(regDate);
	
	$.ajax({
		url: "/labeling/bratView.do",
		type: "POST",
		data: {"colId":colId,"groupName":groupName, "docId":docId, "recordSeq" : recordSeq},
		success: function (data) {
		    var visualizer = new Visualizer(dispatcher2, 'brat_viewer2', webFontURLs);
		    
			var collData = {};	
			collData.entity_types = data.collData.entities;
			collData.relation_types = data.collData.relations;
			dispatcher2.post('collectionLoaded', [collData]);
			
			var docData = {};
			docData.text = data.docData.text;
			
			docData.entities = data.docData.entities;
			docData.relations = data.docData.relations;
			dispatcher2.post('requestRenderData', [docData]); 
			
			setTimeout("fn_compareLoc();" , 700);
			setTimeout("$('#brat-loading2').hide()" , 500);
		}
    });
	
}

function fn_restore() {
	alert('준비중입니다.');
}

function fn_bratView() {
	$("#brat-loading1").show();
	
	$.ajax({
		url: "/labeling/bratView.do",
		type: "POST",
		data: $("#docInfo").serialize(),
		success: function (data) {
		    var visualizer = new Visualizer(dispatcher1, 'brat_viewer1', webFontURLs);
		    
			var collData = {};	
			collData.entity_types = data.collData.entities;
			collData.relation_types = data.collData.relations;
			dispatcher1.post('collectionLoaded', [collData]);
			
			var docData = {};
			docData.text = data.docData.text;
			
			docData.entities = data.docData.entities;
			docData.relations = data.docData.relations;
			dispatcher1.post('requestRenderData', [docData]); 

			setTimeout("$('#brat-loading1').hide()" , 500);
		}
    });
}

function fn_compareLoc() {
	$("rect").removeAttr("stroke");
	$("rect").removeAttr("stroke-width");
	
	$.ajax({
		url: "/work/document/compareLoc.do",
		type: "POST",
		data: $("#docInfo").serialize(),
		success: function (data) {
			var list = data.list;
			if (list.length > 0) {
				for (var i=0; i<list.length; i++) {
					$("rect[id*='"+list[i].annId+"']").attr("stroke","red");
					$("rect[id*='"+list[i].annId+"']").attr("stroke-width","3");
				}
			}
		}
    });
	
}