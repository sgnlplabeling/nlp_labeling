<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<script type="text/javascript" src="/resources/js/page/data/document/list.js"></script>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags"%>

<script>
	$(window).ready(function() {
		<c:if test="${ sessionScope.userLoginInfo.type ne 'SUPER' }">
			$("[type='radio']").attr('disabled', 'disabled');
		</c:if>
	});

	var isDuplication = true;

	function chkUserId() {
		var userId = $('#userId').val();
		
		$.ajax({
			url: "/work/user/chkUserId.do",
			method: "post",
			data: {userId:userId},
			success:function(data){
				if(data.count > 0) {
					alert("'" + userId + "'는  이미 사용중입니다.");	
				} else {
					alert("사용가능한 아이디입니다.");
					isDuplication = false;
				}
			},
		    error:function(request,status,error){
		        
		    },
			complete:function(){
				
			}
		});
	}
	
	function save(mode) {
		var userId = $.trim($('#userId').val());
		var username = $.trim($('#username').val());
		var newPwd = $.trim($('#newPwd').val());
		var newPwdConf = $.trim($('#newPwdConf').val());
		
	    if(username == ''){
	    	alert('이름을 입력하세요.');
	    	$('#username').focus();
	    	return;
	    }
        
		if(mode == 'C') {
			if(userId == ''){
		    	alert('아이디를 입력하세요.');
		    	$('#userId').focus();
		    	return;
		    } 
		    
		    if(userId.length < 3){
		    	alert('아이디는 최소 4자까지 입력돼야 합니다.');
		        $('#userId').select();
		        $('#userId').focus();
		        return;
		    }
		    
		    if(userId.length > 15){
		    	alert('아이디는 최대 15까지 입력할 수 있습니다.');
		    	$('#userId').select();
		        $('#userId').focus();
		        return;
		    }
			
			if(isDuplication) {
		    	alert('중복검사를 실시해 주시기 바랍니다.');
		    	return;
		    }
			
			if(userId.match(/[^A-Z가-힣0-9a-z]/gi) != null){
		    	alert('아이디에는 공백과 특수문자를 입력할 수 없습니다.');
		    	$('#userId').select();
		        $('#userId').focus();
		        return;
		    }
		    
		    if(newPwd == ''){
	        	alert('비밀번호를 입력하세요');
	            $('#newPwd').focus();
	            return;
	        }
			
			if(newPwd.length < 4){
	        	alert('비밀번호는 최소 4자까지 입력돼야 합니다.');
	            $('#newPwd').select();
	            $('#newPwd').focus();
	            return;
	        }
	        
	        if(newPwd.length > 12){
	        	alert('비밀번호 최대 12자리까지 입력할 수 있습니다.');
	            $('#newPwd').select();
	            $('#newPwd').focus();
	            return;
	        }
	        
	        if(newPwd.match(/\s/gi)){
	        	alert('비밀번호에는 공백이 포함될 수 없습니다.');
	        	$('#newPwd').select();
	            $('#newPwd').focus();
	            return;
	        }
	        
	        if(newPwd != newPwdConf){
	        	alert('입력한 비밀번호가 서로 일치하지 않습니다.');
	            $('#newPwdConf').focus();
	            return;
	        }
	        
	        $("#password").val(SHA256(newPwd));
	        
	        if(confirm("계정을 등록 하시겠습니까?")) {
	        	$.ajax({
	    			url: "/work/user/insertUser.do",
	    			method: "post",
	    			data: $("#userForm").serialize(),
	    			success:function(data){
	    				if(data.result == 'success') {
	    					alert("계정이 등록 되었습니다.");
	    					window.location.href = "/work/user/list.do";
	    				} else if(data.result == 'fail'){
	    					alert(data.message);
	    				} else {
	    					alert("계정등록을 실패하였습니다.");
	    				}
	    			},
	    		    error:function(request,status,error){
	    		        
	    		    },
	    			complete:function(){
	    				
	    			}
	    		});
	        }
		} else {
			if(confirm("계정을 수정 하시겠습니까?")) {
	        	$.ajax({
	    			url: "/work/user/updateUser.do",
	    			method: "post",
	    			data: $("#userForm").serialize(),
	    			success:function(data){
	    				if(data.result == 'success') {
	    					alert("계정이 수정 되었습니다.");
	    					window.location.href = "/work/user/edit.do?userId="+userId+"&mode=M";
	    				} else if(data.result == 'fail'){
	    					alert(data.message);
	    				} else {
	    					alert("계정 수정을 실패하였습니다.");
	    				}
	    			},
	    		    error:function(request,status,error){
	    		        
	    		    },
	    			complete:function(){
	    				
	    			}
	    		});
	        }
		}
	}
	
	function savePwd() {
		var userId = $.trim($('#userId').val());
		var curPassword = $.trim($('#curPassword').val());
		var newPwd = $.trim($('#newPwd').val());
		var newPwdConf = $.trim($('#newPwdConf').val());
        
		if(curPassword == ''){
        	alert('현재 비밀번호를 입력하세요');
            $('#password').focus();
            return;
        }
		
	    if(newPwd == ''){
        	alert('새 비밀번호를 입력하세요');
            $('#newPwd').focus();
            return;
        }
		
		if(newPwd.length < 4){
        	alert('새 비밀번호는 최소 4자까지 입력돼야 합니다.');
            $('#newPwd').select();
            $('#newPwd').focus();	
            return;
        }
        
        if(newPwd.length > 12){
        	alert('새 비밀번호 최대 12자리까지 입력할 수 있습니다.');
            $('#newPwd').select();
            $('#newPwd').focus();
            return;
        }
        
        if(newPwd.match(/\s/gi)){
        	alert('새 비밀번호에는 공백이 포함될 수 없습니다.');
        	$('#newPwd').select();
            $('#newPwd').focus();
            return;
        }
        
        if(newPwd != newPwdConf){
        	alert('입력한 새 비밀번호가 서로 일치하지 않습니다.');
            $('#newPwdConf').focus();
            return;
        }
        
        $('#password').val(SHA256(curPassword));
        $('#newPassword').val(SHA256(newPwd));
        
        if(confirm("비밀번호를 수정 하시겠습니까?")) {
        	$.ajax({
    			url: "/work/user/updateUserPwd.do",
    			method: "post",
    			data: $("#userForm").serialize(),
    			success:function(data){
    				if(data.result == 'success') {
    					alert("비밀번호가 수정 되었습니다.");
    					window.location.href = "/work/user/edit.do?userId="+userId+"&mode=M";
    				} else if(data.result == 'fail'){
    					alert(data.message);
    				} else {
    					alert("비밀번호 수정을 실패하였습니다.");
    				}
    			},
    		    error:function(request,status,error){
    		    },
    			complete:function(){
    			}
    		});
        }
	}
	
	function SHA256(s){
	    var chrsz   = 8;
	    var hexcase = 0;
	  
	    function safe_add (x, y) {
	        var lsw = (x & 0xFFFF) + (y & 0xFFFF);
	        var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
	        return (msw << 16) | (lsw & 0xFFFF);
	    }
	  
	    function S (X, n) { return ( X >>> n ) | (X << (32 - n)); }
	    function R (X, n) { return ( X >>> n ); }
	    function Ch(x, y, z) { return ((x & y) ^ ((~x) & z)); }
	    function Maj(x, y, z) { return ((x & y) ^ (x & z) ^ (y & z)); }
	    function Sigma0256(x) { return (S(x, 2) ^ S(x, 13) ^ S(x, 22)); }
	    function Sigma1256(x) { return (S(x, 6) ^ S(x, 11) ^ S(x, 25)); }
	    function Gamma0256(x) { return (S(x, 7) ^ S(x, 18) ^ R(x, 3)); }
	    function Gamma1256(x) { return (S(x, 17) ^ S(x, 19) ^ R(x, 10)); }
	  
	    function core_sha256 (m, l) {
	         
	        var K = new Array(0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1,
	            0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
	            0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786,
	            0xFC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
	            0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147,
	            0x6CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
	            0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B,
	            0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
	            0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A,
	            0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
	            0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2);

	        var HASH = new Array(0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19);

	        var W = new Array(64);
	        var a, b, c, d, e, f, g, h, i, j;
	        var T1, T2;
	  
	        m[l >> 5] |= 0x80 << (24 - l % 32);
	        m[((l + 64 >> 9) << 4) + 15] = l;
	  
	        for ( var i = 0; i<m.length; i+=16 ) {
	            a = HASH[0];
	            b = HASH[1];
	            c = HASH[2];
	            d = HASH[3];
	            e = HASH[4];
	            f = HASH[5];
	            g = HASH[6];
	            h = HASH[7];
	  
	            for ( var j = 0; j<64; j++) {
	                if (j < 16) W[j] = m[j + i];
	                else W[j] = safe_add(safe_add(safe_add(Gamma1256(W[j - 2]), W[j - 7]), Gamma0256(W[j - 15])), W[j - 16]);
	  
	                T1 = safe_add(safe_add(safe_add(safe_add(h, Sigma1256(e)), Ch(e, f, g)), K[j]), W[j]);
	                T2 = safe_add(Sigma0256(a), Maj(a, b, c));
	  
	                h = g;
	                g = f;
	                f = e;
	                e = safe_add(d, T1);
	                d = c;
	                c = b;
	                b = a;
	                a = safe_add(T1, T2);
	            }
	  
	            HASH[0] = safe_add(a, HASH[0]);
	            HASH[1] = safe_add(b, HASH[1]);
	            HASH[2] = safe_add(c, HASH[2]);
	            HASH[3] = safe_add(d, HASH[3]);
	            HASH[4] = safe_add(e, HASH[4]);
	            HASH[5] = safe_add(f, HASH[5]);
	            HASH[6] = safe_add(g, HASH[6]);
	            HASH[7] = safe_add(h, HASH[7]);
	        }
	        return HASH;
	    }
	  
	    function str2binb (str) {
	        var bin = Array();
	        var mask = (1 << chrsz) - 1;
	        for(var i = 0; i < str.length * chrsz; i += chrsz) {
	            bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (24 - i%32);
	        }
	        return bin;
	    }
	  
	    function Utf8Encode(string) {
	        string = string.replace(/\r\n/g,"\n");
	        var utftext = "";
	  
	        for (var n = 0; n < string.length; n++) {
	  
	            var c = string.charCodeAt(n);
	  
	            if (c < 128) {
	                utftext += String.fromCharCode(c);
	            }
	            else if((c > 127) && (c < 2048)) {
	                utftext += String.fromCharCode((c >> 6) | 192);
	                utftext += String.fromCharCode((c & 63) | 128);
	            }
	            else {
	                utftext += String.fromCharCode((c >> 12) | 224);
	                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
	                utftext += String.fromCharCode((c & 63) | 128);
	            }
	  
	        }
	  
	        return utftext;
	    }
	  
	    function binb2hex (binarray) {
	        var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
	        var str = "";
	        for(var i = 0; i < binarray.length * 4; i++) {
	            str += hex_tab.charAt((binarray[i>>2] >> ((3 - i%4)*8+4)) & 0xF) +
	            hex_tab.charAt((binarray[i>>2] >> ((3 - i%4)*8  )) & 0xF);
	        }
	        return str;
	    }
	  
	    s = Utf8Encode(s);
	    return binb2hex(core_sha256(str2binb(s), s.length * chrsz));
	  
	}
</script>
<form id="userForm" action="" method="post">
<input type="hidden" id="password" name="password"/>
<input type="hidden" id="newPassword" name="newPassword"/>
<!-- content start -->
<div id="content">
	<!-- page title start -->
	<div class="tit_page clear2">
		<h2>회원관리</h2><span>관리도구 회원을 관리할 수 있습니다.</span>
	
		<div class="location">
			<ul>
			<li>Home</li>
			<li>작업관리</li>
			<li class="loc_this">회원관리</li>
			</ul>
		</div>
	</div>
	<!--// page title end -->

	<div class="cont">

		<!-- full area start -->
		<div class="full_area">

					<!-- 회원 추가/수정 start -->				
					<div class="center_area">
						
						<fieldset><legend>회원 추가/수정</legend>
							<div class="cont_tit2 sub_tit">회원 추가 (수정)</div>
							<table class="tbl_write type_slim mt_10">
				                <caption>회원 추가/수정 양식</caption>
				                <colgroup>
				                    <col style="width: 150px;">
				                    <col>
				                </colgroup>
				                <tbody>
									<tr>
										<th scope="row"><label for="form01_01">아이디</label></th>
										<c:choose>
											<c:when test="${ param.mode eq 'C' }">
												<td><input type="text" id="userId" name="userId" class="gray w300px"/><a href="javascript:chkUserId();" class="btn b_gray ssmall ml_5">아이디 중복확인</a></td>
											</c:when>
											<c:when test="${ param.mode eq 'M' }">
												<td><input type="text" id="userId" name="userId" class="gray w300px" value="${ user.userId }" readonly="readonly" style="border: 0px solid #d1d1d1;background-color: white;"/>
											</c:when>
											<c:otherwise></c:otherwise>
										</c:choose>
									</tr>
									<tr>
										<th scope="row"><label for="form01_02">이름</label></th>
										<td><input type="text" id="username" name="username" class="gray w300px" value="${ user.username }"/></td>
									</tr>
									<tr>
										<th scope="row"><label for="form01_03">구분</label></th>
										<td>
											<select id="type" name="type" <c:if test="${ sessionScope.userLoginInfo.type ne 'SUPER' }">disabled=disabled</c:if>>
												<option value="SUPER" <c:if test="${ user.type eq 'SUPER' }">selected="selected"</c:if>>최고 관리자</option>
												<option value="ADMIN" <c:if test="${ user.type eq 'ADMIN' }">selected="selected"</c:if>>관리자</option>
												<option value="USER" <c:if test="${ user.type eq 'USER' }">selected="selected"</c:if>>사용자</option>
											</select>
										</td>
									</tr>
									<c:choose>
										<c:when test="${ param.mode eq 'C' }">
											<tr>
												<th scope="row"><label for="form01_05">비밀번호</label></th>
												<td><input type="password" id="newPwd" name="newPwd" class="gray w300px"/></td>
											</tr>
											<tr>
												<th scope="row"><label for="form01_06">비밀번호 확인</label></th>
												<td><input type="password" id="newPwdConf" name="newPwdConf" class="gray w300px"/></td>
											</tr>
										</c:when>
										<c:when test="${ param.mode eq 'M' }">
											<tr>
												<th scope="row"><label for="form01_04">현재 비밀번호</label></th>
												<td><input type="password" id="curPassword" name="curPassword" class="gray w300px"/><a href="javascript:savePwd();" class="btn b_gray ssmall ml_5">비밀번호 변경</a></td>
											</tr>
											<tr>
												<th scope="row"><label for="form01_05">새 비밀번호</label></th>
												<td><input type="password" id="newPwd" name="newPwd" class="gray w300px"/></td>
											</tr>
											<tr>
												<th scope="row"><label for="form01_06">새 비밀번호 확인</label></th>
												<td><input type="password" id="newPwdConf" name="newPwdConf" class="gray w300px"/></td>
											</tr>
										</c:when>
										<c:otherwise></c:otherwise>
									</c:choose>
									<tr>
										<th scope="row"><label for="form01_07">상세 설명</label></th>
										<td><input type="text" id="note" name="note" class="gray w300px" value="${ user.note }"/></td>
									</tr>

								</tbody>
							</table>
						</fieldset>
						
						<fieldset><legend>계정 권한 관리</legend>
							<div class="cont_tit2 sub_tit mt_30">계정 권한 관리</div>
							<table class="tbl_write type_slim mt_10">
				                <caption>계정 권한 관리 양식</caption>
				                <colgroup>
				                    <col style="width: 150px;">
				                    <col>
				                </colgroup>
				                <tbody>
									<tr>
										<th scope="row">도메인관리</th>
										<td>
											<ul class="user_authority">
												<li>
													<span>도메인</span>
													<ul>
														<li><input type="radio" id="authDomainMng_01" name="authDomainMng" value="NONE" <c:if test="${ user.authDomainMng eq 'NONE' || empty user.authDomainMng }">checked="checkted"</c:if>/><label for="radio01_01">권한없음</label></li>
														<li><input type="radio" id="authDomainMng_02" name="authDomainMng" value="SELF" <c:if test="${ user.authDomainMng eq 'SELF' }">checked="checkted"</c:if>/><label for="radio01_02">본인</label></li>
														<li><input type="radio" id="authDomainMng_03" name="authDomainMng" value="ALL" <c:if test="${ user.authDomainMng eq 'ALL' }">checked="checkted"</c:if>/><label for="radio01_03">전체</label></li>
													</ul>
												</li>
											</ul>
										</td>
									</tr>
									<tr>
										<th scope="row">문서관리</th>
										<td>
											<ul class="user_authority">
												<li>
													<span>문서</span>
													<ul>
														<li><input type="radio" id="authDocMng_01" name="authDocMng" value="NONE" <c:if test="${ user.authDocMng eq 'NONE' || empty user.authDocMng }">checked="checkted"</c:if>/><label for="radio02_01">권한없음</label></li>
														<li><input type="radio" id="authDocMng_02" name="authDocMng" value="SELF" <c:if test="${ user.authDocMng eq 'SELF' }">checked="checkted"</c:if>/><label for="radio02_02">본인</label></li>
														<li><input type="radio" id="authDocMng_03" name="authDocMng" value="ALL" <c:if test="${ user.authDocMng eq 'ALL' }">checked="checkted"</c:if>/><label for="radio02_03">전체</label></li>
													</ul>
												</li>
												<li>
													<span>태그</span>
													<ul>
														<li><input type="radio" id="authTagMng_01" name="authTagMng" value="NONE" <c:if test="${ user.authTagMng eq 'NONE' || empty user.authTagMng }">checked="checkted"</c:if>/><label for="radio03_01">권한없음</label></li>
														<li><input type="radio" id="authTagMng_02" name="authTagMng" value="SELF" <c:if test="${ user.authTagMng eq 'SELF' }">checked="checkted"</c:if>/><label for="radio03_02">본인</label></li>
														<li><input type="radio" id="authTagMng_03" name="authTagMng" value="ALL" <c:if test="${ user.authTagMng eq 'ALL' }">checked="checkted"</c:if>/><label for="radio03_03">전체</label></li>
													</ul>
												</li>
												<li>
													<span>작업완료</span>
													<ul>
														<li><input type="radio" id="authConfMng_01" name="authConfMng" value="NONE" <c:if test="${ user.authConfMng eq 'NONE' || empty user.authConfMng }">checked="checkted"</c:if>/><label for="radio04_01">권한없음</label></li>
														<li><input type="radio" id="authConfMng_02" name="authConfMng" value="SELF" <c:if test="${ user.authConfMng eq 'SELF' }">checked="checkted"</c:if>/><label for="radio04_02">본인</label></li>
														<li><input type="radio" id="authConfMng_03" name="authConfMng" value="ALL" <c:if test="${ user.authConfMng eq 'ALL' }">checked="checkted"</c:if>/><label for="radio04_03">전체</label></li>
													</ul>
												</li>
											</ul>
										</td>
									</tr>
									<tr>
										<th scope="row">개체관래</th>
										<td>
											<ul class="user_authority">
												<li>
													<span>Entity</span>
													<ul>
														<li><input type="radio" id="authEntityMng_01" name="authEntityMng" value="NONE" <c:if test="${ user.authEntityMng eq 'NONE' || empty user.authEntityMng }">checked="checkted"</c:if>/><label for="radio05_01">권한없음</label></li>
														<li><input type="radio" id="authEntityMng_02" name="authEntityMng" value="SELF" <c:if test="${ user.authEntityMng eq 'SELF' }">checked="checkted"</c:if>/><label for="radio05_02">본인</label></li>
														<li><input type="radio" id="authEntityMng_03" name="authEntityMng" value="ALL" <c:if test="${ user.authEntityMng eq 'ALL' }">checked="checkted"</c:if>/><label for="radio05_03">전체</label></li>
													</ul>
												</li>
												<li>
													<span>Relation</span>
													<ul>
														<li><input type="radio" id="authRelationMng_01" name="authRelationMng" value="NONE" <c:if test="${ user.authRelationMng eq 'NONE' || empty user.authRelationMng }">checked="checkted"</c:if>/><label for="radio06_01">권한없음</label></li>
														<li><input type="radio" id="authRelationMng_02" name="authRelationMng" value="SELF" <c:if test="${ user.authRelationMng eq 'SELF' }">checked="checkted"</c:if>/><label for="radio06_02">본인</label></li>
														<li><input type="radio" id="authRelationMng_03" name="authRelationMng" value="ALL" <c:if test="${ user.authRelationMng eq 'ALL' }">checked="checkted"</c:if>/><label for="radio06_03">전체</label></li>
													</ul>
												</li>
											</ul>
										</td>
									</tr>
									<tr>
										<th scope="row">레이블링 관리</th>
										<td>
											<ul class="user_authority">
												<li>
													<span>레이블링</span>
													<ul>
														<li><input type="radio" id="authLabelMng_01" name="authLabelMng" value="NONE" <c:if test="${ user.authLabelMng eq 'NONE' || empty user.authLabelMng }">checked="checkted"</c:if>/><label for="radio07_01">권한없음</label></li>
														<li><input type="radio" id="authLabelMng_02" name="authLabelMng" value="SELF" <c:if test="${ user.authLabelMng eq 'SELF' }">checked="checkted"</c:if>/><label for="radio07_02">본인</label></li>
														<li><input type="radio" id="authLabelMng_03" name="authLabelMng" value="ALL" <c:if test="${ user.authLabelMng eq 'ALL' }">checked="checkted"</c:if>/><label for="radio07_03">전체</label></li>
													</ul>
												</li>
												<li>
													<span>학습</span>
													<ul>
														<li><input type="radio" id="authLearnMng_01" name="authLearnMng" value="NONE" <c:if test="${ user.authLearnMng eq 'NONE' || empty user.authLearnMng }">checked="checkted"</c:if>/><label for="radio08_01">권한없음</label></li>
														<li><input type="radio" id="authLearnMng_02" name="authLearnMng" value="SELF" <c:if test="${ user.authLearnMng eq 'SELF' }">checked="checkted"</c:if>/><label for="radio08_02">본인</label></li>
														<li><input type="radio" id="authLearnMng_03" name="authLearnMng" value="ALL" <c:if test="${ user.authLearnMng eq 'ALL' }">checked="checkted"</c:if>/><label for="radio08_03">전체</label></li>
													</ul>
												</li>
											</ul>
										</td>
									</tr>
								</tbody>
							</table>
						</fieldset>	
						<div class="align_c mt_20">
							<c:choose>
								<c:when test="${ param.mode eq 'C' }"><a href="javascript:save('C');" class="btn b_orange large">저장</a></c:when>
								<c:when test="${ param.mode eq 'M' }"><a href="javascript:save('M');" class="btn b_orange large">수정</a></c:when>
								<c:otherwise></c:otherwise>
							</c:choose>	
							<a href="/work/user/list.do" class="btn b_gray large">취소</a>				
						</div>
					</div>
					<!--// 회원 추가/수정 end -->


		</div>
		<!--// full area end -->

	</div>

</div>
</form>
<!--// content end -->
<div id="div-loading" style="background-color:#fffff;opacity:0.5;width:100%;height:100%;top:0;left:15%;position:fixed;z-index: 99; display:none;">
	<img src="/resources/images/common/loading.gif" style="position:absolute;top:40%;left:40%;z-index:100;width:80px;"/>
</div>
