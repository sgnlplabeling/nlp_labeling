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

<script type="text/javascript" src="/resources/js/page/check/labeling/list.js"></script>

<!-- content start -->
<div id="content">
	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>레이블링 검증</h2>
	
		<div class="location">
			<ul>
			<li>Home</li>
			<li class="loc_this">레이블링 검증</li>
			</ul>
		</div>
	</div>
	<!--// page title end -->

	<div class="cont">
		<form id="docInfo">
			<input type="hidden" name="docId" id="docId" value=""/> 
			<input type="hidden" name="colId" id="colId" value=""/>
			<input type="hidden" name="domain" id="domain" value=""/> 
			<input type="hidden" name="groupName" id="groupName" value=""/>
			<input type="hidden" name="searchTerm" id="searchTerm" value=""/>
			<input type="hidden" name="userId" id="userId" value="${user.userId}"/> 
		</form>
		<form id="bratCurrentDoc">
			<input type="hidden" name="docType" id="docType" value=""/> 
			<input type="hidden" name="winNum" id="winNum" value=""/> 
		</form>
		<input type="hidden" name="labelGrade" id="labelGrade" value=""/> 
		<!-- full area start -->
		<div class="full_area">
			<div class="type_label01 clear2">

				<!-- 도메인 start -->
				<div class="cont_win label_01">
					<div class="cont_tit2">문서집합</div>
					<div class="cont_gray clear2" style="height:630px;">
						<div id="domain_tree_list">
							 ${domainJstreeHtml}
						</div>
					</div>
				</div>
				<!--// 도메인 end -->

				<!-- 개체명 start -->
				<div class="label_02">
					<div class="cont_win">
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
						</ul>
					</div>
				</div>
				<!--// 개체명 end -->

				<div class="label_03">
					<!-- 문서목록 start -->
					<div class="cont_win">
						<div class="cont_tit2">문서목록 (총 <span id="docCount">0</span>건)
							<div class="tit_opt type_label">
								<span style="font-size:12px;font-weight:normal;padding:0 10px;display:inline-block;">검색</span>
								<input id="docSearchTerm" class="tit_search" onkeyup="javascript:fn_docList();" type="text"/>
							</div>
						</div>
					
						<div class="cont_gray clear2" style="height:130px;">
							<ul id="docList" class="label_cyan_list">
								
							</ul>
						</div>
					</div>
					<!--// 문서목록 end -->

					<!-- 1차 레이블링 start -->
					<div class="cont_win mt_20">
						<div class="cont_tit2">1차 레이블링 결과 (<div id="labelingGroup" style="display:inline-block;">개체명</div>)
							<div class="tit_opt type_label">
								<!-- <ul id="labelingType" class="ul_lc_none mr_10">
									<li><a onclick="javscript:fn_bratView('','all');" class="on">전체<span></span></a></li>
									<li><a onclick="javscript:fn_bratView('','entity');" >개체명<span></span></a></li>
									<li><a onclick="javscript:fn_bratView('','relation');">구문분석<span></span></a></li>
								</ul>
								 -->
								<a href="javascript:fn_bratEdit();" class="btn_tit_box">편집</a>
								<!--<a href="#" class="btn_tit_box">비교</a>  -->
							</div>
						</div>
						<div id="docContent" class="cont_gray clear2" style="height:450px;">
							<div id="brat-loading" style="opacity:0.5;width:100%;height:100%;top:0;left:0;position:static;display:none;z-index: 99;">
								<img src="/resources/images/common/loading.gif" style="position:absolute;top:45%;left:45%;z-index:100;width:80px;"/>
							</div>
							<div id="brat_viewer1"></div>
						</div>
					</div>
					<!--// 1차 레이블링 end -->

					<!-- 2차 레이블링 start 
					<div class="cont_win mt_20">
						<div class="cont_tit2">2차 레이블링
							<div class="tit_opt type_label">
								<ul class="ul_lc_none mr_10">
									<li><a href="#" class="on">전체<span></span></a></li>
									<li><a href="#">의미역<span></span></a></li>
									<li><a href="#">인과관계<span></span></a></li>
									<li><a href="#">화행<span></span></a></li>
								</ul>
								<a href="#" class="btn_tit_box">편집</a>
								<a href="#" class="btn_tit_box">비교</a>
							</div>
						</div>
						<div class="cont_gray clear2" style="height:178px;">
						내용 삽입<br />
						</div>
					</div>-->
					<!--// 2차 레이블링 end -->


				</div>
			</div>


		
		</div>
		<!--// full area end -->

	</div>

</div>
<!--// content end -->

<script id="tmpl_doc" type="text/x-jsrender">
{{if #data}}
	{{for docList}}
	<li><a onclick="javascript:fn_bratView('{{>docId}}')">{{>subject}}</a></li>
	{{/for}}
{{/if}}
</script>