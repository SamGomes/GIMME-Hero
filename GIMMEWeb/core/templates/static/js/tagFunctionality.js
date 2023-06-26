const addTagButton = document.getElementById('addTagButton');
const addTagContainer = document.getElementById('addTagContainer');
const tagInput = document.getElementById('tagInput');





// Add event listener for selecting tags
const tagButtons = document.querySelectorAll('.tagButton');
	tagButtons.forEach(button => {
		button.addEventListener('click', () => {
			button.classList.toggle('selected');
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
            const url = '/addStudentTag/';
            const data = { tag: tagName};

            $.ajax({
                url: url,
                type: 'POST',
                headers: {
                  'X-CSRFToken': getCookie('csrftoken') // Use the getCookie function to retrieve CSRF token
                },
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function(result) {
                  // Handle the response from the server
                  // Refresh the tag list after saving the tag
                },
                error: function(error) {
                  // Handle any errors
                }
              });
            // Reset the input field and hide the add tag container

            // Send an AJAX request to your Django view to save the tag
            // You can use the tagName value to store the new tag
            // Refresh the tag list after saving the tag

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
    console.log(document.cookie.length)
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