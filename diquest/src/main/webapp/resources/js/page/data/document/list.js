
$(function () { 
	bindToggleCheckbox();
	bindDomainTree();
	bindDocDelete();
	bindDocAdd();
});

function bindDomainTree(){
	var domainTree = $('#domain_tree_list');
	
	domainTree.jstree({
		'plugins': ["themes", "html_data", "sort", "ui"]}); 
	domainTree.on("changed.jstree", function(e, data){
        if (data == null || data.selected == null)
            return;
        $("#domain").val(data.instance.get_path(data.node,'/'));
        $("#colId").val(domainTree.jstree(true).get_selected());
	});
	domainTree.jstree('open_all');
	
}

function bindDocAdd() {
	$("#form_doc_insert").submit(function (e) {
		e.preventDefault();
		
		var thumbext = $("#file").val();
		thumbext = thumbext.slice(thumbext.indexOf(".") + 1).toLowerCase();
		
		if (thumbext != "txt" && thumbext != "zip"){
			alert('파일은 txt, zip 확장자만 등록이 가능합니다.');
			return;
		}
		
		var colId = $("#colId").val();
		
		if (colId == '' || typeof colId == 'undefined') {
			alert('도메인을 선택해주세요.');
			return;
		}
		
		var form = this;
		var data = new FormData($(this)[0]);
		data.append("file",$("#file")[0].files[0]);
		
		if (!confirm("문서를 등록하시겠습니까?")) {
		    return false;
		}
		
		$("#div-loading").show();
		
		$.ajax({
			url: form.action,
			method: form.method,
			contentType: false,
			processData: false,
			data: data,
			success: function (data) {
				var result = JSON.parse(data);
					
				if (result.overlapDocSubject != "" && typeof result.overlapDocSubject != 'undefined') {
					alert('다음 문서의 이름이 이미 존재합니다. \n'+result.overlapDocSubject);
				}
				
				if (result.failDocSubject != "" && typeof result.failDocSubject != 'undefined') {
					alert('다음 문서 등록이 실패하였습니다. 관리자에게 문의해주세요 \n'+result.failDocSubject);
				} 
				
				if (result.successDocIds != "" && typeof result.successDocIds != 'undefined') {
					$("#docIds").val(result.successDocIds);
					alert('문서 등록이 완료되었습니다.');
				}
				
				$("#searchForm").submit();
			
			}
			,error: function(request,status,error){
				alert('문서 등록에 실패하였습니다. 관리자에게 문의해주세요.');
				console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
			}
			,complete: function() {
				$("#div-loading").hide();
			}
		});
	});
}

function fn_pageSizeEdit() {
	var pageSize = $("#boardtop01_right").val();
	$("#pageSize").val(pageSize);
	$("#searchForm").submit();
}

function fn_search() {
	$("#searchForm").submit();
}

function fn_recordDelete(recordId) {
    if (!confirm('정말 삭제하시겠습니까?'))
        return false;

    $.ajax({
    	url: '/data/document/recordDelete.do?_format=json'
    	, dataType: 'json'
    	, data: {'recordId' : recordId }
    	, success: function (data) {
    		alert('삭제가 완료되었습니다.');
    		
    		var form = $("#searchForm");
    	    form.submit();
    	},error: function(request,status,error){
        	alert('문서 삭제에 실패하였습니다. 관리자에게 문의해주세요.');
        	console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
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
    	e.preventDefault();
        if (!confirm('체크된 문서를 삭제하시겠습니까?'))
            return false;

        var deleteForm = $('#delete_form').serialize();

        $.ajax({
        	url: '/data/document/delete.do?_format=json'
        	, dataType: 'json'
        	, data: deleteForm
        	, success: function (data) {
        		alert('삭제가 완료되었습니다.');
        		
        		var form = $("#searchForm");
        	    form.submit();
        	},error: function(request,status,error){
            	alert('문서 삭제에 실패하였습니다. 관리자에게 문의해주세요.');
            	console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
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
