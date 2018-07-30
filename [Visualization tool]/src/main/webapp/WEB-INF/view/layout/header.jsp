<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<!-- header start -->
<script>
function logout() {
	$("#logoutForm").submit();
}
	</script>
<div class="header">
	<!-- csrt for log out-->
	<c:url value="/logout" var="logoutUrl" /> 
	<form:form id="logoutForm" name="frm" action="${logoutUrl}" method="post">
		<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
	</form:form>
	<div class="head_top clear">
		<h1><a href="/check/labeling/list.do"><img src="/resources/images/common/logo.png" alt="학습 코퍼스 구축 도구" class="top_logo" /></a></h1>
		<ul class="util_menu">
			<li><a href="/work/user/edit.do?userId=${ sessionScope.userLoginInfo.userId }&mode=M" class="util_user" id="util_user">${sessionScope.userLoginInfo.username}</a></li>
			<li><a href="javascript:logout();" class="util_signout">Logout</a></li>
		</ul>
	</div>

	<!-- 주메뉴 start : 1depth 활성화시 li 에 class="on" 추가 -->
	<div id="menu">
		<ul id="main-menu">
			<li <c:if test="${currentMenu == 'dataManage'}">class="on"</c:if>>
			<a href="/data/domain/list.do">데이터 관리</a>
				<ul class="sub-menu">
				<li><a href="/data/domain/list.do">도메인/문서관리</a></li>
				<li><a href="/data/document/list.do">문서추가</a></li>
				</ul>
			</li>
			<li <c:if test="${currentMenu == 'auto'}">class="on"</c:if>>
			<a href="/auto/list.do">자동 레이블링</a>
			</li>
			<li <c:if test="${currentMenu == 'check'}">class="on"</c:if>>
			<a href="/check/labeling/list.do">레이블링 검증</a>
				<ul class="sub-menu">
					<li><a href="/check/labeling/list.do">레이블링 검증</a></li>
					<li><a href="/check/entity/list.do">개체명 검증</a></li>
					<li><a href="/check/relation/list.do">의존관계 검증</a></li>
				</ul>				
			</li>
			<li <c:if test="${currentMenu == 'create'}">class="on"</c:if>>
				<a href="/learning/list.do">학습데이터 생성</a>
			</li>
			<li <c:if test="${currentMenu == 'workManage'}">class="on"</c:if>>
				<a href="/work/document/list.do">작업관리</a>
				<ul class="sub-menu">
					<li><a href="/work/document/list.do">문서이력관리</a></li>
					<li><a href="/work/service/list.do">서비스작업관리</a></li>
					<li><a href="/work/user/list.do">계정관리</a></li>
				</ul>
			</li>
		</ul>
	</div>
	<!--// 주메뉴 end -->

</div>
<!--// header end -->