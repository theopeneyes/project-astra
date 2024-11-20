topic_strength_prompt: str = """
Assign the degree of relationship between the following:
{} and {}

Using the scale below, provide only a numeric value (1–5) as a JSON output that represents the degree of relationship between the text and the topic.

### Scale ###
1: Not Related
2: Weakly Related
3: Moderately Related
4: Strongly Related
5: Directly and Fully Related

### Definitions ###
Not Related (1): The text has no connection to the topic. There is no overlap in themes, ideas, or relevance.
Weakly Related (2): The text is tangentially related to the topic but does not explicitly address it or contributes minimal relevance.
Moderately Related (3): The text discusses the topic to some extent but lacks depth or direct alignment with the core theme.
Strongly Related (4): The text substantially engages with the topic, providing significant insights, context, or relevance.
Directly and Fully Related (5): The text directly addresses the topic with full alignment, providing comprehensive and highly relevant information.

###Output Format:###
You MUST write your score within <score></score> tags.
"""

representation_strength_prompt: str = """
Assess the representative value of the following text in relation to the specified topic. The representative value measures how well the text captures and reflects the essence of the topic, based on its relevance, specificity, and alignment. This is distinct from the general degree of relationship, which only considers the extent of connection between the text and the topic without evaluating its depth or clarity. Input topic {} and {}

Using the scale below, provide only High/ Medium/ Low as a JSON output that represents the representative value of the text to the topic.

### Scale ###
1: High
2: Medium
3: Low

### Definitions ###
High: The text is highly relevant, specific, and strongly aligned with the topic, effectively capturing its core elements or addressing its main aspects.
Medium: The text has moderate relevance and alignment with the topic. It includes related elements but lacks specificity or direct focus.
Low: The text is minimally relevant, vague, or only tangentially connected to the topic, failing to reflect its key aspects

###Output Format:###
You MUST write your score within <score></score> tags.
"""

representation_depth_prompt: str = """
Assess the representative depth of the following text in relation to the specified topic.
The representative depth measures the level of detail and granularity within the text concerning
the topic, focusing on how finely and specifically the subject matter is addressed.
This is distinct from the representative value, which evaluates alignment and relevance
without emphasizing detail or granularity.

Input text {} under the topic {}

Using the scale below, provide only a numeric value (1–5) as a JSON output that represents the representative depth of the text under the topic.

### Scale ###
1: Minimal detail
2: Limited detail
3: Moderately detail
4: Substantial detail
5: Exceptional detail

### Definitions ###
Minimal Detail: The text provides minimal detail and granularity, addressing the topic in a vague or overly general manner.
Limited Detail: The text offers limited detail, touching on some aspects but lacking specificity or precision.
Moderate Detail: The text presents a moderate level of detail, addressing essential aspects with a fair degree of granularity.
Substantial Detail: The text contains substantial detail, addressing key aspects with significant specificity and precision.
Exceptional Detail: The text is highly detailed, offering exceptional granularity and addressing the topic with meticulous precision.

###Output Format:###
You MUST write your score within <score></score> tags.
"""