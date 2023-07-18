package de.webis;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
 
public class ResourcesServlet extends HttpServlet {

  private static final long serialVersionUID = -1319260613062890588L;
  
  private String documents;
  
  private String topics;
  
  private String topicSuggestions;
  
  @Override
  public void init(final ServletConfig config) throws ServletException {
    super.init(config);
    try {
      this.documents =
          "const documentTexts = " + Resources.loadDocumentsMap() + ";";
      this.topics =
          "const topics = " + Resources.loadTopicsMap() + ";";
      this.topicSuggestions =
          "const topicSuggestions = " + Resources.loadTopicSuggestions() + ";";
    } catch (final IOException e) {
      throw new ServletException(e);
    }
  }

  protected void doGet(
      final HttpServletRequest request,
      final HttpServletResponse response)
  throws ServletException, IOException {
    final String content = this.get(request);
    response.setContentType("text/javascript;charset=utf-8");
    try (final PrintWriter writer = response.getWriter()) {
      writer.append(content);
    }
  }
  
  protected String get(final HttpServletRequest request) {
    final String pathInfo = request.getPathInfo();
    switch (pathInfo) {
    case "/documents.js":
      return this.documents;
    case "/topics.js":
      return this.topics;
    case "/topic-suggestions.js":
      return this.topicSuggestions;
    }
    throw new IllegalArgumentException("Unknown resources: " + pathInfo);
  }
}