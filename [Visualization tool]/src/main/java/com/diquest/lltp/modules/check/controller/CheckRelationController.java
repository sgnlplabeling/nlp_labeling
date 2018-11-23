package com.diquest.lltp.modules.check.controller;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.RelationVo;
import com.diquest.lltp.modules.brat.service.BratService;
import com.diquest.lltp.modules.check.service.CheckRelationService;

@Controller
public class CheckRelationController {

   @Autowired
   public CheckRelationService checkRelationService;

   @Autowired
   public BratService bratService;
   
    @RequestMapping(value="/check/relation/list.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView getRelationList(DocumentVo documentVo) throws Exception{
        ModelAndView mv = new ModelAndView();
        mv.setViewName("check/relation/list");
        
        String syntacticJstreeHtml = checkRelationService.relationJstreeHtml("syntactic");
        String causationJstreeHtml = checkRelationService.relationJstreeHtml("causation");
        String simenticJstreeHtml = checkRelationService.relationJstreeHtml("simentic");
        mv.addObject("syntacticJstreeHtml", syntacticJstreeHtml);
        mv.addObject("causationJstreeHtml", causationJstreeHtml);
        mv.addObject("simenticJstreeHtml", simenticJstreeHtml);
        return mv;
    }
    
    @RequestMapping(value="/check/relation/keywordList.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView getKeywordList(RelationVo vo) throws Exception{
		ModelAndView mv = new ModelAndView("jsonView");
		    
		List<AnnotationVo> keywordList = new ArrayList<>();
		String relation = vo.getRelId();
		relation = relation.replaceAll("rel", "");
		String [] relIds = relation.split(",");
		vo.setRelIds(relIds);
		
		keywordList = checkRelationService.getKeywordList(vo); 
		mv.addObject("keywordList", keywordList);
		mv.addObject("keywordListCount", keywordList.size());
    
		return mv;
    }	    

    @RequestMapping(value="/check/relation/docList.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView getLabelingDocList(AnnotationVo vo, String relation) throws Exception{
        ModelAndView mv = new ModelAndView("jsonView");
        
		relation = relation.replaceAll("rel", "");
		String [] relIds = relation.split(",");
		vo.setRelIds(relIds);
		
        List<DocumentVo> labelingList = checkRelationService.getLabelingDocList(vo);
        List<DocumentVo> unlabelingList = checkRelationService.getUnlabelingList(labelingList);
        
        mv.addObject("labelingList", labelingList);
        mv.addObject("labelingListCount", labelingList.size());
        mv.addObject("unlabelingList", unlabelingList);
        mv.addObject("unlabelingListCount", unlabelingList.size());
        return mv;
    }	
    
    @RequestMapping(value="/check/relation/bratDetailView.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView bratDetailView(DocumentVo documentVo) throws Exception{
        ModelAndView mv = new ModelAndView("jsonView");
        mv.addObject("map",bratService.bratReadOnly(documentVo));
        return mv;
    }
    
    @RequestMapping(value="/check/relation/RelationLoc.do", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView RelationLoc(AnnotationVo vo, String relation) throws Exception {
        ModelAndView mv = new ModelAndView("jsonView");

    	relation = relation.replaceAll("rel", "");
		String [] relIds = relation.split(",");
		vo.setRelIds(relIds);
		
        List<RelationVo> list = checkRelationService.getRelationLoc(vo);
        
        List<String> keywordLoc = new ArrayList<String>();
        List<String> relationLoc = new ArrayList<String>();
        
        for (RelationVo rel : list) {
        	if (!StringUtils.isEmpty(rel.getStartRel())) {
            	keywordLoc.add(rel.getStartRel());
        	}
        	if (!StringUtils.isEmpty(rel.getEndRel())) {
            	keywordLoc.add(rel.getEndRel());
        	}
        	relationLoc.add(rel.getRelId());
        }
        mv.addObject("relationLoc", relationLoc);
        mv.addObject("keywordLoc", keywordLoc);
        return mv;
    }
}
