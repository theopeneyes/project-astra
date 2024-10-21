# Workflow 

## **Step 1: The conversion of PDF to A list of Images**
Input: Uploaded pdf file to the `/convert_pdf` endpoint

Output: A JSON with a list of images: 
`JSON {"images": List[str]}`

Example: 

```json
{
    "images":[
        "encoding_one", 
        "encoding_two", 
        .
        .
        .
        "encoding_three", 
    ]
}
```

Here the List contains `base64` encoded strings of Images. 

This list of encoded strings next go to the data loader endpoint 

## **Step 2: The data loader endpoint processing the images**

From `/convert_pdf` it comes to the `/data_loader` endpoint

Input: `List[base64_encoded_strings]`

Output: List of Dictionaries as JSON `List[Dict[str, str| int| None]]` 

Example: 

```json
[
    {
        "heading_identifier":"Carburetor",
        "heading_text":"Introduction",
        "sub_heading_text":null,
        "text_type":"text",
        "paragraph_number":1,
        "text":"Sample text about carburetor"
    }, 
    .
    .

    .
    {
        "heading_identifier":"Dinosaurs",
        "heading_text":"Jurassic Era",
        "sub_heading_text": "Trannosaurous Rex",
        "text_type":"text",
        "paragraph_number":9,
        "text":"Sample text about Dinosaurs"
    }, 

]
```

## **Step 3: The data classifier endpoint processing the JSON from the previous step** 

From `/data_loader` it goes to the `/data_classifier` endpoint

Input: Output from the previous step : `List[Dict[str, str| int| None]]`

Output: `List[Dict[str, str| int| None]]` Similar output. A list of dicitonaries with a few extra features

Example: 

```json
[
    {
        "root_concept": "Carburetor",
        "major_domains": [
            "Automotive Engineering",
        ],
        "sub_domains": [
            "Fuel Injection Systems",
        ],
        "concepts": [
            "Venturi Tube",
            "Air Supply"
        ],
        "Attributes and connections": {
            "Venturi Tube": [
                "Pressure Drop",
            ],
            "Metering Circuit": [
                "Fuel Delivery",
            ],
            "Fuel Addition": [
                "Fuel Injector",
                "Fuel Pump"
            ],
            "Air Supply": [
                "Air Filter",
            ]
        },
        "formal_representations": {
            "Venturi Tube": [
                "Flowchart"
            ],
            "Metering Circuit": [
                "Schematic",
            ],
            "Fuel Addition": [
                "Injector Diagram"
            ],
            "Air Supply": [
                "Air Filter Diagram",
                "Air Intake System Diagram"
            ]
        },
        "heading_identifier": "Carburetors",
        "heading_text": "Carburetor",
        "sub_heading_text": null,
        "text_type": "text",
        "paragraph_number": 1,
        "text": "Sample Text for Carburator"
    },
    {
        "root_concept": "Carburetors and Fuel Injection in Engines",
        "major_domains": [
            "Engine Technology",
            "Automotive Engineering",
        ],
        "sub_domains": [
            "Carburetors",
            "Fuel Injection",
        ],
        "concepts": [
            "Carburetor",
            "Generator",
        ],
        "Attributes and connections": {
            "Carburetor": [
                "Mechanical device",
                "Throttle control"
            ],
            "Fuel Injection": [
                "Electronic system",
                "Direct injection",
            ],
            "Small Engine": [
                "Low power",
            ],
            "Aircraft Engine": [
                "High power",
                "Aerodynamic design",
            ],
            "Lawnmower": [
                "Outdoor equipment",
                "Grass cutting"
            ],
            "Generator": [
                "Backup power"
            ],
            "Concrete Mixer": [
                "Construction equipment",
            ],
            "Piston Engine": [
                "Internal combustion",
            ],
            "Diesel Engine": [
                "Compression ignition",
            ]
        },
        "formal_representations": {
            "Diagrams": [
                "Carburetor schematic",
                "Fuel injection system",
            ],
            "Models": [
                "Engine performance model",
            ],
            "Frameworks": [
                "Engine technology framework",
            ]
        },
        "heading_identifier": "Carburetors",
        "heading_text": "Carburetor",
        "sub_heading_text": null,
        "text_type": "text",
        "paragraph_number": 2,
        "text": "Sample text for Carburator Engines"
    }
]

```

## **Step 4: Question Answer Generation endpoint taking input from the data classifier endpoint**

From `/data_classifier` endpoint it goes to the `/generation` endpoint

Input: Previous Input from JSON `List[Dict[str, str| int| None]]`

Output: For now it's a string but eventually it has to be a `List[Dict[str, str]]`

Example: 
```json
[
    {
        "question": "Sample Question", 
        "answer": "sample answer", 
    }, 
    .
    .

    . 
    {
        "question": "Another sample question", 
        "answer": "Another sample answer", 
    }
]
```


