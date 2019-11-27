<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="tiles" uri="http://tiles.apache.org/tags-tiles" %>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=Edge" />
<title>학습 코퍼스 구축 도구</title>
<link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/resources/css/style.css" />
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/jquery-1.9.0/jquery-1.9.0.min.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/jquery.ui-1.10.4/jquery-ui.min.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/jquery-migrate-1.4.1/jquery-migrate-1.4.1.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/common.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/jsrender.min.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/datepicker_kr.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/jquery.floatThead.min.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/moment.js-2.17.1/moment-with-locales.min.js"></script>

<!-- jstree -->
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/jstree-3.3.1/jstree.min.js"></script>
<link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/resources/lib/jstree-3.3.1/themes/default/style.min.css" />
 
<script type="text/javascript">
var contextPath = '${pageContext.request.contextPath}';
$(function(){
	
	var groupName = $("#groupName").val();
	
	if (typeof groupName == 'undefined'|| groupName == '') {
		groupName = $('.label_accordion li:first-child').attr('id');
		$("#groupName").val(groupName);
		
		//개채명 외 아코디언
		$('.label_accordion li:first-child').addClass('on');
		$('.label_accordion li:first-child .cont_gray').show();
	} else {
		$('.label_accordion #'+groupName).addClass('on');
		$('.label_accordion #'+groupName+' .cont_gray').show();
	}
	
	
// 	$('.btn_label_onoff').click(function(){
// 		if(!$(this).closest('li').hasClass('on')){
// 			$(this).closest('.label_accordion').find('.cont_gray').slideUp('fast');
// 			$(this).closest('.label_accordion').find('li').removeClass('on');
// 			$(this).closest('.label_accordion').find('.btn_label_onoff').attr('title','펼치기');
// 			$(this).closest('li').addClass('on');
// 			$(this).parent().next('.cont_gray').slideDown('fast');
// 			$(this).attr('title','');
// 		};
// 		return false;
// 	});
	
	$('.tit_opt.type_label > ul > li > a').click(function(){
		$(this).closest('ul').find('a').removeClass('on');
		$(this).addClass('on');
		return false;
	});

});

$(document).on("click", ".label_cyan_list > li > a", function() {
	var id = $(this).closest('ul').attr('id');
	
	if (id == 'labelingList' || id == 'unLabelingList') {
		$("#labelingList").find('a').removeClass('on');
		$("#unLabelingList").find('a').removeClass('on');
	} else {
		$(this).closest('ul').find('a').removeClass('on');
	}
	
	$(this).addClass('on');
	return false;
});

// $(document).on("click", ".tbl_scroll tbody tr", function() {
// 	var id = $(this).closest('tbody').attr('id');
// 	console.log(id);
// 	if (id == 'labelingList' || id == 'unLabelingList') {
// 		$("#labelingList tr").removeClass('on');
// 		$("#unLabelingList tr").removeClass('on');
// 	} else {
// 		if($(this).hasClass('on')){
// 			$(this).removeClass('on');
// 		}else{
// 			$(this).closest('tbody').find('tr').removeClass('on');
// 			$(this).addClass('on');
// 		};
// 	}
	
// 	$(this).addClass('on');
// 	return false;
// });

$(function(){
	
	//thead 고정
    $('.tbl_scroll').floatThead({
        scrollContainer: function($table){
            return $table.closest('div');
        }
    });
    
	//테이블 선택,헤제
	/*$('.tbl_scroll tbody tr').click(function(){
    	
    	if($(this).hasClass('on')){
    		$(this).removeClass('on');
    	}else{
    		$(this).closest('tbody').find('tr').removeClass('on');
    		$(this).addClass('on');
    	};
    	return false;
    });*/
	
	//테이블 체크박스
	var checkboxes = document.querySelectorAll("tr input");

	for (var i = 0, l = checkboxes.length; i < l; i++) {
	    checkboxes[i].onclick = function(e) {
	        e.stopPropagation();
    	}
	};
    
});

</script>
</head>
<body>
<div id="div-loading" style="opacity:0.5;width:100%;height:100%;top:0;left:0;position:fixed;display:none;z-index:1;">
	<img src="${pageContext.request.contextPath}/resources/images/common/loading.gif" style="position:absolute;top:45%;left:45%;z-index:100;width:80px;"/>
</div>
	<div id="skipnavi">
		<ul>
		<li><a href="#menu">주메뉴 바로가기</a></li>
		<li><a href="#content">본문 바로가기</a></li>
		</ul>
	</div>
	
	<hr />
	
	<div id="wrapper">
		<!--  여기에 내용  -->
		<tiles:insertAttribute name="header"/>
		<hr />
		<tiles:insertAttribute name="content"/>
		<hr />
		<tiles:insertAttribute name="footer"/>
	</div>
</body>
</html>
