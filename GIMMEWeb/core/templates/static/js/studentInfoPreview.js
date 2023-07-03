const previewElement = document.getElementById('student-info-preview');
const placeholderElement = document.getElementById('student-info-placeholder');



function previewStudentInfo(studentId){


    hidePlaceholder();

}



function hidePlaceholder(){
    placeholderElement.style.display = 'none';
    previewElement.style.display = 'block';
}


