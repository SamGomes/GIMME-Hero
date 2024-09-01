let previewElement = $('#student-info-preview_professor_dash'),
    placeholderElement = $('#student-info-placeholder_professor_dash'),
    availableTagsTable = $('#student-info-available-tags-table_professor_dash'),
    assignedTagsTable = $('#student-info-assigned-tags-table_professor_dash'), 
    assignTagButton = $('#assign-tag-to-student-button_professor_dash');

let currentTargetId = undefined;


function previewInfo(domElement, animDelay, currServerState, infoType, id){
    
    currentTargetId = id;
    
    if(infoType === "student"){
        previewElement = $('#student-info-preview_professor_dash');
        placeholderElement = $('#student-info-placeholder_professor_dash');
        availableTagsTable = $('#student-info-available-tags-table_professor_dash');
        assignedTagsTable = $('#student-info-assigned-tags-table_professor_dash');
        assignTagButton = $('#assign-tag-to-student-button_professor_dash');

        freeTable = $('#freeUsersTable_professor_dash');
        selectedTable = $('#selectedUsersTable_professor_dash');
    }
    else if(infoType === "task"){
        previewElement = $('#task-info-preview_professor_dash');
        placeholderElement = $('#task-info-placeholder_professor_dash');
        availableTagsTable = $('#task-info-available-tags-table_professor_dash');
        assignedTagsTable = $('#task-info-assigned-tags-table_professor_dash');
        assignTagButton = $('#assign-tag-to-task-button_professor_dash');

        freeTable = $('#freeTasksTable_professor_dash');
        selectedTable = $('#selectedTasksTable_professor_dash');
    }else{
        return;
    }

    nonSelectedDomElements = Array.from(freeTable.children()[0].children).concat(
        Array.from(selectedTable.children()[0].children));
    
    if(!domElement){
        nonSelectedDomElements.forEach(node => {
            $(node).css('opacity',1.0);
        });
        showInfoPlaceholder();
        return;
    }
    
    nonSelectedDomElements.forEach(node => {
        $(node).css('opacity',0.8);
    });
    $(domElement).css('opacity',1.0);
    
    previewElement.hide(animDelay, function() {
        if(infoType === "student"){
            $.ajax({
                url: '/fetchStudentInfo/',
                type: 'POST',
                dataType: 'json',
                data: {'username': id},
                complete:
                    function (res) {
                        $('#student-info-name_professor_dash').text(res.responseJSON.fullname);
                        $('#student-info-email_professor_dash').text(res.responseJSON.email);
                        var assignedTags = res.responseJSON.tags;
                        updateAssignedTagsTable(domElement,currServerState,assignedTags);
                        updateAvailableTagsTable(domElement,infoType,currServerState,assignedTags);
                    }
            });
            
        }else if(infoType === "task"){
            $.ajax({
                url: '/fetchTasksFromId/',
                type: 'POST',
                dataType: 'json',
                data: {'tasks': id},
                complete:
                    function (res) {
                        res = res.responseJSON;
                        $('#task-info-name_professor_dash').text(id);
                        $('#task-info-desc_professor_dash').text(res[0].description);
                        $('#task-info-files_professor_dash').text(res[0].files);
                        var assignedTags = res[0].tags;
                        updateAssignedTagsTable(domElement,currServerState,assignedTags);
                        updateAvailableTagsTable(domElement,infoType,currServerState,assignedTags);
                    }
            });
        }else{
            return;
        }
        hideInfoPlaceholder();
    });
    previewElement.show(animDelay);
}


function updateAvailableTagsTable(domElement,infoType,serverState,assignedTags){
    assignTagButton.toggleClass('active', true);

    availableTagsTable.empty();
    availableTagsTable.show();
    
    var serverTags = [];
    if(infoType === "student"){
        serverTags = serverState.studentTags;
    }else if(infoType === "task"){
        serverTags = serverState.taskTags;
    }
    
    var tags = $('<i></i>');
    serverTags.forEach(tag => {
        var isAssigned = false;
        for (var i=0;i<assignedTags.length;i++){
            if (assignedTags[i].id == tag.id){
                isAssigned = true;
                break;
            }
        }
        if (!tag.is_assignable || isAssigned){
            return;
        }
        
        const element = $("<span class='card-tag pointer'></span>").text(tag.name);
        element.on('click', function(){
            const data = {name: tag.name, target: tag.target, targetId: currentTargetId};

            $.ajax({
                url: '/assignTag/',
                type: 'POST',
                data: data,
                complete: function (){
                    previewInfo(domElement,0, serverState, tag.target, currentTargetId);
                }
            });
        });
        tags.append(element);
    });
    availableTagsTable.append(tags);
    
}


function updateAssignedTagsTable(domElement,serverState,assignedTags){
    assignedTagsTable.empty();
    var tags = $("<i></i>");
    var bckColor = $(previewElement[0].parentElement).css('background-color');
    assignedTags.forEach(tag => {
        const element = $("<span class='card-tag' style='background-color: white; color:"+bckColor+";'></span>")
            .text(tag.name);

        if (tag.is_assignable) {
            const removeDiv = $("<i class='has-tooltip-arrow' style='color:"+bckColor+"' data-tooltip='Deassociate tag'></i>");
            const removeButton = $("<i class='fa fa-remove pointer fa-fw'></i>");

            removeDiv.append(removeButton);       
            removeDiv.on('click', function(){
                const data = {tag: tag.name, target: tag.target, targetId: currentTargetId};
                
                $.ajax({
                    url: '/removeAssignedTag/',
                    type: 'POST',
                    data: data,
                    complete: function (){
                        previewInfo(domElement,0, serverState, tag.target, currentTargetId);
                    }
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


function showInfoPlaceholder(){
    placeholderElement.show(500);
    previewElement.hide(500);
}