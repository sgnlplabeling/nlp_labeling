<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="tiles" uri="http://tiles.apache.org/tags-tiles" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>

<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=Edge" />
<title>학습 코퍼스 구축 도구</title>
<link rel="stylesheet" type="text/css" href="/resources/css/style.css" />
<script type="text/javascript" src="/resources/lib/jquery-1.9.0/jquery-1.9.0.min.js"></script>
<script type="text/javascript" src="/resources/lib/jquery.ui-1.10.4/jquery-ui.min.js"></script>
<script type="text/javascript" src="/resources/lib/jquery-migrate-1.4.1/jquery-migrate-1.4.1.js"></script>

<script type="text/javascript" src="/resources/js/jsrender.min.js"></script>
<script type="text/javascript" src="/resources/js/datepicker_kr.js"></script>
</head>
<script type="text/javascript">
	$(document).ready(function(){
		
	});
	
	var count = '${docList.size()}';
	var subject = '${docList[0].subject}';
	var exportIDInfo = '';
	var intervalExport = null;
	function exportProgress(exportID) {		
		$("#count").html("다운로드 상태 : "+subject+"(1/"+count+")");
		
		var docIds = new Array();
		
		<c:forEach items="${ PARAM.docIds }" var="docId">
			docIds.push('${ docId }');
		</c:forEach>
		
		jQuery.ajaxSettings.traditional = true;
						
		var seccess = false;
		$.ajax({
			type :'post',
			url : '/learning/downloadProcessing.do',
			//data : $('form[name=downloadForm]').serialize(),
			data: {"docIds" : docIds, "groupName" : '${ PARAM.groupName }'},
			beforeSend : function(){
		        $("#ready").hide();
		        $("#down").show();
		        $("#progress").show();
		        $("#count").show();
		        $("#exportBtn").hide();
			}, success : function(result){
				data = $.trim(result.data);
				console.log(data);
				var data = jQuery.trim(data);
		        var datas = data.split('@@@');
				exportIDInfo = datas[0];
				document.downloadForm.downloadPath.value = datas[1];
				document.downloadForm.downloadID.value = datas[0];
                intervalExport = setInterval(downloadCheck, 500);
			}, error : function(){
				$("#exportBtn").show();
				if(intervalExport != null){
                    clearInterval(intervalExport);
                    intervalExport = null;
                }
			}
		});
    }

	
	var downloadCheck = function (){
		$.ajax({type :'post',
				url: '/learning/downloadInfo.do',
	            data : {"exportID" : document.downloadForm.downloadID.value},
	            success : function(result){
	            	data = $.trim(result.data);
	            	console.log(data);
	            	if(data == 'false'){
	            		alert('Export에 실패하였습니다.');
						$('#exportBtn').show();
						if(intervalExport != null){
							clearInterval(intervalExport);
							intervalExport = null;
						}
						$("#ready").show();
	     		        $("#down").hide();
	     		        $("#progress").hide();
	     		        $("#count").hide();
	            	} else if(data == 'true'){
	            		$("#ready").show();
	     		        $("#down").hide();
	     		        $("#progress").hide();
	     		        $("#count").hide();
	            		var arr = data.split("@@@");
	            		$('#exportBtn').show();
						if(intervalExport != null){
							clearInterval(intervalExport);
							intervalExport = null;
						}
	            		 
						download();
	            	} else {
	            		if(data.length > 0){
	                	    $('#count').html("다운로드 상태 : "+data);
	            		}
	            	}
	            }, error : function(){
	                $('#exportBtn').show();
                    if(intervalExport != null){
						clearInterval(intervalExport);
                        intervalExport = null;
                    }
	            }
	    });
	}
	
	function download(){
		document.downloadForm.submit();
		//$('#exportBtn').show();
        //$('#downloadBtn').hide();
		return false;
	}
</script>
<body class="pop_body type_02">

	<div>
		<div class="pop_header"><h1 class="pop_h1">학습데이터 다운로드</h1></div>
		<div class="pop_content clear2">
			<div class="font_b">학습완료 된 학습데이터를 <span class="font_red">${docList.size()}건</span> 다운로드 합니다.</div>
			<div class="pop_download_area mt_10">

				<div id="down" class="pop_down_txt01" style="display:none;">현재 다운로드가 진행중입니다.</div>
				<img id="progress" src="/resources/images/common/loading.gif" class="pop_down_loading" style="display:none;" alt="다운로드 진행중" />
				<div id="count" class="pop_down_txt02" style="display:none;">다운로드 상태 : 문서제목 (2/5)</div>
			
				<ul id="ready" style="display:block;">
					<c:forEach var="result" items="${docList}">
						<li>${ result.subject }</li>
					</c:forEach>
				</ul>

			</div>
			
			<div class="align_c mt_10">
				<a href="javascript:exportProgress();" id="exportBtn" class="btn b_orange medium valign_m">시작</a>
				<a href="javascript:window.close();" class="btn b_gray medium valign_m">닫기</a>
			</div>
			
		</div>
	</div>

</body>
</html>
<form name="downloadForm" action="/learning/download.do" method="post">
	<input type="hidden" name="downloadPath"/>
	<input type="hidden" name="downloadID"/>
</form>