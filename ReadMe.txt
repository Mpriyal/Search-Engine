PROJECT README:

--> To set up the environment for the programs, install Java, Python and Beautiful Soup.
 Following are the system_name for all the tasks.

Phase 1 -> Task 1 -> bm_25
		     lucene
		     smoothed_query_likelihood
		     tf_idf

	   Task 2 -> tf_idf_pseudo

	   Task 3 -> stopping -> bm_25_stopped
				 sqlm_stopped
				 tf_idf_stopped
		     stemming -> bm_25_stemmed
				 sqlm_stemmed
				 tf_idf_stemmed

Phase 2 -> lucene_snippet

Phase 3 -> evaluator (name of the script used for evaluation of all systems)

************************************************************

--> Extract the submitted zip file in a folder which will be the root directory for the project.

In this directory -

-- The 'source_code' folder contains all the source code for the project, lucene and lucene_snippet are done in java
   and the rest of the systems are written in python.

-- The 'output' folder contains the results for all tasks of the project,  inside this folder,
   'system_run_output' folder contains the resuts for phase 1 and phase 2 of the project, and
   'evaluation_output' folder contains the result for the phase 3 evaluation on all systems.

-- The 'resources' folder contains all the given resources and the intermediary resources that
   were created (index,queries,transformed documents etc.), the 'source_code' folder inside the
   'resources' folder contains all scripts that were used to generate these intermediary files.

************************************************************

NOTE -> All paths specified in the scripts are 'relative paths' so changing the ordering of any file
        in the submission folder may give errors (for running lucene_snippet_generator.java, lucene.java and evaluator.py - 
        follow instructions as mentioned below.)

-- For lucene.java and lucene_snippet_generator (using lucene 7.1.0)

   --> Firstly, set values to the string constants (indexDirectory, corpusDirectory, queryFileDirectory, queryFileName, outputDirectory, snippetDirectory)        mentioned as properties of the Main class. The default values of these variables are set for a scenario if the submitted files reside in 
       the directory 'D:\Northeastern\Sem1\IR\ir-project' whith an empty folder named 'index' present at 'D:\Northeastern\Sem1\IR'

  --> Then following jar files are required to index, search and generate snippets for the documents using lucene
      1. lucene-analyzers-common-7.1.0.jar
      2. lucene-core-7.1.0.jar
      3. lucene-highlighter-7.1.0.jar
      4. lucene-memory-7.1.0.jar
      5. lucene-queryparser-7.1.0.jar

-- For evaluator.py 
   
   --> set the global string constant 'system_name' at the top of the script to evaluate the particular system. The results are saved
       inside output->evaluation_output-> <system_name> directory. 