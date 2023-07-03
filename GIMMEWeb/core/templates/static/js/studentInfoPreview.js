const previewElement = document.getElementById('student-info-preview');

const placeholderElement = document.getElementById('student-info-placeholder');

const studentName = document.getElementById('student-info-name');
const studentEmail = document.getElementById('student-info-email');
const personalityColumn = document.getElementById('student-info-personality');


let serverState = undefined;



function previewStudentInfo(studentId){
    if (serverState == undefined)
        return;

    studentInfo = JSON.parse(serverState.studentsStates[studentId]);
    console.log(studentInfo);


    studentName.textContent = studentInfo.fullName;

    studentEmail.textContent = studentInfo.email;

    personalityColumn.textContent = studentInfo.personality;

    hideStudentInfoPlaceholder();
}



function hideStudentInfoPlaceholder(){
    placeholderElement.style.display = 'none';
    previewElement.style.display = 'block';
}


function showStudentInfoPlaceholder(){
    placeholderElement.style.display = 'block';
    previewElement.style.display = 'none';
}


function updateStudentInfoPreview(newServerState){
    serverState = newServerState;
}


