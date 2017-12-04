package com.diquest.lltp.common.interceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.handler.HandlerInterceptorAdapter;

import com.diquest.lltp.domain.UserVo;

public class WebInterceptor extends HandlerInterceptorAdapter{
	
    protected Log log = LogFactory.getLog(WebInterceptor.class);
    
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
    	if (log.isDebugEnabled()) {
            log.debug("======================================          START         ======================================");
            log.debug(" Request URI \t:  " + request.getRequestURI());
        }
        
        return super.preHandle(request, response, handler);
    }
     
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
    	
    	if (log.isDebugEnabled()) {
            log.debug("======================================           END          ======================================\n");
        }
    	/*UserVo user = (UserVo) request.getSession().getAttribute("userLoginInfo");
    	
    	if (user == null) {
    		response.sendRedirect("/login/loginForm.do");
    	}
    	
    	modelAndView.addObject("user", user);
    	String[] url = (request.getRequestURI()).split("/");
    	
    	if (url.length > 1) {
	    	modelAndView.addObject("currentMenu", url[1]);
    	}*/
    }
}
