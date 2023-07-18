package de.webis;

import java.util.logging.Logger;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.DefaultServlet;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.util.resource.ResourceCollection;

/**
 * Runs the judgement server.
 * 
 * @author johannes.kiesel@uni-weimar.de
 */
public class JudgementServer extends Thread {
  
  // -------------------------------------------------------------------------
  // LOGGING
  // -------------------------------------------------------------------------
  
  private static Logger LOG = Logger.getLogger(
      JudgementServer.class.getName());
  
  // -------------------------------------------------------------------------
  // CONSTANTS
  // -------------------------------------------------------------------------
  
  /**
   * Path in the class path at which the static resources (CSS, JavaScript) are
   * stored.
   */
  public static final String STATIC_CONTENT_RESOURCE_DIRECTORY = "web";
  
  public static final String STORAGE_SERVLET_PATH = "/judgements";
  
  public static final String RESOURCES_SERVLET_PATH = "/data/*";
  
  // -------------------------------------------------------------------------
  // MEMBERS
  // -------------------------------------------------------------------------
  
  private Server server;
  
  private ServletContextHandler contextHandler;
  
  // -------------------------------------------------------------------------
  // CONSTRUCTORS
  // -------------------------------------------------------------------------

  protected JudgementServer(final int port) {
    LOG.info("Creating server at port " + port);
    
    this.contextHandler = new ServletContextHandler();
    this.server = new Server(port);
    this.server.setHandler(
        withStaticContent(this.contextHandler));
    
    this.contextHandler.addServlet(
        new ServletHolder(StorageServlet.class),
        STORAGE_SERVLET_PATH);
    this.contextHandler.addServlet(
        new ServletHolder(ResourcesServlet.class),
        RESOURCES_SERVLET_PATH);
    this.contextHandler.setErrorHandler(new JudgementErrorHandler());
  }

  /**
   * Adds static content directories to this handler.
   * <p>
   * Directories within {@link #STATIC_CONTENT_RESOURCE_DIRECTORY} are then
   * served at the root path.
   * </p>
   * @param handler The handler
   * @return The same handler
   */
  protected static ServletContextHandler withStaticContent(
      final ServletContextHandler handler) {
    final String staticContentDirectory =
        JudgementServer.class.getClassLoader()
          .getResource(STATIC_CONTENT_RESOURCE_DIRECTORY).toExternalForm();
    handler.setBaseResource(
        new ResourceCollection(staticContentDirectory));
    handler.addServlet(DefaultServlet.class, "/");
    return handler;
  }
  
  // -------------------------------------------------------------------------
  // GETTERS
  // -------------------------------------------------------------------------
  
  /**
   * Gets the actual server object.
   * @return The server
   */
  protected Server getServer() {
    return this.server;
  }
  
  /**
   * Gets the context handler for this server.
   * @return The handler
   */
  protected ServletContextHandler getContextHandler() {
    return this.contextHandler;
  }
  
  // -------------------------------------------------------------------------
  // FUNCTIONALITY
  // -------------------------------------------------------------------------

  @Override
  public void run() {
    try {
      LOG.fine("Starting server");
      this.getServer().start();
      this.getServer().join();
    } catch (final Exception e) {
      throw new RuntimeException(e);
    }
  }
  
  // -------------------------------------------------------------------------
  // MAIN
  // -------------------------------------------------------------------------
  
  public static void main(final String[] args) {
    final JudgementServer server =
        new JudgementServer(Integer.parseInt(args[0]));
    server.run();
  }

}
