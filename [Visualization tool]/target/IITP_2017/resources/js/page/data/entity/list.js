
$(function () { 
	bindAccrodianList();
	
	bindEntityTree("namedentity");
	bindEntityTree("syntactic");
	bindEntityTree("causation");
	bindEntityTree("simentic");
	bindEntityTree("speech");
	
	bindToggleCheckbox();
	bindRecordEntDelete();
	
});

function bindToggleCheckbox() {
	$(".toggle_checkbox").click(function() {
		var value = $(this).is(":checked");

		$("input[name=recordIds]:checkbox").each(function() {
			$(this).prop("checked", value);
		});
	});
}

function bindAccrodianList() {
	$('.accordion_onoff').click(function(){
		if(!$(this).closest('li').hasClass('on')) {
			$(this).closest('.label_accordion').find('.cont_gray').slideUp('fast');
			$(this).closest('.label_accordion').find('li').removeClass('on');
			$(this).closest('.label_accordion').find('.btn_label_onoff').attr('title','펼치기');
			$(this).closest('li').addClass('on');
			$(this).next('.cont_gray').slideDown('fast');
			$(this).attr('title','');
			
			var groupName = $(this).closest('li').attr('id');
			$("#groupName").val(groupName);
			
			$('#namedentity_tree_list').jstree(true).deselect_all();
			$('#syntactic_tree_list').jstree(true).deselect_all();
			$('#causation_tree_list').jstree(true).deselect_all();
			$('#simentic_tree_list').jstree(true).deselect_all();
		}
	});
}

function bindEntityTree(groupName){
	var entityTree = $('#'+groupName+'_tree_list');
	
	entityTree.jstree({
		'plugins': ["themes", "html_data", "sort", "ui","types"] ,
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
		
		var entId = entityTree.jstree(true).get_selected();
		if (entId != '' && typeof entId != 'undefined') {
			var path = entityTree.jstree().get_path(entityTree.jstree(true).get_selected(),' > ');
			$("#path").html(path);
		}
	});
	
	entityTree.on('select_node.jstree', function (e, data) {
		var name = entityTree.jstree(true).get_selected();
		var url = contextPath+'/data/entity/list.do?';
		url += 'groupName='+groupName;
		url += '&name='+name[0];
		url += '&selIds='+name[0];
		
		location.href = url;
    });
	
	entityTree.on('deselect_node.jstree', function (e, data) {
    });
}

function fn_excelDown() {
	if (confirm("설정데이터를 다운로드하시겠습니까?")) {
		var groupName = $("#downOpt").val();
		
		location.href = contextPath+"/data/entity/excelDown.do?groupName="+groupName;
	}
}

function fn_upload() {
		var groupName = $("#uploadOpt").val();
		
		var thumbext = $("#uploadFile").val();
		thumbext = thumbext.slice(thumbext.indexOf(".") + 1).toLowerCase();
		
		if (thumbext != "xlsx"){
			alert('파일은 xlsx 확장자만 등록이 가능합니다.');
			return;
		}
		var form = this;
		var data = new FormData($(this)[0]);
		data.append("file",$("#uploadFile")[0].files[0]);
		data.append("groupName", groupName);
		
		if (!confirm("문서를 등록하시겠습니까?")) {
		    return false;
		}
		
		$.ajax({
			url: contextPath+'/data/entity/upload.do?_format=json',
			method: 'post',
			contentType: false,
			processData: false,
			data: data,
			success: function (data) {
				var form = $("#searchForm");
				form.children("input[name=pageNo]").val('1');
				form.action = contextPath+"/data/entity/list.do";
				form.submit();
			}
			,error: function(request,status,error){
				console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
			}
			,complete: function() {
			}
		});
}

function fn_lowEntityAdd() {
	var entId = $("#entId").val();
	
	var lowEntity = $("#lowEntity").val();
	var lowbgColor = $("#chosen-color02").val();
	var groupName = $("#groupName").val();
	var parentEnt = $('#'+groupName+'_tree_list').jstree(true).get_selected();
	
	if (typeof lowEntity == 'undefined'|| lowEntity.length<1) {
		alert("하위 entity를 입력해주세요.");
		$("#lowEntity").focus();
		return;
	}
	
	if (typeof parentEnt == 'undefined'|| parentEnt.length<1) {
		alert("상위 entity를 선택해주세요.");
		return;
	}
	
	var checkName = $("#"+groupName).find("#"+lowEntity).text();
	if (checkName) {
		alert('['+lowEntity+']으로 이미 객체 혹은 관계가 존재합니다.');
		return;
	}
	
	$.ajax({
    	url: contextPath+'/data/entity/insert.do?_format=json'
    	, dataType: 'json'
    	, data: {"groupName":groupName, "parentEnt":parentEnt[0], "name":lowEntity, "bgColor":lowbgColor}
    	, success: function (data) {
    		alert('추가가 완료되었습니다.');
    		
			var form = $("#searchForm");
			form.children("input[name=pageNo]").val('1');
			form.children("input[name=selIds]").val(lowEntity);
			form.children("input[name=name]").val(lowEntity);
			form.action = "/data/entity/list.do";
			form.submit();
    	}
    });
}

function fn_lowRelationAdd() {
	var lowRelation = $("#lowRelation").val();
	var groupName = $("#relGroupName").val();
	var parentRel = $('#'+groupName+'_tree_list').jstree(true).get_selected();
	
	if (typeof lowRelation == 'undefined'|| lowRelation.length<1) {
		alert("하위 relation를 입력해주세요.");
		$("#lowRelation").focus();
		return;
	}
	
	if (typeof parentRel == 'undefined'|| parentRel.length<1) {
		alert("상위 relation를 선택해주세요.");
		return;
	}

	var checkName = $("#"+groupName).find("#"+lowRelation).text();
	if (checkName) {
		alert('['+lowEntity+']으로 이미 객체 혹은 관계가 존재합니다.');
		return;
	}
	
	$.ajax({
    	url: contextPath+'/data/relation/insert.do?_format=json'
    	, dataType: 'json'
    	, data: {"groupName":groupName, "parentRel":parentRel[0], "name":lowRelation}
    	, success: function (data) {
    		alert('추가가 완료되었습니다.');
    		var relId = data.relId;
    		
			var form = $("#searchForm");
			form.children("input[name=pageNo]").val('1');
			form.children("input[name=selIds]").val(relId);
			form.action = contextPath+"/data/entity/list.do";
			form.submit();
    	}
    });
}

function fn_recordEntDelete(recordId) {
	var entId = $("#entId").val();
	
	var groupName = $("#groupName").val();
	var name = $('#'+groupName+'_tree_list').jstree(true).get_selected();
	
	if (confirm('문서의 개체명 ['+name[0]+']을 정말 삭제하시겠습니까?')) {
		$.ajax({
	    	url: contextPath+'/data/entity/recordDelete.do?_format=json'
	    	, dataType: 'json'
	    	, data: {"entId":entId, "name":name[0], "recordIds":recordId}
	    	, success: function (data) {
	    		alert('삭제가 완료되었습니다');
	    		
				var form = $("#searchForm");
				form.children("input[name=pageNo]").val('1');
				form.action = contextPath+"/data/entity/list.do";
				form.submit();
	    	}
	    });
	}
}

function bindRecordEntDelete() {
    $("#btn_record_delete").click(function (e) {
    	e.preventDefault();
    	
    	var entId = $("#entId").val();
    	var groupName = $("#groupName").val();
    	var name = $('#'+groupName+'_tree_list').jstree(true).get_selected();
    	
        if (!confirm('체크된 문서의 개체명 ['+name[0]+']을 정말 삭제하시겠습니까?'))
            return false;
        
        var recordId = $("#delete_form").serialize();
        
        var url = contextPath+'/data/entity/recordDelete.do?';
        url += recordId;
        url += '&name='+name[0];
        url += '&entId'+entId;
        
        $.ajax({
        	url: url
        	, dataType: 'json'
        	, success: function (data) {
        		alert('삭제가 완료되었습니다.');
        		
    			var form = $("#searchForm");
    			form.children("input[name=pageNo]").val('1');
    			form.children("input[name=selIds]").val(relId);
    			form.action = contextPath+"/data/entity/list.do";
    			form.submit();
        	}
        });
    });
}

function fn_delete() {
	if (confirm('정말 삭제하시겠습니까?')) {
		var count = $("#count").val();
		
		if (count>0) {
			alert('해당 객체/관계를 사용하는 문서가 존재합니다. \n 문서 목록에서 전부 삭제 후 다시 시도해주세요.');
			return;
		}
		
		var formName = $('.tab_list').find('.on').attr('id');
		
		if (formName == 'entityTab') {
			var entId = $("#entityName").val();
			
			var entId = $("#entId").val();
			
			$.ajax({
		    	url: contextPath+'/data/entity/delete.do?_format=json'
		    	, dataType: 'json'
		    	, data: {"entId" : entId}
		    	, success: function (data) {
		    		alert('삭제가 완료되었습니다.');
		    		
					var form = $("#searchForm");
					form.action = contextPath+"/data/entity/list.do";
					form.submit();
		    	}
		    });
		} else {
			var relationForm = $('#relationForm').serialize();
			$.ajax({
		    	url: contextPath+'/data/relation/delete.do?_format=json'
		    	, dataType: 'json'
		    	, data: relationForm
		    	, success: function (data) {
		    		alert('삭제가 완료되었습니다.');
		    		
					var form = $("#searchForm");
					form.action = contextPath+"/data/entity/list.do";
					form.submit();
		    	}
		    });
		}
		
	}
}

function fn_edit() {
	var formName = $('.tab_list').find('.on').attr('id');
	var relationName = $("#relationName").val();
	var entityName = $("#entityName").val();
	
	if (relationName+entityName <= 0) {
		alert('');
		return;
	}
	
	if (formName == 'entityTab') {
		var entId = $("#entityName").val();
		var entityEditForm = $('#entityForm').serialize();
		
	    $.ajax({
	    	url:contextPath+ '/data/entity/update.do?_format=json'
	    	, dataType: 'json'
	    	, data: entityEditForm
	    	, success: function (data) {
	    		alert('수정이 완료되었습니다.');
	    		
    			var form = $("#searchForm");
    			form.children("input[name=pageNo]").val('1');
    			form.children("input[name=selIds]").val(entId);
    			form.action = contextPath+"/data/entity/list.do";
    			form.submit();
				
	    	}
	    });		
	} else {
		var relationForm = $('#relationForm').serialize();
	  
		var result = true;
		$("#relList > div > select").each(function(index){
			if ($(this).val() == null) {
				alert('소스/타겟을 선택해주세요.');
				result = false;
				return false;
			}
		});
		
		if (result) {
			$.ajax({
		    	url: contextPath+'/data/relation/update.do?_format=json'
		    	, dataType: 'json'
		    	, data: relationForm
		    	, success: function (data) {
		    		alert('수정이 완료되었습니다.');
		    		
		    	}
		    });
		}
	}
}

function fn_docList(pageNo) {
	var formName = $('.tab_list').find('.on').attr('id');
	
	var groupName = $("#groupName").val();
	var name = $('#'+groupName+'_tree_list').jstree(true).get_selected();
	if (typeof pageNo == 'undefined' || pageNo == null) {
		pageNo = 1;
	}
	$("#pageNo").val(pageNo);
	
	$.ajax({
    	url: contextPath+'/data/entity/doclist.do?_format=json'
    	, dataType: 'json'
    	, data: {"groupName":groupName, "name":name[0], "pageNo": pageNo}
    	, success: function (data) {
    			$.views.converters("date", function(val) {
    			  return moment(val).format('YYYY-MM-DD');
    			});
    			
    			var template =  $.templates("#tmpl_doc");
			    var html = template.render(data);
			    $("#docList").html(html);
			    $("#count").val(data.count);
			    fnRenderPaging(data.pagination, data.count);
    	}
    });
}

function fnRenderPaging(pagination,count) {
	$("#pageCount").empty();
	$("#pageCount").append("<input type=\"hidden\" id=\"listCount\" value="+count+"/>");
	$("#pageCount").append("<div class=\"float_l\">총 <strong>"+count+"</strong>건</div>");
	$("#pageCount").append("<div class=\"float_r\">"+pagination.page+"/"+pagination.lastPage+"페이지</div>");
	
    $("#pagination").empty();
    var html = "";
    $("#pagination").append("<li><a href=\"javascript:void(0);\" class='first' onclick=\"fn_docList("+pagination.firstPage+")\">&nbsp;</a></li>");
    $("#pagination").append("<li><a href=\"javascript:void(0);\" class='prev' onclick=\"fn_docList("+pagination.prevBlockPage+")\">&nbsp;</a></li>");
    for (var i=0; i<pagination.pageBlock; i++) {
        if (pagination.startBlockPage+i <= pagination.lastPage) {
            html += "<li><a href=\"javascript:void(0);\" ";
            var index = pagination.startBlockPage+i;
            if (index == pagination.page) {
                html += "class='on' ";
            }
            html += "onclick=\"fn_docList("+index+")\">"+index+"</a></li>";
        }
    }
    $("#pagination").append(html);
    $("#pagination").append("<li><a href=\"javascript:void(0);\" class='next' onclick=\"fn_docList("+pagination.nextBlockPage+")\">&nbsp;</a></li>");
    $("#pagination").append("<li><a href=\"javascript:void(0);\" class='last' onclick=\"fn_docList("+pagination.lastPage+")\">&nbsp;</a></li>");
    
}

function fn_sampleDownload() {
	location.href = contextPath+"/data/entity/excelDown.do";
}

function fn_argAdd() {
	var groupName = $("#groupName").val();
	var entityTree = $('#'+groupName+'_tree_list');
	
	var name = entityTree.jstree(true).get_selected();
	
	$.ajax({
    	url: contextPath+'/data/entity/entityList.do?_format=json'
    	, dataType: 'json'
    	, data: {'name' : name[0] , 'groupName' : groupName}
    	, success: function (data) {
    		var entList = data.entList;
		
    		var html = "";
    		
    		var id = $("#relList > div:last").attr('id');
    		var num = (id.replace("rel_","")*1)+1;
    		
			html += '<div id="rel_'+num+'">';
			html += '<select class="select2" style="width: 200px;" id="startEnt" name="startRels['+num+']" required>';
			html += '<option value="" disabled selected>소스 선택</option>';
			
			for (var j=0; j<entList.length; j++) {
				html += '<option value="'+entList[j].name + '"';
				html += '>'+entList[j].name+'</option>';
			}
			
			html += '</select>';
			html += ' -> ';
			html += '<select class="select2" style="width: 200px;" id="endEnt" name="endRels['+num+']" required>';
			html += '<option value="" disabled selected>타겟 선택</option>';
			
			for (var j=0; j<entList.length; j++) {
				html += '<option value="'+entList[j].name + '"';
				html += '>'+entList[j].name+'</option>';
			}
			html += '</select>';
			html += '	<a name="btnArgDelete" href="javascript:fn_argDelete(\'rel_'+num+'\');" class="btn b_gray ssmall_pm valign_m" title="삭제">X</a>';
			html += '</div>';
			
			$("#relList > div:last").after(html);

			$("a[name=btnArgAdd]").remove();
			
			var html = '<a name="btnArgAdd" href="javascript:fn_argAdd();" class="btn b_gray ssmall_pm valign_m" title="추가">+</a>';
			
			$("#relList > div:last").append(html);
		    $('#relList > div:last > select').select2();
    	}
    });
	}

function fn_argDelete(index) {
	var firstId = $("#relList > div:first").attr('id');
	var lastId = $("#relList > div:last").attr('id');
	
	if (firstId == lastId) {
		alert('마지막은 삭제할수없습니다.');
		return;
	}
	$("#"+index).remove();
	$("a[name=btnArgAdd]").remove();
	
	var html = '<a name="btnArgAdd" href="javascript:fn_argAdd();" class="btn b_gray ssmall_pm valign_m" title="추가">+</a>';
	
	$("#relList > div:last").append(html);
	
    $('.select2').select2();
}