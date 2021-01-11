/* Required variables: ajaxLevelSubjectsURL, ajaxLevelSectionsURL, ajaxSectionSubjectsURL */
level = 'level'
section = 'section'
subject = 'subject'
category = 'category'


function levelSelect(item) {
    level_slug = selectOption(item, level)
    updateSections(level_slug)
    updateSubjectsByLevel(level_slug)
    setDefaultOption(section)
    setDefaultOption(subject)
}

function sectionSelect(item) {
    section_slug = selectOption(item, section)
    updateSubjectsBySection(section_slug)
    setDefaultOption(subject)
}

function subjectSelect(item) {
    selectOption(item, subject)
}

function categorySelect(item) {
    selectOption(item, category)
}

function selectOption(item, dropName) {
    item = $(item)
    item.addClass('active')

    dropdownContainerString = '#' + dropName + '-dropdown-container'
    container = $(dropdownContainerString)

    if (container != null) {
        buttonText = $(dropdownContainerString + ' button span')
        buttonText.text(item.text())
        hiddenInput = $('#' + dropName + '-hidden-input')
        hiddenInput.val(item.data('slug'))
    }

    return item.data('slug')
}

function updateSections(level_slug) {
    $.ajax({
        url: ajaxLevelSectionsURL,
        type: "GET",
        data: {
            'level': level_slug,
        },
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            updateDropdownContent(section, data)
        },
        error: function(ts) { 
            $('#next-btn').attr('disabled', 'false')
            console.log(ts);
        }
    })
}

function updateSubjectsByLevel(level_slug) {
    $.ajax({
        url: ajaxLevelSubjectsURL,
        type: "GET",
        data: {
            'level': level_slug,
        },
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            updateDropdownContent(subject, data)
        },
        error: function(ts) { 
            $('#next-btn').attr('disabled', 'false')
            console.log(ts);
        }
    })
}

function updateSubjectsBySection(section_slug) {
    $.ajax({
        url: ajaxSectionSubjectsURL,
        type: "GET",
        data: {
            'section': section_slug,
        },
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data) {
            updateDropdownContent(subject, data)
        },
        error: function(ts) { 
            $('#next-btn').attr('disabled', 'false')
            console.log(ts);
        }
    })
}

function setDefaultOption(dropName){
    selectOption($('#' + dropName + '-default-dropdown-item')[0], dropName)
}

function updateDropdownContent(dropName, data) {
    dropMenuString = '#' + dropName + '-dropdown-container' + ' .dropdown-menu'
    dropMenu = $(dropMenuString)

    if (dropMenu != null) {
        options = $(dropMenuString + ' li:not("#' + dropName + '-default-dropdown-item")')
        options.remove()
            console.log(data.length)

        for (var row in data) {
            dropMenu.append(
                '<li class="dropdown-item" onclick="' + dropName + 'Select(this)" data-slug="' + data[row]['slug'] + '">' + data[row]['name'] + '</li>'
            )
            console.log(row)
        }
    }
}
