var addStudentTagButton = $('#addStudentTagButton_professor_dash'),
    addStudentTagContainer = $('#addStudentTagContainer_professor_dash'),
    saveStudentTagButton = $('#saveStudentTagButton_professor_dash'),
    cancelStudentTagButton = $('#cancelStudentTagButton_professor_dash'),
    tagInputStudent = $('#tagInputStudent_professor_dash'),
    addTaskTagButton = $('#addTaskTagButton_professor_dash'),
    addTaskTagContainer = $('#addTaskTagContainer_professor_dash'),
    saveTaskTagButton = $('#saveTaskTagButton_professor_dash'),
    tagInputTask = $('#tagInputTask_professor_dash'),
    cancelTaskTagButton = $('#cancelTaskTagButton_professor_dash');


// Add event listener for adding a tag
var addTag = function (target, addTagButton, addTagContainer, saveTagButton, cancelTagButton, tagInput) {
    showAddTagButton(addTagButton, addTagContainer, tagInput);
    
    saveTagButton.click(function () {
        const tagName = tagInput.val().trim();
        if (tagName !== '') {
            $.ajax({
                url: '/createNewTag/',
                type: 'POST',
                data: {name: tagName, target: target}
            });

            // Reset the input field and hide the add tag container
            hideAddTagButton(addTagButton, addTagContainer, tagInput);
        }
    });

    cancelTagButton.click(function () {
        hideAddTagButton(addTagButton, addTagContainer, tagInput);
    });
};

addStudentTagButton.click(function (){
    addTag('student', $(this), addStudentTagContainer, saveStudentTagButton, cancelStudentTagButton, tagInputStudent);
});
addTaskTagButton.click(function (){
    addTag('task', $(this), addTaskTagContainer, saveTaskTagButton, cancelTaskTagButton, tagInputTask);
});


function showAddTagButton(addTagButton, addTagContainer, tagInput){
    tagInput.val('');
    addTagButton.hide(500);
    addTagContainer.show(500);
}
function hideAddTagButton(addTagButton, addTagContainer, tagInput){
    tagInput.val('');
    addTagButton.show(500);
    addTagContainer.hide(500);
}

function generateTagsTable(tagsArray, target) {
    var table = $('<div></div>');
    
    tagsArray.forEach(element => {
        tag = $("<i class='selectable-tag pointer' " +
            "style='height: 2em; align-items: center;'></i>").text(element.name);
        
        tag.toggleClass("selected", element.is_selected);

        tag.click(function() {
            const tagId = element.name;
            const url = '/selectTag/';
            
            $.ajax({
                url: url,
                type: 'POST',
                data: { name: tagId , target: target}
            });

        });

        if(element.is_removable) {
            const deleteButton = $("<div class='is-rounded is-small has-tooltip-arrow pointer' data-tooltip='Delete this tag'></div>");
            const deleteTagButton = $("<div class='fas fa-fw fa-remove' style='height: 0.9rem;'></div>");

            deleteButton.append(deleteTagButton);
        
            deleteButton.click(function() {
                const tagId = element.name;
                const url = '/deleteTag/';
                
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: { name: tagId, target: target }
                });
            });

            tag.append(deleteButton);
        }

        table.append(tag);
    });

    return table;
}