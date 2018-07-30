package com.diquest.lltp.modules.learning.service.download;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.diquest.lltp.domain.DocumentVo;

public abstract class DownloadResult {

	protected String data;
	protected BufferedWriter bw;
	protected DocumentVo vo;
	protected Logger logger = LoggerFactory.getLogger(getClass());

	public DownloadResult(String filePath, DocumentVo vo) throws Exception {
		this.vo = vo;
		try {
			init(filePath);
		} catch (Exception e) {
			throw e;
		}
	}

	protected abstract void init(String filePath) throws Exception;

	public void setData(String data) {
		this.data = data;
		try {
			write();
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
		}
	}

	protected abstract void write() throws Exception;

	public void flush() throws Exception {
		if (bw != null) {
			bw.flush();
		}
	}

	public void close() {
		if (bw != null) {
			try {
				bw.flush();
				bw.close();
			} catch (IOException e) {
			}
		}
	}

}
