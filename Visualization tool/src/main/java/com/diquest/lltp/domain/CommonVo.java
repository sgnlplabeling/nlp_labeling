package com.diquest.lltp.domain;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import org.apache.commons.lang3.StringUtils;
import org.springframework.web.context.request.RequestAttributes;
import org.springframework.web.context.request.RequestContextHolder;

import lombok.Getter;
import lombok.Setter;

public class CommonVo {
	
	@Getter
	@Setter
	String searchTerm;

	@Getter
	@Setter
	String searchTermOpt;
	
	@Getter
	@Setter
	String typeOpt;
	
	@Getter
	@Setter
	String startDate = oneWeekAgo();
	
	@Getter
	@Setter
	String endDate = new SimpleDateFormat("yyyy-MM-dd").format(new Date());
	
	@Getter
	@Setter
	String dateSearchOpt;
	
	@Getter
	@Setter
	String jstreeName;
	
	@Getter
	@Setter
	String jstreeId;
	
	@Getter
	@Setter
	String groupName;
	
	@Getter
	@Setter
	String name;
	
	@Getter
	@Setter
	String []keywords;
	
	@Setter
	String userId;
	
	
	public String getUserId() {
		if (StringUtils.isEmpty(userId)) {
			UserVo vo = (UserVo)RequestContextHolder.getRequestAttributes().getAttribute("userLoginInfo", RequestAttributes.SCOPE_SESSION);
			userId = vo.getUserId();
		}
		return userId;
	}

	@Getter
	String domain;

	public void setDomain(String domain) {
		this.domain = domain.replaceAll("ROOT/", "");
	}

	@Getter
	@Setter
	String domainPath;
	
	@Getter
	@Setter
	boolean result;
	
	@Getter
	@Setter
	String []endIds;
	
	@Getter
	@Setter
	String []docIds;
	
	@Getter
	@Setter
	String []relIds;
	
	@Getter
	@Setter
    Integer pageNo = 1;

	@Getter
	@Setter
    Integer pageSize = 10;
	
	
	Integer offSet;

	public Integer getOffSet() {
		return pageNo == null || pageSize == null ? null : (pageNo - 1) * pageSize;
	}

	public String oneWeekAgo() {
		Calendar week = Calendar.getInstance();
		week.add(Calendar.DATE , -7);
		String date = new java.text.SimpleDateFormat("yyyy-MM-dd").format(week.getTime());
		return date;
	}

}
