
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
	
	bindbratInit();
	bindAccrodianList();
});

function bindbratInit() {
	var bratLocation = '/resources/lib/brat';
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
                'icon': '/resources/images/common/tag_blue.png'
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
			$("#unlabelingListCount").html('0');
			$("#keywordListCount").html('0');
			
			var tree = $("#"+groupName+"_tree_list").jstree(true);
			var selectedNodes = tree.get_selected()[0];
			var i, j, r = [];
			$('#entity').val('');
			
	        for (i = 0, j = tree.get_selected().length; i < j; i++) {
	            r.push(tree.get_path(tree.get_selected()[i],"/"));
	            $('#entity').val(r.join(', '));
	        }
	        
			fn_getKeyword();
		};
		return false;
	});
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
	  	
	  	var url ='/check/entity/unlabeling.do?_format=json';
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

function fn_getKeyword() {
	$("#keywordList").html('');
	
	var groupName = $("#groupName").val();
	var entity = getEntity(groupName);
	var searchTerm = $("#searchTerm").val();
	
	if (entity != '' && typeof entity != 'undefined') {
		var url ='/check/entity/keywordList.do?_format=json';
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
			    
			    $("#keywordList").html(html);
			    $("#keywordListCount").text(data.keywordListCount);
			}
	    });
	}
	
}

function fn_search() {
	var entity = $("#entity").val();
	if (entity == '' || typeof entity == 'undefined') {
		alert('개체명을 선택해주세요.');
		return;
	} 
	
	var content = $("#searchTerm").val();
	if (content == '' || typeof content == 'undefined') {
		alert('키워드를 입력해주세요');
		$("#searchTerm").focus();
		return;
	} 
	
	fn_LabelingDoc(content);
}

function fn_LabelingDoc(content) {
	var groupName = $("#groupName").val();
	
	var url ='/check/entity/docList.do?_format=json';
	url += '&groupName='+encodeURI(groupName);
	url += '&content='+encodeURI(content);
	
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
		    
		    $("span[name=keyword]").html("["+content+"]으로 ");
		    $("#keyword").val(content);
		}
    });
}

function fn_bratView(type,id){
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
		url: "/labeling/keyowrdLoc.do",
		type: "POST",
		data: $("#docInfo").serialize(),
		success: function (data) {
			keywordLoc = data.keywordLoc;
			
			if (keywordLoc.length > 0) {
				for (var i=0; i<keywordLoc.length; i++) {
					$("rect[id*='"+keywordLoc[i]+"']").attr("stroke","red");
					$("rect[id*='"+keywordLoc[i]+"']").attr("stroke-width","3");
				}
				fn_keywordScroll(keywordnum);
			}
			
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

function getEntity(groupName){
	var entity = "";
	if ($("#"+groupName+"_tree_list").find("li").length > 0) {
		entity = $("#"+groupName+"_tree_list").jstree(true).get_selected();
	}
	return entity;
}
window.onunload = windowClose;