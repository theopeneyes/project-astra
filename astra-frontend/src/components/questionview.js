import React, { useEffect, useRef } from 'react';
import { Button } from "@progress/kendo-react-buttons";

const QuestionView = () => {
    const softwarecode1 = `def reverse_string(s):
    return s[::-1]

# Test
print(reverse_string("hello"))  # Output: olleh`;
const softwarecode2 = `def top_three_numbers(nums):
    return sorted(set(nums), reverse=True)[:3]

# Test
print(top_three_numbers([3, 1, 4, 1, 5, 9]))  # Output: [9, 5, 4]`;
const softwarecode3 = `def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Test
print(fibonacci(5))  # Output: 5
        `;
const softwarecode4 = `def unique_char_count(s):
    return len(set(s))

# Test
print(unique_char_count("hello"))  # Output: 4
        `;
const softwarecode5 = `def average(nums):
    return sum(nums) / len(nums)

# Test
print(average([1, 2, 3, 4, 5]))  # Output: 3.0
        `;


        

const computationcode1 = `Profit = Cost Price × Profit Percentage  
Profit = ₹1,500 × 30% = ₹1,500 × 0.30 = ₹450  
Selling Price = Cost Price + Profit  
Selling Price = ₹1,500 + ₹450 = ₹1,950`;
const computationcode2 = `Number of girls = Total Students × Percentage of girls  
Number of girls = 120 × 25% = 120 × 0.25 = 30  
Number of boys = Total Students - Number of girls  
Number of boys = 120 - 30 = 90`;
const computationcode3 = `Distance = Speed × Time  
Distance = 80 km/h × 3 hours = 240 km`;
const computationcode4 = `Average = (Marks1 + Marks2 + Marks3 + Marks4 + Marks5 + Marks6) / Total Subjects  
Average = (75 + 85 + 90 + 80 + 70 + 95) / 6 = 495 / 6 = 82.5`;
const computationcode5 = `Area = Length × Width  
Area = 12 meters × 4 meters = 48 m²`;

    return (
        <>
            <h2>Book name here</h2>
            <div className="default-box bg-transparent p-0 border-0">
            <div className="questionview-tabs">
                <ul className="nav nav-tabs" id="myTab" role="tablist">
                    <li className="nav-item" role="presentation">
                        <button className="nav-link active" id="tab1" data-bs-toggle="tab" data-bs-target="#tab1-content" type="button" role="tab" aria-controls="tab1-content" aria-selected="true">True/False</button>
                    </li>
                    <li className="nav-item" role="presentation">
                        <button className="nav-link" id="tab2" data-bs-toggle="tab" data-bs-target="#tab2-content" type="button" role="tab" aria-controls="tab2-content" aria-selected="false">Fill in the blanks</button>
                    </li>
                    <li className="nav-item" role="presentation">
                        <button className="nav-link" id="tab3" data-bs-toggle="tab" data-bs-target="#tab3-content" type="button" role="tab" aria-controls="tab3-content" aria-selected="false">Show question answer</button>
                    </li>
                    <li className="nav-item" role="presentation">
                        <button className="nav-link" id="tab4" data-bs-toggle="tab" data-bs-target="#tab4-content" type="button" role="tab" aria-controls="tab4-content" aria-selected="false">Multiple choice</button>
                    </li>
                    <li className="nav-item" role="presentation">
                        <button className="nav-link" id="tab5" data-bs-toggle="tab" data-bs-target="#tab5-content" type="button" role="tab" aria-controls="tab5-content" aria-selected="false">Computational questions</button>
                    </li>
                    <li className="nav-item" role="presentation">
                        <button className="nav-link" id="tab6" data-bs-toggle="tab" data-bs-target="#tab6-content" type="button" role="tab" aria-controls="tab6-content" aria-selected="false">Software code questions</button>
                    </li>
                </ul>
                <div className="tab-content" id="myTabContent">
                    <div className="tab-pane fade show active" id="tab1-content" role="tabpanel" aria-labelledby="tab1">
                        <div className='questionview-content'>
                            <div className='qv-box'>
                                <h3>The layout of all elements in this image is balanced and organized.</h3>
                                <p>True. <small>(The layout shows balance and organization of the elements.)</small></p>
                            </div>
                            <div className='qv-box'>
                                <h3>The placement of the title and content sections is not clear in the image.</h3>
                                <p>False. <small>(The placement of the title and content sections is clear and organized.)</small></p>
                            </div>
                            <div className='qv-box'>
                                <h3>A grid was not used in the design.</h3>
                                <p>False. <small>(A grid has been used in the design.)</small></p>
                            </div>
                            <div className='qv-box'>
                                <h3>Font size and color play an important role in text readability.</h3>
                                <p>True. <small>(Font size and color affect text readability.)</small></p>
                            </div>
                            <div className='qv-box'>
                                <h3>The same typography has been used across all sections.</h3>
                                <p>False. <small>(Different typography has been used across sections.)</small></p>
                            </div>
                        </div>
                    </div>
                    <div className="tab-pane fade" id="tab2-content" role="tabpanel" aria-labelledby="tab2">
                    <div className='questionview-content'>
                           <div className='qv-box'>
                                <h3>The natural satellite revolving around the Earth is called __________.</h3>
                                <p>Moon</p>
                            </div>
                            <div className='qv-box'>
                                <h3>In the water cycle, water evaporates due to __________.</h3>
                                <p>Sun</p>
                            </div>
                            <div className='qv-box'>
                                <h3>The main function of blood in the human body is __________.</h3>
                                <p>Transporting oxygen</p>
                            </div>
                            <div className='qv-box'>
                                <h3>The number of fundamental rights in the Indian Constitution is __________.</h3>
                                <p>Six</p>
                            </div>
                            <div className='qv-box'>
                                <h3>The circumference of a complete circle is calculated using the constant __________.</h3>
                                <p>π (pi)</p>
                            </div>
                        </div>
                    </div>
                    <div className="tab-pane fade" id="tab3-content" role="tabpanel" aria-labelledby="tab3">
                    <div className='questionview-content'>
                            <div className='qv-box'>
                                <h3>What is climate change?</h3>
                                <p>Climate change refers to long-term changes in Earth's climate caused by natural factors or human activities.</p>
                            </div>
                            <div className='qv-box'>
                                <h3>What are the main causes of climate change?</h3>
                                <p>The main causes of climate change include greenhouse gas emissions, deforestation, and industrial activities.</p>
                            </div>
                            <div className='qv-box'>
                                <h3>What is the impact of climate change on human health?</h3>
                                <p>Climate change can negatively affect health, causing heat-related illnesses, an increase in climate-related diseases, and reduced food security.</p>
                            </div>
                            <div className='qv-box'>
                                <h3>What steps can be taken to prevent climate change?</h3>
                                <p>Steps to prevent climate change include using renewable energy, conserving energy, and protecting forests.</p>
                            </div>
                            <div className='qv-box'>
                                <h3>What are greenhouse gases?</h3>
                                <p>Greenhouse gases are gases that trap heat in the atmosphere, such as carbon dioxide, methane, and nitrous oxide.</p>
                            </div>
                        </div>
                    
                    </div>
                    <div className="tab-pane fade" id="tab4-content" role="tabpanel" aria-labelledby="tab4">
                    <div className='questionview-content'>
                            <div className='qv-box'>
                                <h3>What is the role of natural selection in the development of an organism?</h3>
                                <ul>
                                    <li>All organisms evolve equally</li>
                                    <li>Only the strongest organisms survive</li>
                                    <li className='currect-ans'>Some organisms are more adapted due to diversity</li>
                                    <li>Evolution happens only due to the environment</li>
                                    <li>Evolution is a linear process</li>
                                </ul>
                                <p className='mt-3 small'><strong>Reason:</strong>  <span>According to the theory of natural selection, organisms exhibit diversity, and certain traits make them more adapted to their environment. </span></p>
                            </div>
                            <div className='qv-box'>
                                <h3>Which element is essential for the process of photosynthesis in plants?</h3>
                                <ul>
                                    <li className='currect-ans'>Carbon dioxide</li>
                                    <li>Nitrogen</li>
                                    <li>Sulfur</li>
                                    <li>Phosphorus</li>
                                    <li>Oxygen</li>
                                </ul>
                                <p className='mt-3 small'><strong>Reason:</strong>  <span>Plants require carbon dioxide for photosynthesis, which they absorb from the atmosphere. </span></p>
                            </div>
                            <div className='qv-box'>
                                <h3>Under which principle is energy conservation explained in a chemical reaction?</h3>
                                <ul>
                                    <li>Newton's First Law of Motion</li>
                                    <li>Principle of Conservation of Energy</li>
                                    <li className='currect-ans'>First Law of Thermodynamics</li>
                                    <li>Principle of Hydrogen</li>
                                    <li>Oxidation-Reduction Principle</li>
                                </ul>
                                <p className='mt-3 small'><strong>Reason:</strong>  <span>The first law of thermodynamics explains the conservation of energy, stating that energy can neither be created nor destroyed but can only be transformed. </span></p>
                            </div>
                            <div className='qv-box'>
                                <h3>What is the alteration in the DNA of an organism called?</h3>
                                <ul>
                                    <li className='currect-ans'>Mutation</li>
                                    <li>Reproduction</li>
                                    <li>Evolution</li>
                                    <li>Genetics</li>
                                    <li>Selection</li>
                                </ul>
                                <p className='mt-3 small'><strong>Reason:</strong>  <span>Changes in DNA are called mutations, which contribute to the genetic diversity of organisms. </span></p>
                            </div>
                            <div className='qv-box'>
                                <h3>In an ecosystem, in which direction does the flow of energy occur?</h3>
                                <ul>
                                    <li>Only towards consumers</li>
                                    <li>Only towards producers</li>
                                    <li className='currect-ans'>From producers to consumers</li>
                                    <li>From consumers to decomposers</li>
                                    <li>Equally in all directions</li>
                                </ul>
                                <p className='mt-3 small'><strong>Reason:</strong>  <span>In an ecosystem, the flow of energy occurs from producers to consumers, where producers utilize the energy from the sun. </span></p>
                            </div>                            
                        </div>
                    </div>
                    <div className="tab-pane fade" id="tab5-content" role="tabpanel" aria-labelledby="tab5">
                    <div className='questionview-content'>                            
                            <div className='qv-box'>
                                <div className='q-mark'>3 Marks</div>
                                <h3>A person bought goods worth ₹1,500 and sold them at a 30% profit. What will be the total amount he will receive?</h3>
                                <div className='computationquestion'>
                                    <pre>{computationcode1}</pre>
                                </div>
                            </div>
                            <div className='qv-box'>
                                <div className='q-mark'>2 Marks</div>
                                <h3>A school has 120 students. If 25% of them are girls, how many boys are there?</h3>
                                <div className='computationquestion'>
                                    <pre>{computationcode2}</pre>
                                </div>
                            </div>
                            <div className='qv-box'>
                                <div className='q-mark'>2 Marks</div>
                                <h3>A car is traveling at a speed of 80 km/h. If it travels for 3 hours, what is the total distance covered?</h3>
                                <div className='computationquestion'>
                                    <pre>{computationcode3}</pre>
                                </div>
                            </div>
                            <div className='qv-box'>
                                <div className='q-mark'>3 Marks</div>
                                <h3>A student scored 75, 85, 90, 80, 70, and 95 marks in 6 subjects. What will be their average score?</h3>
                                <div className='computationquestion'>
                                    <pre>{computationcode4}</pre>
                                </div>
                            </div>
                            <div className='qv-box'>
                                <div className='q-mark'>2 Marks</div>
                                <h3>A rectangle has a length of 12 meters and a width of 4 meters. What is its area?</h3>
                                <div className='computationquestion'>
                                    <pre>{computationcode5}</pre>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="tab-pane fade" id="tab6-content" role="tabpanel" aria-labelledby="tab6">
                    <div className='questionview-content'>
                            <div className='qv-box'>
                                <h3>Write a function that reverses a string. For example, if the input is "hello", the output should be "olleh".</h3>
                                <pre>{softwarecode1}</pre>
                            </div>
                            <div className='qv-box'>
                                <h3>Design a function that finds the three largest numbers in a list and returns them in a new list. For example, if the input is [3, 1, 4, 1, 5, 9], the output should be [9, 5, 4].</h3>
                                <pre>{softwarecode2}</pre>
                            </div>
                            <div className='qv-box'>
                                <h3>Write a function that returns the nth Fibonacci number for a given number. For example, if n=5, the output should be 5.</h3>
                                <pre>{softwarecode3}</pre>
                            </div>
                            <div className='qv-box'>
                                <h3>Design a function that returns the count of all unique characters in a string. For example, if the input is "hello", the output should be 4.</h3>
                                <pre>{softwarecode4}</pre>
                            </div>
                            <div className='qv-box'>
                                <h3>Write a function that calculates the average of the numbers in a list. For example, if the input is [1, 2, 3, 4, 5], the output should be 3.0.</h3>
                                <pre>{softwarecode5}</pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </div>
        </>
    );
};

export default QuestionView;
