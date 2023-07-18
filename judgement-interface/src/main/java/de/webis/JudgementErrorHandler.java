package de.webis;

import java.io.IOException;
import java.io.Writer;

import javax.servlet.http.HttpServletRequest;

import org.eclipse.jetty.server.handler.ErrorHandler;

public class JudgementErrorHandler extends ErrorHandler {
 
  @Override
  protected void handleErrorPage(
      final HttpServletRequest request, final Writer writer,
      final int code, final String message)
  throws IOException {
    System.err.println("ERROR: " + message);
    writer.write("<h1>Something went wrong</h1>"
        + "Please ask the examiner for a new link,");
  }

}
