package com.company;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.search.highlight.*;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.Lock;
import org.apache.lucene.store.LockFactory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class Main {

    // String constants for inputs, change these according to use.

    //Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\temp\index)
    private static final String indexDirectory = "D:\\Northeastern\\Sem1\\IR\\index";

    //Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\Users\mydir\docs)
    private static final String corpusDirectory = "D:\\Northeastern\\Sem1\\IR\\ir-project\\resources\\corpus";

    //Enter the path where file containing the query terms is located (q=quit):
    private static final String queryFileDirectory = "D:\\Northeastern\\Sem1\\IR\\ir-project\\resources";

    //Enter the name of the text file containing the queries (without .txt)
    private static final String queryFileName = "queries_lucene";

    //Enter the path of the directory where the query results would be saved
    private static final String outputDirectory = "D:\\Northeastern\\Sem1\\IR\\ir-project\\output\\system_run_output\\lucene";

    //Enter the path of the directory where the snippet text for query results would be saved
    private static final String snippetDirectory = "D:\\Northeastern\\Sem1\\IR\\ir-project\\output\\system_run_output\\lucene_snippet";

    private static Analyzer analyzer = new StandardAnalyzer();
    //private static Analyzer sAnalyzer = new SimpleAnalyzer();

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {

        String indexLocation = null;
        String s = indexDirectory;

        Main indexer = null;
        try {
            indexLocation = s;
            indexer = new Main(s);
        } catch (Exception ex) {
            System.out.println("Cannot create index..." + ex.getMessage());
            System.exit(-1);
        }

        // ===================================================
        // read input from user until he enters q for quit
        // ===================================================
        while (!s.equalsIgnoreCase("q")) {
            try {

                s = corpusDirectory;

                if (s.equalsIgnoreCase("q")) {
                    break;
                }

                // try to add file into the index
                indexer.indexFileOrDirectory(s);
                s = "q";
            } catch (Exception e) {
                System.out.println("Error indexing " + s + " : "
                        + e.getMessage());
            }
        }

        // ===================================================
        // after adding, we always have to call the
        // closeIndex, otherwise the index is not created
        // ===================================================
        indexer.closeIndex();

        // =========================================================
        // Now search
        // =========================================================
        IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexLocation)));
        IndexSearcher searcher = new IndexSearcher(reader);
        TopScoreDocCollector collector;

        s = "";
        while (!s.equalsIgnoreCase("q")) {
            try {
                s = queryFileDirectory;
                String name = queryFileName;
                String outDir = outputDirectory;
                String snippetDir = snippetDirectory;

                File file = new File(s+"\\"+name+".txt");
                BufferedReader f = new BufferedReader(new FileReader(file));

                List<String> queryList = new ArrayList<String>();

                String st;
                while((st=f.readLine())!=null){
                    queryList.add(st);
                }

                f.close();

                if (s.equalsIgnoreCase("q")) {
                    break;
                }

                int queryId = 0;
                for(String queryString : queryList) {

                    queryId++;
                    collector = TopScoreDocCollector.create(100);
                    Query q = new QueryParser("contents",
                            analyzer).parse(queryString.substring(2));
                    searcher.search(q, collector);
                    ScoreDoc[] hits = collector.topDocs().scoreDocs;

                    Formatter formatter = new SimpleHTMLFormatter();
                    QueryScorer queryScorer = new QueryScorer(q);
                    Highlighter highlighter = new Highlighter(formatter, queryScorer);
                    Fragmenter fragmenter = new SimpleSpanFragmenter(queryScorer, 20);
                    highlighter.setTextFragmenter(fragmenter);

                    // 4. display & save results

                    FileWriter outFile = new FileWriter(outDir+"\\lucene_query_"+queryId+".txt");
                    BufferedWriter bw = new BufferedWriter(outFile);

                    FileWriter snippetFile = new FileWriter(snippetDir+"\\snippet_query_"+queryId+".html");
                    BufferedWriter bwSnippet = new BufferedWriter(snippetFile);

                    bwSnippet.write("<h2>Query - "+queryString+"</h2>");

                    System.out.println("\nQuery-"+queryString);
                    System.out.println("Found " + hits.length + " hits.");
                    for (int i = 0; i < hits.length; ++i) {
                        int docId = hits[i].doc;
                        Document d = searcher.doc(docId);

                        String docContent = d.get("contents");

                        TokenStream stream = TokenSources.getTokenStream("contents",null,docContent,analyzer,-1);
                        String[] frags = highlighter.getBestFragments(stream, docContent, 20);

                        for (String frag : frags)
                        {

                            bwSnippet.write("<h3>"+d.get("filename")+"</h3><br>");

                            bwSnippet.write("=========================<br>");

                            bwSnippet.write(frag+"<br>");

                            bwSnippet.write("****************************<br><br><br>");

                        }

                        System.out.println((i + 1) + ". " + d.get("path")
                                + " score=" + hits[i].score);
                        bw.write(queryId+" Q0 "+d.get("filename").substring(0,9)+" "+(i+1)+" "+hits[i].score+" lucene");
                        bw.newLine();

                    }
                    bw.close();
                    outFile.close();
                    bwSnippet.close();
                    snippetFile.close();
                    // 5. term stats --> watch out for which "version" of the term
                    // must be checked here instead!
                    Term termInstance = new Term("contents", s);
                    long termFreq = reader.totalTermFreq(termInstance);
                    long docCount = reader.docFreq(termInstance);
                    System.out.println(s + " Term Frequency " + termFreq
                            + " - Document Frequency " + docCount);

                }

            } catch (Exception e) {
                System.out.println("Error searching " + s + " : "
                        + e.getMessage());
                break;
            }
            s = "q";

        }
        System.out.println("All results saved");

    }

    /**
     * Constructor
     *
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    Main(String indexDir) throws IOException {

        FSDirectory dir = FSDirectory.open(Paths.get(indexDir));

        IndexWriterConfig config = new IndexWriterConfig(analyzer);

        writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     *
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
        // ===================================================
        // gets the list of files in a folder (if user has submitted
        // the name of a folder) or gets a single file name (is user
        // has submitted only the file name)
        // ===================================================
        addFiles(new File(fileName));

        int originalNumDocs = writer.numDocs();
        for (File f : queue) {
            FileReader fr = null;
            try {
                Document doc = new Document();

                // ===================================================
                // add contents of file
                // ===================================================
                fr = new FileReader(f);
                doc.add(new TextField("contents", new String(Files.readAllBytes(Paths.get(f.getPath()))), Field.Store.YES));
                doc.add(new StringField("path", f.getPath(), Field.Store.YES));
                doc.add(new StringField("filename", f.getName(),
                        Field.Store.YES));

                writer.addDocument(doc);
                System.out.println("Added: " + f);
            } catch (Exception e) {
                System.out.println("Could not add: " + f);
            } finally {
                fr.close();
            }
        }

        int newNumDocs = writer.numDocs();
        System.out.println("");
        System.out.println("************************");
        System.out
                .println((newNumDocs - originalNumDocs) + " documents added.");
        System.out.println("************************");

        queue.clear();
    }

    private void addFiles(File file) {

        if (!file.exists()) {
            System.out.println(file + " does not exist.");
        }
        if (file.isDirectory()) {
            for (File f : file.listFiles()) {
                addFiles(f);
            }
        } else {
            String filename = file.getName().toLowerCase();
            // ===================================================
            // Only index text files
            // ===================================================
            if (filename.endsWith(".htm") || filename.endsWith(".html")
                    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
                queue.add(file);
            } else {
                System.out.println("Skipped " + filename);
            }
        }
    }

    /**
     * Close the index.
     *
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
        writer.close();
    }
}