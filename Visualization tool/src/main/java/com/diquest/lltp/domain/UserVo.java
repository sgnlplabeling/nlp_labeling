package com.diquest.lltp.domain;

import java.util.Collection;
import java.util.Date;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;


import lombok.Data;
import lombok.ToString;

@Data
@ToString
public class UserVo implements UserDetails  {
	/**
	 * 
	 */
	private static final long serialVersionUID = 4437933663565206188L;
	
	private String userId;
	private String password;
	private String newPassword;
	private String newPwd;
	private String newPwdConf;
	private String username;
	private String type;
	private String note;
	
	private Date regDate;
	private Date modDate;
	
	private Collection<? extends GrantedAuthority> authorities;
	
	private boolean isAccountNonExpired; 
	private boolean isAccountNonLocked; 
	private boolean isCredentialsNonExpired; 
	private boolean isEnabled;
	
	private String authDomainMng;
	private String authDocMng;
	private String authTagMng;
	private String authConfMng;
	private String authEntityMng;
	private String authRelationMng;
	private String authLabelMng;
	private String authLearnMng;
	
	private String mode;
}
