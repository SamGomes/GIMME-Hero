let previewElement = $('#student-info-preview_professor_dash'),
    placeholderElement = $('#student-info-placeholder_professor_dash'),
    infoName = $('#student-info-name_professor_dash'),
    infoEmail = $('#student-info-email_professor_dash'),
    availableTagsTable = $('#student-info-available-tags-table_professor_dash'),
    assignedTagsTable = $('#student-info-assigned-tags-table_professor_dash'), 
    assignTagButton = $('#assign-tag-to-student-button_professor_dash');


let serverState = undefined;
let currentElem = undefined;


function previewInfo(currServerState, infoType, id){

    if(infoType === "student"){
        console.log(currServerState);
        console.log(infoType+','+id);

        $.ajax(
            {
                url: '/fetchStudentInfo/',
                type: 'POST',
                dataType: 'json',
                data: {'username': id},
                complete:
                    function (res) {
                        console.log(res);
                        $('#student-info-name_professor_dash').text(res.responseJSON.fullname);
                        $('#student-info-email_professor_dash').text(res.responseJSON.email);
                    }
            });
        
        
        previewElement = $('#student-info-preview_professor_dash');
        placeholderElement = $('#student-info-placeholder_professor_dash');
        availableTagsTable = $('#student-info-available-tags-table_professor_dash');
        assignedTagsTable = $('#student-info-assigned-tags-table_professor_dash');
        assignTagButton = $('#assign-tag-to-student-button_professor_dash');
    }else if(infoType === "task"){

        $.ajax({
            url: '/fetchTasksFromId/',
            type: 'POST',
            dataType: 'json',
            data: {'tasks': id},
            success:
                function (res) {
                    console.log(res);
                    $('#task-info-desc_professor_dash').text(res[0].description);
                    $('#task-info-files_professor_dash').text(res[0].files);
                }
        });
        
        previewElement = $('#task-info-preview_professor_dash');
        placeholderElement = $('#task-info-placeholder_professor_dash');
        availableTagsTable = $('#task-info-available-tags-table_professor_dash');
        assignedTagsTable = $('#task-info-assigned-tags-table_professor_dash');
        assignTagButton = $('#assign-tag-to-task-button_professor_dash');
    }else{
        return;
    }
    
    previewElement.hide(500, function() {
        updateAssignedTagsTable();
        updateAvailableTagsTable();
        hideStudentInfoPlaceholder();
    });
    previewElement.show(500);
}


function updateAvailableTagsTable(){
    assignTagButton.toggleClass('active', true);

    availableTagsTable.empty();
    availableTagsTable.show();

    var serverTags = serverState.studentTags;
    var tags = $('<div></div>');

    serverTags.forEach(tag => {
        if (!tag.is_assignable)
            return;
        
        const element = $("<span class='assignable-tag pointer'></span>").text(tag.name);
        element.on('click', function(){
            const data = {name: tag.name, target: tag.target, student: currentElem};

            $.ajax({
                url: '/assignTag/',
                type: 'POST',
                data: data
            });
        });
        tags.append(element);
    });
    availableTagsTable.append(tags);
    
}


function updateAssignedTagsTable(){
    assignedTagsTable.empty();

    var serverTags = serverState.studentTags;
    var tags = $("<div style='display: flex; flex-wrap: wrap; margin-top: 0.3em;'></div>");

    serverTags.forEach(tag => {
        const element = $("<span class='assigned-tag'></span>").text(tag.name);

        if (tag.is_assignable) {
            const removeDiv = $("<div class='has-tooltip-arrow  assigned-tag-remove-button' style='font-size: .75rem; color: #131444; height: fit-content; padding: 0.2em; margin: 0.2em;' data-tooltip='Remove tag'></div>");
            const removeButton = $("<div class='fa fa-remove pointer' style='padding-left: 0.5em;'></div>");

            removeDiv.append(removeButton);       
            removeDiv.on('click', function(){
                const data = {tag: tag.name, target: tag.target, student: currentElem};
                
                $.ajax({
                    url: '/removeAssignedTag/',
                    type: 'POST',
                    data: data,
                    success: function(result) {},
                    error: function(error) {}
                });
            });
              
            element.append(removeDiv);
        }

        tags.append(element);
    });
    
    assignedTagsTable.append(tags);
}
function hideStudentInfoPlaceholder(){
    placeholderElement.hide(500);
    previewElement.show(500);
}


function showStudentInfoPlaceholder(){
    placeholderElement.show(500);
    previewElement.hide(500);
}


function updateStudentInfoPreview(newServerState){
    serverState = newServerState;

    if (currentElem)
    {
        if (!serverState.studentsStates[currentElem]){
            showStudentInfoPlaceholder();
            return;
        }
        else {
            info = JSON.parse(serverState.studentsStates[currentElem]);
        }
    }

    updateAssignedTagsTable();
    updateAvailableTagsTable();
}