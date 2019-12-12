
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

var autoLabelingInterval = null;
function bindLearning() {
    $("#btn_learning_start").click(function (e) {
    	if($('input[name=docIds]:checked').length == 0){
    		alert('학습 데이터를 생성 위해서는 문서를 선택해주세요.');
    		return;
    	}
    	
    	var isProcessing = false;
//    	$('td[id^=learningStatus_]').each(function(){
//    		if($.trim($(this).html()) == '처리중'){
//    			isProcessing = true;
//    		}
//    	});
    	
    	if(isProcessing){
    		alert('학습 데이터를 생성 작업중인 문서가 존재합니다.')
    		return;
    	}
    	
	    if (!confirm('선택하신 문서에 대한 학습 데이터를 생성하시겠습니까?'))
	        return false;
	    
	    var labelingForm = $('#labeling_form').serialize();
	    
	    $.ajax({
	    	url: contextPath+'/learning/start.do?_format=json'
	    	, dataType: 'json'
	    	, data: labelingForm
	    	, beforeSend : function(){
	    		$('input[name=docIds]:checked').each(function(){
	    			$('#learningStatus_'+$(this).val()).html('처리중');
	    		});
	    	} 
	    	, success: function (data) {
	    		autoLabelingInterval = setInterval(function(){checkLearingForm(labelingForm)}, 15000);
	    	}
	    });
    });
}

var checkLearingForm = function (form){
	 $.ajax({
	    	url: contextPath+'/learning/checkLearning.do?_format=json'
	    	, dataType: 'json'
	    	, data: form
	    	, success : function (data){
	    		if(data.docId){
	    			$.each(data.docId, function(index, value){
	    				$('#learningStatus_'+value).html('자동');
	    			});
	    			if($('input[name=docIds]:checked').length == data.docId.length){
    					alert('선택한 문서의 학습 데이터 생성이 완료되었습니다.')
    					clearInterval(autoLabelingInterval);
    					$('input[name=docIds]:checked').prop('checked', false);
    					windowRefresh();
    				}
	    		}
	    	}
	 });
}

function bindDownload() {
    $("#btn_download_start").click(function (e) {
    	
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
	    var url =contextPath+ "/learning/downloadForm.do";
	    f.target = 'download_pop';
	    f.method = 'post';
	    f.action = url;
	    f.submit();
    });
}

function fn_learning(docId) {
	var isProcessing = false;
//	$('td[id^=learningStatus_]').each(function(){
//		if($.trim($(this).html()) == '처리중'){
//			isProcessing = true;
//		}
//	});
	
	if(isProcessing){
		alert('학습 데이터를 생성 작업중인 문서가 존재합니다.')
		return;
	}
	
	
   if (!confirm('문서에 대한 학습 데이터를 생성하시겠습니까?'))
        return false;
    
    var groupName = $("#learningGroupName").val();
    
    $.ajax({
    	url:contextPath+ '/learning/start.do?_format=json'
    	, dataType: 'json'
    	, data: {"docIds" : docId, "groupName" : groupName}
    	, beforeSend : function(){
    		$('#learningStatus_'+docId).html('처리중');
    	} 
    	, success: function (data) {
    		console.log(data);
    		autoLabelingInterval = setInterval(function(){checkLearingValue(docId, groupName)}, 15000);
    	}
    });
}


var checkLearingValue = function (docId, groupName){
	 $.ajax({
	    	url: contextPath+'/learning/checkLearning.do?_format=json'
	    	, dataType: 'json'
    		, data: {"docIds" : docId, "groupName" : groupName}
	    	, success : function (data){
	    		console.log(data);
    			if(data.docId){
    				$.each(data.docId, function(index, value){
    					$('#learningStatus_'+value).html('자동');
    				});
    				if(docId == data.docId[0]){
    					alert('선택한 문서의 학습 데이터 생성이 완료되었습니다.')
    					clearInterval(autoLabelingInterval);
    					windowRefresh();
    				}
        		}
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

function fn_downloadPop(docId) {
	var f = document.popupForm;
	
	var groupName = $("#learningGroupName").val();
	
    window.open('',"download_pop","toolbar=no,status=no,width=500,height=270,directories=no,scrollbars=yes,location=no,resizable=yes,menubar=no");
    var url = contextPath+"/learning/downloadForm.do";
    f.docId.value = docId;
    f.groupName.value = groupName;
    f.target = 'download_pop';
    f.method = 'post';
    f.action = url;
    f.submit();
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
