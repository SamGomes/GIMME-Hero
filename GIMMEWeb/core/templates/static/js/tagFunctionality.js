const addStudentTagButton = document.getElementById('addStudentTagButton_professor_dash'),
    addStudentTagContainer = document.getElementById('addStudentTagContainer_professor_dash'),
    saveStudentTagButton = document.getElementById('saveStudentTagButton_professor_dash'),
    cancelStudentTagButton = document.getElementById('cancelStudentTagButton_professor_dash'),
    tagInputStudent = document.getElementById('tagInputStudent_professor_dash'),
    addTaskTagButton = document.getElementById('addTaskTagButton_professor_dash'),
    addTaskTagContainer = document.getElementById('addTaskTagContainer_professor_dash'),
    saveTaskTagButton = document.getElementById('saveTaskTagButton_professor_dash'),
    tagInputTask = document.getElementById('tagInputTask_professor_dash'),
    cancelTaskTagButton = document.getElementById('cancelTaskTagButton_professor_dash');


// Add event listener for adding a tag
var addTag = function (target, addTagContainer, saveTagButton, deleteTagButton, tagInput) {
    if (addTagContainer.style.display == 'block') {
        showAddTagButton();
        return;
    }

    addTagContainer.style.display = 'block';
    // addTagButton.style.display = 'none';
    
    saveTagButton.addEventListener('click', function () {
        const tagName = tagInput.value.trim();
        if (tagName !== '') {
            $.ajax({
                url: '/createNewTag/',
                type: 'POST',
                data: {name: tagName, target: target}
            });

            // Reset the input field and hide the add tag container
            showAddTagButton(addTagContainer, tagInput);
        }
    });

    deleteTagButton.addEventListener('click', function () {
        showAddTagButton(addTagContainer, tagInput);
    });
};

addStudentTagButton.addEventListener('click',function (){
    addTag('student', addStudentTagContainer, saveStudentTagButton, cancelStudentTagButton, tagInputStudent);
});
addTaskTagButton.addEventListener('click',function (){
    addTag('task', addTaskTagContainer, saveTaskTagButton, cancelTaskTagButton, tagInputTask);
});


function showAddTagButton(addTagContainer, tagInput){
    tagInput.value = '';
    addTagContainer.style.display = 'none';
}

function generateTagsTable(tagsArray, target) {
    var table = $('<div></div>');
    
    tagsArray.forEach(element => {
        tag = $("<span class='selectable-tag pointer has-tooltip-arrow' data-tooltip='Select/Deselect tag' style='border: none; height: 2em; align-items: center;'></span>").text(element.name);
        
        tag.toggleClass("selected", element.is_selected);

        tag.click(function() {
            const clickedTag = $(this);
            const tagId = element.name;
            const url = '/selectTag/';
            
            $.ajax({
                url: url,
                type: 'POST',
                data: { name: tagId , target: target}
            });

        });

        if(element.is_removable) {
            const deleteButton = $("<div class='button is-rounded is-small has-tooltip-arrow pointer delete-tag-button' data-tooltip='Delete this tag'></div>");
            const deleteTagButton = $("<div class='fas fa-trash' style='height: 0.9rem;'></div>");

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