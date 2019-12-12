
var webFontURLs;
var dispatcher;
var bratWin = [];
var bratWinLength;
var keywordLoc;
var keywordnum;

$(function () { 
	bindEntityTree("namedentity");
	bindEntityTree("syntactic");
	bindEntityTree("causation");
	bindEntityTree("speech");
	bindEntityTree("simentic");
	
	bindbratInit();
	bindAccrodianList();
	
	$("#labelDocChkAll").click(function() {
		var value = $(this).is(":checked");
		
		$("input[name=labelDocChk]:checkbox").each(function() {
			$(this).prop("checked", value);
		});
	});
	
	$('#searchTermInfo').keyup(function(e){
		var searchTerm = $(this).val();
		if($.trim(searchTerm) == ''){
			if($.trim($('#searchTerm').val()) != ''){
				$('#searchTerm').val('');
				fn_getKeyword();
				fn_LabelingDoc(searchTerm);
			} else {
				fn_getKeyword();
			}
		}
	})
});

function bindbratInit() {
	var bratLocation = contextPath+'/resources/lib/brat';
	dispatcher = new Dispatcher();
	
	webFontURLs = [];
}

function bindEntityTree(groupName){
	var entityTree = $('#'+groupName+'_tree_list');
	
	entityTree.jstree({
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
	
	entityTree.on("ready.jstree", function() {
		entityTree.jstree('open_all');
	});
	
	entityTree.on('changed.jstree', function (e, data) {
		fn_getKeyword();
		
		var i, j, r = [];
		
		if (data.selected.length == 0) {
			 $('#entity').val("");
		}
        for (i = 0, j = data.selected.length; i < j; i++) {
            r.push(data.instance.get_path(data.selected[i],'/'));
            $('#entity').val(r.join(', '));
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
			
			$("#labelingListCount").html('0');
			$("#labelingCount").html('0');
			$("#unlabelingListCount").html('0');
			$("#keywordListCount").html('0');
			
//			var tree = $("#"+groupName+"_tree_list").jstree(true);
			//var selectedNodes = tree.get_selected()[0];
			var i, j, r = [];
			var tree = $("#"+groupName+"_tree_list");
			var selectedData = tree.jstree('get_selected', true);
			var arr = []
			if(selectedData.length >= 1){
				for(var i = 0 ; i < selectedData.length ; i++) {
					arr.push(tree.jstree(true).get_path(selectedData[i],"/"))
				}
				$('#entity').val(arr.join(', '));
			} else {
				$('#entity').val('');
			}
			fn_getKeyword();
		};
		return false;
	});
}

function replaceSpecialChar(val){
	val = val.replace(/\./gi, '__');
	val = val.replace(/([\s]{1,})/gi, '_')
    return val.replace(/\./gi, '__')
}

function fn_unlabeling() {
	if ($(":checkbox[name='labelingDoc']:checked").length==0) {
		alert("삭제할 항목을 하나이상 체크해주세요.");
	    return;
	}
	
	if (confirm('문서에 대한 언레이블링 처리를 하시겠습니까? 관련된 관계도 모두 언레이블링됩니다.')) {
		$("#div-loading").show();
		
		var docList = new Array();
	  	$(":checkbox[name='labelingDoc']:checked").each(function(i){
	  		docList.push($(this).val());
	    });
	  	
	  	var keyword = $("#keyword").val();
	  	var groupName = $("#groupName").val();
	  	
	  	var url =contextPath+'/check/entity/unlabeling.do?_format=json';
		url += '&docId='+encodeURI(docList);
		url += '&keyword='+encodeURI(keyword);
		url += '&groupName='+encodeURI(groupName);

		$.ajax({
			url: url,
			success: function (data) {
			   alert('언레이블링 처리가 완료되었습니다.');
			   fn_LabelingDoc(keyword);
			},
			error: function (request,status,error) {
				alert('에러가 발생하였습니다. 관리자에게 문의해주세요.');
		        console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
			},
			complete:function () {
				$("#div-loading").hide();
			}
	    });
	}
  
}

function fn_keywordSort(field){
	
	var groupName = $("#groupName").val();
	var entity = getEntity(groupName);
	var searchTerm = $("#searchTerm").val();
	
	if (entity != '' && typeof entity != 'undefined') {
		var sortFlag = $('#sort_'+field).html();
		var sortOption = 'asc'
			if(sortFlag == '▲' || sortFlag == '-'){
			sortOption = 'desc'
		} else {
			sortOption = 'asc'
		}
		
		
		var url =contextPath+'/check/entity/keywordList.do?_format=json';
		url += '&groupName='+encodeURI(groupName);
		url += '&entity='+encodeURI(entity);
		
		if (searchTerm) {
			url += '&searchTerm='+encodeURI(searchTerm);
		}
		url += '&orderField='+encodeURI(field);
		url += '&orderOpt='+encodeURI(sortOption);
		$.ajax({
			url: url,
			success: function (data) {
				var tagInfo = data.selectEntityDesc;
			    var tagName = '';
			    var kTagName = '';
			    if(tagInfo.length == 1){
			    	tagName = tagInfo[0].name+'로';
			    	kTagName= tagInfo[0].name;
			    } else {
			    	tagName = tagInfo[0].name + '등으로';
			    	kTagName = tagInfo[0].name + '등';
			    }
				
			    $("#labelingDocTag").html(tagName);
		    	$('#selectTag').html(' / '+kTagName);
		    	
			    var template =  $.templates("#tmpl_keyword");
			    var html = template.render(data);
			    
			    $("#keywordList").html(html);
			    $("#keywordListCount").text(data.keywordListCount);
			    if(searchTerm != ''){
		    		$('#keyword_'+replaceIdText(searchTerm)).addClass('on');
			    } else {
			    	searchTerm = $("#searchTermInfo").val()
			    	if(searchTerm != ''){
			    		$('#keyword_'+replaceIdText(searchTerm)).addClass('on');
			    	}
			    }
			},
			complete : function (){
				$('a[id^=sort]').html('-');
				
				if(sortOption == 'desc'){
					$('#sort_'+field).html('▼');
				} else {
					$('#sort_'+field).html('▲');
				}
				
				setTimeout(function(){
					setTimeout("$('.tbl_scroll').floatThead('reflow');" , 100);
			    }, 1000);
			}
	    });
	} else {
		$("#labelingDocTag").html('');
	    $("#unLabelingList").html('');
	}
	
}

function fn_getKeyword() {
	$("#keywordList").html('');
	
	var groupName = $("#groupName").val();
	var entity = getEntity(groupName);
	var searchTerm = $("#searchTerm").val();
	if (entity != '' && typeof entity != 'undefined') {
		var url =contextPath+'/check/entity/keywordList.do?_format=json';
		url += '&groupName='+encodeURI(groupName);
		url += '&entity='+encodeURI(entity);
		
		if (searchTerm) {
			url += '&searchTerm='+encodeURI(searchTerm);
		}
		
		$.ajax({
			url: url,
			success: function (data) {
			    var template =  $.templates("#tmpl_keyword");
			    var html = template.render(data);
			    
			    var tagInfo = data.selectEntityDesc;
			    var tagName = '';
			    var kTagName = '';
			    if(tagInfo.length == 1){
			    	tagName = tagInfo[0].name+'로';
			    	kTagName= tagInfo[0].name;
			    } else {
			    	tagName = tagInfo[0].name + '등으로';
			    	kTagName = tagInfo[0].name + '등';
			    }
			    
			    
			    $("#keywordList").html(html);
			    $("#labelingDocTag").html(tagName);
			    $('#selectTag').html(' / '+kTagName);
			    $("#keywordListCount").text(data.keywordListCount);
			    
			    if(searchTerm == ''){
			    	searchTerm = $('#searchTermInfo').val();
			    }
			    
			    if(searchTerm != ''){
			    	$('#keyword_'+replaceIdText(searchTerm)).addClass('on');
		    	}
			},
			complete : function (){
				setTimeout("$('.tbl_scroll').floatThead('reflow');" , 100);
			}
	    });
	} else {
		$("#labelingDocTag").html('');
	    $("#unLabelingList").html('');
	}
	
}

function fn_search() {
	var entity = $("#entity").val();
	if (entity == '' || typeof entity == 'undefined') {
		alert('개체명을 선택해주세요.');
		return;
	} 
	
	var content = $("#searchTermInfo").val();
	if (content == '' || typeof content == 'undefined') {
		alert('키워드를 입력해주세요');
		$("#searchTermInfo").focus();
		return;
	} 
	$("#searchTerm").val(content)
	fn_getKeyword();
	fn_LabelingDoc(content);
}

function fn_LabelingDoc(content) {
	var groupName = $("#groupName").val();
	
	var url =contextPath+'/check/entity/docList.do?_format=json';
	url += '&groupName='+encodeURI(groupName);
	url += '&content='+encodeURI(content);
	
	$.ajax({
		url: url,
		beforeSend : function(){
			  $('tr[id^=keyword_]').removeClass('on');
			  $('#keyword_'+replaceIdText(content)).addClass('on');
			  $('#searchTermInfo').val(content);
		},
		success: function (data) {
		    var template =  $.templates("#tmpl_labelingDoc");
		    var html = template.render(data);
		    $("#labelingList").html(html);
		    $("#labelingListCount").text(data.labelingListCount);
		    $('.tbl_scroll').floatThead('reflow');
		    $("#labelingCount").html(data.labelingCnt);
		    $("#labelDocChkAll").prop('checked', false);
		    $("input[name=labelDocChk]:checkbox").click(function() {
				if($('input[name=labelDocChk]').length == $('input[name=labelDocChk]:checked').length){
					$("#labelDocChkAll").prop("checked", true);
				} else {
					$("#labelDocChkAll").prop("checked", false);
				}
			});
		    
		    
		    template =  $.templates("#tmpl_unLabelingDoc");
		    html = template.render(data);
		    $("#unLabelingList").html(html);
		    $("#unlabelingListCount").text(data.unlabelingListCount);
		    
		    $("#keyword").val(content);
		    $('.tbl_scroll').floatThead('reflow');
		}
    });
}

function fn_bratView(type, docId, recordId){
	$("#brat-loading").show();
	var groupName = $("#groupName").val();
	
	$.ajax({
		url: contextPath+"/labeling/bratView.do",
		type: "POST",
		data: {"docId":docId, "groupName":groupName, "recordId":recordId},
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
	$.ajax({
		url: contextPath+"/labeling/entityLoc.do",
		type: "POST",
		data: $("#docInfo").serialize(),
		success: function (data) {
			keywordLoc = data.keywordLoc;
			
			if (keywordLoc.length > 0) {
				for (var i=0; i<keywordLoc.length; i++) {
					$("rect[id='H_"+keywordLoc[i]+"']").attr("stroke","red");
					$("rect[id='H_"+keywordLoc[i]+"']").attr("stroke-width","3");
				}
				fn_keywordScroll(keywordnum);
			}
			
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

function fn_bratEdit() {
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


function fn_fileDelete(winNum,path) {
	if(!bratWin[winNum]){
		return;
	} else {
		if (!bratWin[winNum].closed) {
			return;
		}
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
	if(!bratWin[winNum]){
		$("#winNum").val(winNum);
		$("#docType").val(docType);
	} else {
		if (!bratWin[winNum].closed) {
			$("#winNum").val(winNum);
			$("#docType").val(docType);
		}
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

function getEntity(groupName){
	var entity = "";
	if ($("#"+groupName+"_tree_list").find("li").length > 0) {
		entity = $("#"+groupName+"_tree_list").jstree(true).get_selected();
	}
	return entity;
}
window.onunload = windowClose;