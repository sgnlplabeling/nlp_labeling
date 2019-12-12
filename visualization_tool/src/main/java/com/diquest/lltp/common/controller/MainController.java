package com.diquest.lltp.common.controller;

import java.security.Principal;

import javax.servlet.http.HttpSession;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.domain.UserVo;
import com.diquest.lltp.modules.user.service.UserService;

 
@Controller
public class MainController {
     
    private static final Logger logger = LoggerFactory.getLogger(MainController.class);
    
    @Autowired
	public UserService userService;
    
    @RequestMapping(value = "/login/loginForm.do", method = RequestMethod.GET)
    public ModelAndView loginForm(String result) {
    	 ModelAndView mv = new ModelAndView();
    	 mv.addObject("result", result);
    	 mv.setViewName("login/login");
    	 return mv;
    }
    	
    @RequestMapping(value = "/login/login.do", method = RequestMethod.GET)
    public void login(HttpSession session) {
        logger.info("Welcome login! {}", session.getId());
    }
     
    @RequestMapping(value = "/login/logout.do", method = RequestMethod.GET)
    public ModelAndView logout(HttpSession session) {
    	ModelAndView mv = new ModelAndView();
        session.invalidate();
        mv.setViewName("login/login");
        return mv;
        
    }
     
    @RequestMapping(value = "/login/login_success.do", method = RequestMethod.GET)
    public ModelAndView login_success(Principal principal, HttpSession session) {
    	ModelAndView mv = new ModelAndView("redirect:/check/labeling/list.do");
    	System.out.println(principal.getName());
    	UserVo vo = userService.selectUser(principal.getName());
    	
    	session.setAttribute("userLoginInfo", vo);
        return mv;
    }
     
    @RequestMapping(value = "/login/login_duplicate.do", method = RequestMethod.GET)
    public void login_duplicate() {    
        
    }
     
}
