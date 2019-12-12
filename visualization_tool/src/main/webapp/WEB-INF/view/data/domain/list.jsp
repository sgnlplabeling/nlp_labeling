<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/page/data/domain/list.js"></script>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags"%>
<!-- content start -->
<div id="content">
	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>도메인/문서 관리</h2>
	
		<div class="location">
			<ul>
			<li>Home</li>
			<li>데이터 관리</li>
			<li class="loc_this">도메인/문서 관리</li>
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
					<!-- 도메인 관리 start -->				
					<div>
						<fieldset><legend>도메인 관리</legend>
							<table class="tbl_write type_slim">
				                <caption>도메인 관리 양식</caption>
				                <colgroup>
				                    <col style="width: 150px;">
				                    <col>
				                </colgroup>
				                <tbody>
									<tr>
										<th scope="row"><label for="domain">도메인</label></th>
										<td><input type="text" name="domain" id="domain" class="gray w300px" readonly/></td>
									</tr>
									<tr>
										<th scope="row"><label for="domainName">도메인명</label></th>
										<td><input type="text" name="domainName" id="domainName" class="gray w300px"/></td>
									</tr>
									<tr>
										<th scope="row"><label for="name">하위도메인 추가</label></th>
										<td><input type="text" name="name" id="name" class="gray w300px" />
										<a href="javascript:fn_DomainAdd();" class="btn b_gray medium valign_m ml_5">추가</a></td>
									</tr>
								</tbody>
							</table>
						</fieldset>
						<div class="align_r mt_10">
						<!-- <a href="javascript:fn_domainInit();" class="btn b_gray medium">초기화</a>										
							 -->	
							<a href="javascript:fn_domainEdit();" class="btn b_gray medium">수정</a>	
							<a href="javascript:fn_domainDelete();" class="btn b_gray medium">삭제</a>				
						</div>
					</div>
					<!--// 도메인 관리 end -->
					
					<!-- 문서목록 start -->
					<div class="mt_30">
						<div class="cont_tit2 sub_tit">문서목록</div>
						<div class="board_top clear2">
						<!-- 목록 검색 start -->
							<form id="searchForm" action="${pageContext.request.contextPath}/data/domain/list.do?_format=json" method="post">
								<input type="hidden" id="pageSize" name="pageSize" value="${doc.pageSize}"/>
								<input type="hidden" id="colId" name="colId" value="${doc.colId}"/>
								
								<div class="float_l">
									<fieldset><legend><label for="searchTermOpt">검색</label></legend>
										<select name="searchTermOpt" id="searchTermOpt" onchange="javascript:fn_searchTermOpt();">
												<option value="all" <c:if test="${doc.searchTermOpt == 'all'}">selected</c:if>>전체</option>
												<option value="labeling" <c:if test="${doc.searchTermOpt == 'labeling'}">selected</c:if>>레이블링</option>
												<option value="domain" <c:if test="${doc.searchTermOpt == 'domain'}">selected</c:if>>도메인</option>
												<option value="confY" <c:if test="${doc.searchTermOpt == 'confY'}">selected</c:if>>작업완료 확인 여부(Y)</option>
												<option value="confN" <c:if test="${doc.searchTermOpt == 'conN'}">selected</c:if>>작업완료 확인 여부(N)</option>
												<option value="confId" <c:if test="${doc.searchTermOpt == 'confId'}">selected</c:if>>작업완료 확인자</option>
												<option value="subject" <c:if test="${doc.searchTermOpt == 'subject'}">selected</c:if>>문서제목</option>
												<option value="regId" <c:if test="${doc.searchTermOpt == 'regId'}">selected</c:if>>등록자</option>
											</select>
											<input type="text" name="searchTerm" id="searchTerm" class="white w200px" title="검색어 입력" onkeydown="javascript:if(event.keyCode==13){fn_search();}" value="${doc.searchTerm}" />
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
						<form id="delete_form" action="${pageContext.request.contextPath}/data/document/delete.do?_format=json">
							<table id="docTable" class="tbl_type03 h_type03 mt_10">
				                <caption>문서 목록</caption>
				                <colgroup>
				                    <col style="width:40px;">
				                    <col style="width:100px;">
				                    <col style="width:150px;">
				                    <col>
				                    <col style="width:7%;">
				                    <col style="width:80px;">
				                    <col style="width:100px;">
				                    <col style="width:70px;">
				                    <col style="width:100px;">
				                    <col style="width:250px;">
				                </colgroup>
				                <thead>
				                	<tr>
				                		<th scope="col"><input type="checkbox" class="toggle_checkbox" title="전체 선택/해제" /></th>
				                		<th scope="col">도메인</th>
				                		<th scope="col">문서제목 (파일명)</th>
				                		<th scope="col">내용</th>
				                		<th scope="col">등록자</th>
				                		<th scope="col">등록일</th>
				                		<th scope="col">그룹명</th>
				                		<th scope="col">레이블링</th>
				                		<th scope="col">작업완료확인</th>
				                		<th scope="col">Action</th>
				                	</tr>
				                </thead>
				                <tbody>
				               		<c:set value="" var="pre_docId"/>
					                <c:if test="${not empty list}">
									<c:forEach var="result" items="${list}" varStatus="status">
										<tr>
											<c:if test="${pre_docId!=result.docId}">
												<c:choose>
													<c:when test="${result.count gt 0}">
														<td rowspan="${result.count}"><input type="checkbox" name="docId" value="${result.docId}"/></td>
								                		<td rowspan="${result.count}"  title='<c:if test="${not empty result.domainPath}">${result.domainPath}/</c:if>${result.domain}'>${result.domain}</td>
								                		<td rowspan="${result.count}" title="${result.subject}">${result.subject}</td>
								                		<td rowspan="${result.count}" title="${fn:substring(result.content,0,200)}" class="left"><div class="of_hidden">${fn:substring(result.content,0,300)}</div></td>
								                		<td rowspan="${result.count}">${result.regId} </td>
								                		<td rowspan="${result.count}"><fmt:formatDate value="${result.regDate}" pattern="yyyy-MM-dd"/></td>
							                		</c:when>
							                		<c:otherwise>
							                			<td><input type="checkbox" name="docId" value="${result.docId}"/></td>
								                		<td title='<c:if test="${not empty result.domainPath}">${result.domainPath}/</c:if>${result.domain}'>
								                			${result.domain}
								                		</td>
								                		<td title="${result.subject}">${result.subject}</td>
								                		<td title="${fn:substring(result.content,0,200)}" class="left"><div class="of_hidden">${fn:substring(result.content,0,300)}</div></td>
								                		<td>${result.regId} </td>
								                		<td><fmt:formatDate value="${result.regDate}" pattern="yyyy-MM-dd"/></td>
							                		</c:otherwise>
						                		</c:choose>
											</c:if>
											<td>
					                			<c:if test="${result.groupName == 'namedentity'}">개체명</c:if>
					                			<c:if test="${result.groupName == 'syntactic'}">구문분석</c:if>
					                			<c:if test="${result.groupName == 'causation'}">인과관계</c:if>
					                			<c:if test="${result.groupName == 'speech'}">화행</c:if>
					                			<c:if test="${result.groupName == 'simentic'}">의미역 결정</c:if>
					                		</td>
					                		<td>${result.rabelStat}</td>
					                		<td>${result.confId}</td>
					                		<td>
												<c:if test="${empty result.groupName}">
												<a href="javascript:fn_docDelete('${result.docId}');" class="btn_td btn_tbl_del" style="display:inline-block; width:100px;">문서삭제</a>
												</c:if>
												<c:if test="${not empty result.groupName}">
													<c:if test="${result.rabelStat != '처리중'}">
														<c:if test="${empty result.confId}">
							                				<a href="javascript:fn_saveConf('${result.recordId}');" class="btn_td btn_tbl_comp" style="display:inline-block; width:70px;">작업완료</a>
							                			</c:if>
							                			<c:if test="${not empty result.confId}">
							                				<a href="javascript:fn_cancelConf('${result.recordId}');" class="btn_td btn_tbl_comp_cancel" style="display:inline-block; width:70px;">작업완료 취소</a>
														</c:if>
							                			<a href="javascript:fn_recordDelete('${result.recordId}');" class="btn_td btn_tbl_del" style="display:inline-block; width:100px;">
							                			<c:if test="${result.groupName == 'namedentity'}">개체명</c:if>
							                			<c:if test="${result.groupName == 'syntactic'}">구문분석</c:if>
							                			<c:if test="${result.groupName == 'causation'}">인과관계</c:if>
							                			<c:if test="${result.groupName == 'speech'}">화행</c:if>
							                			<c:if test="${result.groupName == 'simentic'}">의미역 결정</c:if>
							                			삭제</a>
													</c:if>
												</c:if>
					                		</td>
					                		<c:set value="${result.docId}" var="pre_docId"/>
										</tr>
						                </c:forEach>
					                </c:if>
									<c:if test="${empty list}">
									<tr>
										<td colspan="10">결과가 없습니다.</td>
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

