package com.diquest.lltp.common.utils;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;

@Data
public class Pagination {

    /** HTTP Method: POST */
    private static final String HTTP_METHOD_POST = "POST";

    /** URL 최대 길이 */
    private static final int URL_MAX_LENGTH = 4000;

    /** 페이지 기본값 */
    public static final int DEFAULT_PAGE = 1;

    /** 페이지 크기 기본 값 */
    public static final int DEFAULT_PAGE_SIZE = 10;

    /** 페이지 블록 기본 값 */
    public static final int DEFAULT_PAGE_BLOCK = 10;

    /** 페이지 파라메터 기본값 */
    public static final String DEFAULT_PAGE_PARAM = "pageNo";

    /** 페이지 크기 파라메터 기본 값 */
    public static final String DEFAULT_PAGE_SIZE_PARAM = "pageSize";

    /** 페이지 블록 파라메터 기본 값 */
    public static final String DEFAULT_PAGE_BLOCK_PARAM = "pageBlock";

    @JsonIgnore
    private final HttpServletRequest request;

    /** 페이지 파라메터 */
    private String pageParam = DEFAULT_PAGE_PARAM;

    /** 페이지 크기 파라메터 */
    private String pageSizeParam = DEFAULT_PAGE_SIZE_PARAM;

    /** 페이지 블록 파라메터 */
    private String pageBlockParam = DEFAULT_PAGE_BLOCK_PARAM;

    /** js function, form id (자동생성) */
    private String id;

    /**
     * Pagination 에서 사용할 HTTP Method
     * 값이 없으면 GET/POST Request 요청에 따라 자동설정됨
     * 값을 설정하는 경우 설정값으로 강제됨
     */
    private String httpMethod;

    /** 생성된 Form HTML 저장 (자동생성) */
    private String form;

    /** 생성된 JS Function HTML 저장 (자동생성) */
    private String jsFunc;

    /** 페이지 */
    private int page;

    /** 페이지 크기 */
    private int pageSize;

    /** 페이지 블록 */
    private int pageBlock;

    /** 전체 개수 */
    private int totalCount;

    /** 첫번째 페이지 */
    private int firstPage;

    /** 마지막 페이지 */
    private int lastPage;

    /** 이전 페이지 */
    private int prevPage;

    /** 다음 페이지 */
    private int nextPage;

    /** 시작 블록 */
    private int startBlockPage;

    /** 이전 블록 */
    private int prevBlockPage;

    /** 다음 블록 */
    private int nextBlockPage;

    /** 가상 시작번호 */
    private int virtualStartNo;

    public Pagination(final HttpServletRequest request, int totalCount) {
        this.request = request;
        this.totalCount = totalCount;

        build();
    }

    /**
     * 유효검사
     *
     * @return
     */
    public boolean isValid() {
        return request != null && 0 < totalCount;
    }

    /**
     * 페이지네이셔 생성
     * request, totalCount 기준으로
     * 가상 시작번호, 페이지, 블럭, HTML 생성
     */
    private void build() {
        if (request == null || totalCount <= 0)
            return;

        // 인자값 확인
        page = Integer.parseInt(getParameter(pageParam, Integer.toString(DEFAULT_PAGE)));
        pageSize = Integer.parseInt(getParameter(pageSizeParam, Integer.toString(DEFAULT_PAGE_SIZE)));
        pageBlock = Integer.parseInt(getParameter(pageBlockParam, Integer.toString(DEFAULT_PAGE_BLOCK)));

        // 가상 시작번호
        virtualStartNo = totalCount - ((page - 1) * pageSize);

        // 페이지 계산
        firstPage = 1;
        lastPage = (int) Math.ceil((double) totalCount / (double) pageSize);
        prevPage = page <= 1 ? 1 : page - 1;
        nextPage = page == lastPage ? lastPage : page + 1;

        // 블럭 계산
        int blockPage = (int) Math.ceil((double) page / (double) pageBlock);
        startBlockPage = ((blockPage - 1) * pageBlock) + 1;
        prevBlockPage = Math.max(((blockPage - 1) * pageBlock), 1);
        nextBlockPage = Math.min((blockPage * pageBlock + 1), lastPage);

        // HTML 생성
        form = makeForm();
        jsFunc = makeJsFunc();
    }

    /**
     * TAG,JSP 에서 호출할때 사용하는 Js Function 이름생성
     *
     * @param page
     * @return
     */
    public String callJsFunc(int page) {
        return String.format("_fn_%s(%s);", getId(), page);
    }

    /**
     * JS Function HTML 생성
     *
     * @return
     */
    public String makeJsFunc() {
        return String.format("<script>\nfunction _fn_%s(page) { $('#%s input[name=%s]').val(page); $('#%s').submit(); }\n</script>\n", getId(), getId(), pageParam, getId());
    }

    /**
     * Form HTML 생성
     *
     * @return
     */
    public String makeForm() {
        String html = Form.start(getId(), getMethod(), getRequestURI());

        html += Form.input(Form.INPUT_HIDDEN, pageParam, Integer.toString(page));
        if (getParameter(pageSizeParam, null) != null) {
            html += Form.input(Form.INPUT_HIDDEN, pageSizeParam, Integer.toString(pageSize));
        }
        if (getParameter(pageBlockParam, null) != null) {
            html += Form.input(Form.INPUT_HIDDEN, pageBlockParam, Integer.toString(pageBlock));
        }

        Map<String, String[]> paramMap = request.getParameterMap();
        if (paramMap != null && 0 < paramMap.size()) {
            for (String name : paramMap.keySet()) {
                if (name == null || pageParam.equals(name) || pageSizeParam.equals(name) || pageBlockParam.equals(name)) {
                    continue;
                }

                for (String value : paramMap.get(name)) {
                    if (value == null || value.trim().length() == 0) {
                        continue;
                    }
                    html += Form.input(Form.INPUT_HIDDEN, name, value);
                }
            }
        }

        html += Form.end();

        return html;
    }

    /**
     * js function, form id 생성
     *
     * @return
     */
    public String getId() {
        if (id == null)
            id = "pagination_" + System.currentTimeMillis();
        return id;
    }

    /**
     * 사용할 HTTP Method 결정
     * URL 최대길이(4000자)가 넘어가면 강제 POST 설정됨
     *
     * @return
     */
    public String getMethod() {
        if (httpMethod != null) {
            return httpMethod;
        }

        String queryString = getQueryString();
        if (queryString != null && URL_MAX_LENGTH < queryString.length()) {
            return HTTP_METHOD_POST;
        }

        return request.getMethod();
    }

    private String getQueryString() {
        return request.getQueryString();
    }

    private String getRequestURI() {
        return request.getRequestURI();
    }

    private String getParameter(String name, String defaultValue) {
        String value = request.getParameter(name);
        return value != null ? value : defaultValue;
    }

    private static class Form {

        public static final String INPUT_HIDDEN = "hidden";

        private static final String TMPL_START = "<form id='%s' method='%s' action='%s'>\n";

        private static final String TMPL_END = "</form>\n";

        private static final String TMPL_INPUT = "<input type='%s' name='%s' value='%s'>\n";

        private Form() {

        }

        public static String start(String id, String method, String action) {
            return String.format(TMPL_START, id, method, action);
        }

        public static String end() {
            return TMPL_END;
        }

        public static String input(String type, String name, String value) {
            return String.format(TMPL_INPUT, type, name, value);
        }

    }

}
