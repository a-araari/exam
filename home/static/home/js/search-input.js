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

function similarity(s1, s2) {
    var longer = s1;
    var shorter = s2;
    if (s1.length < s2.length) {
        longer = s2;
        shorter = s1;
    }
    var longerLength = longer.length;
    if (longerLength == 0) {
        return 1.0;
    }
    return (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
}

function editDistance(s1, s2) {
    s1 = s1.toLowerCase();
    s2 = s2.toLowerCase();

    var costs = new Array();
    for (var i = 0; i <= s1.length; i++) {
        var lastValue = i;
        for (var j = 0; j <= s2.length; j++) {
            if (i == 0)
                costs[j] = j;
            else {
                if (j > 0) {
                    var newValue = costs[j - 1];
                    if (s1.charAt(i - 1) != s2.charAt(j - 1))
                        newValue = Math.min(Math.min(newValue, lastValue), costs[j]) + 1;

                    costs[j - 1] = lastValue;
                    lastValue = newValue;
                }
            }
        }
        if (i > 0)
            costs[s2.length] = lastValue;
    }
    return costs[s2.length];
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