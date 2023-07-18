package de.webis;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Objects;

import javax.servlet.http.HttpServletRequest;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.annotation.JsonAutoDetect.Visibility;
import com.fasterxml.jackson.databind.JsonNode;

public class Storage {

  private static final File FILE = new File("judgements-new-3.json");

  public static final Storage INSTANCE = new Storage();

  private final Map<String, Map<String, Map<String, Boolean>>> judgements;

  private Storage() {
    this.judgements = new HashMap<>();
    try {
      if (FILE.exists()) {
        final JsonNode judgements = Resources.JSON_MAPPER.readTree(FILE);
        final Iterator<Entry<String, JsonNode>> judgementsOfAnnotators =
          judgements.fields();
        while (judgementsOfAnnotators.hasNext()) {
          final Entry<String, JsonNode> judgementsOfAnnotator =
              judgementsOfAnnotators.next();
          final String annotatorId = judgementsOfAnnotator.getKey();
          final Iterator<Entry<String, JsonNode>> judgementsForDocuments =
            judgementsOfAnnotator.getValue().fields();

          while (judgementsForDocuments.hasNext()) {
            final Entry<String, JsonNode> judgementsForDocument =
                judgementsForDocuments.next();
            final String documentId = judgementsForDocument.getKey();
            final Iterator<Entry<String, JsonNode>> judgementsForTopics =
                judgementsForDocument.getValue().fields();
            while (judgementsForTopics.hasNext()) {
              final Entry<String, JsonNode> judgementsForTopic =
                  judgementsForTopics.next();
              final String topicId = judgementsForTopic.getKey();
              final boolean isRelevant =
                  judgementsForTopic.getValue().booleanValue();
              this.add(documentId, topicId, annotatorId, isRelevant);
            }
          }
        }
      }
    } catch (final IOException e) {
      throw new RuntimeException(e);
    }
  }

  public void store(final HttpServletRequest request)
  throws IOException {
    try (final InputStream input = request.getInputStream()) {
      this.store(Judgement.parse(input));
    }
  }

  public void store(final Judgement judgement)
  throws IOException {
    this.store(judgement.getDocumentId(), judgement.getTopicId(),
        judgement.getAnnotatorId(), judgement.isRelevant());
  }

  public void store(
      final String documentId, final String topicId, final String annotatorId,
      final boolean isRelevant)
  throws IOException {
    this.add(documentId, topicId, annotatorId, isRelevant);

    synchronized (this) {
      Resources.JSON_MAPPER.writeValue(FILE, this.judgements);
    }
  }

  public void add(
      final String documentId, final String topicId, final String annotatorId,
      final boolean isRelevant) {
    System.out.println("Adding (" + annotatorId + "," + documentId + "," + topicId + "," + isRelevant + ")");
    synchronized (this) {
      Map<String, Map<String, Boolean>> judgementsOfAnnotator =
          this.judgements.get(Objects.requireNonNull(annotatorId));
      if (judgementsOfAnnotator == null) {
        judgementsOfAnnotator = new HashMap<>();
        this.judgements.put(annotatorId, judgementsOfAnnotator);
      }
      
      Map<String, Boolean> judgementsForDocument =
          judgementsOfAnnotator.get(documentId);
      if (judgementsForDocument == null) {
        judgementsForDocument = new HashMap<>();
        judgementsOfAnnotator.put(documentId, judgementsForDocument);
      }
      
      judgementsForDocument.put(topicId, isRelevant);
    }
  }
  
  public String getJudgements(final String annotatorId) {
    final Map<String, Map<String, Boolean>> judgementsOfAnnotator =
        this.judgements.get(Objects.requireNonNull(annotatorId));
    if (judgementsOfAnnotator == null) {
      return "{}";
    } else {
      try {
        return Resources.JSON_MAPPER.writeValueAsString(judgementsOfAnnotator);
      } catch (final JsonProcessingException e) {
        throw new IllegalStateException(e);
      }
    }
  }

  @JsonAutoDetect(
    getterVisibility = Visibility.NONE,
    setterVisibility = Visibility.NONE)
  public static class Judgement {

    public static final String JSON_DOCUMENT_ID = "documentId";

    public static final String JSON_TOPIC_ID = "topicId";

    public static final String JSON_ANNOTATOR_ID = "annotatorId";

    public static final String JSON_IS_RELEVANT = "isRelevant";
    
    private final String documentId;
    
    private final String topicId;
    
    private final String annotatorId;
    
    private final boolean isRelevant;
    
    @JsonCreator
    public Judgement(
        @JsonProperty(JSON_DOCUMENT_ID) final String documentId,
        @JsonProperty(JSON_TOPIC_ID) final String topicId,
        @JsonProperty(JSON_ANNOTATOR_ID) final String annotatorId,
        @JsonProperty(JSON_IS_RELEVANT) final boolean isRelevant) {
      this.documentId = Objects.requireNonNull(documentId);
      this.topicId = Objects.requireNonNull(topicId);
      this.annotatorId = Objects.requireNonNull(annotatorId);
      this.isRelevant = isRelevant;
    }
    
    public static Judgement parse(final InputStream input)
    throws IOException {
      return Resources.JSON_MAPPER.readValue(input, Judgement.class);
    }
    
    public String getDocumentId() {
      return this.documentId;
    }
    
    public String getTopicId() {
      return this.topicId;
    }
    
    public String getAnnotatorId() {
      return this.annotatorId;
    }
    
    public boolean isRelevant() {
      return this.isRelevant;
    }
    
  }

}
