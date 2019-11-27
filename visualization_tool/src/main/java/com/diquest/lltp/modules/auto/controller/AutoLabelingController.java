package com.diquest.lltp.modules.auto.controller;

import java.util.List;

import javax.servlet.http.HttpServletRequest;

import org.apache.commons.lang3.StringUtils;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.common.utils.Pagination;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.auto.service.AutoLabelingService;
import com.diquest.lltp.modules.data.service.CollectionService;

@Controller
public class AutoLabelingController {
	Logger log = Logger.getLogger(this.getClass());
	
	@Autowired
	public CollectionService collectionService;
	
	@Autowired
	public AutoLabelingService autoLabelingService;
	
	@RequestMapping(value="/auto/list.do")
    public ModelAndView getAutoList(HttpServletRequest request, DocumentVo vo) throws Exception {
        ModelAndView mv = new ModelAndView();
        if (StringUtils.isEmpty(vo.getGroupName())) {
        	vo.setGroupName("namedentity");
        }
        
        Integer colId = vo.getColId();
        String domainJstreeHtml = collectionService.domainJstreeHtml(colId);
        
        List<DocumentVo> list = autoLabelingService.getAutoLabelingList(vo);
        int count = autoLabelingService.getAutoLabelingListCount(vo);
        
        mv.addObject("domainJstreeHtml", domainJstreeHtml);
        mv.addObject("list", list);
        mv.addObject("count",count);
        mv.addObject("pagination", new Pagination(request, count));
        mv.addObject("doc", vo);
        mv.setViewName("auto/list");
        return mv;
    }
	
	@RequestMapping(value="/auto/start.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView AutolabelingStart(DocumentVo vo) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");
		autoLabelingService.labelingStart(vo);
		return mv;
	}	
	
	@RequestMapping(value="/auto/checkAutoLabel.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView checkAutoLabel(DocumentVo vo) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");
		List<Integer> checked = autoLabelingService.isRunningAutoLabeled(vo);
		System.out.println(checked);
		if(!checked.isEmpty()) {
			mv.addObject("docId", checked);
		}
		return mv;
	}
	
	@RequestMapping(value="/auto/runChkAutoLabel.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView runChkAutoLabel(DocumentVo vo) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");
		List<Integer> checked = autoLabelingService.isRunningAutoLabeled(vo);
		if(!checked.isEmpty()) {
			mv.addObject("docId", checked);
		}
		return mv;
	}
	
}
