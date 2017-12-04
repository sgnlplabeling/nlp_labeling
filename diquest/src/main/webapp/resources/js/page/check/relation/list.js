
var webFontURLs;
var dispatcher;
var bratWin = [];
var bratWinLength;
var keywordLoc;
var keywordnum;

$(function () { 
	bindEntityTree("syntactic");
	bindEntityTree("causation");
	
	bindbratInit();
	bindAccrodianList();
});

function bindbratInit() {
	var bratLocation = '/resources/lib/brat';
	dispatcher = new Dispatcher();
	
	webFontURLs = [];
}

function bindEntityTree(groupName){
	var relationTree = $('#'+groupName+'_tree_list');
	
	relationTree.jstree({
		'plugins': ["themes", "html_data", "sort", "ui", "checkbox","types"] ,
		'checkbox': {
            'keep_selected_style': false
		} ,
		'types': {
            'default': {
                'icon': '/resources/images/common/tag_blue.png'
            }
        },
	});
	
	relationTree.on("ready.jstree", function() {
		relationTree.jstree('open_all');
	});
	
	relationTree.on('changed.jstree', function (e, data) {
		fn_getKeyword('start');
		fn_getKeyword('end');
		
		var i, j, r = [];
		
		if (data.selected.length == 0) {
			 $('#relation').val("");
		}
		
        for (i = 0, j = data.selected.length; i < j; i++) {
            r.push(data.instance.get_path(data.selected[i],'/'));
            $('#relation').val(r.join(', '));
        }
	});
	
}

function bindAccrodianList() {
	$('.accordion_onoff').click(function(){
		if(!$(this).closest('li').hasClass('on')){
			$(this).closest('.label_accordion').find('.cont_gray').slideUp('fast');
			$(this).closest('.label_accordion').find('li').removeClass('on');
			$(this).closest('.label_accordion').find('.btn_label_onoff').attr('title','펼치기');
			$(this).closest('li').addClass('on');
			$(this).next('.cont_gray').slideDown('fast');
			$(this).attr('title','');
			
			groupName = $(this).closest('li').attr('id');
			$("#groupName").val(groupName);
			
			$("#keywordList").html('');
			$("#labelingList").html('');
			$("#unLabelingList").html('');
			
			fn_getKeyword('start');
			fn_getKeyword('end');
		};
		return false;
	});
}

function fn_getKeyword(type) {
	var groupName = $("#groupName").val();
	var relation = getRelation(groupName);
	
	var searchTerm = "";
	
	if (type =='start') {
		searchTerm = $("#keywordInput1").val();
		$("#keywordList1").html("");
		$("#keywordListCount1").text('0');
		
	} else if (type == 'end') {
		searchTerm = $("#keywordInput2").val();
		$("#keywordList2").html("");
		$("#keywordListCount2").text('0');
    }
	
	if (relation != '' && typeof relation != 'undefined') {
		var url ='/check/relation/keywordList.do?_format=json';
		url += '&type='+type;
		url += '&groupName='+encodeURI(groupName);
		url += '&relation='+encodeURI(relation);
		
		if (searchTerm) {
			url += '&searchTerm='+encodeURI(searchTerm);
		}
		
		$.ajax({
			url: url,
			success: function (data) {
			    if (type =='start') {
			    	
				    var template =  $.templates("#tmpl_keyword1");
				    var html = template.render(data);
				    $("#keywordList1").html(html);
				    $("#keywordListCount1").text(data.keywordListCount);
				    
			    } else if (type == 'end') {
			    	
				    var template =  $.templates("#tmpl_keyword2");
				    var html = template.render(data);
				    $("#keywordList2").html(html);
				    $("#keywordListCount2").text(data.keywordListCount);
				    
			    }
				
			}
	    });
	}
	
}

function fn_LabelingDoc() {
	var groupName = $("#groupName").val();
	var keyword1 = $("#keyword1").val();
	var keyword2 = $("#keyword2").val();
	var relation = getRelation(groupName);
	
	var url ='/check/relation/docList.do?_format=json';
	url += '&groupName='+encodeURI(groupName);
	url += '&relation='+encodeURI(relation);
	if (keyword1) {
		url += '&startPoint='+encodeURI(keyword1);
	}
	if (keyword2) {
		url += '&endPoint='+encodeURI(keyword2);
	}
	
	$.ajax({
		url: url,
		success: function (data) {
		    var template =  $.templates("#tmpl_labelingDoc");
		    var html = template.render(data);
		    $("#labelingList").html(html);
		    $("#labelingListCount").text(data.labelingListCount);
		    
		    template =  $.templates("#tmpl_unLabelingDoc");
		    html = template.render(data);
		    $("#unLabelingList").html(html);
		    $("#unlabelingListCount").text(data.unlabelingListCount);
		}
    });
}

function fn_search() {
	var relation = $("#relation").val();
	if (relation == '' || typeof relation == 'undefined') {
		alert('관계를 선택해주세요.');
		return;
	} 
	
	var keyword1 = $("#keywordInput1").val();
	var keyword2 = $("#keywordInput2").val();

	if ((keyword1+keyword2).length<1) {
		alert('키워드를 입력해주세요.');
		return;
	}
	$("#keyword1").val(keyword1);
	$("#keyword2").val(keyword2);
	
	fn_LabelingDoc();
}

function fn_bratView(id){
	$("#brat-loading").show();
	var groupName = $("#groupName").val();
	
	$.ajax({
		url: "/labeling/bratView.do",
		type: "POST",
		data: {"docId":id, "groupName":groupName} ,
		success: function (data) {
			keywordnum = 0;
		    var visualizer = new Visualizer(dispatcher, 'brat_viewer1', webFontURLs);
		    
			var collData = {};	
			collData.entity_types = data.collData.entities;
			collData.relation_types = data.collData.relations;
			dispatcher.post('collectionLoaded', [collData]);
			
			var docData = {};
			docData.text = data.docData.text;
			
			docData.entities = data.docData.entities;
			docData.relations = data.docData.relations;
			dispatcher.post('requestRenderData', [docData]); 
			
			setTimeout("$('#brat-loading').hide()" , 500);
			$("#docSubject").text(""+$("#doc_"+id).text()+".txt");
			
			$("#docId").val(id);
			$("#docGroupName").val(groupName);
			
			setTimeout("fn_keyowrdLoc();",1000);
		}
    });
}


function fn_keyowrdLoc() {
	var keyword1 = $("#keyword1").val();
	var keyword2 = $("#keyword2").val();
	var keywords = [];
	
	if (keyword1 != '' && typeof keyword1 != 'undefined') {
		keywords.push(keyword1);
	}
	if (keyword2 != '' && typeof keyword2 != 'undefined') {
		keywords.push(keyword2);
	}	
	
	$("#keywords").val(keywords);
	
	$.ajax({
		url: "/labeling/keyowrdLoc.do",
		type: "POST",
		data: $("#docInfo").serialize(),
		success: function (data) {
			keywordLoc = data.keywordLoc;
			
			for (var i=0; i<keywordLoc.length; i++) {
				$("rect[id*='"+keywordLoc[i]+"']").attr("stroke","red");
				$("rect[id*='"+keywordLoc[i]+"']").attr("stroke-width","3");
			}
			fn_keywordScroll(keywordnum);
		}
    });
}

function fn_keywordScroll(num) {
	var offset = $("tspan[id*='"+keywordLoc[num]+"']").attr("y");
	$("#brat_scroll").animate({scrollTop : offset-150}, 400);

	$("#btn_keywordPrev").css("visibility","hidden");
	$("#btn_keywordNext").css("visibility","hidden");
	
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

function fn_bratDetailView() {
	var docId = $("#docId").val();
	
	if (docId) {
		$.ajax({
			url: "/check/entity/bratDetailView.do",
			type: "POST",
			data: $("#docInfo").serialize(),
			success: function (data) {
				var bratPath = "/brat/#/"+data.map.filePath;

				bratWin[bratWinLength] = window.open(bratPath);
				$("#docType").val("readOnly");
				$("#winNum").val(bratWinLength);
				
				bratWinLength++;
			}
		});
	} else {
		alert("문서를 선택해주세요");
	}
}

function setKeyword1(content) {
	$("#keyword1").val(content);
	fn_LabelingDoc();
}

function setKeyword2(content) {
	$("#keyword2").val(content);
	fn_LabelingDoc();	
}

function getRelation(groupName){
	var relation = "";
	if ($("#"+groupName+"_tree_list").find("li").length > 0) {
		relation = $("#"+groupName+"_tree_list").jstree(true).get_selected();
	}
	return relation;
}

function fn_fileDelete(winNum,path) {
	if (!bratWin[winNum].closed) {
		return;
	}
	
	var idx = path.lastIndexOf("/");
	path = path.substring(0,idx);
	
	$.ajax({
		url: "/labeling/deleteFile.do",
		type: "POST",
		data: {"path":path},
		success: function (data) {
		}
	});
}

function bratSetting(winNum,docType){
	if (!bratWin[winNum].closed) {
		$("#winNum").val(winNum);
		$("#docType").val(docType);
	}
}

function bratWindowClose(docInfo) {
	setTimeout("fn_fileDelete('"+docInfo.winNum+"','"+docInfo.path+"')",200);
	setTimeout("bratSetting('"+docInfo.winNum+"','"+docInfo.docType+"')",200);
}

function windowClose() {  
	for (var i=0;i<bratWin.length;i++) {
        if (bratWin[i] && !bratWin[i].closed) {
        	bratWin[i].bratClose();
        }
    }
} 

window.onunload = windowClose;