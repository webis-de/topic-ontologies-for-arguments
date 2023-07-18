package de.webis;

import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Iterator;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.opencsv.CSVReader;



public class Resources {

  public static final ObjectMapper JSON_MAPPER = new ObjectMapper();
  static {
    //JSON_MAPPER.configure(SerializationFeature.ORDER_MAP_ENTRIES_BY_KEYS, true);

  }
  public static final String RESOURCE_DOCUMENTS = "documents";
  
  public static final String RESOURCE_TOPICS = "topics";
  
  public static final String RESOURCE_TOPIC_SUGGESTIONS = "topic-suggestions";
  
  private static final String RESOURCES_DATA = "data";
  
  private static final String RESOURCES_DATA_DOCUMENTS =
      RESOURCES_DATA + "/" + RESOURCE_DOCUMENTS + ".csv";
  
  private static final String RESOURCES_DATA_TOPICS =
      RESOURCES_DATA + "/" + RESOURCE_TOPICS + ".csv";
  
  private static final String RESOURCES_DATA_TOPIC_SUGGESTIONS =
      RESOURCES_DATA + "/" + RESOURCE_TOPIC_SUGGESTIONS + ".csv";
  
  private Resources() { }
  
  public static String loadDocumentsMap()
  throws IOException {
    try (final CSVReader reader = new CSVReader(new InputStreamReader(
        ClassLoader.getSystemResourceAsStream(RESOURCES_DATA_DOCUMENTS),
        "UTF-8"))) {
      final ObjectNode root = JSON_MAPPER.createObjectNode();

      final Iterator<String[]> lines = reader.iterator();
      lines.next(); // header
      while (lines.hasNext()) {
        final String[] line = lines.next();
        final String documentId = line[0];
        final String documentText = line[1];
        root.put(documentId, documentText);

      }
      
      return JSON_MAPPER.writeValueAsString(root);
    }
  }
  
  public static String loadTopicsMap()
  throws IOException {
    try (final CSVReader reader = new CSVReader(new InputStreamReader(
        ClassLoader.getSystemResourceAsStream(RESOURCES_DATA_TOPICS),
        "UTF-8"))) {
      final ObjectNode root = JSON_MAPPER.createObjectNode();

      final Iterator<String[]> lines = reader.iterator();
      lines.next(); // header
      while (lines.hasNext()) {
        final String[] line = lines.next();
        final String topicId = line[0];
        final String topicName = line[1];
        final String topicDescription = line[3];
        final String topicOntology = line[4];
        
        final ObjectNode topic = root.putObject(topicId);
        topic.put("name", topicName);
        topic.put("description", topicDescription);
        topic.put("ontology", topicOntology);
      }
      
      return JSON_MAPPER.writeValueAsString(root);
    }
  }
  
  public static String loadTopicSuggestions()
  throws IOException {
    try (final CSVReader reader = new CSVReader(new InputStreamReader(
        ClassLoader.getSystemResourceAsStream(
            RESOURCES_DATA_TOPIC_SUGGESTIONS),
        "UTF-8"))) {
      final ObjectNode root = JSON_MAPPER.createObjectNode();

      final Iterator<String[]> lines = reader.iterator();
      lines.next(); // header
      while (lines.hasNext()) {
        final String[] line = lines.next();
        final String documentId = line[0];
        final String topicId = line[1];
        final String method = line[2];
        final double score = Double.parseDouble(line[3]);
        
        ArrayNode suggestionsForDocument = (ArrayNode) root.get(documentId);
        if (suggestionsForDocument == null) {
          suggestionsForDocument = root.putArray(documentId);
        }
        final ObjectNode topicSuggestion =
            suggestionsForDocument.addObject();
        topicSuggestion.put("documentId", documentId);
        topicSuggestion.put("topicId", topicId);
        topicSuggestion.put("method", method);
        topicSuggestion.put("score", score);
      }
      
      return JSON_MAPPER.writeValueAsString(root);
    }
  }

}
