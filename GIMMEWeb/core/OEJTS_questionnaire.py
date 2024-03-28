from django.utils import timezone
from GIMMEWeb.core.models import Questionnaire, Submission, LikertQuestion, LikertQuestionnaire, QuestionnaireType



# The Open Extended Jungian Type Scales was developed to be an open source alternative to the Myers-Briggs Type Indicator. 
# http://openpsychometrics.org/tests/OJTS/development/

# IE = 30 - (Q3) - (Q7) - (Q11) + (Q15) - (Q19) + (Q23) + (Q27) - (Q31) = ___

# SN = 12 + (Q4) + (Q8) + (Q12) + (Q16) + (Q20) - (Q24) - (Q28) + (Q32) = ___

# FT = 30 - (Q2) + (Q6) + (Q10) - (Q14) - (Q18) + (Q22) - (Q26) - (Q30) = ___

# JP = 18 + (Q1) + (Q5) - (Q9)  + (Q13) - (Q17) + (Q21) - (Q25) + (Q29) = ___


def calculate_IE(data):
    result = (30 - int(data['question_3']) - int(data['question_7']) 
	             - int(data['question_11']) + int(data['question_15']) 
		         - int(data['question_19']) + int(data['question_23']) 
		         + int(data['question_27']) - int(data['question_31']))
    
    if result > 24:
        return 'E'
    else:
        return 'I'


def calculate_SN(data):
    result = (12 + int(data['question_4']) + int(data['question_8']) 
	             + int(data['question_12']) + int(data['question_16']) 
		         + int(data['question_20']) - int(data['question_24']) 
		         - int(data['question_28']) + int(data['question_32']))
    
    if result > 24:
        return 'N'
    else:
        return 'S'


def calculate_FT(data):
    result = (30 - int(data['question_2']) + int(data['question_6']) 
	             + int(data['question_10']) - int(data['question_14']) 
		         - int(data['question_18']) + int(data['question_22']) 
		         - int(data['question_26']) - int(data['question_30']))
    
    if result > 24:
        return 'T'
    else:
        return 'F'


def calculate_JP(data):
    result = (18 + int(data['question_1']) + int(data['question_5']) 
	             - int(data['question_9']) + int(data['question_13']) 
		         - int(data['question_17']) + int(data['question_21']) 
		         - int(data['question_25']) + int(data['question_29']))
    
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
        description='The following questionnaire consists of 32 pairs of descriptors, connected by a five point scale. For each pair, you must choose where on the scale between them you think you are. For example, if the pair is “angry” versus “calm”, you should circle a 1 if you are always angry and never calm, a 3 if you are half and half, etc.',
        is_active=True,
        created_at=timezone.now(),
        type=QuestionnaireType.MBTI,
        dashboard_message='In order to complete your profile, please answer the <b class="contrast-color">First Questionnaire</b> below.</p>'
    )

    # Create LikertQuestion instances
    question_1 = LikertQuestion.objects.create(
        left_extremity='makes lists',
        right_extremity='relies on memory'
    )
    question_2 = LikertQuestion.objects.create(
        left_extremity='sceptical',
        right_extremity=' wants to believe'
    )
    question_3 = LikertQuestion.objects.create(
        left_extremity='bored by time alone',
        right_extremity='needs time alone'
    )
    question_4 = LikertQuestion.objects.create(
        left_extremity='accepts things as they are',
        right_extremity='unsatisfied with the ways things are'
    )
    question_5 = LikertQuestion.objects.create(
        left_extremity='keeps a clean room',
        right_extremity='just puts stuff where ever'
    )
    question_6 = LikertQuestion.objects.create(
        left_extremity='thinks "robotic" is an insult',
        right_extremity='strives to have a mechanical mind'
    )
    question_7 = LikertQuestion.objects.create(
        left_extremity='energetic',
        right_extremity='mellow'
    )
    question_8 = LikertQuestion.objects.create(
        left_extremity='prefer to take multiple choice test',
        right_extremity='prefer essay answers'
    )
    question_9 = LikertQuestion.objects.create(
        left_extremity='chaotic',
        right_extremity='organized'
    )
    question_10 = LikertQuestion.objects.create(
        left_extremity='easily hurt',
        right_extremity='thick-skinned'
    )
    question_11 = LikertQuestion.objects.create(
        left_extremity='works best in groups',
        right_extremity='works best alone'
    )
    question_12 = LikertQuestion.objects.create(
        left_extremity='focused on the present',
        right_extremity='focused on the future'
    )
    question_13 = LikertQuestion.objects.create(
        left_extremity='plans far ahead',
        right_extremity='plans at the last minute'
    )
    question_14 = LikertQuestion.objects.create(
        left_extremity='wants people\'s respect',
        right_extremity='wants their love'
    )
    question_15 = LikertQuestion.objects.create(
        left_extremity='gets worn out by parties',
        right_extremity='gets fired up by parties'
    )
    question_16 = LikertQuestion.objects.create(
        left_extremity='fits in',
        right_extremity='stands out'
    )
    question_17 = LikertQuestion.objects.create(
        left_extremity='keeps options open',
        right_extremity='commits'
    )
    question_18 = LikertQuestion.objects.create(
        left_extremity='wants to be good at fixing things ',
        right_extremity='wants to be good at fixing people'
    )
    question_19 = LikertQuestion.objects.create(
        left_extremity='talks more',
        right_extremity='listens more'
    )
    question_20 = LikertQuestion.objects.create(
        left_extremity='when describing an event, will tell people what happened',
        right_extremity='when describing an event, will tell people what it meant'
    )
    question_21 = LikertQuestion.objects.create(
        left_extremity='gets work done right away',
        right_extremity='procrastinates'
    )
    question_22 = LikertQuestion.objects.create(
        left_extremity='follows the heart',
        right_extremity='follows the head'
    )
    question_23 = LikertQuestion.objects.create(
        left_extremity='stays at home',
        right_extremity='goes out on the town'
    )
    question_24 = LikertQuestion.objects.create(
        left_extremity='wants the big picture',
        right_extremity='wants the details'
    )
    question_25 = LikertQuestion.objects.create(
        left_extremity='improvises',
        right_extremity='prepares'
    )
    question_26 = LikertQuestion.objects.create(
        left_extremity='bases morality on justice',
        right_extremity='bases morality on compassion'
    )
    question_27 = LikertQuestion.objects.create(
        left_extremity='finds it difficult to yell very loudly',
        right_extremity='yelling to others when they are far away comes naturally'
    )
    question_28 = LikertQuestion.objects.create(
        left_extremity='theoretical',
        right_extremity='empirical'
    )
    question_29 = LikertQuestion.objects.create(
        left_extremity='works hard',
        right_extremity=' plays hard'
    )
    question_30 = LikertQuestion.objects.create(
        left_extremity='uncomfortable with emotions',
        right_extremity='values emotions'
    )
    question_31 = LikertQuestion.objects.create(
        left_extremity='likes to perform in front of other people',
        right_extremity='avoids public speaking'
    )
    question_32 = LikertQuestion.objects.create(
        left_extremity='likes to know "who?", "what?", "when?"',
        right_extremity='likes to know "why?"'
    )

    # Add the LikertQuestion instances to the LikertQuestionnaire
    questionnaire.questions.add(question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10,
                                question_11, question_12, question_13, question_14, question_15, question_16, question_17, question_18, question_19, question_20,
                                question_21, question_22, question_23, question_24, question_25, question_26, question_27, question_28, question_29, question_30,
                                question_31, question_32)

