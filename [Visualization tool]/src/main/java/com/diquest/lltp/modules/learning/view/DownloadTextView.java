/**
 * 
 */
package com.diquest.lltp.modules.learning.view;

import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.FileCopyUtils;

/**
 * 분석 파일 Export를 위한 view<br>
 * 
 * @author number40
 * @date 2017. 11. 28.
 */
public class DownloadTextView extends ADownloadView {

	Logger logger = LoggerFactory.getLogger(getClass());

	public DownloadTextView() {
		setContentType("application/download;charset=utf-8");
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * org.springframework.web.servlet.view.AbstractView#renderMergedOutputModel
	 * (java.util.Map, javax.servlet.http.HttpServletRequest,
	 * javax.servlet.http.HttpServletResponse)
	 */
	@Override
	protected void renderMergedOutputModel(Map<String, Object> model, HttpServletRequest req, HttpServletResponse res)
			throws Exception {
		String fileName = String.valueOf(model.get("downloadFileName"));
		String rname = String.valueOf(model.get("rname"));
		File file = new File(fileName);
		String downloadFileName = file.getName();
		
		try {
			if(rname == null || rname.length() == 0 || "null".equalsIgnoreCase(rname)) {
				downloadFileName = URLEncoder.encode(downloadFileName, "utf-8");
			} else {
				downloadFileName = URLEncoder.encode(rname, "utf-8");
			}
			
			downloadFileName = downloadFileName.replaceAll("\\+", " ");
			downloadFileName = downloadFileName.replaceAll("%5B", "(");
			downloadFileName = downloadFileName.replaceAll("%5D", ")");
			downloadFileName = downloadFileName.replaceAll("%28", "(");
			downloadFileName = downloadFileName.replaceAll("%29", ")");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}

		res.setContentType(getContentType());
		res.setContentLength((int) file.length());
		res.setHeader("Content-Transfer-Encoding", "binary");
		res.setHeader("Content-Disposition", "attachment;fileName=\"" + downloadFileName + "\";");

		OutputStream out = res.getOutputStream();
		FileInputStream fis = null;
		try {
			fis = new FileInputStream(file);
			FileCopyUtils.copy(fis, out);
		} catch (java.io.IOException ioe) {
			ioe.printStackTrace();
		} finally {
			if (fis != null)
				fis.close();
		}
	}

}
