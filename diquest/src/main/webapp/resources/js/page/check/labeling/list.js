
var webFontURLs;
var dispatcher;
var bratWin = [];
var bratWinLength;

$(function () { 
	bindDomainTree();
	
	bindEntityTree("namedentity");
	bindEntityTree("syntactic");
	bindEntityTree("causation");
	
	bindbratInit();
	bindAccrodianList();
	bratWinLength = 1;
});

function bindbratInit() {
	var bratLocation = '/resources/lib/brat';
	dispatcher = new Dispatcher();
	
	webFontURLs = [];
}

function bindDomainTree(){
	var domainTree = $('#domain_tree_list');
	
	domainTree.jstree({
		'plugins': ["themes", "html_data", "sort", "ui"]}); 
	domainTree.on("changed.jstree", function(e, data){
        if (data == null || data.selected == null)
            return;
        
        $("#docId").val("");
        $("#domain").val(data.instance.get_path(data.node,'/'));
        $("#colId").val(domainTree.jstree(true).get_selected());
        fn_docList();
	});
	domainTree.jstree('open_all');
	
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
			
			if (groupName == 'namedentity') {
				$("#labelingGroup").html("개체명");
			} else if (groupName == 'syntactic') {
				$("#labelingGroup").html("구문분석");
			} else if (groupName == 'causation') {
				$("#labelingGroup").html("인과관계");
			}
			
			if ($("#docId").val()) setTimeout("fn_bratView()" , 500);
		};
		return false;
	});
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
		
	    var session = sessionStorage.getItem(groupName);
	    
	    if (session) {
	    	entityTree.jstree(true).check_node(session.split(","));
	    } else {
	    	entityTree.jstree('check_all');
	    }
	});
	
	entityTree.on('select_node.jstree', function (e, data) {
		fn_selectEntity();
    });
	
	entityTree.on('deselect_node.jstree', function (e, data) {
		fn_selectEntity();
    });
}

function fn_docList(){
	var searchTerm = $("#docSearchTerm").val();
	var url = '/check/labeling/docList.do?_format=json';
	url += '&colId=' + $("#colId").val();
	if (searchTerm) url += '&searchTerm='+encodeURI(searchTerm);
	
	$.ajax({
		url: url,
		success: function (data) {
		    var template =  $.templates("#tmpl_doc");
		    var html = template.render(data);
		    $("#docList").html(html);
		    $("#docCount").html(data.count);
		}
    });
}

function fn_bratView(id){
	$("#brat-loading").show();
	
	var searchTerm = getEntity();
	$("#searchTerm").val(searchTerm);
	
	if (id) {
		$("#docId").val(id);
	}
	
	$.ajax({
		url: "/labeling/bratView.do",
		type: "POST",
		data: $("#docInfo").serialize(),
		success: function (data) {
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
		}
    });
}

function fn_selectEntity() {
	var entity = getEntity();
	var groupName = $("#groupName").val();
	
	sessionStorage.setItem(groupName, entity);
	
	var docId = $("#docId").val();
	if (docId.length > 0) {
		fn_bratView(docId);
	}
}

function getEntity(){
	var groupName = $("#groupName").val();
	var entity = "";

	if ($("#"+groupName+"_tree_list").find("li").length > 0) {
		entity = $("#"+groupName+"_tree_list").jstree(true).get_selected();
	}
	
	return entity;
}

function fn_bratEdit() {
	var docId = $("#docId").val();
	
	if (docId) {
		$.ajax({
			url: "/labeling/bratEdit.do",
			type: "POST",
			data: $("#docInfo").serialize(),
			success: function (data) {
				if (data.map.userId != '' && typeof data.map.userId != 'undefined') {
					if (!confirm("해당 파일은 [ID: "+data.map.userId+"]님이 편집중입니다. 읽기전용으로 열립니다."))
						return;
				}
				
				$("#winNum").val(bratWinLength);
				var bratPath = "/brat/#/"+data.map.filePath;

				bratWin[bratWinLength] = window.open(bratPath);
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