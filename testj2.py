from tools.translation_nllb import language_detector, detection_and_translation_nllb

que_text = '''What is oxidation, and how does it differ from reduction?
What role does oxygen play in the oxidation process?
Can oxidation occur without the involvement of oxygen? If so, give an example.

'''
x = detection_and_translation_nllb(que_text, "French")
print(x)

# ஆக்சிஜனேற்றம் என்றால் என்ன, அது குறைப்பிலிருந்து எவ்வாறு வேறுபடுகிறது?
# ஆக்ஸிஜன் ஆக்ஸிஜனேற்ற செயல்பாட்டில் என்ன பங்கு வகிக்கிறது?
# ஆக்ஸிஜன் ஈடுபடாமல் ஆக்ஸிஜனேற்றம் ஏற்பட முடியுமா? அப்படியானால், ஒரு உதாரணத்தை வழங்கவும்.

# ઓક્સિડેશન શું છે અને તે ઘટાડાથી કેવી રીતે અલગ છે?
# ઓક્સિજન ઓક્સિડેશન પ્રક્રિયામાં કઈ ભૂમિકા ભજવે છે?
# ઓક્સિડેશન ઓક્સિડેશનના સંડોવણી વિના થઈ શકે છે? જો એમ હોય તો, ઉદાહરણ આપો.

# ऑक्सीकरण क्या है और यह कमी से कैसे भिन्न होता है?
# ऑक्सीजन ऑक्सीकरण प्रक्रिया में क्या भूमिका निभाता है?
# ऑक्सीजन की भागीदारी के बिना ऑक्सीकरण हो सकता है? यदि हां, तो एक उदाहरण दें.

# Was ist Oxidation und wie unterscheidet sich sie von Reduktion?
# Welche Rolle spielt Sauerstoff im Oxidationsprozess?
# Könnte Oxidation ohne die Beteiligung von Sauerstoff stattfinden?