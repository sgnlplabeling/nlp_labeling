package com.diquest.lltp.modules.learning.service.download;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;

import com.diquest.lltp.domain.DocumentVo;

public class DownloadResultText extends DownloadResult {

	public DownloadResultText(String filePath, DocumentVo vo) throws Exception {
		super(filePath, vo);
		initField();
	}

	private void initField() throws Exception {
		
	}

	protected void init(String filePath) throws Exception {
		bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filePath), "UTF-8"));
	}

	protected void write() throws Exception {
		if (bw == null) {
			return;
		}
		
		bw.write(data);
	}

}
