var webFontURLs;
var dispatcher1;
var dispatcher2;

var keywordLoc;
var keywordnum;

$(function () { 
	bindbratInit(); 
	fn_bratView();

	var recordSeq = $("#lastRecordSeq").val();
	
	if (recordSeq != '' && typeof recordSeq !='undefined') {
		fn_LastBratView(recordSeq);
	}
	
	keywordnum = 0;
	
	//the long scrolling elements
	var left = $("#brat_scroll1");
	var right = $("#brat_scroll2");
	
	//get the height offset
	var height = parseInt(right.css("height"));
	
	//assign the handling
	var hold = false;
	var window_scroll = true;
	left.add(right)
	    .mouseenter(function() { window_scroll = false; })
	    .mouseleave(function() { window_scroll = true; });
	      
	//handle monitoring how the window is changing
	window.onmousewheel = function(e) {
//		if (window_scroll) return true;
//		
//		//check the current scroll position
//		var percent = left.scrollTop() / (left[0].scrollHeight - height);
//		var going_up = e.wheelDeltaX < 0;
//		var at_bottom = percent == 1
//		
//		return going_up == at_bottom;
	};
	
	//syncs to long scrolling elements
	var locked = false;
	var sync_to = function(source, target) {
		//make sure not to capture multiple scroll events
		//since one call is setting the scroll of the other
		//element it causes them to both fire
		if (locked) { return locked = false, true; }
		locked = true;
		
		var x = source.offset().left - $(window).scrollLeft();
		var y = source.offset().top - $(window).scrollTop();
		var h = $('.cont_tit2').eq(0).height();
		var brow = document.elementFromPoint(x + 5, y + h);
		var tag = $(brow);
		var browId;
		
		if(tag.prop("tagName") == "rect") {
			browId = tag.attr("id");
		} else if(tag.prop("tagName") == "text"){
			browId = "BROW_" + tag.html();
		}
		var offset = target.find("div>*>*>rect[id^='"+browId+"']").attr("y");
		target[0].scrollTop = offset;
		
		//make sure they move relative to each other
//		var percent = source.scrollTop() / (source[0].scrollHeight - height);
//		var top = (target[0].scrollHeight - height) * percent;
//		target[0].scrollTop = top;
	};
	

	//cause the two elements to sync
	left.scroll(function(e) { sync_to.call(e, left, right); });
	right.scroll(function(e) { sync_to.call(e, right, left); });

});


function bindbratInit() {
	var bratLocation = contextPath+'/resources/lib/brat';
	dispatcher1 = new Dispatcher();
	dispatcher2 = new Dispatcher();
	webFontURLs = [];
}

function fn_LastBratView(recordSeq) {

	$("#brat-loading2").show();
	$("#brat-loading1").show();
	
	var docId = $("#docId").val();
	var groupName = $("#groupName").val();
	var recordId = $("#recordId").val();
	
	$("#lastRecordSeq").val(recordSeq);

	var regDate = $("#history_"+recordSeq).text();
	$("#lastBratRegDate").text(regDate);
	
	$.ajax({
		url: contextPath+"/labeling/bratView.do",
		type: "POST",
		data: {"recordId":recordId, "groupName":groupName, "docId":docId, "recordSeq" : recordSeq},
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
			
			setTimeout("fn_compareLoc();" , 500);
			setTimeout("$('#brat-loading2').hide();$('#brat-loading1').hide();" , 500);
		}
    });
	
}

function fn_restore() {
	var lastBratRegDate = $("#lastBratRegDate").val();
	if (confirm('정말 복원하시겠습니까?')) {
		alert('준비중입니다.');
	}
}

function fn_bratView() {
	$("#brat-loading1").show();
	
	$.ajax({
		url: contextPath+"/labeling/bratView.do",
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

	// 2017.12.01 number40 라인color 초기화
	$.each($(".background").children(), function(index) {
		var rest = index % 2;
		$(".background").children().eq(index).attr("class", "background"+rest);
	});
	
	$.ajax({
		url:contextPath+ "/work/document/compareLoc.do",
		type: "POST",
		data: $("#docInfo").serialize(),
		success: function (data) {
			keywordLoc = new Array();
			keywordnum = 0;
			
			var list = data.compareList1;
			if (list.length > 0) {
				for (var i=0; i<list.length; i++) {
					$("#brat_viewer1>*>*>rect[id='H_"+list[i].annId+"']").attr("stroke","red");
					$("#brat_viewer1>*>*>rect[id='H_"+list[i].annId+"']").attr("stroke-width","3");
					
					// 2017.12.01 number40 해당하는 라인 색깔 변경
					var line;
					$("#brat_viewer1>*>*>*>tspan[id*='"+list[i].annId+"']").each(function(){
						var ids = $(this).attr('id');
						var arrIds = ids.split('_');
						for (var idx=0; idx < arrIds.length; idx++) {
							if(list[i].annId == arrIds[idx]) {
								line = $(this).parent().index();
							}
						}
					});
					
					$("rect[id^='BROW_"+Number(line+1)+"_']").attr('class','backgroundHighlight');
//					$("#brat_viewer1>*>*>rect[id^='BROW_"+Number(line+1)+"_']").attr('class','backgroundHighlight');
				}
			}
			
			list = data.compareList2;
			if (list.length > 0) {
				for (var i=0; i<list.length; i++) {
					$("#brat_viewer2>*>*>rect[id='H_"+list[i].annId+"']").attr("stroke","red");
					$("#brat_viewer2>*>*>rect[id='H_"+list[i].annId+"']").attr("stroke-width","3");
					
					// 2017.12.01 number40 해당하는 라인 색깔 변경
					var line;
					$("#brat_viewer2>*>*>*>tspan[id*='"+list[i].annId+"']").each(function(){
						var ids = $(this).attr('id');
						var arrIds = ids.split('_');
						for (var idx=0; idx < arrIds.length; idx++) {
							if(list[i].annId == arrIds[idx]) {
								line = $(this).parent().index();
							}
						}
					});
					
					$("rect[id^='BROW_"+Number(line+1)+"_']").attr('class','backgroundHighlight');
//					$("#brat_viewer2>*>*>rect[id^='BROW_"+Number(line+1)+"_']").attr('class','backgroundHighlight');
				}
			}
			
			fn_keywordScroll(keywordnum);
			
		}
    });
}

function fn_keywordScroll(num) {
	$("#btn_keywordPrev").css("visibility","hidden");
	$("#btn_keywordNext").css("visibility","hidden");
	
	var bratHeight = $("#brat_viewer1").height();
	if (bratHeight <= 550) {
		return;
	}
	
	var offset = $("#brat_viewer1>*>*>rect[id='"+keywordLoc[num]+"']").attr("y");
	$("#brat_scroll1").animate({scrollTop : offset-150}, 400);
	
	if (num != 0) {
		$("#btn_keywordPrev").css("visibility","visible");
	}
	if (num != (keywordLoc.length-1)) {
		$("#btn_keywordNext").css("visibility","visible");
	}
}

function fn_keywordPrev() {
	if (keywordnum == 0) {
		alert("이동할 키워드가 없습니다.");
		return;
	}

	keywordnum--;
	fn_keywordScroll(keywordnum);
}

function fn_keywordNext() {
	if (keywordnum == (keywordLoc.length-1)) {
		alert("이동할 키워드가 없습니다.");
		return;
	}
	
	keywordnum++;
	fn_keywordScroll(keywordnum);
}
