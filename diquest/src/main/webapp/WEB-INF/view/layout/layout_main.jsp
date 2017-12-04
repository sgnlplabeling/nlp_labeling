<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="tiles" uri="http://tiles.apache.org/tags-tiles" %>
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

<!-- jstree -->
<script type="text/javascript" src="/resources/lib/jstree-3.3.1/jstree.min.js"></script>
<link rel="stylesheet" type="text/css" href="/resources/lib/jstree-3.3.1/themes/default/style.min.css" />
 
<script type="text/javascript">
$(function(){
	var groupName = $('.label_accordion li:first-child').attr('id');
	if (groupName) {
		$("#groupName").val(groupName);
	}
	
	//개채명 외 아코디언
	$('.label_accordion li:first-child').addClass('on');
	$('.label_accordion li:first-child .cont_gray').show();
	$('.btn_label_onoff').click(function(){
		if(!$(this).closest('li').hasClass('on')){
			$(this).closest('.label_accordion').find('.cont_gray').slideUp('fast');
			$(this).closest('.label_accordion').find('li').removeClass('on');
			$(this).closest('.label_accordion').find('.btn_label_onoff').attr('title','펼치기');
			$(this).closest('li').addClass('on');
			$(this).parent().next('.cont_gray').slideDown('fast');
			$(this).attr('title','');
		};
		return false;
	});
	
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
</script>
</head>
<body>
<div id="div-loading" style="opacity:0.5;width:100%;height:100%;top:0;left:0;position:fixed;display:none;z-index:1;">
	<img src="/resources/images/common/loading.gif" style="position:absolute;top:45%;left:45%;z-index:100;width:80px;"/>
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
