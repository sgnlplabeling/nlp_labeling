package com.diquest.lltp.modules.work.controller;

import java.util.List;

import javax.servlet.http.HttpServletRequest;

import org.apache.commons.lang3.StringUtils;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.common.utils.Pagination;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.HistoryVo;
import com.diquest.lltp.modules.brat.service.BratService;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.modules.work.service.HistoryService;

@Controller
public class HistoryController {
	Logger log = Logger.getLogger(this.getClass());
	
	@Autowired
	public DocumentService documentService;
	
	@Autowired
	public HistoryService historyService;	
	
	@Autowired
	public BratService bratService;
	   
	@RequestMapping(value="/work/document/list.do")
    public ModelAndView getWorkDocumentList(HttpServletRequest request, DocumentVo vo) throws Exception {
        ModelAndView mv = new ModelAndView();
        if (StringUtils.isEmpty(vo.getDateSearchOpt())) {
        	vo.setDateSearchOpt("all");
        }
        
        List<DocumentVo> docList = documentService.getDocHistoryList(vo);
        
        int count = documentService.getDocHistoryListCount(vo);
        
        mv.addObject("list", docList);
        mv.addObject("count", count);
        mv.addObject("pagination", new Pagination(request, count));
        mv.addObject("doc", vo);
        
        mv.setViewName("work/document/list");
        return mv;
    }
	
    @RequestMapping(value="/work/document/detail.do")
    public ModelAndView workDocumentDetail(DocumentVo vo) throws Exception{
        ModelAndView mv = new ModelAndView();
        
        List<HistoryVo> jobList = historyService.getRecordHistoryList(vo);
        DocumentVo currentRecord = documentService.getRecordOne(vo);
        String recordSeq = vo.getRecordSeq();
        
        if (StringUtils.isEmpty(recordSeq) || 
        		recordSeq.equals(currentRecord.getRecordSeq())) {
        	if (jobList.size()>0) {
            	recordSeq = String.valueOf(jobList.get(0).getRecordSeq());
        	} else {
        		recordSeq = "";
        	}
        }
        
        mv.addObject("doc", currentRecord);
        mv.addObject("job", jobList);
        mv.addObject("lastRecordSeq", recordSeq);
        
        mv.setViewName("work/document/detail");
        return mv;
    }
    
    @RequestMapping(value="/work/document/compareLoc.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView compareLoc(DocumentVo documentVo) throws Exception{
        ModelAndView mv = new ModelAndView("jsonView");
        List<AnnotationVo> list = historyService.getCompareLoc(documentVo);
        mv.addObject("list", list);
        return mv;
    }
    
    @RequestMapping(value="/work/service/list.do")
    public ModelAndView getWorkServiceList(HttpServletRequest request, CommonVo vo) throws Exception{
        ModelAndView mv = new ModelAndView();
        
        List<HistoryVo> hitoryList = historyService.getHistoryList(vo);
        
        int count = historyService.getHistoryListCount(vo);
        
        mv.addObject("list", hitoryList);
        mv.addObject("count", count);
        mv.addObject("pagination", new Pagination(request, count));
        mv.addObject("doc", vo);
        
        mv.setViewName("work/service/list");
        return mv;
    }
}
