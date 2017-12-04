
$(function () { 
	bindToggleCheckbox();
	bindDomainTree();
	bindDocDelete();
});

function bindDomainTree(domainJstreeHtml) {
	var domainTree = $('#domain_tree_list');
	domainTree.jstree("destroy");
	
	if (domainJstreeHtml != '' || typeof domainJstreeHtml != 'undefined') {
		domainTree.html(domainJstreeHtml);
	}
	
	domainTree.jstree({
		'plugins': ["themes", "html_data", "sort", "ui"]}); 
	
	domainTree.on('ready.jstree', function() {
		var path = domainTree.jstree().get_path(domainTree.jstree(true).get_selected(),'/');     
		var domain = domainTree.jstree().get_text(domainTree.jstree(true).get_selected()); 
		
		if (path) {
			$("#domain").val(path);
			$("#domainName").val(domain);
			
			var colId = $("#colId").val();
			if (colId == 0 || path == 'ROOT') {
				$("#domainName").attr("readOnly","readOnly");
			}
		}
	});
	
	domainTree.on("select_node.jstree", function(e, data){
        if (data == null || data.selected == null)
            return;
        
        $("#colId").val(domainTree.jstree(true).get_selected());
        $("#searchTermOpt").val('');
        $("#searchTerm").val('');
        $("#searchForm").submit();
	});
	
	domainTree.jstree('open_all');
}

function fn_pageSizeEdit() {
	var pageSize = $("#boardtop01_right").val();
	$("#pageSize").val(pageSize);
	$("#searchForm").submit();
}

function fn_recordDelete(recordId) {
    if (!confirm('정말 삭제하시겠습니까?\n삭제하실경우 해당 레이블링도 모두 삭제됩니다.'))
        return false;

    $.ajax({
    	url: '/data/document/recordDelete.do?_format=json'
    	, dataType: 'json'
    	, data: {'recordId' : recordId }
    	, success: function (data) {
    		alert('삭제가 완료되었습니다.');

    		var form = $("#searchForm");
    	    form.submit();
    	}
    });
}

function fn_docDelete(docId) {
    if (!confirm('문서를 정말 삭제하시겠습니까?'))
        return false;

    $.ajax({
    	url: '/data/document/delete.do?_format=json'
    	, dataType: 'json'
    	, data: {'docId' : docId }
    	, success: function (data) {
    		alert('삭제가 완료되었습니다.');

    		var form = $("#searchForm");
    	    form.submit();
    	}
    });
}

function bindDocDelete() {
    $("#btn_doc_delete").click(function (e) {
        if (!confirm('체크된 문서를 삭제하시겠습니까?\n 삭제하실경우 해당 레이블링도 모두 삭제됩니다.'))
            return false;

        var deleteForm = $('#delete_form').serialize();

        $.ajax({
        	url: '/data/document/delete.do?_format=json'
        	, dataType: 'json'
        	, data: deleteForm
        	, success: function (data) {
        		alert('삭제가 완료되었습니다.');
        		
        		var form = $("#searchForm");
        		$("#pageNo").val('1');
        	    form.submit();
        	}
        });
    });
}

function bindToggleCheckbox() {
	$(".toggle_checkbox").click(function() {
		var value = $(this).is(":checked");

		$("input[name=docId]:checkbox").each(function() {
			$(this).prop("checked", value);
		});
	});
}

function fn_saveConf(recordId) {
	if (!confirm('작업완료 처리를 하시겠습니까?'))
        return false;
	
    $.ajax({
    	url: '/data/document/editConf.do?_format=json'
    	, dataType: 'json'
    	, data: {'recordId' : recordId, "typeOpt" : "save"}
    	, success: function (data) {
    		alert('작업완료 처리되었습니다.');
    		windowRefresh();
    	}
    });
}

function fn_cancelConf(recordId) {
	if (!confirm('작업완료 취소를 하시겠습니까?'))
        return false;
	
    $.ajax({
    	url: '/data/document/editConf.do?_format=json'
    	, dataType: 'json'
    	, data: {'recordId' : recordId, "typeOpt" : "cancel" }
    	, success: function (data) {
    		alert('작업완료 취소되었습니다.');
    		
    		windowRefresh();
    	}
    });
}

function fn_DomainAdd() {
	var name = $("#name").val();
	if (name == '' || typeof name == 'undefined') {
		alert('하위 도메인을 입력해주세요.');
		$("#name").focus();	
		 return false;
	}
	
	if (!confirm('도메인을 등록하시겠습니까?'))
        return false;
	
	var form = this;
	var parentId = $("#colId").val();
	var domain = $("#domain").val()+"/"+name;
	
	$.ajax({
	    	url: '/data/domain/insert.do?_format=json'
	    	, dataType: 'json'
	    	, data: {"parentId":parentId, "name":name, "domain":domain}
	    	, success: function (data) {
	    		alert('추가가 완료되었습니다.');
	    		
	    		bindDomainTree(data.domainJstreeHtml);
	    		$("#name").val('');
	    	},error: function(request,status,error){
	    		alert('도메인 추가에 실패하였습니다.');
	    	}
	    });
}

function fn_domainEdit() {
	var domainName = $("#domainName").val();
	var domain = $("#domain").val();
	
	var colId = $("#colId").val();
	if (colId == 0) {
		alert('ROOT는 수정 혹은 삭제할수없습니다.');
		return false;
	}
	
	if (domain == '' || typeof domain == 'undefined') {
		alert('도메인을 선택해주세요.');
		return false;
	} 
	
	if (domainName == '' || typeof domainName == 'undefined') {
		alert('도메인을 입력해주세요.');
		$("#domainName").focus();	
		 return false;
	}
		
	if (!confirm('도메인을 수정하시겠습니까?'))
        return false;
	
	 $.ajax({
	    	url: '/data/domain/edit.do?_format=json'
	    	, dataType: 'json'
	    	, data: {'colId':colId, 'name':domainName, "domain":domain }
	    	, success: function (data) {
	    		alert('수정이 완료되었습니다.');
	    		bindDomainTree(data.domainJstreeHtml);
	    		
	    	},error: function(request,status,error){
	    		alert('도메인 수정에 실패하였습니다.');
	    	}
	 });
}

function fn_domainDelete() {
	var tree = $("#domain_tree_list");
	var childrens = tree.jstree("get_children_dom",tree.jstree("get_selected"));
	
	if (childrens.length > 0) {
		alert('해당 도메인에 하위 도메인이 존재합니다.');
		return false;
	}
	
	var listCount = $("#listCount").val();
	if (listCount != '0') {
		alert('해당 도메인에 문서가 존재합니다. \n문서를 지우고 다시 시도해주세요.');
		return false;
	}
	
	var domain = $("#domain").val();
	
	var colId = $("#colId").val();
	if (colId == 0) {
		alert('ROOT는 수정 혹은 삭제할수없습니다.');
		return false;
	}
	
	if (domain == '' || typeof domain == 'undefined') {
		alert('도메인을 선택해주세요.');
		return false;
	}
	
	if (!confirm('도메인 [ '+domain+' ] 을 삭제하시겠습니까?'))
        return false;
	
	var colId =  $("#colId").val();
	
	 $.ajax({
	    	url: '/data/domain/delete.do?_format=json'
	    	, dataType: 'json'
	    	, data: {'colId':colId, "domain":domain}
	    	, success: function (data) {
	    		alert('삭제가 완료되었습니다.');
	    		
	    		$("#colId").val(0);
	    		$("#searchForm").submit();
	    	},error: function(request,status,error){
	    		alert('도메인 삭제에 실패하였습니다.');
	    	}
	    });
}

function docChange() {
	var parentCol = $("#parentId option:selected").text();
	$("#parentCol").val(parentCol);
	
	parentCol = parentCol.substring(parentCol.lastIndexOf("/")+1);
	$("#domainName").val(parentCol);
}

function fn_search() {
	$("#searchForm").submit();
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
