About tw2.asyncresources
-------------------------

tw2.asyncresources provides support for loading ToscaWidgets resources using a
Javascript Loader instead of injecting ``<script>`` and ``<link>`` into the
page head.

Also every ``JSSource`` used by the Widget will be patched to run when
the loader finished loading all the required resources.

Installing
-------------------------------

tw2.asyncresources can be installed from pypi (currently not released)::

    pip install tw2.asyncresources

should just work for most of the users

Using tw2.asyncresources
-----------------------------

Whenever you want to use a widget with asynchronous resources just apply the
``@with_loader`` decorator and specify the desidered loader. Currently
only the `requirejs <http://requirejs.org/>`_ and `axel <https://github.com/amol-/axel>`_
loaders are supported.

Please not that the specified loader should have already been enabled inside
your application. tw2.asynresources won't inject the loader itself.

Here is a plain TW2 form that displays a text field and two calendars::

    from tw2.forms import TableForm
    from tw2.forms import TextField, CalendarDatePicker

    class TestForm(TableForm):
        name = TextField()
        date = CalendarDatePicker()
        other_date = CalendarDatePicker()

Such a form will usually output the following html::

    <html>
        <head>
            <script type="text/javascript" src="/tw2/resources/tw2.forms/static/calendar/calendar.js"></script>
            <script type="text/javascript" src="/tw2/resources/tw2.forms/static/calendar/calendar-setup.js"></script>
            <script type="text/javascript" src="/tw2/resources/tw2.forms/static/calendar/lang/calendar-en.js"></script>
        </head>
        <body>
            <form action="/check_form" enctype="multipart/form-data" method="post">
                <!-- Form definition here -->
            </form>
            <script type="text/javascript">Calendar.setup({"ifFormat": "%Y-%m-%d", "button": "date_trigger", "inputField": "date", "showsTime": "false"})</script>
            <script type="text/javascript">Calendar.setup({"ifFormat": "%Y-%m-%d", "button": "other_date_trigger", "inputField": "other_date", "showsTime": "false"})</script>
        </body>

When patched with the ``@with_loader('requirejs')`` decorator::

    from tw2.forms import TableForm
    from tw2.forms import TextField, CalendarDatePicker
    from tw2.asyncresources import with_loader

    @with_loader('requirejs')
    class TestForm(TableForm):
        name = TextField()
        date = CalendarDatePicker()
        other_date = CalendarDatePicker()

The following gets generated::

    <html>
        <head>
            <script type="text/javascript">require(["/tw2/resources/tw2.forms/static/calendar/calendar.js"])</script>
            <script type="text/javascript">require(["/tw2/resources/tw2.forms/static/calendar/calendar-setup.js"])</script>
            <script type="text/javascript">require(["/tw2/resources/tw2.forms/static/calendar/lang/calendar-en.js"])</script>
        </head>
        <body>
            <form action="/check_form" enctype="multipart/form-data" method="post">
                <!-- Form definition here -->
            </form>
            <script type="text/javascript">require(["/tw2/resources/tw2.forms/static/calendar/calendar.js", "/tw2/resources/tw2.forms/static/calendar/calendar-setup.js", "/tw2/resources/tw2.forms/static/calendar/lang/calendar-en.js"], function() { Calendar.setup({"ifFormat": "%Y-%m-%d", "showsTime": "false", "inputField": "date", "button": "date_trigger"}) })</script>
            <script type="text/javascript">require(["/tw2/resources/tw2.forms/static/calendar/calendar.js", "/tw2/resources/tw2.forms/static/calendar/calendar-setup.js", "/tw2/resources/tw2.forms/static/calendar/lang/calendar-en.js"], function() { Calendar.setup({"ifFormat": "%Y-%m-%d", "showsTime": "false", "inputField": "other_date", "button": "other_date_trigger"}) })</script>
        </body>





