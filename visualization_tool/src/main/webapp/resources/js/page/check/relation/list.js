
var webFontURLs;
var dispatcher;
var bratWin = [];
var bratWinLength;
var keywordLoc;
var keywordnum;

$(function () { 
	bindEntityTree("syntactic");
	bindEntityTree("causation");
	bindEntityTree("simentic");
	bindbratInit();
	bindAccrodianList();
});

function bindbratInit() {
	var bratLocation = contextPath+'/resources/lib/brat';
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
                'icon': contextPath+'/resources/images/common/tag_blue.png'
            }
        },
	});
	
	relationTree.on("ready.jstree", function() {
		relationTree.jstree('open_all');
	});
	
	relationTree.on('changed.jstree', function (e, data) {
		var i, j, r = [];
		
		if (data.selected.length == 0) {
			fn_keywordClear();
		}
		
        for (i = 0, j = data.selected.length; i < j; i++) {
            r.push(data.instance.get_path(data.selected[i],'/'));
            $('#relation').val(r.join(', '));
        }
		fn_getKeyword('start', null);
		
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
			
			fn_keywordClear();
			fn_getKeyword('start', null);
		};
		return false;
	});
}

function fn_keywordClear() {
	$('#relation').val('');
	$("#keyword1").val('');
	$("#keyword2").val('');

    $("#keywordList1").html('');
    $("#keywordListCount1").text('0');
    
    $("#keywordList2").html('');
    $("#keywordListCount2").text('0');
}

function fn_getKeyword(type, searchTerm) {
	var groupName = $("#groupName").val();
	var relation = getRelation(groupName);
	
	if (relation != '' && typeof relation != 'undefined') {
		var url =contextPath+'/check/relation/keywordList.do?_format=json';
		url += '&type='+type;
		url += '&groupName='+encodeURI(groupName);
		url += '&relId='+encodeURI(relation);
		
		if (searchTerm) {
			url += '&searchTerm='+encodeURI(searchTerm);
		}
		
		if (type =='start') {
			
			$("#keyword-loading1").show();
			
		} else if (type =='end') {
			
			$("#keyword-loading2").show();
			
			var keyword1 = $("#keyword1").val();
			var keyword2 = $("#keyword2").val();
			
			if (keyword1) {
				url += '&startRel='+encodeURI(keyword1);
			}		
			if (keyword2) {
				url += '&endRel='+encodeURI(keyword2);
			}
		}
		
		$.ajax({
			url: url,
			success: function (data) {
			    if (type =='start') {
			    	setTimeout("$('#keyword-loading1').hide();" , 100);
				    var template =  $.templates("#tmpl_keyword1");
				    var html = template.render(data);
				    $("#keywordList1").html(html);
				    $("#keywordListCount1").text(data.keywordListCount);
			    } else if (type == 'end') {
			    	setTimeout("$('#keyword-loading2').hide();" , 100);
				    var template =  $.templates("#tmpl_keyword2");
				    var html = template.render(data);
				    $("#keywordList2").html(html);
				    $("#keywordListCount2").text(data.keywordListCount);
			    }
			},
			complete : function (){
				setTimeout("$('.tbl_scroll').floatThead('reflow');" , 100);
			}
	    });
	}
}

function fn_LabelingDoc() {
	var groupName = $("#groupName").val();
	var keyword1 = $("#keyword1").val();
	var keyword2 = $("#keyword2").val();
	var relation = getRelation(groupName);

	var url =contextPath+'/check/relation/docList.do?_format=json';
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
		    $('.tbl_scroll').floatThead('reflow');
		    template =  $.templates("#tmpl_unLabelingDoc");
		    html = template.render(data);
		    $("#unLabelingList").html(html);
		    $("#unlabelingListCount").text(data.unlabelingListCount);
		    $('.tbl_scroll').floatThead('reflow');
		}
    });
}

function fn_keywordSearch(type) {
	if (type == 'start') {
		var keywordInput1 = $("#keywordInput1").val();
		$("#keyword1").val('');
		fn_getKeyword('start', keywordInput1);
		
	} else if (type == 'end') {
		var keyword1 = $("#keyword1").val();
		if (keyword1 == '' || typeof keyword1 == 'undefined') {
			$("#keywordList2").html('');
		    $("#keywordListCount2").text('0');
			return;
		}
		var keywordInput2 = $("#keywordInput2").val();
		fn_getKeyword('end', keywordInput2);
	}
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

function fn_bratView(type, docId, recordId){
	$("#brat-loading").show();
	var groupName = $("#groupName").val();
	
	$.ajax({
		url: contextPath+"/labeling/bratView.do",
		type: "POST",
		data: {"docId":docId, "groupName":groupName, "recordId":recordId} ,
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
			$("#docSubject").text(""+$("#doc_"+docId).text()+".txt");
			
			$("#docId").val(docId);
			$("#recordId").val(recordId);
			$("#docGroupName").val(groupName);
			
			$("#btn_keywordPrev").css("visibility","hidden");
			$("#btn_keywordNext").css("visibility","hidden");
			
			if (type == 'labeling') {
				setTimeout("fn_keyowrdLoc();",1000);
			}
		}
    });
}

function fn_keyowrdLoc() {
	var relation = getRelation(groupName);
	$("#docInfo").append("<input type='hidden' name='relation' value='"+relation+"'/>")
	
	$.ajax({
		url: contextPath+"/check/relation/RelationLoc.do",
		type: "POST",
		data: $("#docInfo").serialize(),
		success: function (data) {
			keywordLoc = data.keywordLoc;
			var relationLoc = data.relationLoc;
			
			for (var i=0; i<keywordLoc.length; i++) {
				$("rect[id='H_"+keywordLoc[i]+"']").attr("stroke","red");
				$("rect[id='H_"+keywordLoc[i]+"']").attr("stroke-width","3");
			}

			for (var i=0; i<relationLoc.length; i++) {
				$("text[data-arc-ed='"+relationLoc[i]+"']").parent().addClass('highlight');
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
	
	var offset = $("tspan[id*='"+keywordLoc[num]+"']").attr("y");
	$("#brat_scroll").animate({scrollTop : offset-150}, 400);
	
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
			url: contextPath+"/labeling/bratEdit.do",
			type: "POST",
			data: $("#docInfo").serialize(),
			success: function (data) {
				if(!openPopup()){
					
					var path = data.map.filePath;
					var idx = path.lastIndexOf("/");
					path = path.substring(0,idx);
					
					$.ajax({
						url: contextPath+"/labeling/deleteFile.do",
						type: "POST",
						data: {"path":path},
						success: function (data) {
						},
						complete: function () {
							//setTimeout("window.close();",200);
						}
					});
					return;
				}
				
				if (data.map.userId != '' && typeof data.map.userId != 'undefined') {
					if (!confirm("해당 파일은 [ID: "+data.map.userId+"]님이 편집중입니다. 읽기전용으로 열립니다."))
						return;
				}
							
				bratWin[bratWinLength] = window.open("about:blank", 'TEST_POPUP',"width=800,height=600");
				
				$("#winNum").val(bratWinLength);
				var bratPath = contextPath+"/brat/#/"+data.map.filePath;
				bratWin[bratWinLength].location.href = bratPath;
				if (data.map.userId != '' && typeof data.map.userId != 'undefined') {
					$("#docType").val("readOnly");
				} else {
					$("#docType").val("edit");
				}
				//2017.11.22 number40 레이블링 점수 추가
				$("#labelGrade").val(data.map.labelGrade);
				bratWinLength++;
			}
		});
	} else {
		alert("문서를 선택해주세요");
	}
}

function setKeyword1(type, content) {
	$("#keyword1").val('');
	$("#keyword2").val('');
	
	if (type == 'start') {
		$("#keyword1").val(content);
	} else if (type == 'end') {
		$("#keyword2").val(content);
	}
	fn_getKeyword('end', null);
	fn_LabelingDoc();
}

function setKeyword2(type, content) {
	if (type == 'start') {
		$("#keyword1").val(content);
	} else if (type == 'end') {
		$("#keyword2").val(content);
	}
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
		url: contextPath+"/labeling/deleteFile.do",
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