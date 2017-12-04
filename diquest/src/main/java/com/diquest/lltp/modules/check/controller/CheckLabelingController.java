package com.diquest.lltp.modules.check.controller;

import java.util.List;

import javax.servlet.http.HttpSession;

import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.brat.service.BratService;
import com.diquest.lltp.modules.check.service.CheckLabelingService;
import com.diquest.lltp.modules.data.service.CollectionService;
import com.diquest.lltp.modules.data.service.DocumentService;

@Controller
public class CheckLabelingController {
	   Logger log = Logger.getLogger(this.getClass());
	   
	   @Autowired
	   public BratService bratService;
	   
	   @Autowired
	   public CheckLabelingService checkLabelingService;
	   
	   @Autowired
	   public CollectionService collectionService;
	   
		@Autowired
		public DocumentService documentService;
	   
	    @RequestMapping(value="/check/labeling/list.do")
	    public ModelAndView main(HttpSession session) throws Exception{
	        ModelAndView mv = new ModelAndView();
	        mv.setViewName("check/labeling/list");

	        String domainJstreeHtml = collectionService.domainJstreeHtml(null);
	        
	        String namedentityJstreeHtml = checkLabelingService.elementJstreeHtml("namedentity");
	        String syntacticJstreeHtml = checkLabelingService.elementJstreeHtml("syntactic");
	        String causationJstreeHtml = checkLabelingService.elementJstreeHtml("causation");
	        
	        mv.addObject("domainJstreeHtml", domainJstreeHtml);
	        mv.addObject("namedentityJstreeHtml", namedentityJstreeHtml);
	        mv.addObject("syntacticJstreeHtml", syntacticJstreeHtml);
	        mv.addObject("causationJstreeHtml", causationJstreeHtml);
	        return mv;
	    }

	    @RequestMapping(value="/check/labeling/docList.do", produces = MediaType.APPLICATION_JSON_VALUE)
	    public ModelAndView getDocList(DocumentVo documentVo) throws Exception{
	        ModelAndView mv = new ModelAndView("jsonView");
	        List<DocumentVo> docList = documentService.getDocSubjectList(documentVo);
	        
	        mv.addObject("docList", docList);
	        mv.addObject("count", docList.size());
	        return mv;
	    }

	    @RequestMapping(value="/data/entity/list.do")
	    public ModelAndView entity() throws Exception{
	        ModelAndView mv = new ModelAndView();
	        mv.setViewName("data/entity/list");
	        return mv;
	    }
	    
}
