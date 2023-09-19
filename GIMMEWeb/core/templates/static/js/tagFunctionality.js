const addTagButton = document.getElementById('addTagButton');
const addTagContainer = document.getElementById('addTagContainer');
const tagInput = document.getElementById('tagInput');
const randomizeButton = document.getElementById('randomizeGroupsButton');

let isEveryoneSelected = false;
// // Add event listener for selecting tags
// const tagButtons = document.querySelectorAll('.tagButton');
// 	tagButtons.forEach(button => {
// 		button.addEventListener('click', () => {
// 			button.classList.toggle('selected');
// 		});
// 	});


randomizeButton.addEventListener('click', () => {
    const url = '/randomizeGroupTags/';

    $.ajax({
        url: url,
        type: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function(result) {},
        error: function(error) {}
    });
});

// Add event listener for adding a tag
addTagButton.addEventListener('click', () => {
    if (addTagContainer.style.display == 'block')
    {
        ShowAddTagButton();
        return;
    }

    addTagContainer.style.display = 'block';
    addTagButton.style.display = 'none';

    // Add event listener for saving a tag
    const saveTagButton = document.getElementById('saveTagButton');
    const cancelTagButton = document.getElementById('cancelTagButton');


    saveTagButton.addEventListener('click', () => {
        const tagName = tagInput.value.trim();
        if (tagName !== '') {
            const url = '/createNewTag/';
            const data = { name: tagName };

            
            $.ajax({
                url: url,
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: data,
                success: function(result) {
                    // Handle the response from the server
                    // Refresh the tag list after saving the tag
                },
                error: function(error) {
                    // Handle any errors
                }
            });

            // Reset the input field and hide the add tag container
            ShowAddTagButton();
        }
    });

    cancelTagButton.addEventListener('click', () => {
        ShowAddTagButton();
    });

});


function ShowAddTagButton(){
    tagInput.value = '';
    addTagContainer.style.display = 'none';
    addTagButton.style.display = 'block';
}


function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }


 function toggleEveryoneTag(clickedTag) {
    isEveryoneSelected = !isEveryoneSelected;
    clickedTag.toggleClass("selected", isEveryoneSelected);
                
    if (isEveryoneSelected)
        var url = '/addAllUsersSelected/';
    else
        var url = '/removeAllUsersSelected/';

    $.ajax({
        url: url,
        type: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Use the getCookie function to retrieve CSRF token
        },
        success: function(result) {},
        error: function(error) {}
    });
}


function generateTagsTable(tagsArray) {
    var table = $('<div></div>');

    everyone = $("<span class='selectable-tag pointer has-tooltip-arrow' data-tooltip='Select/Deselect tag' style='border: none; height: 2em; align-items: center;'></span>").text("Everyone");
    everyone.toggleClass("selected", isEveryoneSelected);
    everyone.click(function() {
        const clickedTag = $(this);
        toggleEveryoneTag(clickedTag);
    });

    table.append(everyone)


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
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Use the getCookie function to retrieve CSRF token
            },
            data: { name: tagId },
            success: function(result) {},
            error: function(error) {}
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
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') // Use the getCookie function to retrieve CSRF token
                },
                data: { name: tagId },
                success: function(result) {},
                error: function(error) {}
                });
            });

            tag.append(deleteButton);
        }

        table.append(tag);
    });

    return table
}