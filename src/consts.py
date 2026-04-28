GRAPH_PATTERNS = [
    r"\bMATCH\s*\(",          # graph match clause
    r"\bcypher\s*\(",         # Apache AGE
    r"\bCREATE\s+GRAPH\b",
    r"\bEDGE\b|\bVERTEX\b",
]

VECTOR_PATTERNS = [
    r"<->|<#>|<=>",           # distance operators
    r"\bcosine_distance\b",
    r"\bl2_distance\b",
    r"\bembedding\b",
    r"\bvector\b",
]

supported_fmts = [".csv",".xls",".xlsx",".pdf",".txt",".html",".docx",".doc",".log",".sql",".com"]

seperator = "<| . |>"

ERR_STR = ["Show Help","Error occured in OS","IO error occured","File Operation Error Occured","Library Not Found",
           "Config file not Found","Format is Unsuppported","Login Failed","Query Failed"]

DBG_STR = """Usage: python3 RelNeCraph [OPTIONS] [FILES...]\n
Options:\n-d, --DEBUG\nEnable debug mode\n
-nr=<name>\nRelational database name / identifier\n
-ng=<name>\nGraph database name / identifier\n
-vdim=<int>\nVector dimension size (integer)\n
-O0 | -O1 | -O2\nOptimization levels:\nO0 → no optimization\nO1 → basic optimization\nO2 → aggressive optimization\n
-r=<string>, --raw=<string>\nAdd raw input string \n
--csv=<string>\nAdd a csv file\n
--xls=<string>\nAdd a xls file\n
--xlsx=<string>\nAdd a xlsx file\n
--pdf=<string>\nAdd a pdf file\n
--txt=<string>\nAdd a txt file\n
--html=<string>\nAdd a html file\n
--doc=<string>\nAdd a doc file\n
--docx=<string>\nAdd a docx file\n
--log=<string>\nAdd a log file\n
--sql=<string>\nAdd a sql file\n
--link=<string>\nAdd a link to a valid page\n
-h, --help\nShow help message and exit\n
Arguments:\nFILES...\nInput files (must match supported formats)\n
Notes:
* Unknown flags or unsupported file formats will trigger this help.
* Multiple -r/--raw entries are appended in order.
* Supported File Formats: .csv, .xls, .xlsx, .pdf, .txt, .html, .docx, .doc, .log, .sql(Will be executed), LINKS.
* Using --fmt type of options assumes that you are responsible for providing the correct type of file, failure might lead to tokens wastage or malicious queries.\n"""

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",

    # Fetch metadata (many CDNs/WAFs look at these)
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",

    # Client hints (optional; some sites check)
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',

    # Contextual
    "Referer": "https://www.google.com/",
    "DNT": "1",
}

DEFAULT_VDIM = 128

STD_DB = "RelNeCraph"

STOPWORDS = set({
    "a","an","the",
    "me","my","we","your"
    "it","them","their",
    "be","been","being",
    "do","does",
    "of","to","in","for","with","on","from",
    "and","or","but","if","as",
    "such","own","so","than","too",
    "a", "an", "the",
    # Pronouns
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those",
    # Auxiliary verbs
    "am", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "having", "do", "does", "did", "doing", "would", "should", "could",
    "ought", "can", "may", "might", "must", "shall", "will",
    # Prepositions
    "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under", "again", "further",
    "then", "once", "here", "there", "when", "where", "why", "how", "all",
    "both", "each", "few", "more", "most", "other", "some", "such", "than",
    "too", "very",
    # Conjunctions
    "and", "but", "if", "or", "because", "as", "until", "while", "nor", "so",
    "yet", "though", "although", "since", "unless", "whereas", "whether",
    # Negations
    "no", "not", "nor", "none", "never", "neither", "nobody", "nothing",
    "nowhere", "hardly", "scarcely",
    # Common verbs
    "get", "got", "gets", "getting", "give", "gave", "given", "giving", "go",
    "goes", "going", "gone", "went", "make", "makes", "made", "making", "put",
    "puts", "putting", "take", "takes", "took", "taken", "taking", "come",
    "comes", "came", "coming", "see", "sees", "saw", "seen", "seeing", "know",
    "knows", "knew", "known", "knowing", "think", "thinks", "thought",
    "thinking", "say", "says", "said", "saying", "tell", "tells", "told",
    "telling", "become", "becomes", "became", "becoming", "leave", "leaves",
    "left", "leaving", "find", "finds", "found", "finding", "seem", "seems",
    "seemed", "seeming", "ask", "asks", "asked", "asking", "work", "works",
    "worked", "working", "feel", "feels", "felt", "feeling", "try", "tries",
    "tried", "trying", "use", "uses", "used", "using", "keep", "keeps", "kept",
    "keeping", "let", "lets", "letting", "begin", "begins", "began", "begun",
    "beginning", "show", "shows", "showed", "shown", "showing", "hear", "hears",
    "heard", "hearing", "play", "plays", "played", "playing", "run", "runs",
    "ran", "running", "move", "moves", "moved", "moving", "like", "likes",
    "liked", "liking", "live", "lives", "lived", "living", "believe",
    "believes", "believed", "believing", "hold", "holds", "held", "holding",
    "bring", "brings", "brought", "bringing", "happen", "happens", "happened",
    "happening", "write", "writes", "wrote", "written", "writing", "sit",
    "sits", "sat", "sitting", "stand", "stands", "stood", "standing", "lose",
    "loses", "lost", "losing", "pay", "pays", "paid", "paying", "meet", "meets",
    "met", "meeting", "include", "includes", "included", "including",
    "continue", "continues", "continued", "continuing", "set", "sets",
    "setting", "learn", "learns", "learned", "learning", "change", "changes",
    "changed", "changing", "lead", "leads", "led", "leading", "understand",
    "understands", "understood", "understanding", "watch", "watches", "watched",
    "watching", "follow", "follows", "followed", "following", "stop", "stops",
    "stopped", "stopping", "create", "creates", "created", "creating", "speak",
    "speaks", "spoke", "spoken", "speaking", "read", "reads", "reading",
    "allow", "allows", "allowed", "allowing", "add", "adds", "added", "adding",
    "spend", "spends", "spent", "spending", "grow", "grows", "grew", "grown",
    "growing", "open", "opens", "opened", "opening", "walk", "walks", "walked",
    "walking", "win", "wins", "won", "winning", "offer", "offers", "offered",
    "offering", "remember", "remembers", "remembered", "remembering", "love",
    "loves", "loved", "loving", "consider", "considers", "considered",
    "considering", "appear", "appears", "appeared", "appearing", "buy", "buys",
    "bought", "buying", "wait", "waits", "waited", "waiting", "serve", "serves",
    "served", "serving", "die", "dies", "died", "dying", "send", "sends",
    "sent", "sending", "expect", "expects", "expected", "expecting", "build",
    "builds", "built", "building", "stay", "stays", "stayed", "staying", "fall",
    "falls", "fell", "fallen", "falling", "cut", "cuts", "cutting", "reach",
    "reaches", "reached", "reaching", "kill", "kills", "killed", "killing",
    "remain", "remains", "remained", "remaining", "suggest", "suggests",
    "suggested", "suggesting", "raise", "raises", "raised", "raising", "pass",
    "passes", "passed", "passing", "sell", "sells", "sold", "selling",
    "require", "requires", "required", "requiring", "report", "reports",
    "reported", "reporting", "decide", "decides", "decided", "deciding", "pull",
    "pulls", "pulled", "pulling",
    # Quantifiers and determiners
    "any", "many", "much", "several", "enough", "little", "less", "least",
    "own", "same", "only", "just", "even", "ever", "also", "either", "neither",
    # Time-related
    "now", "today", "yesterday", "tomorrow", "tonight", "always", "often",
    "sometimes", "usually", "seldom", "rarely", "ever", "never", "already",
    "still", "yet",
    # Contractions (expanded)
    "ain", "aren", "couldn", "didn", "doesn", "hadn", "hasn", "haven", "isn",
    "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren", "won",
    "wouldn", "don", "won't", "can't", "couldn't", "didn't", "doesn't",
    "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't", "needn't",
    "shan't", "shouldn't", "wasn't", "weren't", "wouldn't", "don't", "aren't",
    "i'm", "i've", "i'll", "i'd", "you're", "you've", "you'll", "you'd", "he's",
    "he'll", "he'd", "she's", "she'll", "she'd", "it's", "it'll", "we're",
    "we've", "we'll", "we'd", "they're", "they've", "they'll", "they'd",
    "that's", "that'll", "who's", "who'll", "what's", "what'll", "where's",
    "where'll", "when's", "when'll", "why's", "why'll", "how's", "how'll",
    # Miscellaneous common words
    "yes", "okay", "ok", "um", "hmm", "ah", "oh", "well", "please", "thanks",
    "thank", "hello", "hi", "hey", "bye", "goodbye", "sorry",
    # Additional common words
    "became", "become", "becomes", "becoming", "via", "re", "per", "onto",
    "towards", "upon", "within", "without", "throughout", "hereby", "therein",
    "thereof", "thereon", "thereto", "therefore", "thus", "hence", "however",
    "moreover", "furthermore", "nevertheless", "nonetheless", "meanwhile",
    "otherwise", "instead", "besides", "aside", "apart", "across", "along",
    "among", "amongst", "around", "beyond", "behind", "beside", "besides",
    "concerning", "considering", "despite", "except", "following", "inside",
    "near", "outside", "regarding", "toward", "underneath", "unlike", "onto",
    "about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"
    ,"able","about","above","according","accordingly","across","actually","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","around","aside","ask","asking","associated","available","away","awfully","back","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","came","can","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldnt","course","currently","definitely","described","despite","did","didnt","different","do","does","doesnt","doing","done","down","downwards","during","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","example","except","far","few","fifth","first","five","followed","following","follows","former","formerly","forth","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","happens","hardly","has","hasnt","have","havent","having","he","hello","help","hence","her","here","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isnt","it","its","itself","just","keep","keeps","kept","know","knows","known","last","lately","later","latter","latterly","least","less","lest","let","like","liked","likely","little","look","looking","looks","ltd","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","que","quite","qv","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","take","taken","tell","tends","th","than","thank","thanks","thanx","that","thats","the","their","theirs","them","themselves","then","thence","there","thereafter","thereby","therefore","therein","theres","thereupon","these","they","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","value","various","very","via","viz","vs","want","wants","was","way","we","welcome","well","went","were","what","whatever","when","whence","whenever","where","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","wonder","would","yes","yet","your","yours","yourself","yourselves"
    ,"http","https","www","com","org","net","html","htm","php","amp","utm","ref","src","id","class","div","span","img","href","click","link","page","home","index","login","signup","account","user","admin","data","info","content","read","share","like","comment","subscribe","follow","terms","privacy","cookie","policy","contact","aboutus","services","product","products","company","team","career","careers","help","support","faq","download","uploads","file","files","image","images","video","videos","audio","media","feed","rss","json","xml","api","version","v1","v2","test","testing","debug","temp","tmp","sample","example","demo","default","option","options","param","params","value","values","key","keys","name","names","type","types","message","messages","session","token","tokens","auth","loginid","password","pass","username","email","phone"
    })