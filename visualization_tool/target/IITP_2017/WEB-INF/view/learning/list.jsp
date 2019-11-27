<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/page/learning/list.js"></script>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags"%>

<div id="content">
	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>학습데이터 생성</h2>
	
		<div class="location">
			<ul>
			<li>Home</li>
			<li class="loc_this">학습데이터 생성</li>
			</ul>
		</div>
	</div>
	<!--// page title end -->

	<div class="cont">
		
		<!-- full area start -->
		<div class="full_area">
			<div class="type_domain01 clear2">
				<!-- 문서집합 관리 트리 start -->
				<div class="cont_win domain_01">
					<div class="cont_tit2">문서 집합</div>
					<div class="cont_gray clear2">
						<div id="domain_tree_list">
							 ${domainJstreeHtml}
						</div>
					</div>
				</div>
				<!--// 문서집합 관리 트리 end -->
				
				<div class="cont_win domain_02">
					<form id="searchForm" action="${pageContext.request.contextPath}/learning/list.do?_format=json" method="post">
						<input type="hidden" id="pageSize" name="pageSize" value="${doc.pageSize}"/>
						<input type="hidden" id="colId" name="colId" value="${doc.colId}" />
						<input type="hidden" id="searchTerm" name="searchTerm" value="" />
						<input type="hidden" id="domain" name="domain" value=""/> 
						<input type="hidden" id="searchTermOpt" name="searchTermOpt" value="" />
						<!-- 레이블링  대상 항목 start -->				
						<div class="box_cyan mb_25 ">
							<fieldset><legend>레이블링  대상 항목</legend>
								<div class="radio_select">
									<span>레이블링  대상 항목 선택</span>
									<ul>
										<li><input type="radio" name="groupName" value="namedentity" <c:if test="${doc.groupName == 'namedentity'}">checked</c:if>>개체명</li>
										<li><input type="radio" name="groupName" value="syntactic" <c:if test="${doc.groupName == 'syntactic'}">checked</c:if>>구문분석</li>
										<li><input type="radio" name="groupName" value="causation" <c:if test="${doc.groupName == 'causation'}">checked</c:if>>인과관계</li>
										<li><input type="radio" name="groupName" value="speech" <c:if test="${doc.groupName == 'speech'}">checked</c:if>>화행</li>
										<li><input type="radio" name="groupName" value="simentic" <c:if test="${doc.groupName == 'simentic'}">checked</c:if>>의미역 결정</li>
									 </ul>
								</div>
							</fieldset>
						</div>
					</form>	
					<!--// 레이블링  대상 항목 end -->	
					<!-- 문서목록 start -->
					<div class="mt_30">
						<div class="cont_tit2 sub_tit">
							<c:if test="${not empty doc.domain}">"${doc.domain}"</c:if>
							<c:if test="${empty doc.domain}">전체</c:if> 문서목록</div>
							<div class="board_top clear2">
								<!-- 목록 검색 start -->
								<div class="float_l">
									<fieldset><legend><label for="boardtop01_left">검색</label></legend>
										<select id="boardtop01_left" onchange="javascript:fn_searchTermOpt();">
											<option value="all" <c:if test="${doc.searchTermOpt == 'all'}">selected</c:if>>전체</option>
											<option value="labeling" <c:if test="${doc.searchTermOpt == 'labeling'}">selected</c:if>>레이블링</option>
											<option value="domain" <c:if test="${doc.searchTermOpt == 'domain'}">selected</c:if>>문서제목</option>
											<option value="confY" <c:if test="${doc.searchTermOpt == 'confY'}">selected</c:if>>작업완료 확인 여부(Y)</option>
											<option value="confN" <c:if test="${doc.searchTermOpt == 'conN'}">selected</c:if>>작업완료 확인 여부(N)</option>
											<option value="confId" <c:if test="${doc.searchTermOpt == 'confId'}">selected</c:if>>작업완료 확인자</option>
											<option value="subject" <c:if test="${doc.searchTermOpt == 'subject'}">selected</c:if>>문서제목</option>
											<option value="regId" <c:if test="${doc.searchTermOpt == 'regId'}">selected</c:if>>등록자</option>
										</select>
										<input type="text" id="inputTerm" class="white w200px" title="검색어 입력" onkeydown="javascript:if(event.keyCode==13){fn_search();}" value="${doc.searchTerm}" />
										<a href="javascript:fn_search();" class="btn b_orange medium valign_m">검색</a>	
									</fieldset>
								</div>
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
							<form id="labeling_form" name="labeling_form" action="${pageContext.request.contextPath}/learning/start.do?_format=json">
							<input type="hidden" id="learningGroupName" name="groupName" value="${doc.groupName}"/>
				            <table class="tbl_type03 h_type03 mt_10">
							    <caption>문서 목록</caption>
				                <colgroup>
				                    <col style="width:40px;">
				                    <col style="width:70px;">
				                    <col style="width:70px;">
				                    <col style="width:70px;">
				                    <col style="width:70px;">
				                    <col style="width:70px">
				                    <col style="width:150px;">
				                    <col style="width:70px;">
				                    <col style="width:100px;">
				                    <col style="width:80px;">
				                    <col style="width:150px;">
				                </colgroup>
				                <thead>
				                	<tr>
				                		<th scope="col"><input type="checkbox" class="toggle_checkbox" title="전체 선택/해제" /></th>
				                		<th scope="col">학습상태</th>
				                		<th scope="col">레이블링</th>
				                		<th scope="col">그룹명</th>
				                		<th scope="col">도메인</th>
				                		<th scope="col">문서제목 (파일명)</th>
				                		<th scope="col">내용</th>
				                		<th scope="col">등록자</th>
				                		<th scope="col">작업완료확인</th>
				                		<th scope="col">등록일</th>
				                		<th scope="col">Action</th>
				                	</tr>
				                </thead>
				                <tbody>
				                 <c:if test="${not empty list}">
									<c:forEach var="result" items="${list}">
				                	<tr>
				                		<td><input type="checkbox" name="docIds" value="${result.docId}"/></td>
				                		<td id="learningStatus_${result.docId}">${result.learnStat}</td>
					                	<td>${result.rabelStat}</td>
			                			<td> 
				                			<c:if test="${result.groupName == 'namedentity'}">개체명</c:if>
				                			<c:if test="${result.groupName == 'syntactic'}">구문분석</c:if>
				                			<c:if test="${result.groupName == 'causation'}">인과관계</c:if>
				                			<c:if test="${result.groupName == 'simentic'}">의미역 결정</c:if>
				                			<c:if test="${result.groupName == 'speech'}">화행</c:if>
			                			</td>
					                	<td title='<c:if test="${not empty result.domainPath}">${result.domainPath}/</c:if>${result.domain}'>
					                		${result.domain}
					                	</td>
					                	<td title="${result.subject}"><div class="of_hidden">${result.subject}</div></td>
					                	<td title="${result.content} .." class="left"><div class="of_hidden">${result.content}</div></td>
					                	<td>${result.regId}</td>
				                		<td>${result.confId}</td>
				                		<td><fmt:formatDate value="${result.regDate}" pattern="yyyy-MM-dd"/></td>
					                	<td style="text-align:left">
				                			<a href="javascript:fn_learning('${result.docId}');" class="btn_td btn_tbl_labeling">데이터 생성</a>
				                			<c:if test="${ result.learnStat eq '자동' || result.learnStat eq '완료' }">
				                				<a href="javascript:fn_downloadPop('${result.docId}');" id="down_${result.docId}" class="btn_td btn_tbl_download">다운로드</a>
				                			</c:if>
				                		</td>
				                	</tr>
				                	</c:forEach>
				                </c:if>
				                <c:if test="${empty list}">
									<tr>
										<td colspan="11">결과가 없습니다.</td>
									</tr>
								</c:if>
				                </tbody>
							</table>
				            </form>
							<t:pagination ref="${pagination}" />
							<!--// 페이징 end -->
							
							<div class="align_r mt_5">
								<a href="javascript:alert('준비중입니다');" class="btn b_gray medium">전체 학습 데이터 생성</a>					
								<a href="javascript:void(0);" id="btn_learning_start" class="btn b_gray medium">선택항목 학습 데이터 생성</a>
								<a href="javascript:void(0);" id="btn_download_start" class="btn b_gray medium">선택항목 학습 데이터 다운로드</a>				
							</div>							
						</fieldset>
						<!--// 목록 end -->
														
					</div>					
					<!--// 문서목록 end -->
					
				</div>
				<!--// 도메인 관리   end -->

			</div>


		
		</div>
		<!--// full area end -->

	</div>

</div>
<!--// content end -->
<form id="popupForm" name="popupForm" action="" method="post">
	<input type="hidden" id="docId" name="docId" value="" />
	<input type="hidden" id="groupName" name="groupName" value="" />
</form>