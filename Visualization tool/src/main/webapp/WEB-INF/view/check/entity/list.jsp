<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>

<script type="text/javascript" src="/resources/lib/jquery.svg-1.5.0/jquery.svg.min.js"></script> 
<script type="text/javascript" src="/resources/lib/jquery.svg-1.5.0/jquery.svgdom.min.js"></script>

<!-- brat setting -->
<link rel="stylesheet" type="text/css" href="/resources/css/brat/style-vis.css"/>
<script type="text/javascript" src="/resources/lib/brat/client/src/configuration.js"></script>
<script type="text/javascript" src="/resources/lib/brat/client/src/util.js"></script>
<script type="text/javascript" src="/resources/lib/brat/client/src/annotation_log.js"></script>
<script type="text/javascript" src="/resources/lib/brat/client/lib/webfont.js"></script>

<script type="text/javascript" src="/resources/lib/brat/client/src/dispatcher.js"></script>
<script type="text/javascript" src="/resources/lib/brat/client/src/url_monitor.js"></script>
<script type="text/javascript" src="/resources/lib/brat/client/src/visualizer.js"></script>

<script type="text/javascript" src="/resources/js/page/check/entity/list.js"></script>

<!-- content start -->
<div id="content">

	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>개체명 검증</h2>
		
		<div class="location">
			<ul>
			<li>Home</li>
			<li>레이블링 검증</li>
			<li class="loc_this">개체명 검증</li>
			</ul>
		</div>
	</div>
	<!--// page title end -->



	<div class="cont">
	<input type="hidden" name="groupName" id="groupName" value=""/>
		<!-- full area start -->
		<div class="full_area">
			<!-- 검색 start -->
			<div class="box_cyan mb_25">
				<div class="search_area">
					<label for="form_label1">개체명</label>
					<input type="text" id="entity" class="w300px ml_10 mr_30" title="개체명 입력" readonly>

					<label for="form_label2">키워드</label>
					<input type="text" id="searchTerm" onkeyup="javascript:fn_getKeyword();" onkeydown="javascript:if(event.keyCode==13){fn_search();}" class="w300px ml_10 mr_30" title="키워드 입력">
					<a href="javascript:fn_search();" class="btn_search">검색</a>
				</div>
			</div>
			<!--// 검색 end -->

			<div class="type_label02 clear2">
				<!-- 개체명 start -->
				<div class="label_01">
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
						</ul>
					</div>
				</div>
				<!--// 개체명 end -->

				<!-- 키워드 start -->
				<div class="label_02">
					<div class="cont_win">
						<div class="cont_tit2">키워드(총 <span id="keywordListCount">0</span>건)</div>
						<div class="cont_gray clear2" style="height:530px;">
							<ul id="keywordList" class="label_cyan_list">
							</ul>
						</div>
					</div>
				</div>
				<!--// 키워드 end -->

				<!-- 우측영역 start -->
				<div class="label_03">
					<div class="clear2">

						<!-- 레이블링 된 문서 start -->
						<div class="label_03_1">
							<div class="cont_win">
								<div class="cont_tit2"><span name="keyword"></span>레이블링 된 문서(총 <span id="labelingListCount">0</span>건)
									<div class="tit_opt type_label">
										<a href="javascript:fn_unlabeling();" class="btn_tit_box">언레이블링</a>
									</div>										
								</div>
								<div class="cont_gray clear2" style="height:205px;">
									<ul id="labelingList" class="label_cyan_list type_checkbox" >
									</ul>
								</div>
							</div>
						</div>
						<!--// 레이블링된 문서 end -->

						<!-- 레이블링 안된 문서 start -->
						<div class="label_03_2">
							<div class="cont_win">
								<div class="cont_tit2"><span name="keyword"></span>레이블링 안된 문서(총 <span id="unlabelingListCount">0</span>건)
								</div>
								<div class="cont_gray clear2" style="height:205px;">
									<ul id="unLabelingList" class="label_cyan_list type_checkbox">
									</ul>
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
						<input type="hidden" name="userId" id="userId" value="${user.userId}"/> 
						<input type="hidden" name="winNum" id="winNum" value=""/>
					</form>
						<div class="cont_tit2"><div id="docSubject" style="display:inline-block;">상세보기</div>
							<div class="tit_opt type_label">
								<a href="javascript:fn_keywordPrev();" id="btn_keywordPrev" class="btn_tit_box type_prev">이전</a>
								<a href="javascript:fn_keywordNext();" id="btn_keywordNext" class="btn_tit_box type_next">다음</a>
								<a href="javascript:fn_bratDetailView();" class="btn_tit_box">자세히보기</a>
								</div>
						</div>
						<div id="brat_scroll" class="cont_gray clear2" style="height:274px;">
							<div id="brat-loading" style="opacity:0.5;width:100%;height:100%;top:0;left:0;position:static;display:none;z-index: 99;">
								<img src="/resources/images/common/loading.gif" style="position:absolute;top:45%;left:45%;z-index:100;width:80px;"/>
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
	<li id="keyword_{{>content}}"><a onclick="javascript:fn_LabelingDoc('{{>content}}')">{{>content}}({{>count}}건)</a></li>
	{{/for}}
{{/if}}
</script>

<script id="tmpl_labelingDoc" type="text/x-jsrender">
{{if #data}}
	{{for labelingList}}
	<li id="doc_{{>docId}}"><input type="checkbox" name="labelingDoc" value="{{>docId}}"/><a onclick="javascript:fn_bratView('labeling','{{>docId}}')" href="#">{{>subject}} ({{>count}}건)</a></li>
	{{/for}}
{{/if}}
</script>

<script id="tmpl_unLabelingDoc" type="text/x-jsrender">
{{if #data}}
	{{for unlabelingList}}
	<li id="doc_{{>docId}}"><a onclick="javascript:fn_bratView('unlabeling','{{>docId}}')" href="#">{{>subject}}</a></li>
	{{/for}}
{{/if}}
</script>