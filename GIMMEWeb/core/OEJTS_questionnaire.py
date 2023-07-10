from django.utils import timezone
from GIMMEWeb.core.models import Questionnaire, Submission, LikertQuestion, LikertQuestionnaire, QuestionnaireType



# The Open Extended Jungian Type Scales was developed to be an open source alternative to the Myers-Briggs Type Indicator. 
# http://openpsychometrics.org/tests/OJTS/development/

# IE = 30 - (Q3) - (Q7) - (Q11) + (Q15) - (Q19) + (Q23) + (Q27) - (Q31) = ___

# SN = 12 + (Q4) + (Q8) + (Q12) + (Q16) + (Q20) - (Q24) - (Q28) + (Q32) = ___

# FT = 30 - (Q2) + (Q6) + (Q10) - (Q14) - (Q18) + (Q22) - (Q26) - (Q30) = ___

# JP = 18 + (Q1) + (Q5) - (Q9)  + (Q13) - (Q17) + (Q21) - (Q25) + (Q29) = ___


def calculate_IE(data):
    result = (30 - data['question_3'] - data['question_7'] 
	             - data['question_11'] + data['question_15'] 
		         - data['question_19'] + data['question_23'] 
		         + data['question_27'] - data['question_31'])
    
    if result > 24:
        return 'E'
    else:
        return 'I'


def calculate_SN(data):
    result = (12 + data['question_4'] + data['question_8'] 
	             + data['question_12'] + data['question_16'] 
		         + data['question_20'] - data['question_24'] 
		         - data['question_28'] + data['question_32'])
    
    if result > 24:
        return 'N'
    else:
        return 'S'


def calculate_FT(data):
    result = (30 - data['question_2'] + data['question_6'] 
	             + data['question_10'] - data['question_14'] 
		         - data['question_18'] + data['question_22'] 
		         - data['question_26'] - data['question_30'])
    
    if result > 24:
        return 'T'
    else:
        return 'F'


def calculate_JP(data):
    result = (18 + data['question_1'] + data['question_5'] 
	             - data['question_9'] + data['question_13'] 
		         - data['question_17'] + data['question_21'] 
		         - data['question_25'] + data['question_29'])
    
    if result > 24:
        return 'P'
    else:
        return 'J'


def calculate_personality_MBTI(data):
    try:
        return calculate_IE(data) + calculate_SN(data) + calculate_FT(data) + calculate_JP(data)
    except:
        print("ERROR: Incorrect amount of questions in OEJTS questionnaire (missing questions)")



def create_MBTI_questionnaire():
    # Create a LikertQuestionnaire instance
    questionnaire = LikertQuestionnaire.objects.create(
        title='First_Questionnaire',
        description='Your Questionnaire Description',
        is_active=True,
        created_at=timezone.now(),
        type=QuestionnaireType.MBTI,
        dashboard_message='Your Dashboard Message'
    )

    # Create LikertQuestion instances
    question_1 = LikertQuestion.objects.create(
        left_extremity='Strongly Disagree',
        right_extremity='Strongly Agree'
    )
    question_2 = LikertQuestion.objects.create(
        left_extremity='Not at all',
        right_extremity='Very much'
    )

    # Add the LikertQuestion instances to the LikertQuestionnaire
    questionnaire.questions.add(question_1, question_2)

