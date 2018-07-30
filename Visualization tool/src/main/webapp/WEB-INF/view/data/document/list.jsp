<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<script type="text/javascript" src="/resources/js/page/data/document/list.js"></script>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags"%>
<!-- content start -->
<div id="content">
	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>문서 추가</h2>
	
		<div class="location">
			<ul>
			<li>Home</li>
			<li>데이터 관리</li>
			<li class="loc_this">문서 추가</li>
			</ul>
		</div>
	</div>
	<!--// page title end -->

	<div class="cont">
		<!-- full area start -->
		<div class="full_area">
			<div class="type_domain01 clear2">
				<!-- 문서 트리 start -->
				<div class="cont_win domain_01">
					<div class="cont_tit2">문서 집합</div>
					<div class="cont_gray clear2">
						<div id="domain_tree_list">
							 ${domainJstreeHtml}
						</div>
					</div>
				</div>
				<!--// 문서 트리 end -->
			
				<div class="cont_win domain_02">
					<!-- 문서추가 start -->				
					<form id="form_doc_insert" action="/data/document/insert.do?_format=json" method="post" enctype="multipart/form-data">
						<input type="hidden" id="colId" name="colId" value="" />
						<div>
							<fieldset><legend>문서추가</legend>
								<table class="tbl_write type_slim">
					                <caption>문서추가 양식</caption>
					                <colgroup>
					                    <col style="width: 150px;">
					                    <col>
					                </colgroup>
					                <tbody>
										<tr>
											<th scope="row"><label for="domain">도메인 선택</label></th>
											<td><input type="text" id="domain" name="domain" class="gray w50p" placeholder="왼쪽 Tree 목록에서 도메인을 선택해 주세요." readonly="readonly" required/></td>
										</tr>
										<tr>
											<th scope="row"><label for="file">파일선택</label></th>
											<td><input type="file" id="file" class="gray w50p" required/></td>
										</tr>
									</tbody>
								</table>
							</fieldset>
							
							<div class="align_r mt_10">
								<input type="submit" class="btn b_orange medium" value="신규문서 추가">
								<!-- <a href="#" class="btn b_orange medium">신규문서 추가</a>	-->				
							</div>
						</div>
					</form>
					<!--// 문서추가 end -->
					
					<!-- 추가된 문서목록 start -->
					<div class="mt_30">
						<div class="cont_tit2 sub_tit">추가된 문서 목록</div>
						<div class="board_top clear2">
						<!-- 목록 검색 start -->
						<form id="searchForm" action="/data/document/list.do?_format=json" method="post">
							<input type="hidden" id="docIds" name="docIds" value="${docIds}"/>
							<input type="hidden" id="pageSize" name="pageSize" value="${doc.pageSize}"/>

							<div class="float_l">
								<fieldset><legend><label for="boardtop01_left">검색</label></legend>
									<select name="searchTermOpt" id="searchTermOpt">
											<option value="all" <c:if test="${doc.searchTermOpt == 'all'}">selected</c:if>>전체</option>
											<option value="domain" <c:if test="${doc.searchTermOpt == 'domain'}">selected</c:if>>도메인</option>
											<option value="subject" <c:if test="${doc.searchTermOpt == 'subject'}">selected</c:if>>문서제목</option>
											<option value="content" <c:if test="${doc.searchTermOpt == 'content'}">selected</c:if>>내용</option>
										</select>
										<input type="text" name="searchTerm" id="searchTerm" class="white w200px" title="검색어 입력" onkeydown="javascript:if(event.keyCode==13){fn_search();}" value="${doc.searchTerm}" required/>
										<a href="javascript:fn_search();" class="btn b_orange medium valign_m">검색</a>	
								</fieldset>
							</div>
							</form>
							<!--// 목록 검색 end -->
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
						<form id="delete_form" action="/data/document/delete.do?_format=json">
							<table class="tbl_type03 h_type03 mt_10">
				                <caption>문서 목록</caption>
				                <colgroup>
				                    <col style="width:40px;">
				                    <col style="width:100px;">
				                    <col style="width:130px;">
				                    <col>
				                    <col style="width:7%;">
				                    <col style="width:80px;">
				                    <col style="width:100px;">
				                </colgroup>
				                <thead>
				                	<tr>
				                		<th scope="col"><input type="checkbox" class="toggle_checkbox" title="전체 선택/해제" /></th>
				                		<th scope="col">도메인</th>
				                		<th scope="col">문서제목 (파일명)</th>
				                		<th scope="col">내용</th>
				                		<th scope="col">등록자</th>
				                		<th scope="col">등록일</th>
				                		<th scope="col">Action</th>
				                	</tr>
				                </thead>
				                <tbody>
					                <c:if test="${not empty list}">
									<c:forEach var="result" items="${list}">
										<tr>
					                		<td><input type="checkbox" name="docId" value="${result.docId}"/></td>
					                		<td title='<c:if test="${not empty result.domainPath}">${result.domainPath}/</c:if>${result.domain}'>${result.domain}</td>
					                		<td title="${result.subject}"><div class="of_hidden">${result.subject}</div></td>
					                		<td title="${fn:substring(result.content,0,200)}" class="left"><div class="of_hidden">${fn:substring(result.content,0,300)}</div></td>
					                		<td>${result.regId} </td>
					                		<td ><fmt:formatDate value="${result.regDate}" pattern="yyyy-MM-dd"/></td>
						                	<td><a href="javascript:fn_docDelete('${result.docId}');" class="btn_td btn_tbl_del">문서삭제</a></td>
						                </tr>
					                </c:forEach>
					                </c:if>
									<c:if test="${empty list}">
									<tr>
										<td colspan="7">결과가 없습니다.</td>
									</tr>
									</c:if> 
				                </tbody>
							</table>
							</form>
							<t:pagination ref="${pagination}" />						
							<!--// 페이징 end -->
							
							<div class="align_r mt_5">
								<a href="#" class="btn b_gray medium" id="btn_doc_delete">선택항목 삭제</a>					
							</div>							
						</fieldset>
						<!--// 목록 end -->			
					</div>					
					<!--// 추가된 문서목록 end -->
				</div>
				<!--// 도메인 관리   end -->
			</div>
		</div>
		<!--// full area end -->

	</div>

</div>
<!--// content end -->