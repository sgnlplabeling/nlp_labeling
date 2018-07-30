package com.diquest.lltp.modules.brat.controller;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.brat.service.BratService;


@Controller
public class BratController {
	   Logger log = Logger.getLogger(this.getClass());
	   
	   @Autowired
	   public BratService bratService;
	   
	    @RequestMapping(value="/labeling/bratView.do", produces = MediaType.APPLICATION_JSON_VALUE)
	    public ModelAndView bratView(DocumentVo documentVo) throws Exception{
	        ModelAndView mv = new ModelAndView("jsonView");
	        
	        mv.addObject("docData", bratService.getDocData(documentVo));
	        mv.addObject("collData",bratService.getCollData(documentVo));
	        
	        return mv;
	    }
	    
	    @RequestMapping(value="/labeling/bratEdit.do", produces = MediaType.APPLICATION_JSON_VALUE)
	    public ModelAndView bratEdit(DocumentVo documentVo) throws Exception{
	       ModelAndView mv = new ModelAndView("jsonView");
	       mv.addObject("map",bratService.bratEdit(documentVo));
	       return mv;
	    }	    
	    
	    @RequestMapping(value="/labeling/deleteFile.do", produces = MediaType.APPLICATION_JSON_VALUE)
	    public ModelAndView deleteFile(String path) throws Exception{
	        ModelAndView mv = new ModelAndView("jsonView");
	        bratService.deleteFile(path);
	        return mv;
	    }	   
	    
	    @RequestMapping(value="/labeling/bratSave.do", produces = MediaType.APPLICATION_JSON_VALUE)
	    public ModelAndView bratSave(DocumentVo documentVo) throws Exception{
	        ModelAndView mv = new ModelAndView("jsonView");
	        documentVo = bratService.bratSave(documentVo);
	        
	        mv.addObject("doc", documentVo);
	        return mv;
	    }	 
	    
	    @RequestMapping(value="/labeling/keyowrdLoc.do", produces = MediaType.APPLICATION_JSON_VALUE)
	    public ModelAndView keyowrdLoc(DocumentVo documentVo) throws Exception{
	    	
	        ModelAndView mv = new ModelAndView("jsonView");

	        List<AnnotationVo> list = bratService.getAnnotationList(documentVo);
	        
	        List<String> keywordLoc = new ArrayList<String>();
	        for (AnnotationVo vo : list) {
	        	keywordLoc.add(vo.getAnnId());
	        }
	        mv.addObject("keywordLoc", keywordLoc);
	        return mv;
	    }
}
