<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/page/data/domain/list.js"></script>

<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags"%>
<link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/resources/lib/select2-4.0.3/css/select2-custom.css"/>
<script src="${pageContext.request.contextPath}/resources/lib/select2-4.0.3/js/select2.full.min.js"></script>
	
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/page/data/entity/list.js"></script>

<script type="text/javascript">
$(function(){

	tab_view = $('.tab_list').find('.on').length;
	
	if(tab_view==0){
		$('.tab_list > li').eq(0).addClass('on');
		$('.tab_content > div').eq(0).show();
	};
	
	$('.tab_list > li > a').click(function(){
		
		var index = $('.tab_list > li > a').index(this);
		$(this).closest('ul').children('li').removeClass('on');
		$(this).closest('li').addClass('on');
		
		$('.tab_content > div').hide();
		$('.tab_content > div').eq(index).show();
		return false;
	});

});
</script>

<!-- content start -->
<div id="content">
	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>레이블링 관리</h2>
	
		<div class="location">
			<ul>
			<li>Home</li>
			<li>데이터 관리</li>
			<li class="loc_this">레이블링 관리</li>
			</ul>
		</div>
	</div>
	<!--// page title end -->

	<div class="cont">
		<!-- full area start -->
		<div class="full_area">
			<div class="type_domain01 clear2">

				<!-- 트리 start -->
				<div class="cont_win domain_01 type_entity">

					<ul class="label_accordion">
						<li id="namedentity">
								<div class="cont_tit2 clear2 accordion_onoff">개체명<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:566px;">
									<div id="namedentity_tree_list">
										${namedentityJstreeHtml}
									</div>
								</div>
							</li>
							<li id="syntactic">
								<div class="cont_tit2 clear2 accordion_onoff">구문분석<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:566px;">
									<div id="syntactic_tree_list">
										${syntacticJstreeHtml}
									</div>
								</div>
							</li>
							<li id="causation">
								<div class="cont_tit2 clear2 accordion_onoff">인과관계<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:566px;">
									<div id="causation_tree_list">
										${causationJstreeHtml}
									</div>
								</div>
							</li>
							<li id="speech">
								<div class="cont_tit2 clear2 accordion_onoff">화행<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:566px;">
									<div id="speech_tree_list">
										${speechJstreeHtml}
									</div>
								</div>
							</li>
							<li id="simentic">
								<div class="cont_tit2 clear2 accordion_onoff">의미역 결정<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:566px;">
									<div id="simentic_tree_list">
										${simenticJstreeHtml}
									</div>
								</div>
							</li>
					</ul>

				</div>
				<!--// 트리 end -->
				
				<div class="cont_win domain_02">
				
					<!-- 관리 start -->				
					<fieldset><legend>관리</legend>
						<table class="tbl_write type_slim">
			                <caption>관리 양식</caption>
			                <colgroup>
			                    <col style="width: 150px;">
			                    <col>
			                </colgroup>
			                <tbody>
								<tr>
									<th scope="row"><label for="downOpt">설정데이터 다운로드</label></th>
									<td>
										<select id="downOpt">
											<option value="namedentity">개체명</option>
											<option value="syntactic">구문분석</option>
											<option value="causation">인과관계</option>
											<option value="simentic">의미역 결정</option>
											<option value="speech">화행</option>
										</select>
										<a href="javascript:fn_excelDown();" class="btn b_gray ssmall valign_m">다운로드</a>
									</td>
								</tr>
								<tr>
									<th scope="row"><label for="uploadOpt">일괄등록</label></th>
									<td>
										<select id="uploadOpt">
											<option value="namedentity">개체명</option>
											<option value="syntactic">구문분석</option>
											<option value="causation">인과관계</option>
											<option value="simentic">의미역 결정</option>
											<option value="speech">화행</option>
										</select>
										<input type="file" id="uploadFile" placeholder="파일을 선택해 주세요" class="gray w330px">	
										<a href="javascript:fn_upload();" class="btn b_gray ssmall valign_m">업로드 및 구축</a>
										<a href="javascript:fn_sampleDownload();" class="btn b_gray ssmall valign_m">양식 다운로드</a>	
									</td>
								</tr>
							</tbody>
						</table>
					</fieldset>
					<!--// 관리 end -->

					<!-- tab start -->
					<ul class="mt_30 tab_list">
						<c:if test="${not empty entity}">
							<li id="entityTab"><span></span><a href="#">Entity 편집</a></li>
						</c:if>
						<c:if test="${not empty relation}">
							<li id="relationTab"><span></span><a href="#">Relation 편집</a></li>
						</c:if>
					</ul>
					<!--// tab end -->
					<form id="searchForm">
						<input type="hidden" name="groupName" id="groupName" value="${common.groupName}"/>
						<input type="hidden" name="pageNo" id="pageNo" value="${common.pageNo}"/>
						<input type="hidden" name="selIds" id="selIds" value="${selIds[0]}"/>
						<input type="hidden" name="name" id="name" value="${selIds[0]}"/>
						<input type="hidden" name="count" id="count" value="${count}"/>
					</form>
					
					<c:if test="${not empty relation || not empty entity}">
					<div class="tab_content">
					<c:if test="${not empty entity}">
						<!-- Entity start -->
						<div>
						<form id="entityForm" method="post">
						<input type="hidden" name="entId" id="entId" value="${entity.entId}"/>
						<input type="hidden" name="groupName" id="entGroupName" value="${entity.groupName}"/>
						<!--  <input type="hidden" name="entIds" id="entIds" value="${entity.entIds}"/>
						-->
							<fieldset><legend>Entity 관리</legend>
								<table class="tbl_write type_slim mt_20">
					                <caption>Entity 관리 양식</caption>
					                <colgroup>
					                    <col style="width: 150px;">
					                    <col>
					                </colgroup>
					                <tbody>
					                	<tr>
											<th scope="row"><label for="lowEntity">신규 Entity 추가</label></th>
											<td>
												<span id="path"></span> > <input type="text" id="lowEntity" class="gray w200px " placeholder="개체명을 입력해주세요.">
											<!-- 	<label for="color02" class="ml_30">색상명</label>
												<input name="lowbgColor" id="chosen-color02" type="text" class="gray w50px align_c ml_10" value="#ff0000" readonly>
												<input id="color02" type="color" class="ml_5" value="#ff0000" onchange="javascript:document.getElementById('chosen-color02').value = document.getElementById('color02').value;">
											-->
												<a href="javascript:fn_lowEntityAdd();" class="btn b_gray ssmall valign_m">추가</a>
											</td>
										</tr>
										<tr>
											<th scope="row"><label for="entityName">선택 항목</label></th>
											<td>
												<input type="text" name="name" id="entityName" class="gray w500px" value="${entity.name}" readOnly>	
											</td>
										</tr>
										<tr>
											<th scope="row"><label for="entityLabel">라벨명</label></th>
											<td>
												<input type="text" name="label" id="entityLabel" class="gray w300px" value="${entity.label}">
												<label for="color01" class="ml_30">색상명</label>
												<input name="bgColor" id="chosen-color01" type="text" class="gray w50px align_c ml_10" value="${entity.bgColor}"  readonly>
												<input id="color01" type="color" class="ml_5" value="${entity.bgColor}" onchange="javascript:document.getElementById('chosen-color01').value = document.getElementById('color01').value;">
											</td>
										</tr>
									</tbody>
								</table>
							</fieldset>
						</form>
						</div>
						<!--// Entity end -->
						</c:if>
						
						<c:if test="${not empty relation}">
						<!-- Relation start -->	
						<div>	
						<form id="relationForm" method="post">
						<input type="hidden" name="groupName" id="relGroupName" value="${relation[0].groupName}"/>
						<input type="hidden" name="parentRel" id="relParentRel" value="${relation[0].parentRel}"/>
						<!--	<input type="hidden" name="relIds" id="relIds" value=""/>
						<input type="hidden" name="pageNo" id="pageNo" value=""/>-->
						
							<fieldset><legend>Relation 관리</legend>
								<table class="tbl_write type_slim mt_20">
					                <caption>Relation 관리 양식</caption>
					                <colgroup>
					                    <col style="width: 150px;">
					                    <col>
					                </colgroup>
					                <tbody>
										<tr>
											<th scope="row"><label for="form03_01">신규 Relation</label></th>
											<td>
												<span id="path"></span> > <input type="text" id="lowRelation" class="gray w200px" placeholder="관계명 입력">
												<a href="javascript:fn_lowRelationAdd();" class="btn b_gray ssmall valign_m">추가</a>		
											</td>
										</tr>
										<tr>
											<th scope="row"><label for="relationName">선택 항목</label></th>
											<td>
												<input type="text" name="name" id="relationName" class="gray w500px" value="${relation[0].name}" readOnly>
											</td>
										</tr>
										<tr>
											<th scope="row"><label for="relationLabel">라벨명</label></th>
											<td>
												<input type="text" name="label" id="relationLabel" class="gray w300px" value="${relation[0].label}">
											<!-- 180118 관계 색상은 지금 사용하지않음. JH
												<label for="color03" class="ml_30">색상명</label><input id="chosen-color03" type="text" class="gray w50px align_c ml_10" readonly value="#ff0000"><input id="color03" type="color" class="ml_5" value="#ff0000" onchange="javascript:document.getElementById('chosen-color03').value = document.getElementById('color03').value;">
											 -->
											 </td>
										</tr>
										<tr>
											<th scope="row"><label for="form03_03">소스 / 타겟</label></th>
											<td id="relList" >
											
											<c:set var="cnt" value="0"/>
											<c:forEach var="rel" items="${relation}" varStatus="relationStatus">
											<c:set var="endRelList" value="${fn:split(rel.endRel,'|')}" />
												<c:forEach var="endRel" items="${endRelList}" varStatus="endRelStatus">
												<div id="rel_${cnt}">
													<select class="select2" style="width: 200px;" id="startEnt" name="startRels['${cnt}']">
														<option value="" disabled>소스 선택</option>
														<c:forEach var="result" items="${entList}">
														<option value="${result.name}" <c:if test="${result.name == rel.startRel}">selected</c:if>>${result.name}</option>
														</c:forEach>
													</select>
													->
													<select class="select2" style="width: 200px;" id="endEnt" name="endRels['${cnt}']">
														<option value="" disabled>소스 선택</option>
														<c:forEach var="result" items="${entList}">
														<option value="${result.name}" <c:if test="${result.name == endRel}">selected</c:if>>${result.name}</option>
														</c:forEach>
													</select>
													<a name="btnArgDelete" href="javascript:fn_argDelete('rel_${cnt}');" class="btn b_gray ssmall_pm valign_m" title="삭제">X</a>
													<c:if test="${fn:length(relation) == relationStatus.count}">
													<c:if test="${fn:length(endRelList) == endRelStatus.count}">
														<a name="btnArgAdd" href="javascript:fn_argAdd();" class="btn b_gray ssmall_pm valign_m" title="추가">+</a>
													</c:if>
													</c:if>
												</div>
												<c:set var="cnt" value="${cnt+1}"/>
												</c:forEach>
											</c:forEach>
											
											</td>
										</tr>
									</tbody>
								</table>
							</fieldset>
							</form>
						</div>
						<!--// Relation end -->
						</c:if>
					</div>

					<div class="align_r mt_10">
						<a href="javascript:fn_edit();" class="btn b_gray medium">수정</a>	
						<a href="javascript:fn_delete();" class="btn b_gray medium">삭제</a>				
					</div>
					</c:if>
					
					<!-- 문서목록 start -->
					<div class="mt_30">
						<div class="cont_tit2 sub_tit"> 문서목록</div>
						<div class="board_top clear2">
							<!-- 목록 표시 개수 start -->							
							<div class="float_r">
								<!-- <fieldset><legend><label for="boardtop01_right">표시개수</label></legend>
									<select id="boardtop01_right">
										<option value="10" <c:if test="${doc.pageSize == '10'}">selected</c:if>>10</option>
										<option value="15" <c:if test="${doc.pageSize == '15'}">selected</c:if>>15</option>
										<option value="20" <c:if test="${doc.pageSize == '20'}">selected</c:if>>20</option>
										<option value="30" <c:if test="${doc.pageSize == '30'}">selected</c:if>>30</option>
									</select>
									<a href="javascript:fn_pageSizeEdit();" class="btn b_gray medium valign_m">확인</a>
								</fieldset>	 -->								
							</div>
							<!--// 목록 표시 개수 end -->	
						</div>
						
						<!-- 목록 start -->
						<fieldset><legend>목록</legend>
						<form id="delete_form" action="/data/document/delete.do?_format=json">
							<table id="docTable" class="tbl_type03 h_type03 mt_10">
				                <caption>문서 목록</caption>
				                <colgroup>
				                    <col style="width:40px;">
				                    <col style="width:70px;">
				                    <col style="width:100px;">
				                    <col style="width:15%;">
				                    <col>
				                    <col style="width:80px;">
				                    <col style="width:100px;">
				                    <col style="width:100px;">
				                    <col style="width:150px;">
				                </colgroup>
				                <thead>
				                	<tr>
				                		<th scope="col"><input type="checkbox" class="toggle_checkbox" title="전체 선택/해제" /></th>
				                		<th scope="col">레이블링</th>
				                		<th scope="col">도메인</th>
				                		<th scope="col">문서제목 (파일명)</th>
				                		<th scope="col">내용 (최대 100자)</th>
				                		<th scope="col">등록자</th>
				                		<th scope="col">작업완료확인</th>
				                		<th scope="col">등록일</th>
				                		<th scope="col">Action</th>
				                	</tr>
				                </thead>
				                <tbody id="docList">
				                	<c:forEach var="doc" items="${docList}">		
				                	<tr>
										<td><input type="checkbox" name="recordIds" value="${doc.recordId}"/></td>
										<td>${doc.rabelStat}</td>
										<td>${doc.domain}</td>
										<td><div class="of_hidden">${doc.subject}</div></td>
										<td class="left"><div class="of_hidden">${doc.content}</div></td>
										<td>${doc.regId}</td>
										<td>${doc.confId}</td>
										<td><fmt:formatDate value="${doc.regDate}" pattern="yyyy-MM-dd"/></td>
										<td><a href="javascript:fn_recordEntDelete('${doc.recordId}');" class="btn_td btn_tbl_del">
										<c:if test="${doc.groupName == 'namedentity'}">
											객체명
										</c:if>
										<c:if test="${doc.groupName == 'syntactic'}">
											구문분석
										</c:if>
										<c:if test="${doc.groupName == 'causation'}">
											인과관계
										</c:if>
										<c:if test="${doc.groupName == 'speech'}">
											화행
										</c:if>
										<c:if test="${doc.groupName == 'simentic'}">
											의미역 결정
										</c:if>
										 삭제</a></td>
									</tr>
									</c:forEach>
				                </tbody>
							</table>
							</form>
							<t:pagination ref="${pagination}" />
							<!--// 페이징 end -->
							
							<div class="align_r mt_5">
								<a href="javascript:alert('준비중입니다');" class="btn b_gray medium">전체 삭제</a>
								<a href="#" id="btn_record_delete" class="btn b_gray medium">선택항목 삭제</a>					
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
<script id="tmpl_selRel" type="text/x-jsrender">
{{if #data}}
	{{for relation ~len=relation.length}}
	<div id="ent_{{:#index}}">
		<select class="select2" style="width: 200px;" id="startEnt" name="startEnt">
			<option value="">소스 선택</option>
				{{for entlist}}
					<option value="">{{>name}}</option>
				{{/for}}
		</select>
		->
		<select class="select2" style="width: 200px;" id="endEnt" name="endEnt">
			<option value="">타겟 선택</option>
				
		</select>
 		{{if #index == ~len-1}}
			<a name="btnArgAdd" href="javascript:fn_argAdd();" class="btn b_gray ssmall_pm valign_m" title="추가">+</a>
		{{/if}}
			<a name="btnArgDelete" href="javascript:fn_argDelete('ent_{{:#index}}');" class="btn b_gray ssmall_pm valign_m" title="삭제">X</a>
		</div>
	{{/for}}
{{/if}}
</script>

<script id="tmpl_doc" type="text/x-jsrender">
{{if #data}}
	{{for list}}
		<tr>
			<td><input type="checkbox" name="recordIds" value="{{>recordId}}"/></td>
			<td>{{>rabelStat}}</td>
			<td>{{>domain}}</td>
			<td><div class="of_hidden">{{>subject}}</div></td>
			<td class="left"><div class="of_hidden">{{>content}}</div></td>
			<td>{{>regId}}</td>
			<td>{{>confId}}</td>
			<td>{{date:regDate}}</td>
			<td><a href="javascript:fn_recordEntDelete('{{>recordId}}');" class="btn_td btn_tbl_del">
			{{if groupName == 'namedentity'}}
				객체명
			{{/if}}
			{{if groupName == 'syntactic'}}
				구문분석
			{{/if}}
			{{if groupName == 'causation'}}
				인과관계
			{{/if}}
			 삭제</a></td>
		</tr>
	{{/for}}
{{/if}}
</script>