/* Required variables: ajaxLevelSubjectsURL, ajaxLevelSectionsURL, ajaxSectionSubjectsURL */
levelDropName = 'level'
sectionDropName = 'section'
subjectDropName = 'subject'
categoryDropName = 'category'


function levelSelect(item) {
    level_slug = selectOption(item, levelDropName)
    updateSections(level_slug)
    updateSubjectsByLevel(level_slug)
    setDefaultOption(sectionDropName)
    setDefaultOption(subjectDropName)
}

function sectionSelect(item) {
    section_slug = selectOption(item, sectionDropName)
    updateSubjectsBySection(section_slug)
    setDefaultOption(subjectDropName)
}

function subjectSelect(item) {
    selectOption(item, subjectDropName)
}

function categorySelect(item) {
    selectOption(item, categoryDropName)
}

function selectOption(item, dropName) {
    item = $(item)
    item.addClass('active')

    dropdownContainerString = '#' + dropName + '-dropdown-container'
    container = $(dropdownContainerString)

    if (container != null) {
        buttonText = $(dropdownContainerString + ' button span .to-change')
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
            updateDropContent(sectionDropName, data)
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
            updateDropContent(subjectDropName, data)
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
            updateDropContent(subjectDropName, data)
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

function getDropOptions(dropName) {
    options = $('#' + dropName + '-dropdown-container' + ' .dropdown-menu' + ' li:not("#' + dropName + '-default-dropdown-item")')

    return options
}

function updateDropContent(dropName, data) {
    dropMenuString = '#' + dropName + '-dropdown-container' + ' .dropdown-menu'
    dropMenu = $(dropMenuString)

    if (dropMenu != null) {
        options = getDropOptions(dropName)
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

var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        });

        if (matches.length < 5) {
            new_matches = [];
            $.each(strs, function(i, str) {
                var sim = similarity(q, str);
                if (sim >= 0.1) {
                    new_matches.push([sim, str]);
                }
            });
            new_matches.sort((a, b) => b[0] - a[0])
            $.each(new_matches, function(i, val) {
                    matches.push(val[1]);
            })
        }

        cb(matches);
    };
};

$('#search-input-container .typeahead').typeahead(
    {
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'search_queries',
        source: substringMatcher(search_queries)
    }
);

$('#search-query-input').on('input', function(event) {
    input = $(event.currentTarget)
    q = input.val()

    // Execute this function only of a full new word typed
    if (q.endsWith(' ')) {
        updateDropSelectedValues(q)
    }
});
$('#search-query-input').keydown(function(event) {
    input = $(event.currentTarget)
    q = input.val()

    // Execute this function if any arrow key pressed
    if (event.which == 13 || event.which >= 37 && event.which <= 40) {
        updateDropSelectedValues(q)
    }
});

function updateDropSelectedValues(q) {
    levels = getDropOptions(levelDropName)
    sections = getDropOptions(sectionDropName)
    subjects = getDropOptions(subjectDropName)
    categories = getDropOptions(categoryDropName)

    levels.each(function(index) {
        level = $(this)
        // only for level, e.g 3eme vs 3ème
        if (q.includes(level.text()) || q.includes(level.data('slug'))) {
            selectOption(level, levelDropName)
            return false
        } else {
            setDefaultOption(levelDropName)
        }
    });

    sections.each(function(index) {
        section = $(this)
        if (q.includes(section.text())) {
            selectOption(section, sectionDropName)
            return false
        } else {
            setDefaultOption(sectionDropName)
        }
    });

    subjects.each(function(index) {
        subject = $(this)
        if (q.includes(subject.text())) {
            selectOption(subject, subjectDropName)
            return false
        } else {
            setDefaultOption(subjectDropName)
        }
    });

    categories.each(function(index) {
        category = $(this)
        if (q.includes(category.text())) {
            selectOption(category, categoryDropName)
            return false
        } else {
            setDefaultOption(categoryDropName)
        }
    });
}