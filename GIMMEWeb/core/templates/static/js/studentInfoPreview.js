const previewElement = document.getElementById('student-info-preview');

const placeholderElement = document.getElementById('student-info-placeholder');

const studentName = document.getElementById('student-info-name');
const studentEmail = document.getElementById('student-info-email');
const personalityColumn = document.getElementById('student-info-personality');

const availableTagsTable = $('#student-info-available-tags-table');
const assignedTagsTable = $('#student-info-assigned-tags-table');

const assignTagButton = $('#assign-tag-to-student-button');



let serverState = undefined;
let currentStudent = undefined;

let listAvailableTagsVisible = false;



function previewStudentInfo(studentId){
    if (serverState == undefined)
        return;

    currentStudent = studentId;

    studentInfo = JSON.parse(serverState.studentsStates[studentId]);


    studentName.textContent = studentInfo.fullName;

    studentEmail.textContent = studentInfo.email;

    personalityColumn.textContent = studentInfo.personality;


    showAssignedTags();
    hideAvailableTags();
    hideStudentInfoPlaceholder();
}


function toggleAvailableTags(){
    if (!listAvailableTagsVisible)
        listAvailableTags();
    else
        hideAvailableTags();
}


function updateAvailableTags(){
    if (listAvailableTagsVisible)
        listAvailableTags();

    showAssignedTags();
}


function listAvailableTags(){
    if (serverState == undefined || currentStudent == undefined)
        return;

    listAvailableTagsVisible = true;
    assignTagButton.toggleClass('active', true);

    availableTagsTable.empty();
    availableTagsTable.css('display', 'block');
    
    studentInfo = JSON.parse(serverState.studentsStates[currentStudent]);
    
    studentTags = studentInfo.tags;
    serverTags = serverState.tags;

    serverTags.sort(compareTagNames);

    serverTags.forEach(tag => {
        if (studentTags.some(obj => obj.id === tag.id && obj.name === tag.name))
            return;
        
        const element = $("<span class='assignable-tag pointer'></span>").text(tag.name);

        element.on('click', function(){
            const data = {tag: tag.name, student: currentStudent};

            $.ajax({
                url: '/assignTag/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: data,
                success: function(result) {},
                error: function(error) {}
            });

            updateAvailableTags();
        });

        availableTagsTable.append(element);
        
    });

}


function showAssignedTags(){
    if (serverState == undefined || currentStudent == undefined)
        return;

    assignedTagsTable.empty();

    studentInfo = JSON.parse(serverState.studentsStates[currentStudent]);
    studentTags = studentInfo.tags;

    //studentTags.sort(compareTagNames);

    studentTags.forEach(tag => {
        const element = $("<span class='assigned-tag'></span>").text(tag.name);

        const removeDiv = $("<div class='has-tooltip-arrow  assigned-tag-remove-button' style='font-size: .75rem; color: #131444; height: fit-content; padding: 0.2em; margin: 0.2em;' data-tooltip='Remove tag'></div>");
        const removeButton = $("<div class='fa fa-remove pointer' style='padding-left: 0.5em;'></div>");

        removeDiv.append(removeButton);

        
        removeDiv.on('click', function(){
            const data = {tag: tag.name, student: currentStudent};
            
            $.ajax({
                url: '/removeAssignedTag/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: data,
                success: function(result) {},
                error: function(error) {}
            });
            
            updateAvailableTags();
        });
        
        
        element.append(removeDiv);

        assignedTagsTable.append(element);
    });

}


function hideAvailableTags(){
    availableTagsTable.css('display', 'none');
    listAvailableTagsVisible = false;
    assignTagButton.toggleClass('active', false);
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
    updateAvailableTags();
    showAssignedTags();
}


function compareTagNames( a, b ) {
    if ( a.name < b.name ){
      return -1;
    }
    if ( a.name > b.name ){
      return 1;
    }
    return 0;
  }