function openPopup(){
    var win = window.open('', 'win', 'width=1, height=1, scrollbars=yes, resizable=yes');
    console.log(win);
	if (win == null || typeof(win) == "undefined" || (win == null && win.outerWidth == 0) || (win != null && win.outerHeight == 0) || win.test == "undefined") {
		alert("팝업 차단 기능이 설정되어있습니다\n\n차단 기능을 해제(팝업허용) 한 후 다시 이용해 주십시오.\n\n만약 팝업 차단 기능을 해제하지 않으면\n정상적인 주문이 이루어지지 않습니다.");
	  if(win){
	    win.close();
	  }
	  return false;
	} else if (win)	{
	} else 	{
	    return false;
	}
	if(win){    // 팝업창이 떠있다면 close();
	    win.close();
	}
	return true;
}    // 함수 끝

function replaceIdText(val) {
	val = val.replace(/\./gi, '__');
	val = val.replace(/([\s]{1,})/gi, '_')
	val = val.replace(/(\+|\/)/gi, '__');
	val = val.replace(/\)|\(/gi,"--")
	val = val.replace(/\{|\}/gi,"---")
	
	val = val.replace(/(\\|\'|\")/gi, '_');
    return val.replace(/\./gi, '__')
}