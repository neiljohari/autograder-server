function load_edit_project_view(project_url)
{
    console.log('load_edit_project_view');

    var loaded = $.Deferred();

    $.when(
        $.get(project_url),
        lazy_get_template('edit_project_view'),
        lazy_get_template('test_case_panel'),
        lazy_get_template('test_case_form')
    ).done(function(project_ajax, project_tmpl,
                    test_panel_tmpl, test_form_tmpl) {
        var widget = _render_edit_project_view(
            project_ajax[0], project_tmpl, test_panel_tmpl, test_form_tmpl);
        loaded.resolve();
    });

    return loaded.promise();
}

function _render_edit_project_view(
    project, project_tmpl, test_panel_tmpl, test_form_tmpl)
{
    console.log(project);
    var tmpl_context = {
        project: project
    };
    var tmpl_helpers = {
        test_case_panel: test_panel_tmpl,
        test_case_form: test_form_tmpl,
        populate_fields: true,
        in_array: $.inArray
    };
    $('#main-area').html(project_tmpl.render(tmpl_context, tmpl_helpers));
    // $("a[data-role='ajax']").click(ajax_link_click_handler);
    $('#save-button').click(function(e) {
        _save_project_button_click_handler(e, project);
    });


    var add_test_fields_tmpl_helpers = {
        test_case_form: test_form_tmpl,
        type_override: $('#test_type').val(),
        populate_fields: false
    };

    var add_test_fields = $(
        test_form_tmpl.render(tmpl_context, add_test_fields_tmpl_helpers));
    $('#add_test_fields').append(add_test_fields.html());

    $('#add_test_form').submit(function(e) {
        e.preventDefault();
        var new_test = _extract_test_case_form_fields($(this));
        new_test.data.relationships = {
            'project': project
        };
        _add_test_case_button_handler(
            project, new_test, test_panel_tmpl, test_form_tmpl);
    });
}

function _add_test_case_button_handler(
    project, new_test, test_panel_tmpl, test_form_tmpl)
{
    var tmpl_helpers = {
        test_case_form: test_form_tmpl,
        populate_fields: true,
        in_array: $.inArray
    };

    $.postJSON(
        '/ag-test-cases/ag-test-case/', new_test
    ).done(function(test_response) {
        var tmpl_context = test_response.data;
        tmpl_context.project = project;
        console.log(tmpl_context);
        var new_test_panel = test_panel_tmpl.render(tmpl_context, tmpl_helpers);
        $('#test_cases .panel').append(new_test_panel);
    });
}

function _extract_test_case_form_fields(form)
{
    var test_case = {
        'data': {
            'type': _extract_single_text_field(form, 'test_type'),
            'attributes': {
                'name': _extract_single_text_field(form, 'name', true),
                'hide_from_students': _extract_checkbox_bool(form, 'hide_from_students'),
                'command_line_arguments': _extract_delimited_text_field(form, 'command_line_arguments'),
                'standard_input': _extract_single_text_field(form, 'standard_input'),
                'test_resource_files': _extract_checkbox_group_vals(form, 'test_resource_files'),
                'student_resource_files': _extract_checkbox_group_vals(form, 'student_resource_files'),
                'time_limit': _extract_single_text_field(form, 'time_limit', true, null),
                'expected_return_code': _extract_single_text_field(form, 'expected_return_code', true, null),
                'expect_any_nonzero_return_code': _extract_checkbox_bool(form, 'expect_any_nonzero_return_code'),
                'expected_standard_output': _extract_single_text_field(form, 'expected_standard_output'),
                'expected_standard_error_output': _extract_single_text_field(form, 'expected_standard_error_output'),
                'use_valgrind': _extract_checkbox_bool(form, 'use_valgrind'),
                'valgrind_flags': _extract_delimited_text_field(form, 'valgrind_flags'),
                'compiler': _extract_single_text_field(form, 'compiler'),
                'compiler_flags': _extract_delimited_text_field(form, 'compiler_flags'),
                'files_to_compile_together': _extract_checkbox_group_vals(form, 'files_to_compile_together'),
                'executable_name': _extract_single_text_field(form, 'executable_name'),

                'points_for_correct_return_code': _extract_single_text_field(form, 'points_for_correct_return_code', true, 0),
                'points_for_correct_output': _extract_single_text_field(form, 'points_for_correct_output', true, 0),
                'points_for_no_valgrind_errors': _extract_single_text_field(form, 'points_for_no_valgrind_errors', true, 0),
                'points_for_compilation_success': _extract_single_text_field(form, 'points_for_compilation_success', true, 0)
            }
        }
    };
    console.log(test_case);
    return test_case;
}

function _extract_single_text_field(form, name, trim_whitespace, default_val)
{
    var selector = $(':input[name="' + name + '"]', form);
    var value = selector.val();
    if (trim_whitespace)
    {
        value = value.trim();
    }

    if (value === '' && default_val !== undefined)
    {
        return default_val;
    }

    return value;
}

function _extract_checkbox_bool(form, name)
{
    return $(':input[name="' + name + '"]', form).is(':checked');
}

function _extract_checkbox_group_vals(form, name)
{
    var selector = $(':input[name="' + name + '"]:checked', form);
    var values = [];
    selector.each(function() {
        values.push($(this).val());
    });

    return values;
}

function _extract_delimited_text_field(form, name, delimiter)
{
    if (delimiter === undefined)
    {
        delimiter = ' ';
    }

    var values = _extract_single_text_field(form, name, true).split(delimiter);
    var filtered = [];
    for (index in values)
    {
        if (values[index] !== '')
        {
            filtered.push(values[index]);
        }
    }
    return filtered;
}

function _save_project_button_click_handler(e, project)
{
    console.log(project);
    var new_feedback_config = {
        return_code_feedback_level: $('#return_code_feedback_level').val(),
        output_feedback_level: $('#output_feedback_level').val(),
        compilation_feedback_level: $('#compilation_feedback_level').val(),
        valgrind_feedback_level: $('#valgrind_feedback_level').val(),
        points_feedback_level: $('#points_feedback_level').val()
    };
    project.data.attributes.test_case_feedback_configuration = new_feedback_config;

    project.data.attributes.visible_to_students = (
        $('#visible_to_students').is(':checked'));
    project.data.attributes.disallow_student_submissions = (
        $('#disallow_student_submissions').is(':checked'));
    project.data.attributes.allow_submissions_from_non_enrolled_students = (
        $('#allow_submissions_from_non_enrolled_students').is(':checked'));

    var closing_time = $('#closing_time').val();
    if (closing_time.trim() === '')
    {
        closing_time = null;
    }
    project.data.attributes.closing_time = closing_time;
    project.data.attributes.min_group_size = $('#min_group_size').val().trim();
    project.data.attributes.max_group_size = $('#max_group_size').val().trim();

    $.patchJSON(
        project.data.links.self, project
    ).done(function() {
        console.log('save successful');
    });
}
