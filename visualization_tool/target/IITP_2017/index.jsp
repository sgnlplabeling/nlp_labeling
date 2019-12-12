<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<script>
<%
if(session.getAttribute("userLoginInfo") != null){
%>
location.href="${pageContext.request.contextPath}/check/labeling/list.do";
<%
} else {
%>
location.href="${pageContext.request.contextPath}/login/loginForm.do";
<%
}
%>
</script>
