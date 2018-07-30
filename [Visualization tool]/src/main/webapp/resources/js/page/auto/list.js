
$(function () { 
	bindDomainTree();
	bindToggleCheckbox();
	bindAutoLabeling();
	//bindAutoLabelingAll();
	
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
	
	if (searchTermOpt != 'confY' && searchTermOpt != 'confN') {
		if (searchTerm == '') {
			alert('검색어를 입력해주세요');
			return;
		}
	}
	$("#searchTerm").val(searchTerm);
	$("#searchTermOpt").val(searchTermOpt);
	
	$("#searchForm").submit();
}

function bindAutoLabeling() {
    $("#btn_auto_labeling").click(function (e) {
	    if (!confirm('선택하신 문서에 대한 레이블링 작업을 시작하시겠습니까?'))
	        return false;
	    
	    var labelingForm = $('#labeling_form').serialize();
	    
	    $.ajax({
	    	url: '/auto/start.do?_format=json'
	    	, dataType: 'json'
	    	, data: labelingForm
	    	, success: function (data) {
	    		alert('선택한 문서에 대한 자동 레이블링을 시작합니다.');
	    		
	    		windowRefresh();
	    	}
	    });
    });
}

function fn_AutoLabeling(docId) {
    if (!confirm('문서에 대한 레이블링 작업을 시작하시겠습니까?'))
        return false;
    
    var groupName = $("#autoGroupName").val();
    
    $.ajax({
    	url: '/auto/start.do?_format=json'
    	, dataType: 'json'
    	, data: {"docIds" : docId, "groupName" : groupName}
    	, success: function (data) {
    		alert('요청한 문서에 대한 자동 레이블링을 시작합니다.');
    		
    		windowRefresh();
    	}
    });
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
