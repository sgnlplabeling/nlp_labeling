package com.diquest.lltp.common.utils;

import java.io.FileNotFoundException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.util.Map;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.poi.ss.usermodel.Workbook;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.Resource;
import org.springframework.web.context.support.ServletContextResource;
import org.springframework.web.servlet.view.AbstractView;

import eu.bitwalker.useragentutils.Browser;
import eu.bitwalker.useragentutils.UserAgent;
import net.sf.jxls.transformer.XLSTransformer;

/**
 * Excel View
 *
 * @author yongseoklee
 * @since 0.0.1
 */
public class ExcelView extends AbstractView {

	Logger logger = LoggerFactory.getLogger(getClass());
	/**
	 * Excel contentType
	 */
	public static final String CONTENT_TYPE = "application/vnd.ms-excel";

	private String prefix;

	private String downloadFilename;

	private String templateFilename;

	private DefaultFilenameEncoder filenameEncoder = new DefaultFilenameEncoder();

	public ExcelView() {
		setContentType(CONTENT_TYPE);
	}

	@Override
	protected boolean generatesDownloadContent() {
		return true;
	}

	/**
	 * 다운로드 헤더 준비
	 *
	 * @param request
	 * @param response
	 * @param filename
	 * @throws UnsupportedEncodingException
	 */
	protected void prepareAttachmentFilename(HttpServletRequest request, HttpServletResponse response, String filename)
			throws UnsupportedEncodingException {
		logger.info("FILE NAME PATH : {}", filename);
		String encodeFilename = this.filenameEncoder.encode(request, filename);
		logger.info("TEMPLATE PATH : {}", encodeFilename);
		response.setHeader("Content-Disposition", String.format("attachment; filename=\"%s\"", encodeFilename));
	}

	@Override
	protected void renderMergedOutputModel(Map<String, Object> model, HttpServletRequest request,
			HttpServletResponse response) throws Exception {
		logger.info(getContentType());

		Resource template = this.getTemplateResource(request);
		String filename = this.getFilename(request);
		ServletOutputStream out = null;

		prepareAttachmentFilename(request, response, filename);
		InputStream is = null;
		try {
			XLSTransformer transformer = new XLSTransformer();
			is = template.getInputStream();
			logger.debug("WORK BOOK : {}", is);
			Workbook workbook = transformer.transformXLS(is, model);
			// Flush byte array to servlet output stream.
			logger.debug("WORK BOOK");
			out = response.getOutputStream();
			workbook.write(out);
		} catch (Exception e) {
			logger.info(e.getMessage(), e);
			throw e;
		} finally {
			if (is != null) {
				is.close();
			}
			if (out != null) {
				out.flush();
				out.close();
			}
		}

	}

	public String getDownloadFilename() {
		return downloadFilename;
	}

	public void setDownloadFilename(String downloadFilename) {
		this.downloadFilename = downloadFilename;
	}

	public String getTemplateFilename() {
		return templateFilename;
	}

	public void setTemplateFilename(String templateFilename) {
		this.templateFilename = templateFilename;
	}

	public String getPrefix() {
		return prefix;
	}

	public void setPrefix(String prefix) {
		this.prefix = prefix;
	}

	/**
	 * 다운로드 파일명 조회
	 *
	 * @return
	 * @throws FileNotFoundException
	 */
	public String getFilename(HttpServletRequest request) throws FileNotFoundException {
		String filename = this.getTemplateResource(request).getFilename();

		if (this.getDownloadFilename() != null) {
			filename = this.getDownloadFilename();
		}

		return filename;
	}

	/**
	 * 템플릿 조회
	 *
	 * @return
	 * @throws FileNotFoundException
	 */
	public Resource getTemplateResource(HttpServletRequest request) throws FileNotFoundException {
		Resource template;
		logger.info("TEMPLATE PATH : {}", getPrefix() + "/" + getTemplateFilename());
		template = new ServletContextResource(request.getServletContext(), getPrefix() + "/" + getTemplateFilename());
		if (template.exists()) {
			logger.info("TEMPLATE INFO : {}", template);
			return template;
		}

		throw new FileNotFoundException("Excel templateFilename not found");
	}

	public static class DefaultFilenameEncoder {

		public String encode(HttpServletRequest request, String filename) throws UnsupportedEncodingException {
			String userAgentString = request.getHeader("User-Agent");
			if (userAgentString == null)
				return filename;

			UserAgent userAgent = UserAgent.parseUserAgentString(userAgentString);
			Browser browser = userAgent.getBrowser();
			String encoding = request.getCharacterEncoding();

			if (Browser.IE.equals(browser.getGroup()))
				return java.net.URLEncoder.encode(filename, encoding);
			else
				return new String(filename.getBytes(encoding), "ISO-8859-1");
		}

	}

}