<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<script type="text/javascript" src="/resources/js/page/work/service/list.js"></script>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags"%>

<!-- content start -->
<div id="content">
	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>서비스작업관리</h2><span>서비스 작업 이력을 관리할 수 있습니다.</span>
	
		<div class="location">
			<ul>
			<li>Home</li>
			<li>작업관리</li>
			<li class="loc_this">서비스작업관리</li>
			</ul>
		</div>
	</div>
	<!--// page title end -->

	<div class="cont">

		<!-- full area start -->
		<div class="full_area">
		
			<div class="board_top clear2">
				<form id="searchForm" action="/work/service/list.do?_format=json" method="post">
					<input type="hidden" id="pageSize" name="pageSize" value="${doc.pageSize}"/>
					
					<!-- 목록 검색 start -->
					<div class="float_l">
						<fieldset><legend>검색</legend>
							<label for="dateSearchOpt">기간</label>
							<input type="text" class="w80px date_time white" title="시작날짜 입력" name="startDate" id="startDate" value="${doc.startDate}" readonly required/> 
							~ 
							<input type="text" class="w80px date_time white" title="마지막날짜 입력" name="endDate" id="endDate" value="${doc.endDate}" readonly required/>
	
							<label for="typeOpt" class="ml_20">유형</label>
							<select name="typeOpt" id="typeOpt">
								<option value="">전체</option>
								<option value="도메인" <c:if test="${doc.typeOpt == '도메인'}">selected</c:if>>도메인</option>
								<option value="문서" <c:if test="${doc.typeOpt == '문서'}">selected</c:if>>문서</option>
								<option value="회원" <c:if test="${doc.typeOpt == '회원'}">selected</c:if>>회원</option>
								<option value="개체" <c:if test="${doc.typeOpt == '개체'}">selected</c:if>>개체</option>
								<option value="관계" <c:if test="${doc.typeOpt == '관계'}">selected</c:if>>관계</option>
								<option value="레이블링" <c:if test="${doc.typeOpt == '레이블링'}">selected</c:if>>레이블링</option>
								<option value="학습데이터" <c:if test="${doc.typeOpt == '학습데이터'}">selected</c:if>>학습데이터</option>
							</select>
							
							<label for="searchTermOpt" class="ml_20">검색어</label>
							<select name="searchTermOpt" id="searchTermOpt">
								<option value="all" <c:if test="${doc.searchTermOpt == 'all'}">selected</c:if>>전체</option>
								<option value="subject" <c:if test="${doc.searchTermOpt == 'subject'}">selected</c:if>>문서제목</option>
								<option value="job" <c:if test="${doc.searchTermOpt == 'job'}">selected</c:if>>작업</option>
								<option value="note" <c:if test="${doc.searchTermOpt == 'note'}">selected</c:if>>내용</option>
								<option value="regId" <c:if test="${doc.searchTermOpt == 'regId'}">selected</c:if>>등록자</option>
							</select>
							<input type="text" name="searchTerm" id="searchTerm" class="white w200px" title="검색어 입력" value="${doc.searchTerm}">
							<input type="submit" class="btn b_orange medium valign_m" value="검색" />	
						</fieldset>
					</div>
					<!--// 목록 검색 end -->
				</form>
				<!-- 목록 표시 개수 start -->							
				<div class="float_r">
					<fieldset><legend><label for="boardtop01_right">표시개수</label></legend>
						<select id="boardtop01_right">
							<option value="10" <c:if test="${doc.pageSize == '10'}">selected</c:if>>10</option>
							<option value="15" <c:if test="${doc.pageSize == '15'}">selected</c:if>>15</option>
							<option value="20" <c:if test="${doc.pageSize == '20'}">selected</c:if>>20</option>
							<option value="30" <c:if test="${doc.pageSize == '30'}">selected</c:if>>30</option>
						</select>
						<a href="javascript:fn_pageSizeEdit();" class="btn b_gray medium valign_m">확인</a>
					</fieldset>									
				</div>
				<!--// 목록 표시 개수 end -->	
			</div>
			
			<!-- 목록 start -->
			<fieldset><legend>목록</legend>
	            <table class="tbl_type03 h_type03 mt_10">
				    <caption>문서 목록</caption>
	                <colgroup>
	                    <col style="width:80px;" />
	                    <col style="width:7%;" />
	                    <col style="width:10%;" />
	                    <col style="width:10%;" />
	                    <col style="width:10%;" />
	                    <col style="width:80px" />
	                    <col />
	                    <col style="width:100px;" />
	                    <col style="width:130px;" />
	                </colgroup>
	                <thead>
	                	<tr>
	                		<th scope="col">순번</th>
	                		<th scope="col">유형</th>
	                		<th scope="col">도메인</th>
	                		<th scope="col">문서제목</th>
	                		<th scope="col">Entity</th>
	                		<th scope="col">작업</th>
	                		<th scope="col">내용</th>
	                		<th scope="col">작업자</th>
	                		<th scope="col">작업일</th>
	                	</tr>
	                </thead>
	                <tbody>
					<c:if test="${not empty list}">
						<c:forEach var="result" items="${list}">
							<tr>
								<td>${result.id}</td>
								<td>${result.type}</td>
								<td>${result.domainPath}</td>
		                		<td><div class="of_hidden">${result.subject}</div></td>
								<td>
									<c:if test="${result.groupName == 'namedentity'}">개체명</c:if>
		                			<c:if test="${result.groupName == 'syntactic'}">구문분석</c:if>
		                			<c:if test="${result.groupName == 'causation'}">인과관계</c:if>
		                		</td>
		                		<td>${result.job}</td>
		                		<td style="text-align:left;">
			                		<c:if test="${result.type == 'labeling'}">
			                			<a href="/work/document/detail.do?recordId=${result.recordId}&recordSeq=${result.recordSeq}">${result.note}</a>
			                		</c:if>
			                		<c:if test="${result.type != 'labeling'}">${result.note}</c:if>
			                	</td>
		                		<td>${result.regId}</td>
		                		<td><fmt:formatDate value="${result.regDate}" pattern="yyyy-MM-dd HH:mm:ss"/></td>
	                		</tr>
			            </c:forEach>
	                </c:if>
					<c:if test="${empty list}">
					<tr>
						<td colspan="9">결과가 없습니다.</td>
					</tr>
					</c:if>
                </tbody>
				</table>
				<t:pagination ref="${pagination}" />	
				
			</fieldset>
			<!--// 목록 end -->		
		</div>
		<!--// full area end -->
	</div>
</div>