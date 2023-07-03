const previewElement = document.getElementById('student-info-preview');

const placeholderElement = document.getElementById('student-info-placeholder');

const personalityColumn = document.getElementById('student-info-personality');

let serverState = undefined;



function previewStudentInfo(studentId){
    if (serverState == undefined)
        return;

    studentInfo = JSON.parse(serverState.studentsStates[studentId]);

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


