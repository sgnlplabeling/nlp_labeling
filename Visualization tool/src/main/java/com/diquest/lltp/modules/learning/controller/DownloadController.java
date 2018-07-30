package com.diquest.lltp.modules.learning.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.modules.learning.service.DownloadService;
import com.diquest.lltp.modules.learning.service.thread.DownloadThread;

@Controller
public class DownloadController {
	
	@Autowired
	public DocumentService documentService;

	@Value("#{app['learning.filePath']}") public String DOWN_LOAD_PATH;
	
	public static final Map<String, String> DOWNLOAD_INFO = new HashMap<String, String>();

	/**
	 * 학습데이터 생성 다운로드 폼
	 * 
	 * @author number40
	 * @date 2017. 11. 28.
	 */
	@RequestMapping(value="/learning/downloadForm.do")
    public ModelAndView learningDownload(HttpServletRequest request, DocumentVo vo) throws Exception {
        ModelAndView mv = new ModelAndView();
        mv.setViewName("learning/download");
        
        int docId = vo.getDocId();

        if(docId > 0){
        	String[] docIds = new String[1];
            docIds[0] = String.valueOf(docId);
            vo.setDocIds(docIds);
        }
        
        List<DocumentVo> docList = documentService.getDocIdsRecordList(vo);
        
        mv.addObject("docList", docList);
        mv.addObject("PARAM", vo);
        return mv;
    }
	
	/**
	 * 학습데이터 생성 다운로드 프로세스
	 * 
	 * @author number40
	 * @date 2017. 11. 28.
	 */
	@RequestMapping(value = "/learning/downloadProcessing.do", method = {RequestMethod.GET, RequestMethod.POST})
	public ModelAndView downloadProcessing(HttpSession session, DocumentVo vo) {
		ModelAndView mv = new ModelAndView("jsonView");
		
		String exportId = "EXPORT_" + System.nanoTime();
		
		DownloadService service = new DownloadService(documentService, DOWN_LOAD_PATH, exportId, vo);
		new DownloadThread(exportId, service).start();
		
		StringBuffer sb = new StringBuffer();
		sb.append(exportId + "@@@");
		sb.append(service.getDownloadFilePath() + "@@@");
		String returnStr = sb.toString().trim();
		System.out.println(">>>>>>>>>>>>>>>"+returnStr+">>>>>>>>>>>>>>>>>>>>");
        mv.addObject("data", returnStr);
		
        return mv;
	}
	
	/**
	 * 학습데이터 생성 다운로드 진행정보
	 * 
	 * @author number40
	 * @date 2017. 11. 28.
	 */
	@RequestMapping(value = "/learning/downloadInfo.do", method = {RequestMethod.GET, RequestMethod.POST})
	public ModelAndView downloadInfo(HttpServletRequest request) {
		ModelAndView mv = new ModelAndView("jsonView");
		
		String exportId = request.getParameter("exportID");
		String contents = "false";
		if (exportId != null) {
			contents = DOWNLOAD_INFO.remove(exportId);
		}
		System.out.println("============================="+contents+"=============================");
        mv.addObject("data", contents);
		
        return mv;
	}

	/**
	 * 학습데이터 생성 다운로드
	 * 
	 * @author number40
	 * @date 2017. 11. 28.
	 */
	@RequestMapping(value = "/learning/download.do", method = {RequestMethod.GET, RequestMethod.POST})
	public ModelAndView download(HttpServletRequest request) {
		String exportId = request.getParameter("downloadPath");
		ModelAndView view = new ModelAndView("downloadTextView");
		view.addObject("downloadFileName", exportId);
		return view;
	}

}
