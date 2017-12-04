package com.diquest.lltp.modules.data.controller;

import java.util.ArrayList;
import java.util.List;

import javax.servlet.http.HttpServletRequest;

import org.apache.commons.lang3.StringUtils;
import org.apache.log4j.Logger;
import org.json.simple.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.data.service.CollectionService;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.common.utils.Pagination;

@Controller
public class DocumentController {
	Logger log = Logger.getLogger(this.getClass());
		   
	@Autowired
	public DocumentService documentService;
	
	@Autowired
	public CollectionService collectionService;
	
    @RequestMapping(value="/data/document/list.do")
    public ModelAndView getdocumentList(HttpServletRequest request, DocumentVo vo, String docIds) throws Exception {
        ModelAndView mv = new ModelAndView();

        String domainJstreeHtml = collectionService.domainJstreeHtml(vo.getColId());
        List<DocumentVo> list = new ArrayList<>();
        int count = 0;
        
        if (!StringUtils.isEmpty(docIds)) {
	        vo.setDocIds(docIds.split(","));
	        list = documentService.getDocList(vo);
	        count = documentService.getDocListCount(vo);
        }
        
        mv.addObject("domainJstreeHtml", domainJstreeHtml);
        mv.addObject("list", list);
        mv.addObject("count",count);
        mv.addObject("pagination", new Pagination(request, count));
        mv.addObject("doc", vo);
        mv.addObject("docIds", docIds);
		
        mv.setViewName("data/document/list");
        return mv;
    }
    
    @ResponseBody
    @RequestMapping(value="/data/document/insert.do")
    public String insertDocument(DocumentVo vo) throws Exception {
    	JSONObject result = documentService.insertDocument(vo);
		return result.toJSONString();
    }

    
    @RequestMapping(value="/data/document/delete.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView deleteDocument(Integer[] docId) throws Exception {
    	 ModelAndView mv = new ModelAndView("jsonView");	
    	 documentService.deleteDocument(docId);
         return mv;
    }

    @RequestMapping(value="/data/document/recordDelete.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView deleteRecord(Integer[] recordId) throws Exception {
    	 ModelAndView mv = new ModelAndView("jsonView");	
    	 documentService.deleteRecord(recordId);
         return mv;
    }
    
    @RequestMapping(value="/data/document/editConf.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView editConf(DocumentVo vo) throws Exception {
    	ModelAndView mv = new ModelAndView("jsonView");
    	documentService.updateRecordConf(vo);
        return mv;
    }
    
}
