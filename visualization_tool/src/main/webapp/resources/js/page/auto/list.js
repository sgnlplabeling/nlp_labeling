
var runningChkInterval=null;
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
	$(".toggle_checkbox").change(function() {
		var value = $(this).is(":checked");

		$("input[name=docIds]:checkbox").each(function() {
			$(this).prop("checked", value);
		});
	});
	
	$("input[name=docIds]:checkbox").change(function() {
		if($('input[name=docIds]').length == $('input[name=docIds]:chechked').length){
			$(".toggle_checkbox").prop("checked", true);
		} else {
			$(".toggle_checkbox").prop("checked", false);
		}
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

var autoLabelingInterval = null;
function bindAutoLabeling() {
    $("#btn_auto_labeling").click(function (e) {
    	fn_autoLabelingForm()
    });
}

function fn_autoLabelingForm(){
	if($('input[name=docIds]:checked').length == 0){
		alert('자동레이블링을 하기 위해서는 문서를 선택해주세요.');
		return;
	}
	
	var isProcessing = false;
	var checkedInputBox = $('input[name=docIds]:checked');
	$(checkedInputBox).each(function(){
		if($.trim($('#learningStatus_'+$(this).val()).html()) == '처리중'){
			isProcessing = true;
		}
	});
	
	if(isProcessing){
		alert('이미 선택한 문서중 자동레이블링 작업중인 문서가 존재합니다.')
		return;
	}
	
    if (!confirm('선택하신 문서에 대해서 레이블링 작업을 시작하시겠습니까?'))
        return false;
    
    var labelingForm = $('#labeling_form').serialize();
	$.ajax({
		url: contextPath+'/auto/start.do?_format=json'
		, dataType: 'json'
		, data: labelingForm
		, beforeSend : function(){
    		$('input[name=docIds]:checked').each(function(){
    			$('#learningStatus_'+$(this).val()).html('처리중');
    		});
    	} 
		, success: function (data) {
			autoLabelingInterval = setInterval(function(){checkAutoLabelForm(labelingForm)}, 15000);
		}
	});
}

var checkAutoLabelForm = function (form){
	 $.ajax({
	    	url: contextPath+'/auto/checkAutoLabel.do?_format=json'
	    	, dataType: 'json'
	    	, data: form
	    	, success : function (data){
	    		if(data.docId){
	    			$.each(data.docId, function(index, value){
	    				$('#learningStatus_'+value).html('자동');
	    				$('#docIdChk_'+value).prop("checked", false);
	    			});
	    			if($('input[name=docIds]:checked').length == data.docId.length){
    					alert('선택한 문서의 자동레이블링이 완료되었습니다.')
    					clearInterval(autoLabelingInterval);
    					$('input[name=docIds]:checked').prop('checked', false);
    					windowRefresh();
    				}
	    		}
	    	}
	 });
}

function fn_AutoLabeling(docId) {
	var isProcessing = false;
	if($.trim($('#learningStatus_'+docId).html()) == '처리중'){
		isProcessing = true;
	}
	
	if(isProcessing){
		alert('이미 선택한 문서중 자동레이블링 작업중인 문서가 존재합니다.')
		return;
	}
	
    if (!confirm('문서에 대한 레이블링 작업을 시작하시겠습니까?'))
        return false;
    
    var groupName = $("#autoGroupName").val();
    
	$.ajax({
		url: contextPath+'/auto/start.do?_format=json'
		, dataType: 'json'
    	, data: {"docIds" : docId, "groupName" : groupName}
		, beforeSend : function(){
			$('#learningStatus_'+docId).html('처리중');
		} 
		, success: function (data) {
			alert('선택한 문서에 대한 자동 레이블링을 시작합니다.');
			autoLabelingInterval = setInterval(function(){checkAutoLabelValue(docId, groupName)}, 15000);
		}
	});
}

var checkAutoLabelValue = function (docId, groupName){
	 $.ajax({
	    	url: contextPath+'/auto/checkAutoLabel.do?_format=json'
	    	, dataType: 'json'
	    	, data: {"docIds" : docId, "groupName" : groupName}
	    	, success : function (data){
	    		console.log(data)
    			if(data.docId){
    				$.each(data.docId, function(index, value){
    					$('#docIdChk_'+value).prop("checked", false);
    					$('#learningStatus_'+value).html('자동');
    				});
    				if(docId == data.docId[0]){
    					alert('선택한 문서의 자동레이블링이 완료되었습니다.')
    					clearInterval(autoLabelingInterval);
    					windowRefresh();
    				}
        		}
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
