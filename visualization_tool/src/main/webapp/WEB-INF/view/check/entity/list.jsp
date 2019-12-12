<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>

<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/jquery.svg-1.5.0/jquery.svg.min.js"></script> 
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/jquery.svg-1.5.0/jquery.svgdom.min.js"></script>

<!-- brat setting -->
<link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/resources/css/brat/style-vis.css"/>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/brat/client/src/configuration.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/brat/client/src/util.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/brat/client/src/annotation_log.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/brat/client/lib/webfont.js"></script>

<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/brat/client/src/dispatcher.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/brat/client/src/url_monitor.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/resources/lib/brat/client/src/visualizer.js"></script>

<script type="text/javascript" src="${pageContext.request.contextPath}/resources/js/page/check/entity/list.js"></script>
<script type="text/javascript">
$.views.converters("dotrepl", function(val) {
	val = val.replace(/\./gi, '__');
	val = val.replace(/([\s]{1,})/gi, '_')
	val = val.replace(/(\+|\/)/gi, '__');
	val = val.replace(/\)|\(/gi,"--")
	val = val.replace(/(\\|\'|\"|\{|\})/gi, '_');
    return val.replace(/\./gi, '__')
});

$.views.converters("queteRepl", function(val) {
	val = encodeURIComponent(val);
	val = val.replace(/\'/gi, "\\'")
    return val;
});
</script>
<!-- content start -->
<div id="content">

	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>객체 검증</h2>
		
		<div class="location">
			<ul>
				<li>Home</li>
				<li>레이블링 검증</li>
				<li class="loc_this">객체 검증</li>
			</ul>
		</div>
	</div>
	<!--// page title end -->



	<div class="cont">
		<input type="hidden" name="groupName" id="groupName" value=""/>
		<input type="hidden" name="searchTerm" id="searchTerm" value=""/>
		<!-- full area start -->
		<div class="full_area">
			<!-- 검색 start -->
			<div class="box_cyan mb_25">
				<div class="search_area">
					<label for="form_label1">개체명</label>
					<input type="text" id="entity" class="w300px ml_10 mr_30" title="개체명 입력" readonly>

					<label for="form_label2">키워드</label>
					<input type="text" id="searchTermInfo" onkeydown="javascript:if(event.keyCode==13){fn_search();}" class="w300px ml_10 mr_30" title="키워드 입력">
					<a href="javascript:fn_search();" class="btn_search">검색</a>
				</div>
			</div>
			<!--// 검색 end -->

			<div class="type_label02 clear2">
				<!-- 개체명 start -->
				<div class="label_01" style="width: 16% !important;margin-right: 15px !important;">
					<div class="cont_win">
						<ul class="label_accordion">
							<li id="namedentity">
								<div class="cont_tit2 clear2 accordion_onoff">개체명<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:468px;">
									<div id="namedentity_tree_list">
										${namedentityJstreeHtml}
									</div>
								</div>
							</li>
							<li id="syntactic">
								<div class="cont_tit2 clear2 accordion_onoff">구문분석<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:468px;">
									<div id="syntactic_tree_list">
										${syntacticJstreeHtml}
									</div>
								</div>
							</li>
							<li id="causation">
								<div class="cont_tit2 clear2 accordion_onoff">인과관계<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:468px;">
									<div id="causation_tree_list">
										${causationJstreeHtml}
									</div>
								</div>
							</li>
							<li id="speech">
								<div class="cont_tit2 clear2 accordion_onoff">화행<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:468px;">
									<div id="speech_tree_list">
										${speechJstreeHtml}
									</div>
								</div>
							</li>
							<li id="simentic">
								<div class="cont_tit2 clear2 accordion_onoff">의미역 결정<a href="#" class="btn_label_onoff" title="펼치기"></a></div>
								<div class="cont_gray clear2" style="height:468px;">
									<div id="simentic_tree_list">
										${simenticJstreeHtml}
									</div>
								</div>
							</li>
						</ul>
					</div>
				</div>
				<!--// 개체명 end -->

				<!-- 키워드 start -->
				<div class="label_02" style="width: 25% !important;">
					<div class="cont_win">
						<div class="cont_tit2">키워드 <span id="selectTag"></span> (총 <span id="keywordListCount">0</span>건)</div>
						<div class="cont_gray clear2" style="height:592px;">
							<!-- 
							<ul id="keywordList" class="label_cyan_list">
							</ul>
							-->
							
							<table id="entityKeywordList" class="tbl_scroll">
								<colgroup>
									<col />
									<col style="width:34%;" />
									<col style="width:37%;" />
								</colgroup>
								<thead>
									<tr>
										<th scope="col">키워드</th>
										<th scope="col">레이블개수 <a id="sort_count" href="javascript:fn_keywordSort('count')">-</a></th>
										<th scope="col">오류추정개수 <a id="sort_subCount" href="javascript:fn_keywordSort('subCount')">▼</a></th>
									</tr>
								</thead>
								<tbody id="keywordList">
									
								</tbody>
							</table>
						</div>
					</div>
				</div>
				<!--// 키워드 end -->

				<!-- 우측영역 start -->
				<div class="label_03" style="width:57.3% !important;">
					<div class="clear2">

						<!-- 레이블링 된 문서 start -->
						<div class="label_03_1">
							<div class="cont_win">
								<div class="cont_tit2"><span id="labelingDocTag"></span> 레이블 된 문서 <span id="labelingListCount">0</span>건(키워드 <span id="labelingCount">0</span>개)
									<div class="tit_opt type_label">
										<a href="javascript:fn_unlabeling();" class="btn_tit_box">언레이블링</a>
									</div>										
								</div>
								<div class="cont_gray clear2" style="height:220px;">
									<!--
									<ul id="labelingList" class="label_cyan_list type_checkbox" >
									</ul>
									-->
							
									<table class="tbl_scroll">
										<colgroup>
											<col style="width:50px;" />
											<col />
											<col style="width:80px;" />
										</colgroup>
										<thead>
											<tr>
												<th scope="col"><input type="checkbox" id="labelDocChkAll" title="전체 선택/해제" /></th>
												<th scope="col">문서제목</th>
												<th scope="col">건수</th>
											</tr>
										</thead>
										<tbody id="labelingList">
										</tbody>
									</table>									
								</div>
							</div>
						</div>
						<!--// 레이블링된 문서 end -->

						<!-- 레이블링 안된 문서 start -->
						<div class="label_03_2">
							<div class="cont_win">
								<div class="cont_tit2">레이블을 하지 않은 문서 <span id="unlabelingListCount">0</span>건</div>
								<div class="cont_gray clear2" style="height:220px;">
									<!-- 
									<ul id="unLabelingList" class="label_cyan_list type_checkbox">
									</ul>
									-->

									<table class="tbl_scroll">
										<colgroup>
											<col />
											<col style="width:100px;" />
										</colgroup>
										<thead>
											<tr>
												<th scope="col">문서제목</th>
												<th scope="col">등록자</th>
											</tr>
										</thead>
										<tbody id="unLabelingList">
										</tbody>
									</table>	
																		
								</div>
							</div>
						</div>
						<!--// 레이블링 안된 문서 end -->

					</div>

					<!-- 상세보기 start -->
					<div class="cont_win mt_20">
					<form id="docInfo">
						<input type="hidden" name="docId" id="docId" value=""/> 
						<input type="hidden" name="groupName" id="docGroupName" value=""/>
						<input type="hidden" name="keywords" id="keyword" value=""/>
						<input type="hidden" name="domain" id="domain" value=""/> 
						<input type="hidden" name="userId" id="userId" value="${user.userId}"/> 
						<input type="hidden" name="winNum" id="winNum" value=""/>
						<input type="hidden" name="docType" id="docType" value=""/>
					</form>
					<input type="hidden" name="labelGrade" id="labelGrade" value=""/> 
						<div class="cont_tit2"><div id="docSubject" style="display:inline-block;">상세보기</div>
							<div class="tit_opt type_label">
								<a href="javascript:fn_keywordPrev();" id="btn_keywordPrev" class="btn_tit_box type_prev">이전</a>
								<a href="javascript:fn_keywordNext();" id="btn_keywordNext" class="btn_tit_box type_next">다음</a>
								<a href="javascript:fn_bratEdit();" class="btn_tit_box">편집</a>
							</div>
						</div>
						<div id="brat_scroll" class="cont_gray clear2" style="height:320px;">
							<div id="brat-loading" style="opacity:0.5;width:100%;height:100%;top:0;left:0;position:static;display:none;z-index: 99;">
								<img src="${pageContext.request.contextPath}/resources/images/common/loading.gif" style="position:absolute;top:45%;left:45%;z-index:100;width:80px;"/>
							</div> 
							<div id="brat_viewer1"></div>
							
						</div>
					</div>
					<!--// 상세보기 end -->

				</div>
				<!--// 우측영역 end -->

			</div>
		
		</div>
		<!--// full area end -->

	</div>

</div>
<!--// content end -->

<script id="tmpl_keyword" type="text/x-jsrender">
{{if #data}}
	{{for keywordList}}
		<tr id="keyword_{{dotrepl:content}}" onclick="javascript:fn_LabelingDoc(decodeURIComponent('{{queteRepl:content}}'))">
			{{if content.length > 5}}
				<td class="left" title="{{>content}}">{{>content.substring(0, 5)}}...</td>
			{{else}}
				<td class="left">{{>content}}</td>
			{{/if}}
			<td class="right">{{>count}}</td>
			<td class="right">{{>subCntFmt}}</td>
		</tr>
	{{/for}}
{{/if}}
</script>

<script id="tmpl_labelingDoc" type="text/x-jsrender">
{{if #data}}
	{{for labelingList}}
		<tr id="doc_{{>docId}}" >
			<td><input type="checkbox" name="labelDocChk" value="{{>docId}}"/></td>
			<td onclick="javascript:fn_bratView('labeling','{{>docId}}','{{>recordId}}')" class="left">{{>subject}}</td>
			<td onclick="javascript:fn_bratView('labeling','{{>docId}}','{{>recordId}}')" class="right">{{>count}}</td>
		</tr>
	{{/for}}
{{/if}}
</script>

<script id="tmpl_unLabelingDoc" type="text/x-jsrender">
{{if #data}}
	{{for unlabelingList}}
		<tr id="doc_{{>docId}}" onclick="javascript:fn_bratView('unlabeling','{{>docId}}','{{>recordId}}')">
			<td class="left">{{>subject}}</td>
			<td>{{>regId}}</td>
		</tr>
	{{/for}}
{{/if}}
</script>