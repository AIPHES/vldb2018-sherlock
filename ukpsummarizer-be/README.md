# CASUM SUMMARIZER 

What is CASUM SUMMARIZER?
------------
CASUM - Computer Assisted SUMmariization

Prerequisites
-------------

* python >= 2.7 (tested with 2.7.6)
* on windows: http://aka.ms/vcpython27 

Installation
------------

1. Change the path to the system in settings.py file.
    HOME - Path where the project is present

        HOME = "~/workspace/"

    ROUGE_DIR - Path to the ROUGE files.
        
        Ex: ROUGE_DIR = HOME + "ROUGE/RELEASE-1.5.5/"

2. Install required python packages.

        pip install -r requirements.txt
        
3. [Optional] To run the system for active learning models

		 Download the Google embeddings (English) from [here](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/)
		 >> mkdir -p summarizer/data/embeddings/english
		 >> mv GoogleNews-vectors-negative300.bin.gz summarizer/data/embeddings/english
		 
		 Download the News, Wikipedia embeddings (German) from [here](https://public.ukp.informatik.tu-darmstadt.de/reimers/2014_german_embeddings/2014_tudarmstadt_german_50mincount.vec)
		 >> mkdir -p summarizer/data/embeddings/german
		 >> mv 2014_tudarmstadt_german_50mincount.vec summarizer/data/embeddings/german
		 
		 
ToRun
-------

1. Make sure that you have the raw datasets available. Each **raw** dataset needs to be extracted and follow the following directory structure:       

        +DUC2006
        |
        +--+docs
        |  |
        |  +-+D0601A
        |    | 
        |    +-+ many files
        |  |
        |  +-+D0650E
        |
        +--+models
        |  |
        |  +-+ many files
        |
        +--+topics.xml


2. Before running the pipeline, you have to preprocess the raw datasets using the `make_data.py` script. 
    
       python summarizer/data_processer/make_data.py -d DUC2006  -p ~/.ukpsummarizer/datasets/raw  -a parse -l english
       python summarizer/data_processer/make_data.py -d DUC2004  -p ~/.ukpsummarizer/datasets/raw  -a parse -l english
       python summarizer/data_processer/make_data.py -d TEST  -p ~/.ukpsummarizer/datasets/raw  -a parse -l english
       python summarizer/data_processer/make_data.py -d DBS -p ~/.ukpsummarizer/datasets/raw  -a parse -l german

   The results should then be copied into a directory. We recommend using the `--iobasedir` argument to set the directory
 
        +--+cache/
        |
        +--+datasets/
        |  |
        |  +--+raw/
        |  |
        |  +--+processed/
        |     |
        |     +--+DUC2006/
        |     |  |
        |     |  +--+D0601A/
        |     |  |  |
        |     |  |  +--+docs/
        |     |  |  |
        |     |  |  +--+docs.parsed/
        |     |  |  |
        |     |  |  +--+summaries/
        |     |  |  |
        |     |  |  +--+summaries.parsed/
        |     |  |  |
        |     |  |  +--+summaries.upperbound/
        |     |  |  |
        |     |  |  +--+task.json
        |     |  |
        |     |  +--+...
        |     |
        |     +--+ ...
        |
        +--+embeddings/
        |
        +--+english/
        |  |
        |  +-+GoogleNews->ectors-negative300.bin
        |  |
        |  +-+data/
        |
        +--+german/
           |
           +--+2014_tudarmstadt_german_50mincount.vec

3. Pre-Compute all Extractive Upper Bound summaries (or copy them from somewhere)

This step is not mandatory, as the UB will be calculated if the relevant file is not found, but will save quite some time if it has been done beforehand, though.

        python summarizer/multi_iteration_runner.py -s 100 -data /datasets/processed/DUC2004 --oracle accept_reject --summarizer_type UPPER_BOUND -p parse -l english -r rouge/RELEASE-1.5.5/ -io C:\Users\hatieke\.ukpsummarizer -out ~/.ukpsummarizer/outputs/sume.json
        python summarizer/multi_iteration_runner.py -s 250 -data /datasets/processed/DUC2006 --oracle accept_reject --summarizer_type UPPER_BOUND -p parse -l english -r rouge/RELEASE-1.5.5/ -io C:\Users\hatieke\.ukpsummarizer -out ~/.ukpsummarizer/outputs/sume.json
        
4. python pipeline.py --help for more details
    
        python pipeline.py --summary_size=100 --oracle_type=accept_reject --data_set=TEST --summarizer_type=feedback  --language=english 
        python pipeline.py --summary_size=100 --oracle_type=accept_reject --data_set=TEST --summarizer_type=baselines --language=english --rouge=rouge/RELEASE-1.5.5/ --iobasedir=~/.ukpsummarizer


Dataset notes
=============

* In DUC2004, assignment 5, topic d151h, document `APW20000104.0268` produces and
     
      xml.etree.ElementTree.ParseError: mismatched tag: line 78, column 2

    The reason is a missing opening tag `<P>` in row 72.

* In DUC2006, topic D0614E, Model Summary B `D0614.M.250.E.B`. To fix it, `Chrétien` had to be replaced by `Chretien`. (Two times)
* In DUC2007, topic D0713C, Model Summary D `D0713.M.250.C.D`. To fix it, `communiqué` had been replaced by `communique`. 
* In DUC2007, topic D0713C, Model Summary H `D0740.M.250.I.H`. To fix it, `9.27° west longitude` had been replaced by `9.27 west longitude`. 

Windows setup
=============

Verified by one (1) user.

1. download + install anaconda2 python 2.7.12 64bit from https://www.continuum.io/downloads#windows , e.g. https://repo.continuum.io/archive/Anaconda2-4.2.0-Windows-x86_64.exe
   * take care that it is NOT python 2.7.13, as that version contains a regression bug which breaks pulp
    
    ``TypeError: LoadLibrary() argument 1 must be string, not unicode``
    
    see http://bugs.python.org/issue29294
    
1. download + install strawberry perl 64bit. In my case, Strawberry Perl (5.24.0.1-64bit).
1. download + install eclipse neon.2
1. download + instlal eclipse pydev
1. install perl module `XML::DOM`
1. install python modules

	pip install -r requirements.txt
  
1. configure eclipse pydev run configuration as set up here: 
      
      --summary_size=100 --oracle_type=accept_reject --data_set=TEST --summarizer_type=feedback --language=english
 
1. Create a directory "tmp" on your root, e.g. "C:\tmp"!


![altText][pydev-windows]




[pydev-windows]: docs/windows-eclipse-pydev-run-config.png "Run configuration for windows"
  

