package com.diquest.lltp.common.utils;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

import com.ibm.icu.text.CharsetDetector;
import com.ibm.icu.text.CharsetMatch;

public class FileEncodingCheck {

	public static String getTextFileEncoding(String path) {
		CharsetDetector detector = null;
		CharsetMatch match;

		FileInputStream fis = null;
		File f = new File(path);
		byte[] byteData = new byte[(int) f.length()];
		try {
			fis = new FileInputStream(f);
			fis.read(byteData);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (fis != null) {
				try {
					fis.close();
				} catch (IOException e) {
				}
			}
		}
		detector = new CharsetDetector();
		detector.setText(byteData);
		match = detector.detect();
		if (match == null) {
			return "UTF-8";
		}
		return match.getName();
	}
}
