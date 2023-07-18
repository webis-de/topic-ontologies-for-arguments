package de.webis;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import de.webis.Storage.Judgement;
 
public class StorageServlet extends HttpServlet {

  private static final long serialVersionUID = -1319260613062890588L;

  protected void doPut(
      final HttpServletRequest request,
      final HttpServletResponse response)
  throws ServletException, IOException {
    Storage.INSTANCE.store(request);
  }

  protected void doGet(
      final HttpServletRequest request,
      final HttpServletResponse response)
  throws ServletException, IOException {
    response.setContentType("application/json");
    final String annotatorId =
        request.getParameter(Judgement.JSON_ANNOTATOR_ID);
    final String responseString = Storage.INSTANCE.getJudgements(annotatorId);
    try (final PrintWriter writer = response.getWriter()) {
      writer.append(responseString);
    }
  }
}