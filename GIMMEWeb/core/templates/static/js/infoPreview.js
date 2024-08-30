let previewElement = $('#student-info-preview_professor_dash'),
    placeholderElement = $('#student-info-placeholder_professor_dash'),
    infoName = $('#student-info-name_professor_dash'),
    infoEmail = $('#student-info-email_professor_dash'),
    availableTagsTable = $('#student-info-available-tags-table_professor_dash'),
    assignedTagsTable = $('#student-info-assigned-tags-table_professor_dash'), 
    assignTagButton = $('#assign-tag-to-student-button_professor_dash');

let currentTargetId = undefined;


function previewInfo(currServerState, infoType, id){

    currentTargetId = id;
    if(infoType === "student"){
        previewElement = $('#student-info-preview_professor_dash');
        placeholderElement = $('#student-info-placeholder_professor_dash');
        availableTagsTable = $('#student-info-available-tags-table_professor_dash');
        assignedTagsTable = $('#student-info-assigned-tags-table_professor_dash');
        assignTagButton = $('#assign-tag-to-student-button_professor_dash');
    }
    else if(infoType === "task"){
        previewElement = $('#task-info-preview_professor_dash');
        placeholderElement = $('#task-info-placeholder_professor_dash');
        availableTagsTable = $('#task-info-available-tags-table_professor_dash');
        assignedTagsTable = $('#task-info-assigned-tags-table_professor_dash');
        assignTagButton = $('#assign-tag-to-task-button_professor_dash');
    }
    else{
        return;
    }
    
    previewElement.hide(500, function() {
        if(infoType === "student"){
            $.ajax(
                {
                    url: '/fetchStudentInfo/',
                    type: 'POST',
                    dataType: 'json',
                    data: {'username': id},
                    complete:
                        function (res) {
                            $('#student-info-name_professor_dash').text(res.responseJSON.fullname);
                            $('#student-info-email_professor_dash').text(res.responseJSON.email);
                            var assignedTags = res.responseJSON.tags;
                            updateAssignedTagsTable(assignedTags);
                        }
                });
            
        }else if(infoType === "task"){
    
            $.ajax({
                url: '/fetchTasksFromId/',
                type: 'POST',
                dataType: 'json',
                data: {'tasks': id},
                success:
                    function (res) {
                        $('#task-info-desc_professor_dash').text(res[0].description);
                        $('#task-info-files_professor_dash').text(res[0].files);
                        var assignedTags = res[0].tags;
                        updateAssignedTagsTable(assignedTags);
                    }
            });
        }else{
            return;
        }
        updateAvailableTagsTable(currServerState);
        hideInfoPlaceholder();
    });
    previewElement.show(500);
}


function updateAvailableTagsTable(serverState){
    assignTagButton.toggleClass('active', true);

    availableTagsTable.empty();
    availableTagsTable.show();

    var serverTags = serverState.studentTags;
    var tags = $('<div></div>');

    serverTags.forEach(tag => {
        if (!tag.is_assignable)
            return;
        
        const element = $("<span class='card-tag pointer'></span>").text(tag.name);
        element.on('click', function(){
            const data = {name: tag.name, target: tag.target, targetId: currentTargetId};

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


function updateAssignedTagsTable(assignedTags){
    assignedTagsTable.empty();
    var tags = $("<div></div>");
    assignedTags.forEach(tag => {
        const element = $("<span class='card-tag'></span>").text(tag.name);

        if (tag.is_assignable) {
            const removeDiv = $("<div class='has-tooltip-arrow  assigned-tag-remove-button' data-tooltip='Remove tag'></div>");
            const removeButton = $("<div class='fa fa-remove pointer'></div>");

            removeDiv.append(removeButton);       
            removeDiv.on('click', function(){
                const data = {tag: tag.name, target: tag.target, targetId: currentTargetId};
                
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
function hideInfoPlaceholder(){
    placeholderElement.hide(500);
    previewElement.show(500);
}


function showStudentInfoPlaceholder(){
    placeholderElement.show(500);
    previewElement.hide(500);
}