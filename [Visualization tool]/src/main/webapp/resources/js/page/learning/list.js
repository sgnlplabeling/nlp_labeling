
$(function () { 
	bindDomainTree();
	bindToggleCheckbox();
	bindLearning();
	bindDownload();
	
	$("input:radio[name=groupName]").click(function() { 
		$("#searchForm").submit();
	  });
});

function bindDomainTree(){
	var domainTree = $('#domain_tree_list');
	
	domainTree.jstree({
		'plugins': ["themes", "html_data", "sort", "ui"]}); 
	
	domainTree.on("select_node.jstree", function(e, data){
        if (data == null || data.selected == null)
            return;
        
        $("#domain").val(data.instance.get_path(data.node,'/'));
        $("#colId").val(domainTree.jstree(true).get_selected());
        $("#searchForm").submit();
	});
	domainTree.jstree('open_all');
}

function bindToggleCheckbox() {
	$(".toggle_checkbox").click(function() {
		var value = $(this).is(":checked");

		$("input[name=docIds]:checkbox").each(function() {
			$(this).prop("checked", value);
		});
	});
}

function fn_pageSizeEdit() {
	var pageSize = $("#boardtop01_right").val();
	$("#pageSize").val(pageSize);
	$("#searchForm").submit();
}

function fn_search() {
	var searchTerm = $("#inputTerm").val();
	var searchTermOpt = $("#boardtop01_left").val();
	
	$("#searchTerm").val(searchTerm);
	$("#searchTermOpt").val(searchTermOpt);
	
	$("#searchForm").submit();
}

function bindLearning() {
    $("#btn_learning_start").click(function (e) {
	    if (!confirm('선택하신 문서에 대한 학습 데이터를 생성하시겠습니까?'))
	        return false;
	    
	    var labelingForm = $('#labeling_form').serialize();
	    
	    $.ajax({
	    	url: '/learning/start.do?_format=json'
	    	, dataType: 'json'
	    	, data: labelingForm
	    	, success: function (data) {
	    		alert('학습 요청이 완료되었습니다.');

	    		windowRefresh();
	    	}
	    });
    });
}

function bindDownload() {
    $("#btn_download_start").click(function (e) {
//	    if (!confirm('선택하신 문서에 대한 학습 데이터를 다운로드 하시겠습니까?'))
//	        return false;
    	var flag=false;
	    
	    var f = document.labeling_form;
	    
	    for(var idx=0; idx < f.docIds.length; idx++) {
	    	if($(f.docIds[idx]).is(":checked")) {
	    		var id = $(f.docIds[idx]).val();
	    		if($("#down_"+id).size() == 0) {
	    			alert("학습데이터 생성이 완료된 문서만 다운받을 수 있습니다.");
	    			return;
	    		} else {
	    			flag = true;
	    		}
	    	}
	    }
	    
	    if(!flag) {
	    	alert("선택된 문서가 없습니다.");
	    	return;
	    }
	    
	    window.open('',"download_pop","toolbar=no,status=no,width=500,height=270,directories=no,scrollbars=yes,location=no,resizable=yes,menubar=no");
	    var url = "/learning/downloadForm.do";
	    f.target = 'download_pop';
	    f.method = 'post';
	    f.action = url;
	    f.submit();
    });
}

function fn_learning(docId) {
	  if (!confirm('문서에 대한 학습 데이터를 생성하시겠습니까?'))
	        return false;
	    
	    var groupName = $("#learningGroupName").val();
	    
	    $.ajax({
	    	url: '/learning/start.do?_format=json'
	    	, dataType: 'json'
	    	, data: {"docIds" : docId, "groupName" : groupName}
	    	, success: function (data) {
	    		alert('학습 요청이 완료되었습니다.');

	    		windowRefresh();
	    	}
	    });
}


function fn_searchTermOpt() {
	var searchTermOpt = $("#boardtop01_left").val();
	
	if (searchTermOpt == 'confY' || searchTermOpt == 'confN') {
		$("#inputTerm").val('');
		$("#inputTerm").attr("readonly","readonly");
	} else {
		$("#inputTerm").removeAttr("readonly");
	}
}

function windowRefresh() {
	var pageNo = $("input[name=pageNo]").val();

	var input = document.createElement('input');
	input.type = 'hidden';
	input.name = 'pageNo';
	input.value = pageNo;
	
	var form = $("#searchForm");
	form.append(input);
    form.submit();
}

function fn_downloadPop(docId) {
	var f = document.popupForm;
	
	var groupName = $("#learningGroupName").val();
	
    window.open('',"download_pop","toolbar=no,status=no,width=500,height=270,directories=no,scrollbars=yes,location=no,resizable=yes,menubar=no");
    var url = "/learning/downloadForm.do";
    f.docId.value = docId;
    f.groupName.value = groupName;
    f.target = 'download_pop';
    f.method = 'post';
    f.action = url;
    f.submit();
}

