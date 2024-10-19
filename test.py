import requests 
import os 

from typing import Dict, List

# reading a test pdfs from the endpoint  
PDF_BASE_PATH: str = "pdfs" 
API_URL: str = "http://127.0.0.1:8000"

topics: str = ["computer science", "Data structres", "Arrays", "Linked List"]

book_text: str = '''
In computer science, an array is a data structure consisting of a collection of elements (values or variables), of same memory size, each identified by at least one array index or key. An array is stored such that the position of each element can be computed from its index tuple by a mathematical formula.[1][2][3] The simplest type of data structure is a linear array, also called a one-dimensional array.
For example, an array of ten 32-bit (4-byte) integer variables, with indices 0 through 9, may be stored as ten words at memory addresses 2000, 2004, 2008, ..., 2036, (in hexadecimal: 0x7D0, 0x7D4, 0x7D8, ..., 0x7F4) so that the element with index i has the address 2000 + (i × 4).[4] The memory address of the first element of an array is called first address, foundation address, or base address.
Because the mathematical concept of a matrix can be represented as a two-dimensional grid, two-dimensional arrays are also sometimes called "matrices". In some cases the term "vector" is used in computing to refer to an array, although tuples rather than vectors are the more mathematically correct equivalent. Tables are often implemented in the form of arrays, especially lookup tables; the word "table" is sometimes used as a synonym of array.
Arrays are among the oldest and most important data structures, and are used by almost every program. They are also used to implement many other data structures, such as lists and strings. They effectively exploit the addressing logic of computers. In most modern computers and many external storage devices, the memory is a one-dimensional array of words, whose indices are their addresses. Processors, especially vector processors, are often optimized for array operations.
Arrays are useful mostly because the element indices can be computed at run time. Among other things, this feature allows a single iterative statement to process arbitrarily many elements of an array. For that reason, the elements of an array data structure are required to have the same size and should use the same data representation. The set of valid index tuples and the addresses of the elements (and hence the element addressing formula) are usually,[3][5] but not always,[2] fixed while the array is in use.
The term "array" may also refer to an array data type, a kind of data type provided by most high-level programming languages that consists of a collection of values or variables that can be selected by one or more indices computed at run-time. Array types are often implemented by array structures; however, in some languages they may be implemented by hash tables, linked lists, search trees, or other data structures.
The term is also used, especially in the description of algorithms, to mean associative array or "abstract array", a theoretical computer science model (an abstract data type or ADT) intended to capture the essential properties of arrays.
'''.strip()

null: None = None
data_classifier_json: List[Dict[str, int|str|None]] = [
    {
        "heading_identifier":"Carburetor",
        "heading_text":"Introduction",
        "sub_heading_text":null,
        "text_type":"text",
        "paragraph_number":1,
        "text":"A carburetor (also spelled carburettor or carburetter) is a device used by a gasoline internal combustion engine to control and mix air and fuel entering the engine. The primary method of adding fuel to the intake air is through the Venturi tube in the main metering circuit, though various other components are also used to provide extra fuel or air in specific circumstances."
    },
    {
        "heading_identifier":"Carburetor",
        "heading_text":"Introduction",
        "sub_heading_text":null,
        "text_type":"text",
        "paragraph_number":2,
        "text":"Since the 1990s, carburetors have been largely replaced by fuel injection for cars and trucks, but carburetors are still used by some small engines (e.g., lawnmowers, generators, and concrete mixers) and motorcycles. In addition, they are still widely used on piston engine driven aircraft. Diesel engines have always used fuel injection instead of carburetors, as the compression-based combustion of diesel requires the greater precision and pressure of fuel-injection."
        },
    {
        "heading_identifier":"Carburetor",
        "heading_text":"Etymology",
        "sub_heading_text":null,
        "text_type":"text",
        "paragraph_number":3,
        "text":"The name \"carburetor\" is derived from the verb carburet, which means \"to combine with carbon\", or, in particular, \"to enrich a gas by combining it with carbon or hydrocarbons\". Thus a carburetor mixes intake air with hydrocarbon-based fuel, such as petrol or AutoGas (LPG)."
    },
    {
        "heading_identifier":"Carburetor",
        "heading_text":"Etymology",
        "sub_heading_text":null,
        "text_type":"text",
        "paragraph_number":4,
        "text":"The name is spelled \"carburetor\" in American English and \"carburettor\" in British English. Colloquial abbreviations include carb in the UK and North America or Carby in Australia."
    },{
        "heading_identifier":"Carburetor",
        "heading_text":"Etymology",
        "sub_heading_text":null,
        "text_type":"text",
        "paragraph_number":5,
        "text":"Air from the atmosphere enters the carburetor (usually via an air cleaner), has fuel added within the carburetor, passes into the inlet manifold, then through the inlet valve(s), and finally into the combustion chamber. Most engines use a single carburetor shared between all of the cylinders, though some high-performance engines historically had multiple carburetors."},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":6,"text":"The carburetor works on Bernoulli's principle: the static pressure of the intake air reduces at higher speeds, drawing more fuel into the airstream. In most cases (except for the accelerator pump), the driver pressing the throttle pedal does not directly increase the fuel entering the engine. Instead, the airflow through the carburetor increases, which in turn increases the amount of fuel drawn into the intake mixture."},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":7,"text":"The main disadvantage of basing a carburetor's operation on Bernoulli's Principle is that being a fluid dynamic device, the pressure reduction in a venturi tends to be proportional to the square of the intake airstream. The fuel jets are much smaller and fuel flow is limited mainly by the fuel's viscosity so that the fuel flow tends to be proportional to the pressure difference. So jets sized for full power tend to starve the engine at lower speed and part throttle. Most commonly this has been corrected by using multiple jets. In SU and other (e.g. Zenith-Stromberg) variable jet carburetors, it was corrected by varying the jet size."},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":1,"text":"Galena, also called lead glance, is the natural mineral form of lead(II) sulfide (PbS). It is the most important ore of lead and an important source of silver.[5]"},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":2,"text":"Galena is one of the most abundant and widely distributed sulfide minerals. It crystallizes in the cubic crystal system often showing octahedral forms. It is often associated with the minerals sphalerite, calcite and fluorite."},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":3,"text":"In some deposits, the galena contains up to 0.5% silver, a byproduct that far surpasses the main lead ore in revenue.[9] In these deposits significant amounts of silver occur as included silver sulfide mineral phases or as limited silver in solid solution within the galena structure. These argentiferous galenas have long been an important ore of silver.[6][10] Silver-bearing galena is almost entirely of hydrothermal origin; galena in lead-zinc deposits contains little silver.[8]"},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":4,"text":"Galena deposits are found worldwide in various environments.[4] Noted deposits include those at Freiberg in Saxony;[2] Cornwall, the Mendips in Somerset, Derbyshire, and Cumberland in England; the Linares mines in Spain were worked from before the Roman times until the end of the 20th century;[11] the Madan and Rhodope Mountains in Bulgaria; the Sullivan Mine of British Columbia; Broken Hill and Mount Isa in Australia; and the ancient mines of Sardinia."},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":5,"text":"In the United States, it occurs most notably as lead-zinc ore in the Mississippi Valley type deposits of the Lead Belt in southeastern Missouri, which is the largest known deposit.[2] and in the Driftless Area of Illinois, Iowa and Wisconsin, providing the origin of the name of Galena, Illinois, a historical settlement known for the material. Galena was also a major mineral of the zinc-lead mines of the tri-state district around Joplin in southwestern Missouri and the adjoining areas of Kansas and Oklahoma.[2] Galena is also an important ore mineral in the silver mining regions of Colorado, Idaho, Utah and Montana. Of the latter, the Coeur d'Alene district of northern Idaho was most prominent.[2]"},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":6,"text":"Australia is the world's leading producer of lead as of 2021, most of which is extracted as galena. Argentiferous galena was accidentally discovered at Glen Osmond in 1841, and additional deposits were discovered near Broken Hill in 1876 and at Mount Isa in 1923.[12] Most galena in Australia is found in hydrothermal deposits emplaced around 1680 million years ago, which have since been heavily metamorphosed.[13]"},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":7,"text":"The largest documented crystal of galena is composite cubo-octahedra from the Great Laxey Mine, Isle of Man, measuring 25 cm × 25 cm × 25 cm (10 in × 10 in × 10 in).[14]"},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":1,"text":"Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. Unqualified, the word football generally means the form of football that is the most popular where the word is used. Sports commonly called football include association football (known as soccer in Australia, Canada, South Africa, the United States, and sometimes in Ireland and New Zealand); Australian rules football; Gaelic football; international rules football (specifically American football, arena football, or Canadian football); international rugby league football; and rugby union football. [1] These various forms of football share, to varying degrees, common origins and are known as \"football codes\"."},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":2,"text":"There are a number of references to traditional, ancient, or prehistoric ball games played in many different parts of the world. [2][3][4] Contemporary codes of football can be traced back to the codification of these games at English public schools during the 19th century, itself an outgrowth of medieval football. [5][6] The expansion and cultural power of the British Empire allowed these rules of football to spread to areas of British influence outside the directly controlled empire. [7] By the end of the 19th century, distinct regional codes were already developing: Gaelic football, for example, deliberately incorporated the rules of local traditional football games in order to maintain their heritage. [8] In 1888, the Football League was founded in England, becoming the first of many professional football associations. During the 20th century, several of the various kinds of football grew to become some of the most popular team sports in the world. [9]"},{"heading_identifier":"Carburetor","heading_text":"Etymology","sub_heading_text":null,"text_type":"text","paragraph_number":3,"text":"The various codes of football share certain common elements and can be grouped into two main classes of football: carrying codes like American football, Canadian football, Australian football, rugby union and rugby league, where the ball is moved about the field while being held in the hands or thrown, and kicking codes such as association football and Gaelic football, where the ball is moved primarily with the feet, and where handling is strictly limited. [10]"},{"heading_identifier":"Carburetor","heading_text":"Common rules among the sports include: [11]","sub_heading_text":null,"text_type":"text","paragraph_number":4,"text":"Two teams usually have between 11 and 18 players; some variations that have fewer players (five or more per team) are also popular. [12]"},{"heading_identifier":"Carburetor","heading_text":"Common rules among the sports include: [11]","sub_heading_text":null,"text_type":"text","paragraph_number":5,"text":"A clearly defined area in which to play the game."},{"heading_identifier":"Carburetor","heading_text":"Common rules among the sports include: [11]","sub_heading_text":null,"text_type":"text","paragraph_number":6,"text":"Scoring goals or points by moving the ball to an opposing team's end of the field and either into a goal area, or over a line."},{"heading_identifier":"Carburetor","heading_text":"Common rules among the sports include: [11]","sub_heading_text":null,"text_type":"text","paragraph_number":7,"text":"Goals or points resulting from players putting the ball between two goalposts."},{"heading_identifier":"Carburetor","heading_text":"Common rules among the sports include: [11]","sub_heading_text":null,"text_type":"text","paragraph_number":8,"text":"The goal or line being defended by the opposing team."},
    {
        "heading_identifier":"Carburetor",
        "heading_text":"Common rules among the sports include: [11]",
        "sub_heading_text":null,
        "text_type":"text",
        "paragraph_number":9,
        "text":"Players using only their body to move the ball, i.e. no additional equipment such as bats or sticks."
    }, 
    {
        "heading_identifier":"Carburetor",
        "heading_text":"Common rules among the sports include: [11]",
        "sub_heading_text":null,
        "text_type":"text",
        "paragraph_number":10,
        "text":"In all codes, common skills include passing, tackling, evasion of tackles, catching and kicking. [10] In most codes, there are rules restricting the movement of players offside, and players scoring a goal must put the ball either under or over a crossbar between the goalposts."
    }
]

def test_data_loader() -> None: 
    if not os.listdir(PDF_BASE_PATH): return 
    for pdf_filename in os.listdir(PDF_BASE_PATH): 
        with open(os.path.join(PDF_BASE_PATH, pdf_filename), "rb") as f: 
            byte_content = f.read() # reading the content in bytes 

        # test if the files are working 
        files = {
            "pdf_file": (pdf_filename, byte_content, "application/pdf"), 
        }

        response = requests.post(API_URL + "/data_loader", files=files)
        print(response.content)
        assert isinstance(response.json(), list)
    
    files = {
        "pdf_file": (pdf_filename, b'', "image/jpeg")
    }


    # test if the http error occurs correctly 
    response = requests.post(API_URL + "/data_loader", files=files, timeout=300 )
    assert response.status_code == 400  
   
def test_data_classifer() -> None: 
    headers: Dict[str, str] = {
        "Content-Type": "application/json"
    }
    response = requests.post(
        API_URL + "/data_classifier", 
        json=data_classifier_json, 
        headers=headers, 
        timeout=300, 
    )

    print(response.content)

    output_json: List[Dict] = response.json()

    for json_result in output_json: 
        assert list(json_result.keys()) == [
            "root_concept", 
            "major_domains", 
            "sub_domains", 
            "concepts", 
            "Attributes and connections", 
            "formal_representations", 
            "heading_identifier", 
            "heading_text", 
            "sub_heading_text", 
            "text_type", 
            "paragraph_number", 
            "text", 
        ]

def test_generate() -> None: 
    json: Dict[str, str|List[str]] = {
        "context": book_text, 
        "topics": topics
    }

    headers: Dict[str, str] = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        API_URL + "/generate", 
        json=json, 
        headers=headers, 
    )
    print(response.content)     
    assert isinstance(response.json()["output"], str)  


if __name__ == '__main__': 
    test_data_classifer()
    test_data_loader()
    test_generate()
