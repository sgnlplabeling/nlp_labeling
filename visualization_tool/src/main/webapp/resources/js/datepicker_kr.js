  $(function() {
   $(".date_time").datepicker({
    monthNamesShort: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
    dayNamesMin: ['일','월','화','수','목','금','토'],
    weekHeader: 'Wk',
    dateFormat: 'yy-mm-dd', //형식(2012-03-03)
    autoSize: false, //오토리사이즈(body등 상위태그의 설정에 따른다)
    changeMonth: true, //월변경가능
    changeYear: true, //년변경가능
    showMonthAfterYear: true, //년 뒤에 월 표시
    buttonImageOnly: true, //이미지표시
    buttonImage: contextPath+'/resources/images/common/btn_calendar.gif', //이미지주소
    buttonText: '날짜 선택',
    showOn: "both", //엘리먼트와 이미지 동시 사용
    yearRange: '2005:2020' //2005년부터 2020년까지
   });
  });